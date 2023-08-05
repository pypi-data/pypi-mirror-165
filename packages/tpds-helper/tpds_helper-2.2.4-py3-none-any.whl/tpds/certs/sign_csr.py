# 2021 to present - Copyright Microchip Technology Inc. and its subsidiaries.

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
import os
from datetime import datetime, timezone
from cryptography import x509
from asn1crypto import pem
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from pathlib import Path
from .cert_utils import (pubkey_cert_sn, get_backend)
from .ext_builder import ExtBuilder, TimeFormat


class SignCSR():
    def __init__(self, csr_crt):
        if os.path.exists(csr_crt):
            cert_data = Path(csr_crt).read_bytes()
            if pem.detect(cert_data):
                self.csr = x509.load_pem_x509_csr(
                                    cert_data, get_backend())
            else:
                self.csr = x509.load_der_x509_csr(
                                    cert_data, get_backend())
        else:
            raise RuntimeError(f'{csr_crt} doesnt exists!')
        self.__verify_csr()

    def __verify_csr(self):
        try:
            self.csr.public_key().verify(
                        signature=self.csr.signature,
                        data=self.csr.tbs_certrequest_bytes,
                        signature_algorithm=ec.ECDSA(
                            self.csr.signature_hash_algorithm))
        except Exception as e:
            raise ValueError(f'{e} CSR signature is invalid!')

    def sign_csr(self, fn_ca_cert, fn_ca_key, ca_key_password=None):
        # print(f'Loading CA key:{fn_ca_key}... ', end='')
        with open(fn_ca_key, 'rb') as f:
            ca_priv_key = serialization.load_pem_private_key(
                data=f.read(),
                password=ca_key_password,
                backend=get_backend())

        # print(f'Loading CA certificate:{fn_ca_cert}... ', end='')
        with open(fn_ca_cert, 'rb') as f:
            ca_cert = x509.load_pem_x509_certificate(f.read(), get_backend())

        ca_cert_cn = ca_cert.subject.get_attributes_for_oid(
                        x509.oid.NameOID.COMMON_NAME)[0].value
        signer_id = self.csr.subject.get_attributes_for_oid(
                        x509.oid.NameOID.COMMON_NAME)[0].value[-4:]

        # print(f'Generating signer({signer_id})... ', end='')
        builder = ExtBuilder()
        builder = builder.issuer_name(ca_cert.issuer)
        builder = builder.not_valid_before(
            datetime.utcnow().replace(
                minute=0, second=0, microsecond=0, tzinfo=timezone.utc))
        validity = ca_cert.not_valid_after.year - \
            ca_cert.not_valid_before.year
        if validity > 31:
            builder = builder.not_valid_after(
                datetime(9999, 12, 31, 23, 59, 59, tzinfo=timezone.utc),
                format=TimeFormat.GENERALIZED_TIME)
        else:
            builder = builder.not_valid_after(builder._not_valid_before.replace(
                    year=builder._not_valid_before.year + validity),
                    format=TimeFormat.GENERALIZED_TIME)

        subject_attr = []
        for attr in ca_cert.subject:
            if attr.oid == x509.oid.NameOID.COMMON_NAME:
                cn = ca_cert_cn[:-4]+signer_id
                attr = x509.NameAttribute(
                    x509.oid.NameOID.COMMON_NAME, cn)
            subject_attr.append(attr)
        builder = builder.subject_name(x509.Name(subject_attr))
        builder = builder.public_key(self.csr.public_key())
        builder = builder.serial_number(pubkey_cert_sn(16, builder))
        for extn in ca_cert.extensions:
            if extn.oid._name == 'subjectKeyIdentifier':
                builder = builder.add_extension(
                        x509.SubjectKeyIdentifier.from_public_key(
                            self.csr.public_key()), extn.critical)
            elif extn.oid._name == 'authorityKeyIdentifier':
                builder = builder.add_extension(
                        x509.AuthorityKeyIdentifier.from_issuer_public_key(
                            ca_priv_key.public_key()), extn.critical)
            else:
                builder = builder.add_extension(
                                            extn.value, extn.critical)
        self.signer_crt = builder.sign(
                                private_key=ca_priv_key,
                                algorithm=hashes.SHA256(),
                                backend=get_backend())
        # print('OK')


if __name__ == '__main__':
    pass
