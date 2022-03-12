from serviceCallers.tokenMetadata import getTokenMetadata
import json


class TraitValue:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.occurrence = 1

class TraitType:
    def __init__(self, name):
        self.name = name
        self.totalOccurrence = 0
        self.traitValues = []

    def checkIfValueExists(self, value):
        valueFound = False
        index = 0
        while not valueFound:
            if index == len(self.traitValues):
                self.traitValues.append(TraitValue(self.name, value))
                self.totalOccurrence += 1
                break
            if self.traitValues[index].value == value:
                self.traitValues[index].occurrence += 1
                self.totalOccurrence += 1
                valueFound = True
            index += 1

class TraitTypeList:
    def __init__(self):
        self.traits = []
        self.diversity = 0

    def checkIfTraitTypeExists(self, name, value):
        traitFound = False
        index = 0
        while not traitFound:
            if index == len(self.traits):
                self.traits.append(TraitType(name))
                self.traits[-1].checkIfValueExists(value)
                self.diversity += 1
                break
            if self.traits[index].name == name:
                self.traits[index].checkIfValueExists(value)
                traitFound = True
            index += 1

    def calculateRarity(self, attributes):
        rarityScore = 0
        for elem in attributes:
            dividend = 0
            divisor = 0
            for attr in self.traits:
                if elem["trait_type"] == attr.name:
                    dividend = attr.totalOccurrence
                    for value in attr.traitValues:
                        if elem["value"] == value.value:
                            divisor = value.occurrence
                            break
            rarityScore += dividend/divisor

        rarityScore *= ((self.diversity+abs(self.diversity - len(attributes)))/self.diversity)
        return rarityScore


def rarityCalculationWithinCollection(nftList):
    nftMetadataList = []
    traitList = TraitTypeList()

    for nft in nftList:
        attr = getTokenMetadata(contractAddress=nft["contractAddress"], tokenId=nft["tokenId"])["attributes"]
        nftMetadataList.append({
            'tokenId': nft["tokenId"],
            'attr': attr,
            'rarityScore': 0,
        })

        for newAttr in attr:
            traitList.checkIfTraitTypeExists(newAttr["trait_type"], newAttr["value"])

    for nft in nftMetadataList:
        nft['rarityScore'] = traitList.calculateRarity(nft['attr'])

    return nftMetadataList

def rarityCalculationForOneNft(nftList, nftSearch):
    nftMetadataList = []
    traitList = TraitTypeList()

    nftMetadata = getTokenMetadata(contractAddress=nftSearch["contractAddress"], tokenId=nftSearch["tokenId"])["attributes"]

    for nft in nftList:
        attr = getTokenMetadata(contractAddress=nft["contractAddress"], tokenId=nft["tokenId"])["attributes"]
        nftMetadataList.append({
            'tokenId': nft["tokenId"],
            'attr': attr,
        })

        for newAttr in attr:
            traitList.checkIfTraitTypeExists(newAttr["trait_type"], newAttr["value"])

    return traitList.calculateRarity(nftMetadata)

def rarityCalculationWithMetadata(nftDetails):
    traitList = TraitTypeList()

    for nft in nftDetails:
        try:
            attr = json.loads(nft['metadata']['metadata']['raw'])["attributes"]
            for newAttr in attr:
                traitList.checkIfTraitTypeExists(newAttr["trait_type"], newAttr["value"])
            nft['rarityScore'] = True

        except:
            nft['rarityScore'] = False
            print("Failed to parse attributes from nft with id {}".format(nft['tokenDetails']['tokenId']))

    for nft in nftDetails:
        if nft['rarityScore']:
            nft['rarityScore'] = traitList.calculateRarity(json.loads(nft['metadata']['metadata']['raw'])["attributes"])

    return nftDetails