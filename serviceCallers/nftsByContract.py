import os
from dotenv import load_dotenv
import requests
from requests.models import PreparedRequest
import json

load_dotenv('.env')
X_API_KEY = os.environ.get("X_API_KEY")
BASE_URL = os.environ.get("BASE_URL")

def getNFTsByContract(blockTimestampGt, contractAddress, limit = 500, sortDirection = "SORT_DIRECTION_UNSPECIFIED", contractTypes="TOKEN_TYPE_ERC721"):
    headers = {
        'x-api-key': X_API_KEY,
    }

    params = {
        'limit': limit,
        'offset': 0,
        'sortDirection': sortDirection,
        'blockTimestampGt': blockTimestampGt,
        'contractTypes': contractTypes,
        'contractAddress': contractAddress,
    }

    req = PreparedRequest()
    url = BASE_URL + '/tokens/v1beta1/by_contract/'

    contracts = []

    while True:
        req.prepare_url(url, params)
        resp = requests.get(req.url, headers=headers)
        contracts += (resp.json())["tokens"]
        print("Batch of tokens is received. Total number of tokens received is {}.".format(len(contracts)))
        if len((resp.json())["tokens"]) < limit:
            print("Last batch of tokens is received. Total number of tokens received is {}.".format(len(contracts)))
            break
        else:
            params['offset'] += limit

    return contracts
