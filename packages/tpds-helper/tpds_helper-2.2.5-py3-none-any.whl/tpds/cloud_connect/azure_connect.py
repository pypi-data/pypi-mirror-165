# -*- coding: utf-8 -*-
# 2018 to present - Copyright Microchip Technology Inc. and its subsidiaries.

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
import os
import re
import sys
import yaml
from cryptography import x509
from datetime import datetime, timezone, timedelta
from pathlib import Path
from .cloud_connect import CloudConnect
from tpds.certs.cert import Cert
from tpds.certs.cert_utils import (get_certificate_CN,
                              get_certificate_thumbprint,
                              random_cert_sn)
from tpds.tp_utils.tp_utils import run_subprocess_cmd
from tpds.tp_utils.tp_settings import TPSettings
from tpds.tp_utils.tp_keys import TPAsymmetricKey
from tpds.manifest import ManifestIterator, Manifest


class AzureConnect(CloudConnect):
    def __init__(self):
        self.default_creds = {
            'title': 'Azure IoT Credentials',
            'iot_hub': '',
            'subscription_id': ''
        }
        self.creds_file = os.path.join(
                            TPSettings().get_base_folder(),
                            'azure_credentials.yaml')
        if not os.path.exists(self.creds_file):
            Path(self.creds_file).write_text(
                    yaml.dump(self.default_creds, sort_keys=False))

    def set_credentials(self, credentials):
        """
        Method login azure portal via cli and
        set the credentials in azure cli

        Inputs:
              credentials    contain azure iot hub name and
                             subscription id
        """
        if not isinstance(credentials, dict):
            raise ValueError('Unsupported User credentials type')

        self.n_tail = '.azure-devices.net'
        self.az_hub_name = credentials.get('iot_hub')
        if self.az_hub_name.endswith(self.n_tail):
            self.az_hub_name = self.az_hub_name[:-len(self.n_tail)]
        self.az_subscription_id = credentials.get('subscription_id')

        # login to acccount
        sys_shell = True if sys.platform == 'win32' else False
        print("Login to Azure account....", end='')
        subProcessOut = run_subprocess_cmd(
            cmd=["az", "login"], sys_shell=sys_shell)
        if subProcessOut.returncode:
            raise ValueError('Azure login failed with {}'.format(
                                            subProcessOut.returncode))
        print('OK')

        # Setting up azure subscription id
        print("Setting the Subscription ID....", end='')
        subProcessOut = run_subprocess_cmd(
            cmd=[
                "az", "account", "set",
                "--subscription", self.az_subscription_id],
            sys_newlines=True, sys_shell=sys_shell)
        if subProcessOut.returncode:
            raise ValueError('Setting subscription failed with {}'.format(
                                            subProcessOut.returncode))
        print('OK')

    def register_device_as_self_signed(self, device_cert):
        """
        Method register device with authentication method as
        X509 self signed authentication. In this method, it will
        register device certificate thumbprint to Azure

        Inputs:
              device_cert      device certificate to be registered
        """
        device_id = get_certificate_CN(device_cert)
        thumbprint = get_certificate_thumbprint(device_cert)

        if self.is_device_registered(device_id):
            self.delete_registered_device(device_id)

        sys_shell = True if sys.platform == 'win32' else False
        print('Registering device with thumbprint {}...'.format(
              thumbprint), end='')
        subProcessOut = run_subprocess_cmd(
            cmd=[
                "az", "iot", "hub", "device-identity", "create",
                "-n", self.az_hub_name,
                "-d", device_id,
                "--am", "x509_thumbprint",
                "--ptp", thumbprint,
                "--stp", thumbprint],
            sys_newlines=True, sys_shell=sys_shell)
        if subProcessOut.returncode:
            raise ValueError('Device registration failed with {}'.format(
                                                    subProcessOut.returncode))
        print('OK')

    def register_device_as_CA_signed(self, device_cert):
        """
        Method register device with authentication method as
        X509 CA signed authentication. In this method, device certificate
        common name is registered as device id

        Inputs:
              device_cert     device certificate to be registered
        """
        device_id = get_certificate_CN(device_cert)

        if self.is_device_registered(device_id):
            self.delete_registered_device(device_id)

        print('Registering device with id {}...'.format(device_id), end='')
        sys_shell = True if sys.platform == 'win32' else False
        subProcessOut = run_subprocess_cmd(
            cmd=[
                "az", "iot", "hub", "device-identity", "create",
                "-n", self.az_hub_name,
                "-d", device_id,
                "--am", "x509_ca"],
            sys_newlines=True, sys_shell=sys_shell)
        if subProcessOut.returncode:
            raise ValueError('Device registration failed with {}'.format(
                                                subProcessOut.returncode))
        print('OK')

    def register_device_from_manifest(
            self, device_manifest, device_manifest_ca,
            key_slot=0, as_self_signed=True):
        """
        Method register device from given manifest
        Inputs:
              device_manifest     manifest contains certs and public keys
              device_manifest_ca  manifest signer key
              key_slot            slot where device private key present

            return true if device registered successfully else false
        """
        if os.path.exists(device_manifest) \
                and device_manifest.endswith('.json'):
            with open(device_manifest) as json_data:
                device_manifest = json.load(json_data)

        if not isinstance(device_manifest, list):
            raise ValueError('Unsupport manifest format to process')

        manifest_ca = Cert()
        manifest_ca.set_certificate(device_manifest_ca)
        iterator = ManifestIterator(device_manifest)
        print('Number of Devices: {}'.format(iterator.index))

        while iterator.index != 0:
            se = Manifest().decode_manifest(
                iterator.__next__(), manifest_ca.certificate)
            se_certs = Manifest().extract_public_data_pem(se)
            slot = next((sub for sub in se_certs if sub.get(
                'id') == str(key_slot)), None)
            no_of_certs = len(slot.get('certs'))
            if no_of_certs:
                device_cert = 'device.crt'
                with open(device_cert, 'w') as f:
                    f.write(slot.get('certs')[no_of_certs - 2])
                    f.close()

                if as_self_signed:
                    self.register_device_as_self_signed(device_cert)
                else:
                    self.register_device_as_CA_signed(device_cert)

    def is_device_registered(self, device_id):
        """
        Method checks whether device is registered or not
        Inputs:
             device_id      device certificate common name

            return true if device is registered else false
        """
        sys_shell = True if sys.platform == 'win32' else False
        subProcessOut = run_subprocess_cmd(
            cmd=[
                "az", "iot", "hub", "device-identity", "list",
                "--hub-name", self.az_hub_name,
                "--query", "[].deviceId"],
            sys_newlines=True, sys_shell=sys_shell)
        if subProcessOut.returncode:
            raise ValueError('Device id query failed with {}'.format(
                                                subProcessOut.returncode))

        reg_device_id = re.findall(r'"(.*?)"', subProcessOut.stdout)
        return (device_id in reg_device_id)

    def delete_registered_device(self, device_id):
        '''
        Method delete the registered device in Azure IoT hub
        Inputs:
            device_id        device certificate common name
        '''
        print('Try Deleting device...', end='')
        sys_shell = True if sys.platform == 'win32' else False
        subProcessOut = run_subprocess_cmd(
            cmd=[
                "az", "iot", "hub", "device-identity", "delete",
                "-n", self.az_hub_name,
                "-d", device_id],
            sys_newlines=True, sys_shell=sys_shell)
        if subProcessOut.returncode:
            raise ValueError('Device deletion failed with {}'.format(
                                                subProcessOut.returncode))
        print('OK')

    def register_signer_certificate(
                        self, signer_cert, signer_key='', verify_cert=''):
        '''
        Method register the signer certificate in Azure IoT hub
        Steps followed to register signer:
        1. Upload signer certificate
        2. Get verification code and generate verification certificate
        3. Upload verification certificate

        Inputs:
              signer_cert    signer certificate to be registered
              signer_key     key to sign the verification cert
                             for proof of possession
              verify_cert    verification cert to be uploaded
                             to validate signer certificate
        '''
        if not signer_key and not signer_cert:
            raise ValueError(
                'Either signer key or verify cert required to register')

        if self.is_signer_registered(signer_cert):
            self.delete_registered_signer(signer_cert)

        self.upload_signer_cert(signer_cert)

        if not verify_cert:
            verify_cert = 'verify_cert.cer'
            self.get_verification_cert(signer_key, signer_cert, verify_cert)

        self.activate_signer_cert(signer_cert, verify_cert)

    def upload_signer_cert(self, signer_cert):
        """
        Method upload signer certificate to Azure IoT hub

        Inputs:
            signer_cert      signer certificate
        """
        if not isinstance(signer_cert, str) or not os.path.exists(signer_cert):
            raise FileNotFoundError("Unknown Signer certificate type")

        signer_name = 'signer_{}'.format(
                            get_certificate_thumbprint(signer_cert))

        # Upload the signer certificate
        print('Uploading signer certificate to Azure IoT hub...', end='')
        sys_shell = True if sys.platform == 'win32' else False
        subProcessOut = run_subprocess_cmd(
            cmd=[
                "az", "iot", "hub", "certificate", "create",
                "--hub-name", self.az_hub_name,
                "--name", signer_name,
                "--path", signer_cert],
            sys_newlines=True, sys_shell=sys_shell)
        if subProcessOut.returncode:
            raise ValueError('Uploading Signer failed with {}'.format(
                                                subProcessOut.returncode))
        print('OK')

    def activate_signer_cert(self, signer_cert, verify_cert):
        """
        Method upload verification certificate, by validating this
        certificate, signer certificate will be registered successfully

        Inputs:
            signer_cert    path to signer certificate
            verify_cert    path to verification certificate
        """
        if not isinstance(signer_cert, str) or not os.path.exists(signer_cert):
            raise FileNotFoundError("Unknown Signer certificate type")

        if (not isinstance(verify_cert, str) or
           not os.path.exists(verify_cert)):
            raise FileNotFoundError("Unknown Verification certificate type")

        signer_name = 'signer_{}'.format(
                            get_certificate_thumbprint(signer_cert))
        etag = self.get_signer_certificate_etag(signer_cert)

        # Uploading verification certificate
        print('Uploading verification certificate to azure IoT hub...', end='')
        sys_shell = True if sys.platform == 'win32' else False
        subProcessOut = run_subprocess_cmd(
            cmd=[
                "az", "iot", "hub", "certificate", "verify",
                "--hub-name", self.az_hub_name,
                "--name", signer_name,
                "--path", verify_cert,
                "--etag", etag],
            sys_newlines=True, sys_shell=sys_shell)
        if subProcessOut.returncode:
            raise ValueError('Uploading Verify cert failed with {}'.format(
                                                subProcessOut.returncode))
        print('OK')

    def is_signer_registered(self, signer_cert):
        """
        Method check whether signer certificate is registered or not
        Inputs:
              signer_cert    signer certificate

            return true if signer certificate registered else false
        """
        signer_fingerprint = get_certificate_thumbprint(signer_cert)

        sys_shell = True if sys.platform == 'win32' else False
        subProcessOut = run_subprocess_cmd(
            cmd=[
                "az", "iot", "hub", "certificate", "list",
                "--hub-name", self.az_hub_name,
                "--query", "value[].properties[].thumbprint"],
            sys_newlines=True, sys_shell=sys_shell)
        if subProcessOut.returncode:
            raise ValueError('Certificate list failed with {}'.format(
                                                subProcessOut.returncode))

        reg_signer_fignerprint = re.findall(r'"(.*?)"', subProcessOut.stdout)
        return (signer_fingerprint in reg_signer_fignerprint)

    def delete_registered_signer(self, signer_cert):
        """
        Method delete the registered signer certificate in Azure IoT hub
        Inputs:
             signer_cert      signer certificate registered already
        """
        signer_name = 'signer_{}'.format(
                            get_certificate_thumbprint(signer_cert))

        # Get eTag
        eTag = self.get_signer_certificate_etag(signer_cert)

        print('Try Deleting Signer...', end='')
        sys_shell = True if sys.platform == 'win32' else False
        subProcessOut = run_subprocess_cmd(
            cmd=[
                "az", "iot", "hub", "certificate", "delete",
                "--etag", eTag,
                "--name", signer_name,
                "--hub-name", self.az_hub_name],
            sys_newlines=True, sys_shell=sys_shell)
        if subProcessOut.returncode:
            raise ValueError('Device deletion failed with {}'.format(
                                                subProcessOut.returncode))
        print('OK')

    def get_verification_cert(self, signer_key, signer_cert, file=''):
        """
        Method get the verification code and generate verification cert

        Inputs:
              signer_key      signer key which sign the verification cert
              signer_cert     signer certificate
              file            path where verification cert loaded

            return verification certificate
        """
        ca_key = TPAsymmetricKey(signer_key)
        ca_cert = Cert()
        ca_cert.set_certificate(signer_cert)

        etag_id = self.get_signer_certificate_etag(signer_cert)
        signer_fingerprint = get_certificate_thumbprint(signer_cert)
        signer_name = 'signer_{}'.format(signer_fingerprint)

        # Request a verification code for signer certificate
        print('Getting verification code from azure IoT hub...', end='')
        sys_shell = True if sys.platform == 'win32' else False
        subProcessOut = run_subprocess_cmd(
            cmd=[
                "az", "iot", "hub", "certificate",
                "generate-verification-code", "--hub-name", self.az_hub_name,
                "--name", signer_name, "--etag", etag_id],
            sys_newlines=True, sys_shell=sys_shell)
        if subProcessOut.returncode:
            raise ValueError('Verification code request failed with {}'.format(
                                                    subProcessOut.returncode))
        reg_code = json.loads(subProcessOut.stdout).get(
            'properties').get('verificationCode')
        print('{}'.format(reg_code))

        # Generate a verification certificate around the registration code
        # (subject common name)
        print('Generating signer CA verification certificate...', end='')
        verify_cert = Cert()
        verify_cert.builder = x509.CertificateBuilder()
        verify_cert.builder = verify_cert.builder.serial_number(
                                random_cert_sn(16))
        verify_cert.builder = verify_cert.builder.issuer_name(
            ca_cert.certificate.subject)
        verify_cert.builder = verify_cert.builder.not_valid_before(
            datetime.utcnow().replace(tzinfo=timezone.utc))
        verify_cert.builder = verify_cert.builder.not_valid_after(
            verify_cert.builder._not_valid_before + timedelta(days=1))
        verify_cert.builder = verify_cert.builder.subject_name(
            x509.Name(
                [x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, reg_code)]))
        verify_cert.builder = verify_cert.builder.public_key(
            ca_cert.certificate.public_key())
        verify_cert.sign_builder(ca_key.get_private_key())
        print('OK')

        if file:
            Path(file).write_bytes(verify_cert.get_certificate_in_pem())

        return verify_cert

    def get_signer_certificate_etag(self, signer_cert):
        """
        Methos get the etag from Azure IoT hub for given signer certificate
        Inputs:
              signer_cert       signer certificate
        Outputs:
              etag              etag for signer certifcate
        """
        signer_name = 'signer_{}'.format(
                            get_certificate_thumbprint(signer_cert))

        sys_shell = True if sys.platform == 'win32' else False
        subProcessOut = run_subprocess_cmd(
            cmd=[
                "az", "iot", "hub", "certificate", "show",
                "--hub-name", self.az_hub_name,
                "--name", signer_name,
                "--query", "etag"],
            sys_newlines=True, sys_shell=sys_shell)
        if subProcessOut.returncode:
            raise ValueError('Certificate list failed with {}'.format(
                                                subProcessOut.returncode))

        # Get eTag
        return subProcessOut.stdout.rstrip("\n")


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    pass
