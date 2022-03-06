from serviceCallers.allContracts import getAllContracts
from serviceCallers.transfersByContract import getTransfersByContract


def sortCollections(blockTimestampGt, contractList, listLength = 100):
    contractDict = {}

    for contract in contractList:
        transferCount = len(getTransfersByContract(blockTimestampGt, contractAddress=contract["address"]))
        contractDict[contract["address"]] = transferCount

    sortedContracts = dict(sorted(contractDict.items(), key=lambda item: -item[1]))
    sortedContracts = list(sortedContracts.items())[:listLength]

    return sortedContracts

