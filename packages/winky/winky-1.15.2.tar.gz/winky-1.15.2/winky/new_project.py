# coding=utf-8
import os
import shutil
import pip
import pip._internal


class NewProject:
    __folders = ['sql', 'other', 'allure-results', 'stubs', 'templates', 'tests', 'xpath', 'helpers']

    @staticmethod
    def create(demo=False):
        answer = input('Creating a template will remove files if there are any. [y\\n]')
        if answer.lower() != 'y':
            return 0
        # if hasattr(pip, 'main'):
        #     pip.main(['install', 'pytest'])
        #     pip.main(['install', 'allure-pytest'])
        # else:
        #     pip._internal.main(['install', 'pytest'])
        #     pip._internal.main(['install', 'allure-pytest'])

        for folder in NewProject.__folders:
            if os.path.exists(f'./{folder}'):
                shutil.rmtree(f'./{folder}')
            os.mkdir(folder)

        if not demo:
            with open('./config.py', 'w', encoding='utf-8') as file:
                file.write(file_config)
            with open('./stubs/mock.py', 'w', encoding='utf-8') as file:
                file.write(file_mock)
            with open('./tests/test_positive.py', 'w', encoding='utf-8') as file:
                file.write(file_test)
            with open('./conftest.py', 'w', encoding='utf-8') as file:
                file.write(file_conftest)

        else:
            with open('./config.py', 'w', encoding='utf-8') as file:
                file.write(file_config_demo)
            with open('./stubs/mock_json.py', 'w', encoding='utf-8') as file:
                file.write(file_mock_json_demo)
            with open('./stubs/mock_xml.py', 'w', encoding='utf-8') as file:
                file.write(file_mock_xml_demo)
            with open('./tests/test_positive_json.py', 'w', encoding='utf-8') as file:
                file.write(file_test_positive_json_demo)
            with open('./tests/test_positive_xml.py', 'w', encoding='utf-8') as file:
                file.write(file_test_positive_xml_demo)
            with open('./templates/request_service_json.json', 'w', encoding='utf-8') as file:
                file.write(file_request_service_json_demo)
            with open('./templates/request_service_xml.xml', 'w', encoding='utf-8') as file:
                file.write(file_request_service_xml_demo)
            with open('./templates/response_service_json.json', 'w', encoding='utf-8') as file:
                file.write(file_response_service_json_demo)
            with open('./templates/response_service_xml.xml', 'w', encoding='utf-8') as file:
                file.write(file_response_service_xml_demo)
            with open('./xpath/response_service_xml.xpath', 'w', encoding='utf-8') as file:
                file.write(file_response_service_xml_xpath_demo)
            with open('./xpath/request_service_xml.xpath', 'w', encoding='utf-8') as file:
                file.write(file_request_service_xml_xpath_demo)
            with open('./conftest.py', 'w', encoding='utf-8') as file:
                file.write(file_conftest_demo)

        with open('./templates/__init__.py', 'w', encoding='utf-8') as file:
            file.write(file_template)

        with open('./sql/__init__.py', 'w', encoding='utf-8') as file:
            file.write(file_sql)

        print('success')


file_config = \
    '''import os

base_path = os.path.dirname(os.path.abspath(__file__)) + '/'

mock_port = os.environ.get('MOCK_PORT', 8080)
'''

file_mock = \
    '''import winky
import config


def logic(request: winky.HTTPMessage, response: winky.HTTPMessage):
    pass


mock = winky.HTTPStub(logic, config.mock_port)

if __name__ == "__main__":
    mock.run()
    input()
'''

file_test = \
    '''import winky
import allure
import config


def test_positive():
    with allure.step("Step name"):
        pass
'''

file_conftest = \
    '''from stubs.mock import mock
import pytest


@pytest.fixture()
def mock_stop(request):
    def fin():
        mock.stop()

    request.addfinalizer(fin)
'''

file_config_demo = \
    '''import os

base_path = os.path.dirname(os.path.abspath(__file__)) + '/'

mock_json_port = os.environ.get('MOCK_JSON_PORT', 8080)
mock_xml_port = os.environ.get('MOCK_XML_PORT', 8090)

service_json_host = os.environ.get('SERVICE_JSON_HOST', 'http://localhost')
service_json_port = os.environ.get('SERVICE_JSON_PORT', 8080)

service_xml_host = os.environ.get('SERVICE_XML_HOST', 'http://localhost')
service_xml_port = os.environ.get('SERVICE_XML_PORT', 8090)
'''

file_mock_json_demo = \
    '''import winky
import config


def logic(request: winky.HTTPMessage, response: winky.HTTPMessage):
    tmp_request = winky.TemplateJSON(request.body)
    tmp_response = winky.TemplateJSON()
    tmp_response.set_body_from_file(f'{config.base_path}templates/response_service_json.json')

    try:
        tmp_response['firstName'] = tmp_request['firstName']
        tmp_response['lastName'] = tmp_request['lastName']
        tmp_response['status']['home'] = 'OK'
        tmp_response['status']['city'] = 'OK'
    except KeyError:
        response.code = 400
        return 0

    response.code = 200
    response.headers["Content-Type"] = "application/json"
    response.body = tmp_response.body


mock_json = winky.HTTPStub(logic, config.mock_json_port)

if __name__ == "__main__":
    mock_json.run()
    input()
'''

file_mock_xml_demo = \
    '''import winky
import config


def logic(request: winky.HTTPMessage, response: winky.HTTPMessage):
    tmp_request = winky.TemplateXML(request.body)
    tmp_request.set_xpath_mask(f'{config.base_path}xpath/request_service_xml.xpath')
    tmp_response = winky.TemplateXML()
    tmp_response.set_body_from_file(f'{config.base_path}templates/response_service_xml.xml')
    tmp_response.set_xpath_mask(f'{config.base_path}xpath/response_service_xml.xpath')

    try:
        tmp_response['firstName'] = tmp_request['firstName']
        tmp_response['lastName'] = tmp_request['lastName']
        tmp_response['home'] = 'OK'
        tmp_response['city'] = 'OK'
    except KeyError:
        response.code = 400
        return 0

    response.code = 200
    response.headers["Content-Type"] = "application/xml"
    response.body = tmp_response.body


mock_xml = winky.HTTPStub(logic, config.mock_xml_port)

if __name__ == "__main__":
    mock_xml.run()
    input()
'''

file_request_service_json_demo = \
    '''{
   "firstName": "Ivan",
   "lastName": "Ivanov",
   "address": {
       "streetAddress": "Lenina",
       "city": "Moscow",
       "postalCode": "101101"
   },
   "phoneNumbers": [
       "812 123-1234",
       "916 123-4567"
   ]
}
'''

file_request_service_xml_demo = \
    '''<person>
  <firstName>Ivan</firstName>
  <lastName>Ivanov</lastName>
  <address>
    <streetAddress>Lenina</streetAddress>
    <city>Moscow</city>
    <postalCode>101101</postalCode>
  </address>
  <phoneNumbers>
    <phoneNumber>812 123-1234</phoneNumber>
    <phoneNumber>916 123-4567</phoneNumber>
  </phoneNumbers>
</person>
'''

file_response_service_json_demo = \
    '''{
   "firstName": "Ivan",
   "lastName": "Ivanov",
   "status": {
     "home": "OK",
     "city": "OK"
   }
}
'''

file_response_service_xml_demo = \
    '''<person>
  <firstName>Ivan</firstName>
  <lastName>Ivanov</lastName>
  <status>
    <home>OK</home>
    <city>OK</city>
  </status>
</person>
'''

file_test_positive_json_demo = \
    '''import winky
import allure
import config
from stubs.mock_json import mock_json


def test_positive_json():
    mock_json.run()

    with allure.step("Отправка запроса сервису mock_json"):
        request = winky.HTTPMessage()
        request.set_body_from_file(f'{config.base_path}templates/request_service_json.json')
        request.headers["Content-Type"] = "application/json"
        response = request.post(config.service_json_host, config.service_json_port)

    with allure.step("Валидация ответа сервиса mock_json"):
        tmp_response_json = winky.TemplateJSON()
        tmp_response_json.set_body_from_file(f'{config.base_path}templates/response_service_json.json')
        assert response.code == 200
        assert response.headers["Content-Type"] == "application/json"
        assert response.body == tmp_response_json.body

    mock_json.stop()
'''

file_test_positive_xml_demo = \
    '''import winky
import allure
import config
from stubs.mock_xml import mock_xml


def test_positive_xml():
    mock_xml.run()

    with allure.step("Отправка запроса сервису mock_xml"):
        request = winky.HTTPMessage()
        request.set_body_from_file(f'{config.base_path}templates/request_service_xml.xml')
        request.headers["Content-Type"] = "application/xml"
        response = request.post(config.service_xml_host, config.service_xml_port)

    with allure.step("Валидация ответа сервиса mock_xml"):
        tmp_response_xml = winky.TemplateXML()
        tmp_response_xml.set_body_from_file(f'{config.base_path}templates/response_service_xml.xml')
        assert response.code == 200
        assert response.headers["Content-Type"] == "application/xml"
        assert response.body == tmp_response_xml.body

    mock_xml.stop()
'''

file_request_service_xml_xpath_demo = \
    '''{
  "firstName": "/*[local-name()='person']/*[local-name()='firstName']",
  "lastName": "/*[local-name()='person']/*[local-name()='lastName']"
}
'''

file_response_service_xml_xpath_demo = \
    '''{
  "firstName": "/*[local-name()='person']/*[local-name()='firstName']",
  "lastName": "/*[local-name()='person']/*[local-name()='lastName']",
  "city": "/*[local-name()='person']/*[local-name()='status']/*[local-name()='city']",
  "home": "/*[local-name()='person']/*[local-name()='status']/*[local-name()='home']"
}
'''

file_conftest_demo = \
    '''from stubs.mock_json import mock_json
from stubs.mock_xml import mock_xml
import pytest


@pytest.fixture(autouse=True)
def mock_stop(request):
    def fin():
        mock_json.stop()
        mock_xml.stop()

    request.addfinalizer(fin)
'''

file_template = \
'''import os


class Template:

    def __class_getitem__(cls, name):
        root_dir = os.path.abspath(__file__ + "/../../")
        with open(f"{root_dir}/{name}", 'r') as f:
            return f.read()
'''

file_sql = \
"""import os


class Query:

    def __class_getitem__(cls, name):
        root_dir = os.path.abspath(__file__ + "/../../")
        with open(f"{root_dir}/{name}", 'r') as f:
            return f.read()
"""