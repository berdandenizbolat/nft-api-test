def calculateAverageTransferPrice(transfers):
    averageValue = 0
    for transfer in transfers:
        averageValue += transfer["txValue"]["decimalValue"]

    return averageValue / len(transfers)