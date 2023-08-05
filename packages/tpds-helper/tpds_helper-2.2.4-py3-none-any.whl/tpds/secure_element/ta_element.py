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
try:
    import cryptoauthlib_ta as cal
except (ModuleNotFoundError, ImportError) as e:
    import cryptoauthlib as cal
from ctypes import create_string_buffer, byref, c_bool
from ctypes import cast, c_void_p, c_uint8, c_char_p


class TAElement():
    def __init__(self):
        pass

    def connect(self, cfg):
        '''
        Connects to ta using cfg provided
        '''
        assert cal.atcab_init(cfg) \
            == cal.Status.ATCA_SUCCESS, 'Can\'t connect to device'
        self.device = cast(cal.atcab_get_device(), c_void_p)

    def get_device_revision(self):
        '''
        Returns device revision from connected device
        '''
        revision = create_string_buffer(4)
        assert cal.talib_info_compat(self.device, revision) \
            == cal.Status.ATCA_SUCCESS
        return bytes(revision.raw)

    def get_device_serial_number(self):
        '''
        Returns device serial number from connected device
        '''
        c_serial_number = create_string_buffer(8)
        assert cal.talib_info_serial_number(self.device, c_serial_number) \
            == cal.Status.ATCA_SUCCESS
        return bytes(c_serial_number.raw)

    def is_config_zone_locked(self):
        '''
        Returns config memory lock status from connected device
        '''
        is_locked = c_bool()
        assert cal.talib_is_config_locked(self.device, byref(is_locked)) \
            == cal.Status.ATCA_SUCCESS, 'Reading config lock status failed'
        return bool(is_locked.value)

    def is_setup_locked(self):
        '''
        Returns setup lock status from connected device
        '''
        is_locked = c_bool()
        assert cal.talib_is_setup_locked(self.device, byref(is_locked)) \
            == cal.Status.ATCA_SUCCESS, 'Reading setup lock status failed'
        return bool(is_locked.value)

    def is_handle_valid(self, target_handle):
        '''
        Returns target_handle validity status from connected device
        '''
        c_is_valid = c_uint8()
        assert cal.get_cryptoauthlib().talib_is_handle_valid(
            self.device, target_handle, cast(byref(c_is_valid), c_char_p)) \
            == cal.Status.ATCA_SUCCESS, 'Reading handle validity failed'
        return bool(c_is_valid.value)

    def lock_setup(self):
        '''Lock the setup
        '''
        assert cal.get_cryptoauthlib().talib_lock_setup(
            self.device) == cal.Status.ATCA_SUCCESS, 'Locking setup failed'

    def get_handles_array(self):
        '''
        Returns all handles present from connected device
        '''
        handles = []
        assert cal.talib_info_get_handles_array(self.device, handles) \
            == cal.Status.ATCA_SUCCESS, 'Reading handle validity failed'
        return handles

    def get_handle_info(self, target_handle):
        '''
        Returns target_handle attributes info from connected device
        '''
        handle_info = cal.ta_element_attributes_t()
        assert cal.talib_info_get_handle_info(
            self.device, target_handle, handle_info) \
            == cal.Status.ATCA_SUCCESS, 'Reading handle info failed'
        return handle_info

    def get_device_details(self):
        '''
        Returns device basic information like Revision, Serial No,
        Config status etc..,
        '''
        device_info = dict()
        device_info['revision'] = self.get_device_revision().hex()
        device_info['serial_number'] \
            = self.get_device_serial_number().hex().upper()
        device_info['lock_status'] \
            = [self.is_config_zone_locked(), self.is_setup_locked()]
        device_info['handles'] = []
        for handle in self.get_handles_array():
            handle_info = {}
            handle_info.update({'handle': f'{handle:04X}'})
            handle_info.update({
                'validity':
                'Valid' if self.is_handle_valid(handle) else 'Invalid'})
            handle_info.update({
                'attr':
                bytes(self.get_handle_info(handle)).hex().upper()})
            device_info['handles'].append(handle_info)

        return device_info

    def delete_handle(self, handle):
        '''Delete the handle if read permission is set
        '''
        # Read attribute info - delete permission
        attrib = cal.ta_element_attributes_t()
        assert cal.talib_info_get_handle_info(
            cal.atcab_get_device(), handle, attrib) \
            == cal.Status.ATCA_SUCCESS, 'Fetching handle info failed'

        if attrib.Delete_Perm == 1:
            assert cal.talib_delete_handle(
                cal.atcab_get_device(), handle) \
                == cal.Status.ATCA_SUCCESS, 'Handle deletion failed'
            return True

        return False

    def write_config_memory(self, config_bytes):
        '''Check configuration memory is locked.
        before writing configuration data
        '''
        assert isinstance(config_bytes, str), \
            'config_bytes should be bytearray'

        if not self.is_config_zone_locked():
            assert cal.atcab_write_config_zone(
                bytearray.fromhex(config_bytes)) == \
                cal.Status.ATCA_SUCCESS, 'Write config zone failed'

        # To read configuration memory, setup should be locked
        # if not self.is_setup_locked():
        #     self.lock_setup()

        # # Test code read after config write
        # ta_config_memory = bytearray(48)

        # assert cal.atcab_read_config_zone(ta_config_memory) == \
        #     cal.Status.ATCA_SUCCESS, 'Read config zone failed'

        # ta_config_memory = bytearray(ta_config_memory)

        # assert bytearray.fromhex(config_bytes) == ta_config_memory[:48], \
        #     'Configuration read does not match'


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    cfg = cal.cfg_ateccx08a_kithid_default()
    cfg.cfg.atcahid.dev_interface = cal.ATCAKitType.ATCA_KIT_I2C_IFACE
    cfg.cfg.atcahid.dev_identity = 0x2E
    cfg.devtype = 0x10

    ta = TAElement()
    ta.connect(cfg)
    print(ta.get_device_details())
    pass
