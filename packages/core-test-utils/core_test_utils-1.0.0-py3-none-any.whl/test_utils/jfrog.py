__author__ = 'sarvesh.singh'

from test_utils.logger import Logger
from test_utils.common import send_get_request, send_delete_request, urljoin, is_key_there_in_dict


class Jfrog:
    """
    Class for JFROG !!
    """

    def __init__(self, base_url=None, repos=None, token=None):
        """
        Connect to JFROG
        :param base_url
        :param repos
        :param token
        """
        self.logger = Logger(name='JFROG').get_logger
        self._headers = {
            'Authorization': token
        }
        self._repos = repos
        self._base_url = base_url

    def folder_info(self, url=None):
        """
        Func to get folder info
        :param url
        :return:
        """
        _folder_info = send_get_request(url=url, headers=self._headers)
        return _folder_info

    def application_folder_exits(self, application_name=None):
        """
        Func to check if application folder exists
        :param application_name
        :return:
        """
        _url = urljoin(self._base_url, 'api/storage', self._repos)
        _folder_info = self.folder_info(url=_url)
        is_key_there_in_dict('children', _folder_info)
        if len(_folder_info['children']) == 0:
            self.logger.error(f'There are no folders under repo: {self._repos}')
            raise Exception(f'There are no folders under repo: {self._repos}')
        for _children in _folder_info['children']:
            if _children['uri'] == f'/{application_name}':
                if _children['folder']:
                    break
        else:
            self.logger.error(f'{application_name} folder does not exist under repo: {self._repos}')
            raise Exception(f'{application_name} folder does not exist under repo: {self._repos}')

    def application_image_exists(self, application_name=None, image_version=None):
        """
        Func to check if application image exists
        :param application_name
        :param image_version
        :return:
        """
        self.application_folder_exits(application_name=application_name)
        _url = urljoin(self._base_url, 'api/storage', self._repos, application_name)
        _folder_info = self.folder_info(url=_url)
        is_key_there_in_dict('children', _folder_info)
        if len(_folder_info['children']) == 0:
            self.logger.error(f'There are no folders under repo: {self._repos}/{application_name}')
            raise Exception(f'There are no folders under repo: {self._repos}/{application_name}')
        for _children in _folder_info['children']:
            if _children['uri'] == f'/{image_version}':
                if _children['folder']:
                    break
        else:
            self.logger.error(
                f'{image_version} for {application_name} does not exist under repo: {self._repos}/{application_name}')
            raise Exception(
                f'{image_version} for {application_name} does not exist under repo: {self._repos}/{application_name}')

    def remove_image(self, application_name=None, image_version=None):
        """
        Func to remove image
        :param application_name
        :param image_version
        :return:
        """
        try:
            self.application_image_exists(application_name=application_name, image_version=image_version)
            _url = urljoin(self._base_url, self._repos, application_name, image_version)
            send_delete_request(url=_url, headers=self._headers)
        except Exception:
            pass
