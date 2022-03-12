import os
from dotenv import load_dotenv
import requests

load_dotenv('.env')
X_API_KEY = os.environ.get("X_API_KEY")
BASE_URL = os.environ.get("BASE_URL")


def getTokenMetadata(contractAddress, tokenId):
    headers = {
        'x-api-key': X_API_KEY,
    }
    url = BASE_URL + '/tokens/v1beta1/token/' + contractAddress + "/" + tokenId + "/metadata"

    resp = requests.get(url, headers=headers)
    metadata = (resp.json())
    print("Metadata for the token {} is received.".format(tokenId))

    return metadata
