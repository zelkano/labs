import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
import os
import datetime
import subprocess
import getpass
import base64

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)