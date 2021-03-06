import os
from dotenv import load_dotenv
import requests
from requests.models import PreparedRequest
import json

load_dotenv('.env')
X_API_KEY = os.environ.get("X_API_KEY")
BASE_URL = os.environ.get("BASE_URL")


def getTransfersByToken(blockTimestampGt, contractAddress, tokenId,
                        limit = 500, sortDirection = "SORT_DIRECTION_UNSPECIFIED", transferTypes="TRANSFER_TYPE_REGULAR"):
    headers = {
        'x-api-key': X_API_KEY,
    }

    params = {
        'limit': limit,
        'offset': 0,
        'sortDirection': sortDirection,
        'blockTimestampGt': blockTimestampGt,
        'transferTypes': transferTypes,
    }


    req = PreparedRequest()
    url = BASE_URL + '/events/v1beta1/transfers/' + contractAddress + "/" + tokenId

    transfers = []

    while True:
        req.prepare_url(url, params)
        resp = requests.get(req.url, headers=headers)
        transfers += (resp.json())["transfers"]
        print("Batch of transfers is received. Total number of transfers received is {}.".format(len(transfers)))
        if len((resp.json())["transfers"]) < limit:
            print(
                "Last batch of transfers is received. Total number of transfers received is {}.".format(len(transfers)))
            break
        else:
            params['offset'] += limit

    return transfers
