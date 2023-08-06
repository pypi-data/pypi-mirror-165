import os
import requests
import json
from typing import List


class SalureConnect(object):

    def __init__(self):
        pass

    def get_system_credentials(self, system: str, salure_token: str, customer: str) -> json:
        """
        This method retrieves authentication credentials from salureconnect.
        It returns the entire authentication response allowing the response to be passed to a system-specific module.
        :param system: specifies which token is used. (lowercase)
        :param salure_token: the token used to authorize credential collection
        :param customer: customer (full name with capitalization and spaces not underscores)
        returns the entire authenication response sent back by salureconnect.
        """
        url = f'https://salureconnect.com/api/v1/connector/{system}'
        payload = {}
        headers = {'Authorization': f'SalureToken {salure_token}','salure-customer': customer}
        response = requests.request("GET", url, headers=headers, data=payload)
        if 200 <= response.status_code < 300:
            data = response.json()
            return data
        else:
            raise ConnectionError(f"Received error from Salureconnect {response.status_code, response.text}")

    def refresh_oauth2_token(self):
        pass


class SalureConnectFiles:
    def __init__(self, customer_name: str, api_token: str):
        self.customer_name = customer_name
        self.api_token = api_token

    def __get_headers(self):
        return {
            'Authorization': f'SalureToken {self.api_token}',
            'salure-customer': self.customer_name
        }

    def download_files(self, output_dir: os.PathLike, filter_upload_definition_ids: List = None, filter_file_names: List = None, deleted = False):
        """
        This method is to download files from SalureConnect API and store them to a folder
        :param output_dir: folder to store files
        :param filter_upload_definition_ids: filter only files with one or more specific upload definition(s)
        :param filter_file_names: filter files based on name
        """
        response = requests.get(url="https://salureconnect.com/api/v1/file-storage/files", headers=self.__get_headers())
        if response.status_code == 200:
            files = response.json()
            for file_object in files:
                # Only get file(s) that are in filter
                if (filter_upload_definition_ids is None or file_object['fileuploadDefinition']['id'] in filter_upload_definition_ids) and (filter_file_names is None or file_object['file_name'] in filter_file_names) and file_object['deleted_at']:
                    file_string = requests.get(url=f"{config.salureconnect['url']}/file-storage/files/{file_description['id']}/download", headers=headers)
                    with open(output_dir + file_description['file_name'], mode='wb') as file:
                        file.write(file_string.content)
