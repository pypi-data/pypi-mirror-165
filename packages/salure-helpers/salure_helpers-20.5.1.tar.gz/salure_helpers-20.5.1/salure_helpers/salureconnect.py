import os

from .helpers.salureconnect.organigram_profit_salureconnect import OrganigramProfitSalureconnect
from .helpers.salureconnect.users_profit_salureconnect import UsersProfitSalureconnect


class SalureConnect(object):

    def __init__(self):
        pass

    def organigram_from_profit_to_salureconnect(self, task_id, customer_mysql_host, customer_mysql_user, customer_mysql_password, customer_mysql_database,
                                                profit_environment, profit_token, profit_url='rest.afas.online'):
        """
        Get the organigram from AFAS and update it into SalureConnect
        :param task_id: give the number of the task in salureconnect. Take care that the task is created already
        :param customer_mysql_host: the IP of the host where the customers MySQL database is located
        :param customer_mysql_user: the username of the customers MySQL database
        :param customer_mysql_password: the password of the customers MySQL database
        :param customer_mysql_database: the databasename of the customers MySQL database
        :param profit_environment: the Profit environment number of the customer
        :param profit_token: the token from the Profit environment
        :param profit_url: the url of the Profit environment, usual rest.afas.online
        """
        organigram = OrganigramProfitSalureconnect(task_id, customer_mysql_host, customer_mysql_user, customer_mysql_password, customer_mysql_database,
                                                   profit_environment, profit_token, profit_url)
        organigram.run_all()

    def users_from_profit_to_salureconnect(self, task_id, mysql_host, customer_mysql_user, customer_mysql_password, customer_mysql_database,
                                           sc_mysql_user, sc_mysql_password, profit_environment, profit_token, profit_url, sc_customer_id):
        """
        Get the organigram from AFAS and update it into SalureConnect
        :param task_id: give the number of the task in salureconnect. Take care that the task is created already
        :param mysql_host: the IP of the host where the customers MySQL database is located
        :param customer_mysql_user: the username of the customers MySQL database
        :param customer_mysql_password: the password of the customers MySQL database
        :param customer_mysql_database: the databasename of the customers MySQL database
        :param sc_mysql_user: the username of the central MySQL database
        :param sc_mysql_password: the password of the central MySQL database
        :param profit_environment: the Profit environment number of the customer
        :param profit_token: the token from the Profit environment
        :param profit_url: the url of the Profit environment, usual rest.afas.online
        """
        users = UsersProfitSalureconnect(task_id, mysql_host, customer_mysql_user, customer_mysql_password, customer_mysql_database,
                                         profit_environment, profit_token, profit_url, sc_mysql_user, sc_mysql_password, sc_customer_id)
        users.run_all()

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
