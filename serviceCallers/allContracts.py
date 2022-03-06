import os
from dotenv import load_dotenv
import requests
from requests.models import PreparedRequest
import json

load_dotenv('.env')
X_API_KEY = os.environ.get("X_API_KEY")
BASE_URL = os.environ.get("BASE_URL")

def getAllContracts(blockTimestampGt, limit = 500, sortDirection = "SORT_DIRECTION_UNSPECIFIED", contractTypes="TOKEN_TYPE_ERC721"):
    headers = {
        'x-api-key': X_API_KEY,
    }

    params = {
        'limit': limit,
        'offset': 0,
        'sortDirection': sortDirection,
        'blockTimestampGt': blockTimestampGt,
        'contractTypes': contractTypes,
    }


    req = PreparedRequest()
    url = BASE_URL + '/contracts/v1beta1/all'

    contracts = []

    while True:
        req.prepare_url(url, params)
        resp = requests.get(req.url, headers=headers)
        contracts += (resp.json())["contracts"]
        if len((resp.json())["contracts"])<limit:
            break
        else:
            params['offset']+=limit

    return contracts
