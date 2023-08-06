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

import struct
import cryptography
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import Encoding
import cryptoauthlib as cal

from tpds.certs.tflex_certs import TFLEXCerts
from tpds.secure_element import ECC204
from tpds.secure_element.constants import Constants
from tpds.certs.cert_utils import is_signature_valid

class ECC204Provision():
    def __init__(self, interface='i2c', address=0x33):
        self.element = ECC204(interface, address)

    def perform_genkey(self, slot):
        slot_public_key = bytearray(64)
        status = cal.atcab_genkey(slot, slot_public_key)
        assert status == cal.Status.ATCA_SUCCESS, 'Genkey failed'
        return slot_public_key

    def perform_slot_write(self, slot, data):
        status = cal.atcab_write_bytes_zone(
                        Constants.ATCA_DATA_ZONE,
                        slot, 0, data, len(data))
        assert status == cal.Status.ATCA_SUCCESS, 'Slot Write failed'

    def provision_cert_slot(self, root_cert, signer_cert, device_cert):
        certs = TFLEXCerts('ECC204')
        certs.set_tflex_certificates(root_cert, signer_cert, device_cert)
        template = certs.get_tflex_py_definitions()
        assert cal.atcacert_write_cert(
                template.get('signer'),
                certs.signer.get_certificate_in_der(),
                len(certs.signer.get_certificate_in_der())) \
            == cal.Status.ATCA_SUCCESS, \
            "Loading signer certificate into slot failed"
        assert cal.atcacert_write_cert(
                template.get('device'),
                certs.device.get_certificate_in_der(),
                len(certs.device.get_certificate_in_der())) \
            == cal.Status.ATCA_SUCCESS, \
            "Loading device certificate into slot failed"

    def provision_wpc_slots(self, root_cert, mfg_cert, pdu_cert):
        assert is_signature_valid(root_cert, root_cert.public_key()) == True, \
            'Root certificate signature verification failed'
        assert is_signature_valid(mfg_cert, root_cert.public_key()) == True, \
            'MFG certificate signature verification failed'
        assert is_signature_valid(pdu_cert, mfg_cert.public_key()) == True, \
            'PDU certificate signature verification failed'

        root_bytes = root_cert.public_bytes(encoding=Encoding.DER)
        mfg_bytes = mfg_cert.public_bytes(encoding=Encoding.DER)
        pdu_bytes = pdu_cert.public_bytes(encoding=Encoding.DER)

        # Calculate root digest, cert chain digest and write to Slot2
        root_hash = hashes.Hash(
                hashes.SHA256(),
                backend=cryptography.hazmat.backends.default_backend())
        root_hash.update(root_bytes)
        root_digest = root_hash.finalize()[:32]

        length = 2 + len(root_digest) + len(mfg_bytes) + len(pdu_bytes)
        cert_chain = b''
        cert_chain += struct.pack('>H', length)
        cert_chain += root_digest + mfg_bytes + pdu_bytes
        chain_hash = hashes.Hash(
                hashes.SHA256(),
                backend=cryptography.hazmat.backends.default_backend())
        chain_hash.update(cert_chain)
        chain_digest = chain_hash.finalize()[:32]

        # Write Slot1 and Slot2 data to device
        self.perform_slot_write(1, pdu_bytes)
        self.perform_slot_write(2, chain_digest)

        return {
            'root_cert': root_bytes,
            'root_digest': root_digest,
            'mfg_cert': mfg_bytes
        }




# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    pass
