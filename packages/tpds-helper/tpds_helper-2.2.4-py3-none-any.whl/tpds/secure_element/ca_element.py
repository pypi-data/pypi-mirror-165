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

import cryptoauthlib as cal
from .constants import Constants
from cryptography.hazmat.primitives.asymmetric import ec
from tpds.certs.cert_utils import get_device_public_key, get_backend


class CAElement():
    def __init__(self):
        pass

    def connect(self, cfg):

        assert cal.atcab_init(cfg) \
            == cal.Status.ATCA_SUCCESS, 'Can\'t connect to device'

    def get_device_revision(self):
        '''
        Returns device revision from connected device
        '''
        revision = bytearray(4)
        assert cal.atcab_info(revision) \
            == cal.Status.ATCA_SUCCESS, 'Reading Revision failed'
        return revision

    def get_device_serial_number(self):
        '''
        Returns device serial number from connected device
        '''
        serial_num = bytearray(9)
        assert cal.atcab_read_serial_number(serial_num) \
            == cal.Status.ATCA_SUCCESS, 'Reading Serial Number'
        return serial_num

    def is_config_zone_locked(self):
        is_locked = cal.AtcaReference(False)
        assert cal.atcab_is_locked(Constants.LOCK_ZONE_CONFIG, is_locked) \
            == cal.Status.ATCA_SUCCESS, 'Reading lock status failed'
        return bool(is_locked.value)

    def is_data_zone_locked(self):
        is_locked = cal.AtcaReference(False)
        assert cal.atcab_is_locked(Constants.LOCK_ZONE_DATA, is_locked) \
            == cal.Status.ATCA_SUCCESS, 'Reading lock status failed'
        return bool(is_locked.value)

    def load_config_zone(self, config_data):
        '''
        Loads configuration data to config zone
        '''
        assert self.is_config_zone_locked() == False, \
            'Device config zone is already locked.'

        # Write configuration
        assert cal.atcab_write_bytes_zone(
            Constants.ATCA_CONFIG_ZONE,
            0,
            16,
            config_data,
            len(config_data)) \
            == cal.Status.ATCA_SUCCESS, 'Writing Config zone failed'

        # Verify Config Zone
        config_qa = bytearray(len(config_data))
        assert cal.atcab_read_bytes_zone(
            Constants.ATCA_CONFIG_ZONE,
            0,
            16,
            config_qa,
            len(config_qa)) \
            == cal.Status.ATCA_SUCCESS, 'Reading Config zone failed'

        assert config_data \
            == config_qa, 'Configuration read does not match'

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
            = [self.is_config_zone_locked(), self.is_data_zone_locked()]

        return device_info

    def read_device_public_key(self, slot):
        device_pubkey = bytearray(64)
        assert cal.atcab_get_pubkey(slot, device_pubkey) \
            == cal.Status.ATCA_SUCCESS, 'Reading Public key is failed'
        device_pubkey = get_device_public_key(device_pubkey)
        device_pubkey = ec.EllipticCurvePublicNumbers(
                                x=int(device_pubkey[:64], 16),
                                y=int(device_pubkey[64:], 16),
                                curve=ec.SECP256R1()).public_key(get_backend())
        return device_pubkey

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    pass
