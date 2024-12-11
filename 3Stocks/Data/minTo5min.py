with open('BTCMin.csv', 'r') as fp:
    data = fp.readlines()

l = data

with open('BTC5min.csv', 'w') as fp:
    fp.write(data[0])
    for dataPt in data[1:-1:5]:
        fp.write(dataPt)