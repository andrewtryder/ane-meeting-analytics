import os
import platform
import pytz
import time
from typing import Dict, List, Optional, Union, Any

import pandas as pd
from authlib.jose import jwt
import requests
from requests import Response

if platform.system() != "Windows":
    from dotenv import load_dotenv
    load_dotenv()



ZOOM_API_KEY = os.environ.get('ZOOM_API_KEY')
ZOOM_API_SECRET = os.environ.get('ZOOM_API_SECRET')

class Zoom:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.zoom.us/v2"
        self.reports_url = f"{self.base_url}/report/meetings"
        self.jwt_token_exp = 1800
        self.jwt_token_algo = "HS256"

    def fetch_meeting_registrants(self, meeting_id: str, jwt_token: bytes,
                                 next_page_token: Optional[str] = None) -> Response:
        url: str = f"{self.base_url}/meetings/{meeting_id}/registrants"
        query_params: Dict[str, Union[int, str]] = {"page_size": 300}
        if next_page_token:
            query_params.update({"next_page_token": next_page_token})
        r: Response = requests.get(url,
                                   headers={"Authorization": f"Bearer {jwt_token.decode('utf-8')}"},
                                   params=query_params)
        return r


    def fetch_meeting_participants(self, meeting_id: str, jwt_token: bytes,
                                 next_page_token: Optional[str] = None) -> Response:
        url: str = f"{self.reports_url}/{meeting_id}/participants"
        query_params: Dict[str, Union[int, str]] = {"page_size": 300}
        if next_page_token:
            query_params.update({"next_page_token": next_page_token})
        r: Response = requests.get(url,
                                   headers={"Authorization": f"Bearer {jwt_token.decode('utf-8')}"},
                                   params=query_params)
        return r

    def generate_jwt_token(self) -> bytes:
        iat = int(time.time())
        jwt_payload: Dict[str, Any] = {
            "aud": None,
            "iss": self.api_key,
            "exp": iat + self.jwt_token_exp,
            "iat": iat
        }
        header: Dict[str, str] = {"alg": self.jwt_token_algo}
        jwt_token: bytes = jwt.encode(header, jwt_payload, self.api_secret)
        return jwt_token

    def get_meeting_registrants(meetingid: str) -> int:
        zoom = Zoom(ZOOM_API_KEY, ZOOM_API_SECRET)
        jwt_token1: bytes = zoom.generate_jwt_token()
        registrants: requests.Response = zoom.fetch_meeting_registrants(meetingid, jwt_token1)
        # this is the total count
        count = len(registrants.json().get("registrants"))
        while token := registrants.json().get("next_page_token"):
            registrants = zoom.fetch_meeting_registrants(meetingid, jwt_token1, token)
            count += len(registrants.json().get("registrants"))
        # lets also iterate over the JSON and figure out who is in-person.
        inperson = 0
        for i in registrants.json().get("registrants"):
            for question in i['custom_questions']:
                if question['title'] == 'Do you plan to be in person or remote?' and question['value'] == "In person":
                    inperson += 1
        return count, inperson

    def get_meeting_attendees(meetingid):
        zoom = Zoom(ZOOM_API_KEY, ZOOM_API_SECRET)
        jwt_token: bytes = zoom.generate_jwt_token()
        response: Response = zoom.fetch_meeting_participants(meetingid, jwt_token)
        list_of_participants: List[dict] = response.json().get("participants")
        while token := response.json().get("next_page_token"):
            response = zoom.get_meeting_participants(meetingid, jwt_token, token)
            list_of_participants += response.json().get("participants")

        return list_of_participants