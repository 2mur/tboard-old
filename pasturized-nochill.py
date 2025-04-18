import pandas as pd

# Load the data
df = pd.read_csv('dune/raw-milk-nochill.csv')

bins = []
flow = []

datelen = len('2025-03-06 14:24:37')

bins = []
flow = []
binsfound = []
bindict = {'[0-100)': 1, '[100-500)':2, '[500-1k)': 3,
           '[1k-2.5k)':4, '[2.5k-5k)':5, '[5k-10k)':6,
           '[>10k]':7}

for i, row in df.iterrows():
    v = row.iloc[0].split(',')
    if v[0] == 'b':
        #"b,[1k-2.5k),0,1,0E0,1.0231172384598141E3"
        binname = v[1]
        row = {'bin': v[1],
               'buy_count': v[2],
               'sell_count': v[3],
               'buy_bin_volume': v[4],
               'sell_bin_volume': v[5],
               'rank': bindict[binname]}
        binsfound.append(v[1])
        bins.append(row)

    if v[0] == 'f':
        #NOCHILL-WAVAX:uniswap-v3
        pool, dexver = v[2].split(':')
        dex, ver = dexver.split('-')
        row = {'day': pd.to_datetime(v[1][:datelen]),
               'dex':dex,
               'ver':ver,
               'pool': pool,
               'positive_flow': float(v[3]),
               'negative_flow': float(v[4]), 
               'netflow': float(v[5]), 
               'volume': float(v[6])}
        flow.append(row)

missingbins = set(bindict.keys()) - set(binsfound)

for b in missingbins:
    row = {'bin': b,
            'buy_count': 0,
            'sell_count': 0,
            'buy_bin_volume': 0,
            'sell_bin_volume': 0,
            'rank': bindict[b]}
    bins.append(row)

binsdf = pd.DataFrame(bins).set_index('rank')
binsdf.sort_index(inplace=True)
binsdf.to_csv('pasturize/pasturized-jugs-nochill.csv')

flowdf = pd.DataFrame(flow).set_index('day')
flowdf.sort_values(by="day", ascending=False,inplace=True)
flowdf.to_csv('pasturize/pasturized-milk-nochill.csv')

