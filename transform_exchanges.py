import pandas as pd


# Load data into a dataframe
df = pd.read_csv("exchanges.csv")
print(df.head())

# Make columns snake case and lower case
def change_case(str):
    return "".join(["_" + i.lower() if i.isupper() else i for i in str]).lstrip("_")


df.columns = df.columns.map(change_case)
print(df.head())

# Convert Unix timestamp to datetime in Asia/Bangkok
df["updated_gmt_7"] = df["updated"].astype({"updated": "datetime64[ms]"}) \
                        .dt.tz_localize("UTC") \
                        .dt.tz_convert("Asia/Bangkok")
print(df.head())