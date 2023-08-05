# 2018 to present - Copyright Microchip Technology Inc. and its subsidiaries.

# Subject to your compliance with these terms, you may use Microchip software
# and any derivatives exclusively with Microchip products. It is your
# responsibility to comply with third party license terms applicable to your
# use of third party software (including open source software) that may
# accompany Microchip software.

# THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS".  NO WARRANTIES, WHETHER
# EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY IMPLIED
# WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A PARTICULAR
# PURPOSE. IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT, SPECIAL,
# PUNITIVE, INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE OF ANY
# KIND WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF MICROCHIP
# HAS BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE FORESEEABLE. TO THE
# FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL LIABILITY ON ALL CLAIMS IN
# ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED THE AMOUNT OF FEES, IF ANY,
# THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR THIS SOFTWARE.

import binascii
import os
import asn1crypto
import cryptography
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography import x509
from base64 import b16encode
from .cert import Cert
from .timefix_backend import backend
from OpenSSL import crypto


_backend = None


def get_backend():
    global _backend
    if not _backend:
        _backend = backend
    return _backend


def get_org_name(name):
    """
    Get the org name string from a distinguished name (RDNSequence)
    """
    for attr in name:
        if attr.oid == x509.oid.NameOID.ORGANIZATION_NAME:
            return attr.value
    return None


def get_device_sn_cert(cert, find_value='0123'):
    """
    Get the device serial number from certificate and return it.
    """
    for attr in cert.subject:
        if attr.oid == x509.oid.NameOID.COMMON_NAME:
            x = attr.value.find(find_value)
            if (x != -1):
                return attr.value[x:x+18]
            else:
                return None
    return None


def get_ca_status(cert):
    """
    Return the CA value of the certificate
    Inputs:
        cert       the certificate for which the CA valuen is to be checked
    Outputs:
        True/False True if the certificate is CA otherwise False
    """
    try:
        return cert.extensions.get_extension_for_oid(
            x509.oid.ExtensionOID.BASIC_CONSTRAINTS).value.ca
    except Exception:
        return None


def random_cert_sn(size):
    """
    Create a positive, non-trimmable serial number for X.509 certificates
    """
    raw_sn = bytearray(os.urandom(size))
    # Force MSB bit to 0 to ensure positive integer
    # Force next bit to 1 to ensure the integer won't be trimmed
    # in ASN.1 DER encoding
    raw_sn[0] = raw_sn[0] & 0x7F
    raw_sn[0] = raw_sn[0] | 0x40

    return int.from_bytes(raw_sn, byteorder='big', signed=False)


def pubkey_cert_sn(size, builder):
    """
    Cert serial number is the SHA256(Subject public key + Encoded dates)
    """
    # Get the public key as X and Y integers concatenated
    pub_nums = builder._public_key.public_numbers()
    pubkey = pub_nums.x.to_bytes(32, byteorder='big', signed=False)
    pubkey += pub_nums.y.to_bytes(32, byteorder='big', signed=False)

    # Get the encoded dates
    expire_years = builder._not_valid_after.year - \
        builder._not_valid_before.year
    if builder._not_valid_after.year == 9999:
        # This year is used when indicating no expiration
        expire_years = 0
    elif expire_years > 31:
        # We default to 1 when using a static expire beyond 31
        expire_years = 1

    enc_dates = bytearray(b'\x00'*3)
    enc_dates[0] = (enc_dates[0] & 0x07) \
        | ((((builder._not_valid_before.year - 2000) & 0x1F) << 3) & 0xFF)
    enc_dates[0] = (enc_dates[0] & 0xF8) \
        | ((((builder._not_valid_before.month) & 0x0F) >> 1) & 0xFF)
    enc_dates[1] = (enc_dates[1] & 0x7F) \
        | ((((builder._not_valid_before.month) & 0x0F) << 7) & 0xFF)
    enc_dates[1] = (enc_dates[1] & 0x83) \
        | (((builder._not_valid_before.day & 0x1F) << 2) & 0xFF)
    enc_dates[1] = (enc_dates[1] & 0xFC) \
        | (((builder._not_valid_before.hour & 0x1F) >> 3) & 0xFF)
    enc_dates[2] = (enc_dates[2] & 0x1F) \
        | (((builder._not_valid_before.hour & 0x1F) << 5) & 0xFF)
    enc_dates[2] = (enc_dates[2] & 0xE0) | ((expire_years & 0x1F) & 0xFF)
    enc_dates = bytes(enc_dates)

    # SAH256 hash of the public key and encoded dates
    digest = hashes.Hash(
        hashes.SHA256(),
        backend=cryptography.hazmat.backends.default_backend())
    digest.update(pubkey)
    digest.update(enc_dates)
    raw_sn = bytearray(digest.finalize()[:size])
    # Force MSB bit to 0 to ensure positive integer
    # Force next bit to 1 to ensure the integer won't be trimmed
    # in ASN.1 DER encoding
    raw_sn[0] = raw_sn[0] & 0x7F
    raw_sn[0] = raw_sn[0] | 0x40

    return int.from_bytes(raw_sn, byteorder='big', signed=False)


def is_key_file_password_protected(key_filename):
    """Check if the file is protected with password or not

    Args:
        key_filename (file): File name

    Returns:
        bool: True if yes, False if no.
    """
    try:
        with open(key_filename, 'rb') as f:
            serialization.load_pem_private_key(
                data=f.read(), password=None, backend=get_backend())
        return False
    except TypeError:
        return True


def add_signer_extensions(builder, public_key=None, authority_cert=None):
    if public_key is None:
        # Public key not specified, assume its in the builder (cert builder)
        public_key = builder._public_key

    builder = builder.add_extension(
        x509.KeyUsage(
            digital_signature=True,
            content_commitment=False,
            key_encipherment=False,
            data_encipherment=False,
            key_agreement=False,
            key_cert_sign=True,
            crl_sign=True,
            encipher_only=False,
            decipher_only=False),
        critical=True)

    builder = builder.add_extension(
        x509.BasicConstraints(ca=True, path_length=0),
        critical=True)
    builder = builder.add_extension(
        x509.SubjectKeyIdentifier.from_public_key(public_key),
        critical=False)

    # Save newly created subj key id extension
    subj_key_id_ext = builder._extensions[-1]

    if authority_cert:
        # We have an authority certificate, use its subject key id
        builder = builder.add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_subject_key_identifier(
                authority_cert.extensions.get_extension_for_class(
                    x509.SubjectKeyIdentifier).value),
            critical=False)
    else:
        # No authority cert, assume this is a CSR and just use its own
        # subject key id
        builder = builder.add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_subject_key_identifier(
                subj_key_id_ext.value),
            critical=False)

    return builder


def get_device_sn_number(device_sn, prefix='sn'):
    """
    Helper function to convert the device serial number to
    ascii format
    """
    if device_sn is None:
        device_sn = 'sn0123030405060708EE'
    elif isinstance(device_sn, bytearray):
        device_sn = prefix+b16encode(device_sn).decode('ascii')
    elif isinstance(device_sn, str):
        pass
    else:
        raise ValueError('Unknown device_sn type ')

    return device_sn


def get_device_public_key(device_public_key):
    """
    Helper function to convert the public key to
    ascii format
    """
    if device_public_key is None:
        device_public_key = '' \
            '71f1a70da379a3fded6b5010bdad6e1f' \
            'b9e8eba7df2c4b5c67d35eba84da09e7' \
            '7ae8db2ccb9628eeeb85cdaab35c92e5' \
            '3e1c44d55a2ba7a024aa92603b68948a'
    elif isinstance(device_public_key, bytearray):
        device_public_key = b16encode(device_public_key).decode('ascii')
    elif isinstance(device_public_key, str):
        pass
    else:
        raise ValueError('Unknown device_public_key type')

    return device_public_key


def get_certificate_thumbprint(cert):
    """
    Function return thumbprint of the given certificate
    Inputs:
            cert           certificate contain thumbprint
    Outputs:
            fignerprint    cerificate thumbprint/fingerprint
    """
    crt = Cert()
    crt.set_certificate(cert)
    fingerprint = binascii.hexlify(crt.certificate.fingerprint(
                        hashes.SHA1())).decode().upper()

    return fingerprint


def get_certificate_CN(cert):
    """
    Function return certificate common name
    Inputs:
            cert         path to certificate
    Outputs:
            return certificate common name
    """
    crt = Cert()
    crt.set_certificate(cert)
    device_id = crt.certificate.subject.get_attributes_for_oid(
                        x509.oid.NameOID.COMMON_NAME)[0].value

    return device_id


def get_certificate_tbs(cert):
    """
    Function return certificate tbs
    Inputs:
        cert      path to certificate
    Outputs:
        return certificate tbs
    """
    crt = Cert()
    crt.set_certificate(cert)
    cert_tbs = asn1crypto.x509.Certificate.load(
        crt.certificate.public_bytes(
            encoding=serialization.Encoding.DER))['tbs_certificate']

    return cert_tbs.dump()


def get_cert_content(certificate):
    """
    Function return certificate in TEXT format
    Inputs:
            certificate             Contains certificate in PEM format

    Outputs:
            cert_content            Contains certificate in TEXT format
    """
    cert_object = crypto.load_certificate(crypto.FILETYPE_PEM, certificate)
    cert_content = crypto.dump_certificate(crypto.FILETYPE_TEXT, cert_object)
    return cert_content


def get_cert_print_bytes(cert):
    """
    Function return string contains certificate PEM + TEXT format
    Inputs:
            cert                  Contains certificate in PEM or bytes format

    Outputs:
            cert_bytes            Contains certificate in PEM + TEXT format
    """
    # collect PEM bytes
    cert_bytes = cert.decode("utf-8")
    cert_bytes += '\n'

    # collect certificate text
    cert_bytes += get_cert_content(cert).decode("utf-8")
    cert_bytes += '\n'

    # contains both PEM and certificate text
    return cert_bytes

def is_signature_valid(certificate, public_key):
    """
    Verifies the certificate with the public key
    """
    if not isinstance(public_key, ec.EllipticCurvePublicKey):
        raise ValueError("Invalid public key received")

    try:
        public_key.verify(
                    signature=certificate.signature,
                    data=certificate.tbs_certificate_bytes,
                    signature_algorithm=ec.ECDSA(
                        certificate.signature_hash_algorithm))
        return True
    except Exception as e:
        return False