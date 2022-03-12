from matplotlib import pyplot as plt
import numpy as np


def plotTokensRarityVsAveragePrice(tokenDetails):
    rarityList = []
    priceList = []
    for token in tokenDetails:
        if token['rarityScore'] and token['averagePrice']:
            if token['averagePrice'] < 30 and token['rarityScore'] < 10000:
                rarityList.append(token['rarityScore'])
                priceList.append(token['averagePrice'])

    fig = plt.figure()
    plt.scatter(rarityList, priceList, s=10)
    fig.suptitle('CyberBrokers: 0x892848074ddea461a15f337250da3ce55580ca85')
    plt.xlabel('rarity score')
    plt.ylabel('average price (ETH)')
    fig.savefig('test_outliers_removed.jpg')
