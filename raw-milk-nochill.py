from dune_client.client import DuneClient
import dotenv
import os
dotenv.load_dotenv()

# DUNE API CONNECTION
os.chdir("C:/Users/tima-/Desktop/web/backend-t-site")
dotenv.load_dotenv(".env")
dune = DuneClient.from_env()

# Output - 386 rows (53.3 KB)
daily_milk = dune.get_latest_result_dataframe(4897792)
daily_milk.to_csv("dune/raw-milk-nochill.csv", index=False)
