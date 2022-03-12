from serviceCallers.nftsByContract import getNFTsByContract
from serviceCallers.tokenMetadata import getTokenMetadata
from serviceCallers.transfersByToken import getTransfersByToken
from utils.rarityCalculation import rarityCalculationWithMetadata
from utils.calculateAverageTransferPrice import calculateAverageTransferPrice
from utils.plot import plotTokensRarityVsAveragePrice
import os
import pickle


def getCollectionDetails(blockTimestampGt, contractAddress):
    if not os.path.exists("tokens_buffer"):
        tokens = getNFTsByContract(blockTimestampGt=blockTimestampGt, contractAddress=contractAddress)
        with open("tokens_buffer", "wb") as f:
            pickle.dump(tokens, f)
    else:
        with open("tokens_buffer", "rb") as f:
            tokens = pickle.load(f)


    if not os.path.exists("token_details"):
        token_details = []
    else:
        with open("token_details", "rb") as f:
            token_details = pickle.load(f)
    for token in tokens[len(token_details):]:
        metadata = getTokenMetadata(contractAddress, token['tokenId'])
        transfer = getTransfersByToken(blockTimestampGt, contractAddress,
                                       token['tokenId'])
        newAttr = {
            'tokenDetails': token,
            'metadata': metadata,
            'transfer': transfer,
        }
        token_details.append(newAttr)
        with open("token_details", "wb") as f:
            pickle.dump(token_details, f)

    token_details = rarityCalculationWithMetadata(token_details)

    for token in token_details:
        token['averagePrice'] = calculateAverageTransferPrice(token)

    plotTokensRarityVsAveragePrice(token_details)