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

# Generate list of last 2 dates (now, -1 day)
now_utc = datetime.now(timezone.utc)
date_list = [(now_utc - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(2)]
for day in date_list:
    bins_collection.delete_many({"day": day})
    netflows_collection.delete_many({"day": day})
    bins_collection.delete_many({"day": pd.to_datetime(day)})
    netflows_collection.delete_many({"day": pd.to_datetime(day)})
print(f"Deleted records for the last 2 days: {date_list}")


# PROCESSING THE DATAFRAME
datelen = len('2025-03-06')
bindict = {'[0-100)': 1, '[100-500)':2, '[500-1k)': 3,
           '[1k-2.5k)':4, '[2.5k-5k)':5, '[5k-10k)':6,
           '[>10k]':7, 'nan-bin':0}
init_bins = []
for day in date_list:
    for token in ['COQ', 'NOCHILL', 'WAIFU', 'KET']:
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
init_bins = pd.DataFrame(init_bins)


def delete_upload_recents(df,init_bins):
    flow = []
    for i, row in df.iterrows():
        v = row.iloc[0].split(',')
        if v[0] == 'b':
            #"b,2025-04-17 00:00:00.000 UTC,WAIFU,[>10k],1,2,0E0,0E0"
            # 0 1                           2     3      4 5 6   7
            if bindict[v[3]] == 0:
                continue
            else:
                mask = (init_bins['day'] == v[1][:datelen]) & (init_bins['token'] == v[2]) & (init_bins['bin'] == v[3])
                update_col = ['buy_count', 'sell_count', 'buy_bin_volume', 'sell_bin_volume']
                update_val =[round(float(v[4]), 2), round(float(v[5]), 2),round(float(v[6]), 2),round(float(v[7]), 2)]
                init_bins.loc[mask,update_col] = update_val

        if v[0] == 'f':
            #f,COQ,2025-04-17 00:00:00.000 UTC,COQ-OSAK:trader_joe-v1,5.600489981972303E-1,-6.89735066038711E0,-6.33730166218988E0,7.45739965858434E0
            pool, dexver = v[3].split(':')
            row = {'day': v[2][:datelen],
                    'token': v[1],
                    'dex':dexver,
                    'pool': pool,
                    'positive_flow': round(float(v[4]), 2),
                    'negative_flow': round(float(v[5]), 2), 
                    'netflow': round(float(v[6]), 2),
                    'volume': round(float(v[7]), 2)}
            flow.append(row)

    return init_bins, flow

#UPLOAD DATA ON MONGODB
f_bins, flow = delete_upload_recents(df,init_bins)
today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
f_bins.to_csv(f'daily-milk-{today}.csv',index=False)
bins = f_bins.to_dict('records')

bins_collection.insert_many(bins)
netflows_collection.insert_many(flow)
print(f"Updated FLOW and BINS for {today}")
client.close()

