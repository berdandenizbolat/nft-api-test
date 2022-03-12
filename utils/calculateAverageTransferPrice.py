def calculateAverageTransferPrice(tokenDetail):
    averageValue = 0
    nonZeroValues = 0

    for transfer in tokenDetail['transfer']:
        if float(transfer["txValue"]["decimalValue"]) != 0:
            averageValue += float(transfer["txValue"]["decimalValue"]) / int(transfer['nftTransfersQuantity'])
            nonZeroValues += 1

    if nonZeroValues == 0:
        return 0

    return averageValue / nonZeroValues

