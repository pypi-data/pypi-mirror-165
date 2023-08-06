import os
import sys
from pathlib import Path
import yaml
import getpass
import rsa
from Crypto.PublicKey import RSA


ENCRYPTION_SLICE_SIZE = 500


class FilePath:
    api_configure = str(Path.home()) + "/.eaaip"
    credentials_file_name = "credentials.yaml"
    pri_key_file_name = "PROFILE_rsa.pem"
    credentials = os.path.join(api_configure, credentials_file_name)
    private_key = os.path.join(api_configure, pri_key_file_name)


class AIPLogin:
    """
        Login to AI Platform servers from the command line

    Usage:
        $ aip-login [command]
    Available Commands:
        configure           login with company email and password
    Use "aip-login [command] --help" for more information about a command.
    """
    def __init__(self, token=None):
        self._token = token
        self.credentials_temp = {
            "default":
                {
                    "ea_account": "username@ea.com",
                    "ea_password": "userpassword",
                    "public_key": "RSAPublicKey"
                }
        }

    def login(self, username=None, password=None, profile="default"):
        if not username or not password:
            username = input("EA Account: ")
            password = getpass.getpass(prompt="EA Account Password: ")

        # check if credential files exist, if exist update existing profile file
        if self._credential_files_exist():
            if self._profile_exist(profile):
                print("[INFO] Updating {} credential.".format(profile))
            else:
                print("[INFO] Adding {} profile.".format(profile))
            self._update_credentials(username, password, profile)
        else:
            print("[INFO] Creating {} credential.".format(profile))
            self._create_credentials(username, password, profile)

    def _create_credentials(self, username, password, profile_type="default"):
        credentials = self.credentials_temp
        try:
            if profile_type != "default":
                credentials[profile_type] = credentials.pop("default")

            public_key, private_key = self._generate_rsa_keys()
            encrypted_password = self._encrypt_data(password, public_key)
            credentials[profile_type]["ea_account"] = username
            credentials[profile_type]["ea_password"] = encrypted_password
            credentials[profile_type]["public_key"] = public_key

            os.mkdir(FilePath.api_configure)

            with open(FilePath.credentials, "w") as credentials_file:
                credentials_file.write(yaml.dump(credentials))
                print("[INFO] {} credential profile is created successfully at {}.".format(profile_type,
                                                                                           FilePath.credentials))
            with open(FilePath.private_key, "w") as private_key_file:
                private_key_file.write(private_key)
        except Exception as e:
            print("[ERROR]: Failed to create credentials files. ", e, file=sys.stderr)
        return

    def _credential_files_exist(self):
        try:
            if os.path.exists(FilePath.credentials) and os.path.exists(FilePath.private_key):
                return True
            else:
                return False
        except Exception as e:
            print("[ERROR] ", e)

    def _profile_exist(self, profile_type):
        try:
            with open(FilePath.credentials, "r") as credentials_file:
                credentials_dict = yaml.safe_load(credentials_file.read())
                if profile_type in credentials_dict.keys():
                    return True
                else:
                    print("[INFO] The {} profile is not found in your credentials file.".format(profile_type))
                    return False
        except Exception as e:
            print("[ERROR] ", e)

    def _generate_rsa_keys(self):
        try:
            public_key, private_key = rsa.newkeys(2048)

            # Export public key in PKCS#1 format, PEM encoded;  publicKey obj -> byte ->(decode) -> string
            public_key_pkcs1_pem = public_key.save_pkcs1().decode('utf8')
            private_key_pkcs1_pem = private_key.save_pkcs1().decode('utf8')
        except Exception as e:
            raise Exception(e)
        return public_key_pkcs1_pem, private_key_pkcs1_pem

    def _encrypt_data(self, data, public_key):
        try:
            pubkey = RSA.importKey(public_key)
            data_slices = []
            index = 0
            while index < len(data):
                data_slices.append(data[index:index+ENCRYPTION_SLICE_SIZE])
                index += ENCRYPTION_SLICE_SIZE

            enc_data = b""
            for i in range(0, len(data_slices)):
                enc_data += rsa.encrypt(data_slices[i].encode(), pubkey)
        except Exception as e:
            raise Exception(e)
        return enc_data

    def _update_credentials(self, username, password, profile_type="default"):
        try:
            with open(FilePath.credentials, "r+") as credentials_file:
                credentials = yaml.safe_load(credentials_file.read())

                public_key = credentials[list(credentials.keys())[0]]["public_key"]
                if profile_type not in credentials.keys():
                    credentials[profile_type] = credentials[list(credentials.keys())[0]].copy()
                encrypted_password = self._encrypt_data(password, public_key)
                credentials[profile_type]["ea_account"] = username
                credentials[profile_type]["ea_password"] = encrypted_password
                credentials_file.seek(0)
                credentials_file.write(yaml.dump(credentials))
                credentials_file.truncate()
                print("[INFO] {} credential profile is updated successfully.".format(profile_type))
        except Exception as e:
            raise Exception(e)
