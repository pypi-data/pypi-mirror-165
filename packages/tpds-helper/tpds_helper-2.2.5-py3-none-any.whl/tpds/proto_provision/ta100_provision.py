# -*- coding: utf-8 -*-
# 2019 to present - Copyright Microchip Technology Inc. and its subsidiaries.

# Subject to your compliance with these terms, you may use Microchip software
# and any derivatives exclusively with Microchip products. It is your
# responsibility to comply with third party license terms applicable to your
# use of third party software (including open source software) that may
# accompany Microchip software.

# THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES, WHETHER
# EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY IMPLIED
# WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A PARTICULAR
# PURPOSE. IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT, SPECIAL,
# PUNITIVE, INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE OF ANY
# KIND WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF MICROCHIP
# HAS BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE FORESEEABLE. TO THE
# FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL LIABILITY ON ALL CLAIMS IN
# ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED THE AMOUNT OF FEES, IF ANY,
# THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR THIS SOFTWARE.
import json
from tpds.secure_element.ta_element import TAElement
try:
    import cryptoauthlib_ta as cal
except (ModuleNotFoundError, ImportError) as e:
    import cryptoauthlib as cal
from tpds.tp_utils.tp_keys import TPSymmetricKey, TPAsymmetricKey
from enum import Enum
from ctypes import c_uint16, byref


class ClassType(Enum):
    public_key = 0
    private_key = 1
    symmetric_key = 2
    data = 3
    extracted_certificate = 4
    reserved = 5
    fast_crypto_key_group = 6
    crl = 7


key_info = {
    0: {'algorithm': 'ECC', 'size': 'secp256r1'},
    1: {'algorithm': 'ECC', 'size': 'secp224r1'},
    2: {'algorithm': 'ECC', 'size': 'secp384r1'},
    4: {'algorithm': 'RSA', 'size': 1024},
    5: {'algorithm': 'RSA', 'size': 2048},
    6: {'algorithm': 'RSA', 'size': 3072},
    8: {'algorithm': 'HMAC', 'size': 32},
    9: {'algorithm': 'ECC', 'size': 'secp256k1'},
    10: {'algorithm': 'ECC', 'size': 32},
    12: {'algorithm': 'AES', 'size': 16}
}


class TA100Provision():
    def __init__(self, cfg):
        self.element = TAElement()
        self.element.connect(cfg)

    def load_handles(self, handles):
        handles_status = list()
        for handle in handles:
            try:
                handle_id = int(handle['handle'], 16)
                handle_exist = self.element.is_handle_valid(handle_id)
                if handle_exist:
                    if self.element.delete_handle(handle_id):
                        handle_exist = False
                handle_status = ''
                if not handle_exist:
                    attr_byte_buff = cal.ta_element_attributes_t.from_buffer(
                        bytearray.fromhex(handle['attrib']))
                    create_details = int(handle['details'], 16)
                    c_handle_out = c_uint16(0)
                    status = cal.get_cryptoauthlib().talib_create(
                                                self.element.device, 0, create_details, handle_id,
                                                byref(attr_byte_buff), byref(c_handle_out))
                    if not status:
                        data_bytes = self.get_key_from_handle(handle)
                        if data_bytes:
                            status = cal.talib_write_element(
                                                cal.atcab_get_device(), handle_id,
                                                len(data_bytes), data_bytes)
                            if status != cal.Status.ATCA_SUCCESS:
                                handle_status = f'Write element failed with 0x{status:02X} code'
                        else:
                            handle_status = f'No data bytes to provision'
                    else:
                        handle_status = f'Creation failed with 0x{status:02X} code'
                else:
                    handle_status = 'Exists with no delete option'
            except BaseException as e:
                handle_status = f'{e}'
            handles_status.append({'handle': f'{handle_id:02X}', 'status':handle_status})
        return handles_status

    def provision_device(self, json_obj):
        ''' Provision the TA100
        Steps
        1. Write the configuration memory, If configuration memory is not
                locked.
        2. Read the previously created handles and delete - if delete_perm is
                always
        3. Create & write the handles available in the JSON file, if key is
                not available and source is HSM generate the keys internally
                and write
        '''
        self.ta_config = json.loads(json_obj)
        provision_info = dict()
        if self.ta_config:
            if self.ta_config['TA100Attributes']['ConfigurationMemory']["attrib"]:
                self.config_bytes = \
                    self.ta_config['TA100Attributes']['ConfigurationMemory']["attrib"]
                if self.element.is_config_zone_locked():
                    provision_info.update(config_status='Skipping Configuration write as it is already locked')
                else:
                    self.element.write_config_memory(self.config_bytes)
            else:
                raise ('Configuration memory not available')

            if self.ta_config['TA100Attributes']['HandleList']:
                self.handles = self.ta_config['TA100Attributes']['HandleList']
                provision_info.update(handles_status=self.load_handles(self.handles))
            else:
                raise ('Memory handles not created')
        else:
            raise('Empty File')

        return provision_info

    def get_key_from_handle(self, handle):
        '''Parse attribute to get class and key_type
        for key generation Symmetric/Asymmetric
        '''
        data_bytes = None
        try:
            if handle.get('source') == 'user':
                data_bytes = bytearray.fromhex(handle.get('value'))
            elif handle.get('source') == 'hsm':
                attr_info = cal.ta_element_attributes_t.from_buffer(
                    bytearray.fromhex(handle.get('attrib')))
                data_bytes = self.get_key_bytes(
                    attr_info.Class, attr_info.Key_Type)
        except BaseException as e:
            data_bytes = None

        return data_bytes

    def get_key_bytes(self, class_type, key_type):
        # HSM support only symmetric key and Private key generation
        key_bytes = None
        if class_type == ClassType.symmetric_key.value:
            symmetric_key = TPSymmetricKey(
                None, key_info.get(key_type).get('size'))
            key_bytes = symmetric_key.get_bytes()
        elif class_type == ClassType.private_key.value:
            key_algo = key_info.get(key_type).get('algorithm')
            assert key_algo in ['ECC', 'RSA'], 'Unsupported Algorithm'
            key = TPAsymmetricKey(
                None, algo=key_algo,
                size=key_info.get(key_type).get('size'))
            key_bytes = key.get_private_key_bytes()
        # elif class_type == ClassType.public_key.value:
        #     key_algo = key_info.get(key_type).get('algorithm')
        #     assert key_algo in ['ECC', 'RSA'], 'Unsupported Algorithm'
        #     key = TPAsymmetricKey(
        #         None, algo=key_algo,
        #         size=key_info.get(key_type).get('size'))
        #     key_bytes = key.public_key_bytes
        return key_bytes


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    # cfg = cal.cfg_ateccx08a_kithid_default()
    # cfg.cfg.atcahid.dev_interface = cal.ATCAKitType.ATCA_KIT_SPI_IFACE
    # cfg.cfg.atcahid.dev_identity = 0x0
    # cfg.devtype = 0x10
    # provision = TA100Provision(cfg)
    # print(provision.element.get_device_details())
    # json_obj = "{\"VersionAttributes\":{\"TaConfiguratorVersion\":\"2.0.2.0\",\"JsonVersion\":\"1.5.0\"},\"TA100Attributes\":{\"PackageOption\":\"_8PinSOIC\",\"IoType\":\"SPIInterface\",\"Lock\":{\"config\":true,\"setup\":true},\"Options\":{\"disable_aes\":false,\"force_fips\":false,\"bsd\":false,\"disable_rsa\":false},\"PullUps\":\"0xEF\",\"GroupNumber\":\"0x0000\",\"ConfigurationMemory\":{\"handle\":\"0xC000\",\"attrib\":\"000000000000000000000000000000002E00000000000100000000000000000000000000000000000000000000000000\"},\"HandleList\":[{\"name\":\"APP.PRI\",\"handle\":\"0x8000\",\"details\":\"0x0000\",\"attrib\":\"01FF040100004600\",\"source\":\"hsm\",\"value\":null},{\"name\":\"APP_HSM_AUTH_KEY\",\"handle\":\"0x8001\",\"details\":\"0x2000\",\"attrib\":\"42001800000B6500\",\"source\":\"user\",\"value\":\"b9e746b4264ea6dc58cda50d82fc2e8cf737e78227f0a43403a291833f5b768a\"},{\"name\":\"COMMON_KEY\",\"handle\":\"0x800b\",\"details\":\"0x0000\",\"attrib\":\"E2000E0000004510\",\"source\":\"user\",\"value\":\"b9e746b4264ea6dc58cda50d82fc2e8c\"},{\"name\":\"WLAN_KEY\",\"handle\":\"0x8008\",\"details\":\"0x0000\",\"attrib\":\"0320000009096500\",\"source\":\"user\",\"value\":\"0111111111111111111111111111111111111111111111111111111111111111\"},{\"name\":\"APP_HSM_TRNSPT_KEY\",\"handle\":\"0x8009\",\"details\":\"0x0000\",\"attrib\":\"E2001D00000B6500\",\"source\":\"user\",\"value\":\"b9e746b4264ea6dc58cda50d82fc2e8c\"},{\"name\":\"CA_ROOT_CLOUD.PUB\",\"handle\":\"0x800c\",\"details\":\"0x0000\",\"attrib\":\"00FF000000005500\",\"source\":\"user\",\"value\":\"b9e746b4264ea6dc58cda50d82fc2e8cf737e78227f0a43403a291833f5b768a52cf72794101ef673cbbef6381e8b545c1835231279814f7183763507a5fd117\"},{\"name\":\"APP_CERT\",\"handle\":\"0x800e\",\"details\":\"0x0000\",\"attrib\":\"030F000009005410\",\"source\":\"user\",\"value\":\"111111111111111111111111111111\"},{\"name\":\"SIGNER_CERT\",\"handle\":\"0x800f\",\"details\":\"0x0000\",\"attrib\":\"030E000009005410\",\"source\":\"user\",\"value\":\"1111111111111111111111111111\"},{\"name\":\"SIGNER.PUB\",\"handle\":\"0x800d\",\"details\":\"0x0000\",\"attrib\":\"0000000000005400\",\"source\":\"user\",\"value\":\"b9e746b4264ea6dc58cda50d82fc2e8cf737e78227f0a43403a291833f5b768a52cf72794101ef673cbbef6381e8b545c1835231279814f7183763507a5fd117\"}],\"DeviceUpdatePublicKey\":null}}"
    # print(provision.provision_device(json_obj))
    pass
