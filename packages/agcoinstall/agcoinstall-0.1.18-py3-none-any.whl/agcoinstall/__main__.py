"""Command-line interface."""
import base64
import configparser
import fileinput
import hashlib
import hmac
import logging
import os
import platform
import random
import shutil
import subprocess
import time
import json

from pathlib import Path
import arrow
import click
import psutil
import pyautogui
import regobj
import requests
from lxml import etree
from clumper import Clumper
from requests.auth import AuthBase

host = ''
base_url = ''
mac_id = ''
mac_token = ''
state = 'InitialMonitoring'

save_path = os.path.expanduser('~\\Desktop\\agcoinstall.log')
logging.basicConfig(filename=save_path, level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


class MACAuth(AuthBase):
    """
    Attaches HTTP Authentication to the given Request object, and formats the header for every API call used
    """

    def __init__(self, mac_id, mac_token, host):
        # setup any auth-related data here
        self.mac_id = mac_id
        self.mac_token = mac_token
        self.host = host

    def __call__(self, r):
        # modify and return the request
        r.headers['Authorization'] = self.generate_header(r.method, r.path_url)
        return r

    def get_hmac(self, method, uri, milliseconds, nonce):
        http_version = 'HTTP/1.1'
        # host = HOST
        request_string = f'{method} {uri} {http_version}\n{self.host}\n{milliseconds}\n{nonce}\n'
        return base64.b64encode(
            hmac.new(self.mac_token.lower().encode(), request_string.encode(), hashlib.sha256).digest()).decode()

    def generate_header(self, method, uri):
        milliseconds = str(int(time.time() * 1000))
        nonce = ''.join(str(random.randint(0, 9)) for _i in range(8))
        formatted_hmac = self.get_hmac(method, uri, milliseconds, nonce)
        return f'MAC kid={self.mac_id},ts={milliseconds},nonce={nonce},mac=\"{formatted_hmac}\"'


# class RegistryValues:
#
#     def __init__(self):
#         self._voucher = ''
#         self._edt_update = ''
#         self._mtapi = ''
#
#     @property
#     def voucher(self):
#         """
#         gets and return the voucher in the registry
#         @return: voucher code as text
#         """
#         try:
#             voucher_id = regobj.HKLM.SOFTWARE.WOW6432Node.get_subkey(r'AGCO Corporation').EDT['Voucher'].data
#         except AttributeError as e:
#             click.secho(f'Voucher ID was not present in registry. Please confirm that EDT has been vouchered {e}',
#                         fg='red')
#             logging.error(f'Voucher ID was not present in registry. Please confirm that EDT has been vouchered {e}')
#             voucher_id = ''
#         except KeyError:
#             voucher_id = ''
#         self._voucher = voucher_id
#         return voucher_id
#
#     @property
#     def edt_update(self):
#         """
#             gets and return the edt_update in the registry
#             @return: edt_update code as text
#             """
#         try:
#             edt_update = regobj.HKLM.SOFTWARE.WOW6432Node.get_subkey(r'AGCO Corporation').EDT['UpdateNumber'].data
#         except AttributeError as e:
#             click.secho(f'UpdateNumber was not present in registry. It does not appear that EDT is currently'
#                         f'installed.  \n {e}', fg='red')
#             edt_update = ''
#         except KeyError:
#             edt_update = ''
#         self._edt_update = edt_update
#         return edt_update
#
#     @property
#     def mtapi(self):
#         """
#             gets and return the mtapi in the registry
#             @return: mtapi code as text
#         """
#         try:
#             mtapi = regobj.HKLM.SOFTWARE.WOW6432Node.get_subkey(r'AGCO Corporation').EDT['MTAPISync_Version'].data
#         except AttributeError as e:
#             click.secho(f'UpdateNumber was not present in registry. It does not appear that EDT is currently '
#                         f'installed. \n {e}', fg='red')
#             mtapi = ''
#         except KeyError:
#             mtapi = ''
#         self._mtapi = mtapi
#         return mtapi


class AUC:
    def __init__(self):
        self.installed = Path(
            r"C:\Program Files (x86)\AGCO Corporation\AGCO Update Client\AGCOUpdateService.exe").is_file()
        self._environment = ''
        self.auc_state = ''
        self._client_id = ''
        self._hardware_id = ''
        self._version = ''
        self._check_in_status = ''
        self._last_check_in = ''
        self._active_packages = ''

    @property
    def environment(self):
        environment_dict = {'https://secure.agco-ats.com/api/v2': "Production",
                            'https://edtsystems-webtest.azurewebsites.net/api/v2': "Test",
                            'https://edtsystems-webtest-dev.azurewebsites.net/api/v2': "Development",
                            }
        parser = configparser.ConfigParser()
        if Path(r"C:\ProgramData\AGCO Corporation\AGCO Update\config.ini").is_file():
            try:
                parser.read(r'C:\ProgramData\AGCO Corporation\AGCO Update\config.ini')
                update_host = parser.get('Settings', 'UpdateHost')
                auc_environment = environment_dict[update_host]
                self._environment = auc_environment
                return auc_environment
            except Exception as ex:
                logging.debug(f'Could not read config.ini to determine the environment\n{ex}')
        else:
            logging.info("AUC does not seem to be installed")

    @property
    def client_info(self):
        base_url = "http://localhost:51712"
        endpoint = "/ClientInfo"
        uri = f"{base_url}{endpoint}"
        r = requests.get(uri)
        results = r.json()
        self._client_id = results["ClientID"]
        self._hardware_id = results["HardwareID"]
        self._version = results["Version"]
        return results

    @property
    def active_packages(self):
        base_url = "http://localhost:51712"
        endpoint = "/ActivePackages"
        uri = f"{base_url}{endpoint}"
        r = requests.get(uri)
        results = r.json()
        self._active_packages = results
        return results

    @property
    def edt_is_installed(self):
        edt_install_status = Clumper(self.active_packages).keep(lambda d: 'EDT Framework' in d["Description"])\
            .keep(lambda d: d['Status'] == "Success").blob
        if len(edt_install_status) > 0:
            return True
        else:
            try:
                edt_update = regobj.HKLM.SOFTWARE.WOW6432Node.get_subkey(r'AGCO Corporation').EDT['UpdateNumber'].data
                if edt_update:
                    return True
            except (AttributeError, KeyError) as e:
                click.secho(f'UpdateNumber was not present in registry. It does not appear that EDT is currently'
                            f'installed.  \n {e}', fg='red')
                return False

    @property
    def client_status(self):
        logging.debug("Attempting to update AUC client status")
        base_url = "http://localhost:51712"
        endpoint = "/ClientStatus"
        uri = f"{base_url}{endpoint}"
        r = requests.get(uri)
        results = r.json()
        self.auc_state = results['State']
        self._check_in_status = results['CheckInStatus']
        self._last_check_in = results['LastCheckIn']
        if r.status_code == 200:
            logging.debug(f"AUC's client status is refreshed.")
        elif r.status_code == 500:
            self.start_auc()
        else:
            logging.debug(f"The attempt to update the AUC's client status resulted in a  {r.status_code} StatusCode")
        return results

    def install_now(self):
        logging.debug("Attempting to have AUC start installs")
        base_url = "http://localhost:51712"
        endpoint = "/ClientStatus/InstallNow?sessionID=1"
        uri = f"{base_url}{endpoint}"
        r = requests.post(uri)
        if r.status_code == 200:
            logging.debug("AUC starting installs")
        else:
            logging.debug(f"The attempt to install downloaded packages resulted in a {r.status_code} StatusCode")


    def check_in(self, force=True):
        logging.debug("Attempting to have AUC checkin")
        base_url = "http://localhost:51712"
        endpoint = "/ClientStatus/CheckIn"
        uri = f"{base_url}{endpoint}?force={force}"
        r = requests.post(uri)
        if r.status_code == 200:
            logging.debug("AUC checked in")
        else:
            logging.debug(f"The attempt to have AUC check in  resulted in a {r.status_code} StatusCode")


    def update_all(self):
        self.client_info
        self.client_status
        self.active_packages

    def download(self):
        url = 'https://agcoedtdyn.azurewebsites.net/AGCOUpdateClient'
        save_path = os.path.expanduser('~\\Desktop\\AGCOUpdateClient.exe')
        try:
            r = requests.get(url, allow_redirects=True)
            try:
                open(save_path, 'wb').write(r.content)
            except:
                logging.error('Unable to download the AUC client')
        except:
            logging.error('The link to download the latest AUC is down')

    def install(self):
        execute_command(os.path.expanduser('~\\Desktop\\AGCOUpdateClient.exe /S /V INITCLIENT 1'))

    def start_auc(self):
        logging.debug('Attempting to start AUC')
        if is_os_64bit():
            loc = r'C:\Program Files (x86)\AGCO Corporation\AGCO Update Client\AGCOUpdateService.exe'
        else:
            loc = r'C:\Program Files\AGCO Corporation\AGCO Update Client\AGCOUpdateService.exe'
        try:
            os.startfile(loc)
        except:
            logging.error('Unable to start AGCOUpdateService.exe')

    def restart(self):
        logging.info(f'Attempting to restart AUC')
        kill_process_by_name('AGCOUpdateService')
        set_service_running('AGCO Update')
        self.start_auc()
        time.sleep(5)

    def set_environment(self, env_base_url):
        logging.info(f'Attempting to set the env url of {env_base_url} in the config.ini file')
        kill_process_by_name('AGCOUpdateService')
        with fileinput.FileInput(r'C:\ProgramData\AGCO Corporation\AGCO Update\config.ini', inplace=True,
                                 backup='.bak') as file:
            for line in file:
                if "UpdateHost2" in line:
                    line = f'UpdateHost2={env_base_url}/api/v2\n'
                elif "UpdateHost" in line:
                    line = f'UpdateHost={env_base_url}/api/v2\n'
            print(line, end='')
        set_service_running('AGCO Update')
        self.start_auc()
        time.sleep(5)

    def bypass_download_scheduler(self):
        """Bypasses the download Scheduler by writing a line in the registry that the current AUC checks before applying
        the download scheduler"""
        current_time = arrow.utcnow().format('MM/DD/YYYY h:mm:ss A')
        try:
            regobj.HKLM.SOFTWARE.WOW6432Node.get_subkey(r'AGCO Corporation').get_subkey(r'AGCO Update')[
                'AUCConfiguration.LastExecutedUTC'] = current_time
        except AttributeError as e:
            logging.error(
                f'AGCO Update was not found in the registry. Please confirm that you have AGCO update client '
                f'installed. {e}')

    def get_client_relationships(self):
        uri = f'{base_url}/api/v2/UpdateGroupClientRelationships'
        payload = {
            "limit": 100,
            "ClientID": self._client_id
        }
        r = requests.get(uri, auth=MACAuth(mac_id, mac_token, host), params=payload)
        returned_relationships = json.loads(r.text)
        return returned_relationships['Entities']

    def subscribe_or_update_client_relationships(self, ug_to_be_assigned, ug_client_relationships, remove_ug_dict, client_id):
        ugs_to_be_removed = set(remove_ug_dict.values())
        to_be_assigned_in_relationships = False
        for relationship in ug_client_relationships:
            if ug_to_be_assigned == relationship['UpdateGroupID'] and relationship['Active'] is True:
                to_be_assigned_in_relationships = True

            if relationship['UpdateGroupID'] in ugs_to_be_removed and relationship['Active'] is True:
                relationship['Active'] = False
                relationship_id = relationship['RelationshipID']
                uri = f'{base_url}/api/v2/UpdateGroupClientRelationships/{relationship_id}'
                r = requests.put(uri, auth=MACAuth(mac_id, mac_token, host), data=relationship)

            if relationship['UpdateGroupID'] == ug_to_be_assigned and relationship['Active'] is False:
                relationship['Active'] = True
                relationship_id = relationship['RelationshipID']
                uri = f'{base_url}/api/v2/UpdateGroupClientRelationships/{relationship_id}'
                r = requests.put(uri, auth=MACAuth(mac_id, mac_token, host), data=relationship)
                to_be_assigned_in_relationships = True

        if not to_be_assigned_in_relationships:
            win_ug = 'f23c4a77-a200-4551-bf61-64aef94c185e'
            ug_plus_basic_inventory = [ug_to_be_assigned, win_ug]
            for ug in ug_plus_basic_inventory:
                try:
                    uri = f'{base_url}/api/v2/UpdateGroupClientRelationships'
                    relationship = {'UpdateGroupID': ug,
                                    'ClientID': client_id,
                                    'Active': True,
                                    }
                    r = requests.post(uri, auth=MACAuth(mac_id, mac_token, host), data=relationship)
                except Exception as ex:
                    logging.error(f'There was an error assigning UpdateGroup: {ug}...\n{ex}')


class EDT:
    def __init__(self):
        self.installed = Path(r"C:\Program Files (x86)\AGCO Corporation\EDT\AgcoGT.exe").is_file()
        self._voucher = ""
        self._region = ""
        self._version = ""
        self._release_name = ""
        self._framework_components = dict()

    @property
    def voucher(self):
        try:
            reg_voucher = regobj.HKLM.SOFTWARE.WOW6432Node.get_subkey(r'AGCO Corporation').EDT['Voucher'].data

        except (AttributeError, KeyError):
             reg_voucher = ''
        self._voucher = reg_voucher
        return reg_voucher

    @property
    def version(self):
        try:
            reg_version = regobj.HKLM.SOFTWARE.WOW6432Node.get_subkey(r'AGCO Corporation').EDT['Version'].data

        except AttributeError:
            reg_version = ''
        self._version = reg_version
        return reg_version

    @property
    def release_name(self):
        try:
            reg_release_name = regobj.HKLM.SOFTWARE.WOW6432Node.get_subkey(r'AGCO Corporation').EDT['Release_Name'].data
        except AttributeError:
            reg_release_name = ''
        self._release_name = reg_release_name
        return reg_release_name

    @property
    def region(self):
        try:
            reg_region = regobj.HKLM.SOFTWARE.WOW6432Node.get_subkey(r'AGCO Corporation').EDT['Region'].data
        except AttributeError:
            reg_region = ''
        self._release_name = reg_region
        return reg_region

    @property
    def framework_components(self):
        framework_versions = {}
        framework_components = {'DataCollection_MDTVersion',
                                'Globals_Version',
                                'MTAPISync_Version',
                                'Plug-Ins_Version',
                                'Update_MF_Activity_Version',
                                'Version',
                                'X1000Components_Version',
                                'EDT.SontheimComponents_Version',
                                'VDWPlug-Ins_Version',
                                'UpdateNumber',
                                'VDW_Version',
                                'ErrorCode',
                                'SIE44J32Patch_Version',
                                }
        try:
            edt_values = regobj.HKLM.SOFTWARE.WOW6432Node.get_subkey(r'AGCO Corporation').EDT.values()
            sontheim_values = regobj.HKLM.SOFTWARE.WOW6432Node.get_subkey(r'AGCO Corporation').get_subkey(
                r'Sontheim Components').values()
            for i in edt_values:
                if i.name in framework_components:
                    framework_versions.update({i.name: i.data})
            for i in sontheim_values:
                if i.name in framework_components:
                    framework_versions.update({i.name: i.data})
        except AttributeError as e:
            click.secho(f'EDT does not appear to be installed. Please confirm that EDT is installed.  {e}', fg='red')
        self._framework_components = framework_versions
        return framework_versions

    def set_environment(self, env_base_url):
        if is_os_64bit():
            files = [r'C:\Program Files (x86)\AGCO Corporation\EDT\EDTUpdateService.exe.config',
                     r'C:\Program Files (x86)\AGCO Corporation\EDT\AgcoGT.exe.config']
        else:
            files = [r'C:\Program Files\AGCO Corporation\EDT\EDTUpdateService.exe.config',
                     r'C:\Program Files\AGCO Corporation\EDT\AgcoGT.exe.config']

        kill_process_by_name('EDTUpdate')
        for file in files:
            logging.debug(f'Attempting to set the env url to {env_base_url} in the {file}')
            root = etree.parse(file)
            for event, element in etree.iterwalk(root):
                if element.text and 'https' in element.text:
                    logging.debug(f'Changing url from {element.text} to https://{env_base_url}/api/v2')
                    element.text = f'https://{env_base_url}/api/v2'
            with open(file, 'wb') as f:
                f.write(etree.tostring(root, encoding='UTF-8', xml_declaration=True, pretty_print=True))
        set_service_running('EDTUpdate')
        if not Path(r"C:\ProgramData\AGCO Corporation\EDT\Translations\Translations-test.sdf").is_file() and \
               Path(r"C:\ProgramData\AGCO Corporation\EDT\Translations\Translations.sdf").is_file():
            shutil.copy(r"C:\ProgramData\AGCO Corporation\EDT\Translations\Translations.sdf",
                        r"C:\ProgramData\AGCO Corporation\EDT\Translations\Translations-test.sdf")

    def set_edt_region(self, region=1):
        try:
            regobj.HKLM.SOFTWARE.WOW6432Node.get_subkey(r'AGCO Corporation').EDT[
                'Region'] = region
        except AttributeError as e:
            logging.error(f'EDT was not found in registry. Please confirm that EDT is installed to set the region {e}')
            click.secho(f'EDT was not found in registry. Please confirm that EDT is installed to set the region {e}',
                        fg='red')

    def import_globals(self):
        logging.debug('Attempting to import global strings')
        if is_os_64bit():
            command = rf'"C:\Program Files (x86)\AGCO Corporation\EDT\AgcoGT.exe" INITIALIZELANGUAGESDB'
        else:
            command = rf'"C:\Program Files\AGCO Corporation\EDT\AgcoGT.exe" INITIALIZELANGUAGESDB'

        logging.info(f'Importing globals via command line \"{command}\"')
        execute_command(command)

    def get_license_id(self, voucher):

        logging.info(f'Attempting to get license id using the voucher code')
        uri = f'{base_url}/api/v2/Licenses'
        payload = {
            "VoucherCode": voucher,
            "Status": "Active",
        }
        r = requests.get(uri, auth=MACAuth(mac_id, mac_token, host), params=payload)
        license_dict = json.loads(r.text)
        return license_dict['Entities'][0]['LicenseID']

    def add_services_to_license(self):
        license_id = self.get_license_id(self.voucher)
        logging.debug(f'Attempting to add AuthCode to License for Dev environment')
        uri = f'{base_url}/api/v2/AuthorizationCodes'
        payload = {'DefinitionID': '7a3d3576-62c6-48bb-8456-0c27fa3e5eec',
                   'ValidationParameters': [
                       {'Name': 'EDTInstanceID',
                        'Value': license_id}
                   ],
                   'DataParameters': [
                       {'Name': 'AGCODA',
                        'Value': 'True'},

                       {'Name': 'VDW',
                        'Value': 'True'},

                       {'Name': 'TestMode',
                        'Value': 'True'}
                   ]
                   }
        r = requests.post(uri, auth=MACAuth(mac_id, mac_token, host), json=payload)
        if not r.status_code == 200:
            logging.debug(f'The attempt to authorize {license_id} to enable VDW, AGCODA, and TestMode was unsuccessful')
        else:
            logging.debug(f'The attempt to authorize {license_id} to enable VDW, AGCODA, and TestMode was successful')

    def start_edt(self):
        logging.debug('Attempting to start EDT')
        if is_os_64bit():
            subprocess.call(r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe Start-Process '
                        r'\"C:\Progra~2\AGCO Corporation\EDT\AgcoGT.exe\" EDT', shell=True)
        else:
            subprocess.call(r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe Start-Process '
                            r'\"C:\ProgramFiles\AGCO Corporation\EDT\AgcoGT.exe\" EDT', shell=True)

    def create_voucher(self, voucher_type="temp", duration=8):
        """Creates voucher of a given type and duration. Valid types include temp, internal, commercial, r2r.
        voucher_type defaults to temp and duration defaults to 8 weeks from now."""
        expire_date = get_date_x_weeks_from_now(duration)
        logging.info(f'Attempting to create a voucher that expires {expire_date}')
        uri = f'{base_url}/api/v2/Vouchers'
        payload = {'temp': {"Type": "Temporary",
                            "DealerCode": "NA0001",
                            "Email": "darrin.fraser@agcocorp.com",
                            "ExpirationDate": expire_date,
                            },
                   'internal': {"Type": "Internal",
                                "DealerCode": "NA0001",
                                "Purpose": "Testing",
                                "LicenseTo": "Darrin Fraser",
                                "Email": "darrin.fraser@agcocorp.com",
                                },
                   'commercial': {"Type": "Commercial",
                                  "DealerCode": "NA0001",
                                  "OrderNumber": "ABCTest",
                                  "Email": "darrin.fraser@agcocorp.com",
                                  },
                   'r2r': {"Type": "RightToRepair",
                           "DealerCode": "NA0001",
                           "OrderNumber": "ABCTest",
                           "ExpirationDate": expire_date,
                           "Email": "darrin.fraser@agcocorp.com",
                           },
                   }
        r = requests.post(f'{uri}', auth=MACAuth(mac_id, mac_token, host), data=payload[voucher_type])
        return r.text.strip('"')

    def apply_voucher(self, voucher_id, is_edtlite=False):
        loc = "Program Files (x86)" if is_os_64bit() else "Program Files"
        if is_edtlite:
            logging.info(
                f'Applying voucher via command line \"AgcoGT.exe APPLYVoucher {voucher_id} NA0001 30096 EDTLITE\"')
            try:
                execute_command(rf'"C:\{loc}\AGCO Corporation\EDT\AgcoGT.exe" APPLYVoucher {voucher_id} NA0001 30096 EDTLITE')
            except subprocess.CalledProcessError as ex:
                logging.error(f"Voucher was not applied for the following: \n{ex}")
        else:
            logging.info(f'Applying voucher via command line \"AgcoGT.exe APPLYVoucher {voucher_id} NA0001 30096\"')
            try:
                execute_command(rf'"C:\{loc}\AGCO Corporation\EDT\AgcoGT.exe" APPLYVoucher {voucher_id} NA0001 30096')
            except subprocess.CalledProcessError as ex:
                logging.error(f"Voucher was not applied for the following: \n{ex}")


def is_os_64bit():
    return platform.machine().endswith('64')


# def config_ini_find_and_replace(find_text, replace_text):
#     logging.info(f'Attempting to replace \"{find_text}\" with \"{replace_text}\" in the config.ini file')
#     kill_process_by_name('AGCOUpdateService')
#     with fileinput.FileInput(r'C:\ProgramData\AGCO Corporation\AGCO Update\config.ini', inplace=True,
#                              backup='.bak') as file:
#         for line in file:
#             print(line.replace(find_text, replace_text), end='')
#     set_service_running('AGCO Update')
#     start_auc()
#     time.sleep(10)


def get_auth(username, password):
    auth = requests.auth.HTTPBasicAuth(username, password)
    uri = f'{base_url}/api/v2/Authentication'

    payload = {'username': username,
               'password': password
               }
    r = requests.post(uri, auth=auth, data=payload)
    user_auth = r.json()
    m_id = user_auth['MACId']
    m_token = user_auth['MACToken']
    return m_id, m_token


# def set_config_ini_to_original():
#     with fileinput.FileInput(r'C:\ProgramData\AGCO Corporation\AGCO Update\config.ini', inplace=True,
#                              backup='.bak') as file:
#         for line in file:
#             print(line.replace('IsExplicitInstallRunning=True', 'IsExplicitInstallRunning=False'), end='')


def execute_command(path_and_command):
    """
    Runs an inputted command. If the command returns a non-zero return code it will fail. This method is not for
    capturing the output
    """
    logging.debug(f'Attempting to execute: {path_and_command}')
    p1 = subprocess.run(path_and_command,
                        shell=True,
                        check=True,
                        capture_output=True,
                        text=True,
                        )
    logging.debug(f'Command: {path_and_command}')
    logging.debug(f'ReturnCode: {str(p1.returncode)}')


def kill_process_by_name(process_name):
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        current_proc_name = proc.info['name']
        if process_name in current_proc_name:
            logging.info(f'Killing process: {current_proc_name}')
            try:
                proc.kill()
                logging.debug(f'Killed process: {current_proc_name}')
            except:
                logging.debug(f'Unable to kill process: {current_proc_name}')


def apply_certs():
    logging.info('Attempting to apply Trusted Publish certificates')
    certs = Path(__file__).parent.joinpath("data").glob("*.cer")
    for cert in certs:
        subprocess.call(fr"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe certutil -addstore TrustedPublisher {cert}", shell=True)


def set_service_running(service):
    logging.debug(f'Attempting to set the following service to running: {service}')
    p1 = subprocess.run(fr'net start "{service}"', shell=True, capture_output=True, text=True, check=True)
    with open(fr'{save_path}temp_output.txt', 'w') as f:
        f.write(p1.stdout)
    with open(fr"{save_path}temp_output.txt", 'r') as f:
        for line in f.readlines():
            if f'The {service} service was started successfully.' in line:
                logging.debug(f"{service} has started.")


def get_date_x_weeks_from_now(number_of_weeks=8):
    utc = arrow.utcnow()
    x_weeks_from_now = utc.shift(weeks=+number_of_weeks)
    return x_weeks_from_now.isoformat()


def click_on_image(imagefile):
    logging.info(f'Attempting to click on {imagefile}')
    center = pyautogui.locateCenterOnScreen(imagefile)
    pyautogui.click(center)

def status_watcher(vouchertype, auc, edt):
    idle_counter = 0
    while idle_counter <= 4:
        auc.client_status
        if auc.auc_state in {"ReadyToInstall", "InstallingNeedsResume"}:
            auc.install_now()
            continue

        if auc.auc_state in {"CheckingIn", "Downloading", "Initializing"}:
            time.sleep(15)
            continue

        if auc.auc_state == "Installing":
            auc.active_packages
            if auc.edt_is_installed and not edt.voucher:
                voucher = edt.create_voucher(vouchertype)
                edt.apply_voucher(voucher)
                edt.start_edt()
                kill_process_by_name("AgcoGT.exe")
            continue

        if auc.auc_state == "DownloadPaused":
            logging.info('The download of edt packages has been suspended. When you are ready set the download '
                         'schedule in the AUC settings menu')
            time.sleep(60)

        if auc.auc_state == "Idle":
            if auc.edt_is_installed and not edt.voucher:
                voucher = edt.create_voucher(vouchertype)
                edt.apply_voucher(voucher)
            idle_counter += 1
            auc.check_in()
            continue
    logging.debug("AUC checked in 4 times and found no additional packages to download or install")


@click.command()
@click.version_option()
@click.option('--env', '-e', default='prod', type=click.Choice(['prod', 'test', 'dev']))
@click.option('--updategroup', '-ug', default='InternalTestPush', type=click.Choice(['EDTUpdates',
                                                                                     'Dev',
                                                                                     'RC',
                                                                                     'TestPush',
                                                                                     'InternalTestPush',
                                                                                     'InternalDev',
                                                                                     'InternalRC',
                                                                                     ]))
@click.option('--vouchertype', '-vt', default='temp', type=click.Choice(['temp', 'internal', 'commercial', 'r2r']))
@click.option('--username', '-u', prompt=True, help='Enter username')
@click.option('--password', '-p', prompt=True, hide_input=True, help='Enter password')
def main(env, updategroup, vouchertype,  username, password) -> None:
    """Agcoinstall."""

    global host, base_url, mac_id, mac_token

    host = 'secure.agco-ats.com'
    base_url = f'https://{host}'
    m_id, m_token = get_auth(username, password)
    mac_id = m_id
    mac_token = m_token

    apply_certs()

    auc = AUC()
    auc.update_all()

    edt = EDT()

    if not auc.installed:
        auc.download()
        auc.install()

    auc.update_all()

    auc.bypass_download_scheduler()

    ug_dict = {'EDTUpdates': 'eb91c5e8-ffb1-4060-8b97-cb53dcd4858d',
               'Dev': '29527dd4-3828-40f1-91b4-dfa83774e0c5',
               'RC': '30ae5793-67a2-4111-a94a-876a274c3814',
               'InternalTestPush': 'd76d7786-1771-4d3b-89b1-c938061da4ca',
               'TestPush': '42dd2226-cdaa-46b4-8e23-aa98ec790139',
               'InternalDev': '6ed348f3-8e77-4051-a570-4d2a6d86995d',
               'InternalRC': "75a00edd-417b-459f-80d9-789f0c341131",
               }

    env_dict = {'dev': 'edtsystems-webtest-dev.azurewebsites.net',
                'prod': 'secure.agco-ats.com',
                'test': 'edtsystems-webtest.azurewebsites.net',
                }

    update_group_id = ug_dict.pop(updategroup)
    c_relationships = auc.get_client_relationships()
    auc.subscribe_or_update_client_relationships(update_group_id, c_relationships, ug_dict, auc._client_id)

    auc.restart()
    time.sleep(5)
    status_watcher(vouchertype, auc, edt)

    if env in {'dev', 'test'}:
        host = env_dict[env]
        base_url = f'https://{host}'
        auc.set_environment(base_url)
        edt.set_environment(base_url)
        env_voucher = edt.create_voucher(vouchertype)
        edt.apply_voucher(env_voucher)

    if updategroup in {'Dev', 'InternalDev'}:
        edt.add_services_to_license()


if __name__ == "__main__":
    main(prog_name="agcoinstall")  # pragma: no cover
