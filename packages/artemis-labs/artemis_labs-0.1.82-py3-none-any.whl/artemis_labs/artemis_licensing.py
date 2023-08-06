'''
This module handles Artemis licensing
'''

# pylint: disable=line-too-long
# pylint: disable=broad-except
# pylint: disable=wildcard-import
# pylint: disable=import-error


import winreg as reg
from licensing.methods import Key, Helpers

class ArtemisLicensing:
    '''
    This class contains static methods which handle Artemis licensing
    '''

    RSAPubKey = "<RSAKeyValue><Modulus>v7LkLQHHKGelDfPCVFrlgPpgfydlD0x2GhSKTuh2QKaTCwpGFlyHKs3WJW/y0bbgUHxRe4UYIWjb4MS3UMq0QbWvj+i9wPKE0Pj06RPiv+18/MWtIc3BGWGSQLmcfb4kD4dFMKEh9N4S1roNwcYbGjC/Iy4G+Pb6Z9VXKlbfcFtb2qZvypJSOFKHLehe3t67C2AmfuB4Rbb3z1GQrg6vrJMqwh3gpKP+9iUUB7QqdawSguY8rDBqg/wdxxp2oLZAhZNLVkm/EflLGIjN1uQ/r2ytHWdGXT+UxARTFcLIsCjH/r3qWofUrL9Jicd7f5fc28SQbrEw3HUeXo8PLYv05Q==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
    auth = "WyIyNDQ3NTY2NiIsIkJwTFppcXJmRUZOY1ljekdEYW1ENUl1c2FOaVdxVU1KVi85M3NUbzkiXQ=="
    product_id = 16565

    @staticmethod
    def get_cached_license():
        '''
        This method returns the cached license
        '''
        try:
            reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, 'SOFTWARE\\Classes\\artemis_labs')
            license_key = reg.QueryValue(reg_key, '')
            reg_key.Close()
            return license_key
        except FileNotFoundError:
            return None

    @staticmethod
    def set_cached_license(license_key):
        '''
        This method sets the cached license
        '''
        reg_key = reg.CreateKey(reg.HKEY_CURRENT_USER, 'SOFTWARE\\Classes\\artemis_labs')
        reg.SetValue(reg_key, '', reg.REG_SZ, license_key)
        reg_key.Close()


    @staticmethod
    def verify_license(license_key):
        '''
        This method verifies the license
        '''
        try:
            result = Key.activate(token=ArtemisLicensing.auth,\
                   rsa_pub_key=ArtemisLicensing.RSAPubKey,\
                   product_id=ArtemisLicensing.product_id, \
                   key=license_key,\
                   machine_code=Helpers.GetMachineCode(v=2))
        except Exception as exception: # pylint: disable=unused-variable
            return False

        if result[0] is None or not Helpers.IsOnRightMachine(result[0], v=2):
            return False

        return True
