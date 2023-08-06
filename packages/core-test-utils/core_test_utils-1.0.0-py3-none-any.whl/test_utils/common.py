__author__ = 'sarvesh.singh'

import shutil
import string
import uuid
import zipfile
import subprocess
import os
import re
import requests
import yaml
import time
import pytz
import base64
import random
import allure
from functools import wraps
from urllib.parse import urlparse, urlunparse
from json import (
    dumps as json_dumps,
    load as json_load,
    loads as json_loads,
    JSONDecodeError,
)
from test_utils.logger import Logger
from types import SimpleNamespace as Namespace
from collections import namedtuple
from datetime import datetime
from faker import Faker

logger = Logger(name='COMMON').get_logger


def urljoin(*args):
    """
    This function will join a URL and return back proper url
    :return:
    """
    parsed = list(urlparse("/".join(args)))
    parsed[2] = re.sub("/{2,}", "/", parsed[2])
    _host = urlunparse(parsed)
    return _host


def read_json_file(file_name, nt=True):
    """
    This function will read Json and return it back in Named-Tuples format
    :param file_name
    :param nt
    """
    logger.debug(f'Reading json file {file_name}')
    if not os.path.isfile(file_name):
        raise Exception(f'File {file_name} Does Not Exist !!')

    with open(file_name, 'r') as _fp:
        if nt:
            data = json_load(_fp, object_hook=lambda d: Namespace(**d))
        else:
            data = json_load(_fp)

    return data


def is_key_there_in_dict(key, dictionary, empty_check=True, text=None):
    """
    Check if key is there in dictionary
    :param key:
    :param dictionary:
    :param empty_check:
    :param text:
    :return:
    """
    if key not in dictionary:
        if text is None:
            raise Exception(f"'{key}' not found in _content !!")
        else:
            raise Exception(f"'{key}' not found in _content | {text}")
    else:
        if empty_check:
            if isinstance(dictionary[key], (list, tuple, dict)):
                if len(dictionary[key]) == 0:
                    print(f'{key} is empty !!')
            elif dictionary[key] is None:
                pass
            else:
                pass


def send_get_request(url, headers=None, params=None, timeout=None, report=True):
    """
    Send simple GET Request
    :param url:
    :param headers:
    :param params:
    :param timeout:
    :param report:
    :return:
    """
    if report:
        now = datetime.now(pytz.timezone('Asia/Calcutta'))
        name = f'curlCmd_{now.minute}{now.second}{now.microsecond}.json'
        command = create_curl_command(method='GET', headers=headers, url=url, params=params)
        save_allure(data=command, name=name, save_dump=False)
    if timeout:
        response = requests.get(url=url, headers=headers, params=params, timeout=timeout)
    else:
        response = requests.get(url=url, headers=headers, params=params)
    if response.status_code not in [200, 201]:
        if report:
            save_allure(data=response.content.decode('utf-8'), name='failResponse.json', save_dump=False)
        logger.error(f'Status code is : {response.status_code} | Error: {response.text}')
        raise Exception(f'Status code is : {response.status_code} | Error: {response.text}')
    content = response.content.decode('utf-8')
    if report:
        save_allure(data=content, name='passResponse.json', save_dump=False)
    try:
        nt = json_loads(content)
    except:
        nt = json_loads(json_dumps(content))
    return nt


def send_post_request(url, headers=None, json=None, data=None, params=None, report=True):
    """
    Send simple Post Request
    :param url:
    :param json:
    :param headers:
    :param data:
    :param params:
    :param report:
    :return:
    """
    if report:
        now = datetime.now(pytz.timezone('Asia/Calcutta'))
        name = f'curlCmd_{now.minute}{now.second}{now.microsecond}.json'
        command = create_curl_command(method='POST', headers=headers, url=url, params=params, data=json)
        save_allure(data=command, name=name, save_dump=False)
    response = requests.post(url=url, json=json, data=data, headers=headers, params=params)
    if response.status_code not in [200, 201]:
        if report:
            save_allure(data=response.content.decode('utf-8'), name='failResponse.json', save_dump=False)
        logger.error(f'Status code is : {response.status_code} | Error: {response.text}')
        raise Exception(f'Status code is : {response.status_code} | Error: {response.text}')
    content = response.content.decode('utf-8')
    if report:
        save_allure(data=content, name='passResponse.json', save_dump=False)
    try:
        nt = json_loads(content)
    except:
        nt = json_loads(json_dumps(content))
    return nt


def send_put_request(url, headers=None, json=None, data=None, params=None, report=True):
    """
    Send simple Put Request
    :param url:
    :param json:
    :param headers:
    :param data:
    :param params:
    :param report:
    :return:
    """
    if report:
        now = datetime.now(pytz.timezone('Asia/Calcutta'))
        name = f'curlCmd_{now.minute}{now.second}{now.microsecond}.json'
        command = create_curl_command(method='PUT', headers=headers, url=url, params=params, data=json)
        save_allure(data=command, name=name, save_dump=False)
    response = requests.put(url=url, json=json, data=data, headers=headers, params=params)
    if response.status_code not in [200, 201]:
        if report:
            save_allure(data=response.content.decode('utf-8'), name='failResponse.json', save_dump=False)
        logger.error(f'Status code is : {response.status_code} | Error: {response.text}')
        raise Exception(f'Status code is : {response.status_code} | Error: {response.text}')
    content = response.content.decode('utf-8')
    if report:
        save_allure(data=content, name='passResponse.json', save_dump=False)
    try:
        nt = json_loads(content)
    except:
        nt = json_loads(json_dumps(content))
    return nt


def send_delete_request(url, headers=None, params=None, report=True):
    """
    Send simple Delete Request
    :param url:
    :param headers:
    :param params:
    :param report:
    :return:
    """
    if report:
        now = datetime.now(pytz.timezone('Asia/Calcutta'))
        name = f"curlCmd_{now.minute}{now.second}{now.microsecond}.json"
        command = create_curl_command(method='DELETE', headers=headers, url=url, params=params)
        save_allure(data=command, name=name, save_dump=False)
    response = requests.delete(url=url, headers=headers, params=params)
    if response.status_code not in [204]:
        if report:
            save_allure(data=response.content.decode('utf-8'), name='failResponse.json', save_dump=False)
        logger.error(f'Status code is : {response.status_code} | Error: {response.text}')
        raise Exception(f'Status code is : {response.status_code} | Error: {response.text}')
    content = response.content.decode('utf-8')
    if report:
        save_allure(data=content, name='passResponse.json', save_dump=False)
    try:
        nt = json_loads(content)
    except:
        nt = json_loads(json_dumps(content))
    return nt


def save_allure(data, name, save_dump=False):
    """
    Save allure report by converting data to Json
    :param data:
    :param name:
    :param save_dump:
    :type name:
    :return:
    """
    if len(data) != 0:
        if isinstance(data, str):
            name = str(name).replace('.json', '.log')
            allure.attach(data, name=name, attachment_type=allure.attachment_type.TEXT)
            if save_dump:
                with open(name, 'w') as _fp:
                    _fp.write(data)
            return str
        else:
            dump = json_dumps(data, indent=2, sort_keys=True)
            allure.attach(dump, name=name, attachment_type=allure.attachment_type.JSON)
            if save_dump:
                with open(name, 'w') as _fp:
                    _fp.write(dump)
            return dump


def generate_phone_number(max_digits=10):
    """
    Function to generate phone number
    :param max_digits:
    :return:
    """
    return random.randint(10 ** (max_digits - 1), 10 ** max_digits - 1)


def generate_email_id():
    """
    Function to generate Email ID
    :return:
    """
    tail = f"_{str(generate_phone_number(6))}@sample.com"
    email_id = re.sub(
        r"(.*?)@.*", r"\1{}".format(tail), str(Faker().email()), re.I | re.M
    )
    return str(email_id).lower()


def create_curl_command(method, headers, url, params=None, data=None):
    """
    Create the curl command which is being Hit !!
    :param method:
    :param headers:
    :param url:
    :param params:
    :param data:
    :return:
    """
    # Check if data is in Json/dict format, convert it into string after that
    if isinstance(data, dict) or isinstance(data, list):
        data = json_dumps(data)
    headers = ' --header '.join(
        [
            f'"{k}: {v}"'
            for k, v in headers.items()
            if k not in ['User-Agent', 'Accept-Encoding']
        ]
    )

    if params:
        url = f'{url}?{"&".join([f"{k}={v}" for k, v in params.items()])}'

    if data:
        command = f"curl --request {method} --include --silent --show-error --header {headers} --data '{data}' '{url}'"
    else:
        command = f"curl --request {method} --include --silent --show-error --header {headers} '{url}'"

    # We always save Curl Command in environment variable, so that we know (in-case) of an exception what was it.
    os.environ['CURL'] = command
    return command


def read_sample_json():
    """
    This function read all .json file in sample-jsons and return json in format of this {file_name: file_Json} .
    :return:
    """
    logger.debug('Reading all jsons under /sample-json dir !!')
    _json_files = []
    directory = 'sample-jsons'
    for root, dirs, file in os.walk(directory):
        for filename in file:
            if filename.endswith('.json'):
                _json_files.append(os.path.join(root, filename))

    if len(_json_files) != 0:
        final_data = {}
        for _file in _json_files:
            with open(_file, 'r') as _fp:
                try:
                    _file_content = json_load(_fp)
                except (Exception, JSONDecodeError):
                    raise Exception(f'Cannot Read File {_file} !!')
            final_data.update(
                {os.path.basename(_file).split('.json')[0]: _file_content}
            )
        json_files = namedtuple('MyTuple', final_data)
        files = json_files(**final_data)
        return files
    else:
        raise Exception("There's no Json File in {directory} !!")


def random_alpha_numeric_string(length=10):
    """
    Generate random alpha numeric string
    :param length:
    :return:
    """
    alpha_numeric_string = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(length)
    )
    return alpha_numeric_string


def zip_dir(directory_path, zip_name):
    """
    Func to create zip of directory
    :param directory_path:
    :param zip_name:
    :return:
    """
    zip_file = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            zip_file.write(os.path.join(root, file))
    zip_file.close()


def retry(retries=120, interval=5):
    """
    Decorator to retry if a test needs polling
    :param retries:
    :param interval:
    :return:
    """

    def deco(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            r = retries
            final_exception = None
            while r > 0:
                try:
                    response = func(*args, **kwargs)
                except Exception as exp:
                    r -= 1
                    logger.debug(f'{exp} :: {r} of {retries} Retries Left !!')
                    time.sleep(interval)
                    final_exception = exp
                    pass
                else:
                    break
            else:
                logger.error(final_exception)
                raise Exception(f'{retries} Retries Exhausted :: {final_exception} !!')
            return response

        return wrapper

    return deco


def guid():
    """
    Func to generate random GUID
    :return:
    """
    return str(uuid.uuid4())


def update_allure_environment(request, config):
    """
    Func to update allure environment
    :param request
    :param config
    :return:
    """
    _environment_params = dict()
    for _to_add in ['JOB_NAME', 'BUILD_URL']:
        if _to_add in os.environ:
            _environment_params[_to_add] = os.environ[_to_add]

    _environment_params.update({
        'Base-URL': config['baseUrl'],
        'Infra': request.config.getoption('--infra'),
        'Env-Type': request.config.getoption('--env-type'),
        'Send-Report': request.config.getoption('--report'),
    })

    allure_dir = request.config.getoption('--alluredir')
    if allure_dir:
        if not os.path.isdir(allure_dir):
            os.makedirs(allure_dir)
        env_file = os.path.join(allure_dir, 'environment.properties')
        with open(env_file, 'w') as fd:
            for _element in sorted(_environment_params.keys()):
                fd.write(f'{_element}={_environment_params[_element]}\n')


def run_cmd(cmd, wait=True, fail=False, cwd=None, env=None):
    """
    Run a command and return it's output
    :param cmd: command to be executed
    :param fail: Fail execution when command is not a success
    :param wait: Wait for process to complete?
    :param cwd: Current Working DIR
    :param env: Environment Variables to be set
    :return:
    """
    cmd_response = namedtuple('CmdResponse', ['cmd', 'status', 'output', 'error'])
    cmd_env = os.environ.copy()
    if env and isinstance(env, dict):
        for key, value in env.items():
            cmd_env[key] = str(value)

    options = {'capture_output': True, 'env': cmd_env, 'shell': True, 'universal_newlines': True}
    if cwd:
        options['cwd'] = cwd

    now = datetime.now(pytz.timezone('Asia/Calcutta'))
    name = f'command_{now.minute}{now.second}{now.microsecond}.txt'
    save_allure(data=cmd, name=name, save_dump=False)

    if not wait:
        subprocess.Popen([cmd], shell=True, stdin=None, stdout=None, stderr=None)
        return cmd_response(cmd=cmd, status=0, output=None, error=None)

    p = subprocess.run(cmd, **options)
    status = p.returncode
    if fail and status != 0:
        logger.error(f"Command '{cmd}' failed with code:{status}\n{p.stderr.strip()}")
        raise Exception(f"Command '{cmd}' failed with code:{status}\n{p.stderr.strip()}")

    save_allure(data=f'OUT: {p.stdout.strip()}\nERR: {p.stderr.strip()}', name='output.txt', save_dump=False)
    return cmd_response(cmd=cmd, status=status, output=p.stdout.strip(), error=p.stderr.strip())


def base64_encode(_input=None):
    """
    Encode Base64
    :param _input:
    :return:
    """
    encoded = str(base64.b64encode(bytes(_input, 'utf-8')), 'ascii').strip()
    return encoded


def base64_decode(encoded=None):
    """
    Decode Base64
    :param encoded:
    :return:
    """
    decoded = str(base64.b64decode(encoded), 'ascii')
    return decoded


def compare_jsons(json_1=None, json_2=None):
    """
    Func to compare two jsons
    :param json_1:
    :param json_2:
    :return:
    """

    def sorting(item):
        if isinstance(item, dict):
            return sorted((key, sorting(values)) for key, values in item.items())
        if isinstance(item, list):
            return sorted(sorting(x) for x in item)
        else:
            return item

    return sorting(json_loads(json_dumps(json_1))) == sorting(json_loads(json_dumps(json_2)))


def yaml_to_json(yaml_file=None):
    """
    Func to convert yaml data to json
    :param yaml_file:
    :return:
    """
    with open(yaml_file, 'r') as file:
        json_data = yaml.safe_load(file)
    return json_dumps(json_data)


def unescape_string(data=None):
    """
    Func to unescape string
    :param data:
    :return:
    """
    return ''.join(_char for _char in data if _char.isalnum())


def read_yaml_file(file=None):
    """
    Func to read yaml file
    :param file:
    :return:
    """
    with open(file) as _file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        _data = yaml.load(_file, Loader=yaml.FullLoader)
    return _data


def write_yaml_file(file=None, _data=None):
    """
    Func to write yaml file
    :param file:
    :param _data:
    :return:
    """
    with open(file, 'w') as _file:
        yaml.dump(_data, _file)


def remove_file(file_path=None):
    """Remove a file

    Args:
        file_path (_type_, optional): _description_. Defaults to None.
    """
    if os.path.exists(file_path):
        os.remove(file_path)


def read_file(file_path=None):
    """Read a file

    Args:
        file_path (_type_, optional): _description_. Defaults to None.
    """
    _data = open(file_path, 'r+')
    return _data.read()


def write_json(file_path=None, data=None):
    """Func to write data in json

    Args:
        file_path (_type_, optional): _description_. Defaults to None.
        data (_type_, optional): _description_. Defaults to None.
    """
    with open(file_path, 'w+') as _fp:
        _fp.write(json_dumps(data, default=lambda o: o.__dict__, indent=4))


def rename_file(file_path=None, name=None):
    """Func to rename file

    Args:
        file_path (_type_, optional): _description_. Defaults to None.
        name (_type_, optional): _description_. Defaults to None.
    """
    if os.path.exists(file_path):
        os.rename(file_path, name)


def make_directory(path=None):
    """Func to make directory

    Args:
        path (_type_, optional): _description_. Defaults to None.
    """
    if os.path.isdir(path):
        shutil.rmtree(path=path)
    path = os.path.join(path)
    os.mkdir(path)
