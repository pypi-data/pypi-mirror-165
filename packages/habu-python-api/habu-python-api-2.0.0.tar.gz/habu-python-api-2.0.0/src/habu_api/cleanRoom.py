import datetime
import json
import os
import pytz

import requests, base64

from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning

class BaseApi():
    def __init__(self):
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        self.api = os.getenv("HABU_API", "https://localhost:9443")
        self.access_token, self.expire_time = self.login()

    def login(self):
        client = os.getenv("HABU_API_CLIENT")
        secret = os.getenv("HABU_API_SECRET")

        if not client or not secret:
            raise Exception("API Client and Secret must be defined in your environment. Please check documentation!")

        usrPass = "%s:%s" %(client, secret)
        b64Val = base64.b64encode(usrPass.encode()).decode()

        data = {'grant_type': 'client_credentials'}
        response = requests.post("%s/v1/oauth/token" % self.api,
                                 headers={"Authorization": "Basic %s" % b64Val},
                                 data=data,
                                 verify=False)

        if response.status_code != 200:
            raise Exception("Unable to login to habu API. Check your environment and settings!")

        data = response.json()
        access_token = data["accessToken"]
        expires_at = data["expiresAt"]
        return data["accessToken"], datetime.datetime.strptime(data["expiresAt"], '%Y-%m-%dT%H:%M:%S.%f%z')

    def get_token(self):
        if self.expire_time < pytz.UTC.localize(datetime.datetime.now()):
            self.access_token, self.expire_time = self.login()
        return self.access_token

    def post(self, url, key=None):
        response = requests.post(url,
                                 verify=False,
                                 headers={'Authorization': 'Bearer %s' %self.get_token()})
        if response.status_code != 200:
            response.raise_for_status()
        return response.json()[key]

    def get(self, url, key=None):
        response = requests.get(url,
                                verify=False,
                                headers={"Authorization": "Bearer %s" %self.get_token()})
        if response.status_code != 200:
            response.raise_for_status()

        if len(response.text) == 0:
            return []
        else:
            if key:
                return response.json()[key]
            else:
                return response.json()

class CleanRoom(BaseApi):
    def __init__(self):
        BaseApi.__init__(self)
        self.org_uuid = os.getenv("HABU_ORGANIZATION")
        if not self.org_uuid:
            raise Exception("Organization must be defined in your environment. Please check documentation!")

    def get_clean_rooms(self):
        return self.get("%s/v1/cleanrooms" %self.api)

    def get_clean_room_questions(self, cleanroom_uuid):
        return self.get("%s/v1/cleanrooms/%s/cleanroom-questions"
                        % (self.api, cleanroom_uuid))

    def get_question_runs(self, question_uuid):
        return self.get("%s/v1/cleanroom-questions/%s/cleanroom-question-runs"
                        % (self.api, question_uuid))

    def get_question_run_data(self, run_uuid):
        return self.get("%s/v1/cleanroom-question-runs/%s/data"
                        % (self.api, run_uuid))