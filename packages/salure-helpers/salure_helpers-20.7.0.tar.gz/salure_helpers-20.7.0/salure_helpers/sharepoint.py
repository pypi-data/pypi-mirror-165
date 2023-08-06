import os
import requests
import json
import signal
from io import BytesIO
from salure_helpers.salureconnect import SalureConnect


class Sharepoint():
    def __init__(self, credentials: dict, sharepoint_directory: str, token_directory: str, json_subset: int):
        """
        :param credentials: should be stored in salure connect where it can be collected using the api. (salureconnect.get_system_credentials)
        :param sharepoint_directory: storage location of the to be uploaded file
        :param token_directory: location of the stored tokens that are needed to refresh the access token
        """
        self.site = credentials["site"]
        self.siteid = credentials["site_id"]
        self.tenantid = credentials["tenant_id"]
        self.clientid = credentials["client_id"]
        self.clientsecret = credentials["client_secret"]
        self.sharepoint_directory = sharepoint_directory
        self.token_directory = token_directory
        self.json_subset = json_subset

    def get_access_token(self):
        """
        This method is used to retrieve the access token needed to be able to upload files to sharepoint.
        Refresh token is needed to be able to refresh the access token when needed.
        :return: returns the access token that can be used for file retrieval and uploads
        """
        os.makedirs(self.token_directory, exist_ok=True)
        if not os.path.exists(f'{self.token_directory}/tokens_sharepoint.json'):
            def handler(signum, frame):
                print('Token received', signum)
                raise OSError(
                    "Tjongejonge! I cannot believe you are so slow to input the token, be quick next time, bye!")
            # Set the signal handler and a 120-second alarm
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(120)
            refresh_token = input('refresh_token: ')
            signal.alarm(0)
        else:
            with open(f'{self.token_directory}/tokens_sharepoint.json', 'r') as file:
                tokens = file.read()
                tokens = json.loads(tokens)
                refresh_token = tokens['refresh_token']
        url_tokens = f'https://login.microsoftonline.com/{self.tenantid}/oauth2/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        body = {
            "grant_type": "refresh_token",
            "client_id": self.clientid,
            "client_secret": self.clientsecret,
            "refresh_token": refresh_token
        }
        response = requests.post(url=url_tokens, headers=headers, data=body)
        token = response.json()
        if 200 <= response.status_code < 300:
            with open(f'{self.token_directory}/tokens_sharepoint.json', 'w') as f:
                json.dump(token, f)
        else:
            raise Exception(f'Got status_code {response.status_code} with {response.text} from sharepoint')
        return token['access_token']

    def get_driveid(self):
        """
        This method is used to derive the driveid to which the files have to be uploaded. Needed in the upload url for file upload.
        json_subset: fill in the part of the json that needs to be accessed to get the wanted drive id, accompanying the drive you are looking for
        :return: returns the needed driveid
        """
        access_token = self.get_access_token()
        url = f'https://graph.microsoft.com/v1.0/sites/{self.site},{self.siteid}/drives'
        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.get(url, headers=headers)
        if 200 <= response.status_code < 300:
            driveid = response.json()['value'][self.json_subset]['id']
            return driveid
        else:
            raise ConnectionError(f"Received error from Salureconnect {response.status_code, response.text}")



    def upload_files(self, filename, documentlibrary):
        """
        This method performs the actual file upload to the formerly derived site + drive.
        filename: name of the file to be uploaded. For example test.csv
        documentlibrary: folder on sharepoint where it can be found. For example: Documenten or UploadFiles
        :return: File uploaded to sharepoint drive
        """
        access_token = self.get_access_token()
        driveid = self.get_driveid()
        url = f'https://graph.microsoft.com/v1.0/sites/{self.site},{self.siteid}/drives/{driveid}/root:/{documentlibrary}/{filename}:/createUploadSession'
        headers = {'Authorization': f'Bearer {access_token}'}
        try:
            upload_url = requests.post(url, headers=headers).json()['uploadUrl']
        except:
            return requests.post(url, headers=headers).json()

        with open(f'{self.sharepoint_directory}/{filename}', 'rb') as file_input:
            file_bytes = os.path.getsize(f'{self.sharepoint_directory}/{filename}')
            headers_upload = {'Content-Type': 'application/json',
                              'Content-Length': f'{file_bytes}',
                              'Content-Range': f'bytes 0-{file_bytes - 1}/{file_bytes}'}
            response_upload = requests.put(url=upload_url, headers=headers_upload, data=file_input)
            return response_upload

    def open_file(self, remote_path: str):
        access_token = self.get_access_token()
        driveid = self.get_driveid()
        url = f'https://graph.microsoft.com/v1.0/sites/{self.site},{self.siteid}/drives/{driveid}/root:/{remote_path}'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(url=url, headers=headers)
        if 200 <= response.status_code <= 300:
            download_url = response.json()['@microsoft.graph.downloadUrl']
            response_download = requests.get(url=download_url, headers=headers)
            return response_download
        else:
            return response

    def download_sharepoint_file(self, local_path: str, remote_path: str):
        access_token = self.get_access_token()
        driveid = self.get_driveid()
        url = f'https://graph.microsoft.com/v1.0/sites/{self.site},{self.siteid}/drives/{driveid}/root:/{remote_path}'
        response = requests.get(url=url, headers={'Authorization': f'Bearer {access_token}'})
        if 200 <= response.status_code <= 300:
            download_url = response.json()['@microsoft.graph.downloadUrl']
            response_download = requests.get(url=download_url, headers={'Authorization': f'Bearer {access_token}'})
            file = open(file=f'{local_path}', mode='wb')
            file.write(BytesIO(response_download.content).read())
            file.close()
            response.status = 'File successfully downloaded'
            response.status_code = 200
            return response
        else:
            return response

    def list_dir(self, folder_path: str):
        """
        Fetch the contents of the API and return the "children"
        which has the information of all the items under that folder
        :param refresh_token_flag: In case the token expires, refresh the token
        :return: all the contents of the folder items
        """
        access_token = self.get_access_token()
        driveid = self.get_driveid()
        url = f'https://graph.microsoft.com/v1.0/sites/{self.site},{self.siteid}/drives/{driveid}/root:/{folder_path}?expand=children'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(url, headers=headers, timeout=120)

        return response

    def remove_file(self, remote_path: str):
        access_token = self.get_access_token()
        driveid = self.get_driveid()
        url = f'https://graph.microsoft.com/v1.0/sites/{self.site},{self.siteid}/drives/{driveid}/root:/{remote_path}'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.delete(url=url, headers=headers)

        return response

