from dune_client.client import DuneClient
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime, timezone, timedelta
import pandas as pd
import dotenv
import os
dotenv.load_dotenv()

# DUNE API CONNECTION
os.chdir("/home/twom/web/")
dotenv.load_dotenv(".env")
dune = DuneClient.from_env()
df = dune.get_latest_result_dataframe(4897792)

# MONGO DB CONNECTION
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
mongo_db = client["t-site"]
bins_collection = mongo_db['bins']
netflows_collection = mongo_db['netflows']

# PROCESSING THE DATAFRAME
bindict = {'[0-100)': 1, '[100-500)':2, '[500-1k)': 3,
           '[1k-2.5k)':4, '[2.5k-5k)':5, '[5k-10k)':6,
           '[>10k]':7, 'nan-bin':0}

def process_dune(df_raw):
    df_split = df_raw['cat'].str.split(',', expand=True)
    bins = df_split[df_split[0]=='b'].copy()
    bins.columns = [
        'type',
        'day',
        'token',
        'bin',
        'buy_count',
        'sell_count',
        'buy_bin_volume',
        'sell_bin_volume']
    
    # Optional: Convert data types (e.g., timestamp)
    bins['day'] = pd.to_datetime(bins['day'])
    bins['buy_count'] = bins['buy_count'].astype(float)
    bins['sell_count'] = bins['sell_count'].astype(float)
    bins['buy_bin_volume'] = bins['buy_bin_volume'].astype(float)
    bins['sell_bin_volume'] = bins['sell_bin_volume'].astype(float)
    
    def bin_rank(row):
        return bindict[row['bin']]
    
    bins['rank']= bins.apply(bin_rank, axis=1)
    bins.drop('type', axis=1, inplace=True)
    
    flow = df_split[df_split[0]=='f'].copy()
    flow.columns = [
        'type',
        'token',
        'day',
        'pool-dex',
        'positive_flow',
        'negative_flow',
        'netflow',
        'volume'
    ]
    # Optional: Convert data types (e.g., timestamp)
    flow['day'] = pd.to_datetime(flow['day'])
    flow['positive_flow'] = flow['positive_flow'].astype(float)
    flow['negative_flow'] = flow['negative_flow'].astype(float)
    flow['netflow'] = flow['netflow'].astype(float)
    flow['volume'] = flow['volume'].astype(float)
    pooldex = flow['pool-dex'].str.split(':', expand=True)
    flow['pool'] = pooldex[0]

    def flow_dex(row):
        return row[1].split('-')[0]
    
    flow['dex'] = pooldex.apply(flow_dex, axis=1)
    flow.drop(['type','pool-dex'], axis=1, inplace=True)
    return bins, flow

prebins, flow = process_dune(json_data)
tokens = flow['token'].unique()
days = prebins['day'].unique()

init_bins = []
for day in days:
    for token in tokens:
        for bin_label, rank in bindict.items():
            if rank == 0:  # Skip the '[nan]' bin
                continue
            init_bins.append({
                'day': day,
                'token': token,
                'bin': bin_label,
                'buy_count': 0,
                'sell_count': 0,
                'buy_bin_volume': 0.0,
                'sell_bin_volume': 0.0,
                'rank': rank
            })

# MAKE EMPTY BINS
init_bins = pd.DataFrame(init_bins)

combined_prebins = pd.concat([prebins, init_bins], ignore_index=True)
cols_to_check = ['buy_count','sell_count','buy_bin_volume','sell_bin_volume'] 
combined_prebins = combined_prebins.sort_values(by=cols_to_check, ascending=False)
bins = combined_prebins.drop_duplicates(subset=['day', 'token', 'bin','rank'])

latest_date = prebins['day'].min()
print(f'updating dates: {days}')

# SAVE TODAYS DATA
today = datetime.now(timezone.utc)
bins.to_csv(f'milk-bottles-{today}.csv',index=False)
flow.to_csv(f'milk-flow-{today}.csv',index=False)

#UPLOAD DATA ON MONGODB
bins_collection.delete_many({ 'day': { '$gte': latest_date } })
netflows_collection.delete_many({ 'day': { '$gte': latest_date } })

binsrec = bins.to_dict('records')
flowrec = flow.to_dict('records')

bins_collection.insert_many(binsrec)
netflows_collection.insert_many(flowrec)

print(f"Updated FLOW and BINS for {today}")
client.close()
