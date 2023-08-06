from winky.http_message import HTTPMessage
from winky.http_stub import HTTPStub
from winky.ssl import SSL
from winky.template_xml import TemplateXML
from winky.template_json import TemplateJSON
from winky.template_text import TemplateText
from winky.new_project import NewProject
from winky.database_postgre import Postgre
from winky.database_oracle import Oracle
from winky.database_mysql import MySQL
from time import sleep
import urllib3

urllib3.disable_warnings()
