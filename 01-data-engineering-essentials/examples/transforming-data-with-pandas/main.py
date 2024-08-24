import pandas as pd


# Load data into a dataframe
df = pd.read_csv("sample_data.csv")
print(df.head())

# Make columns lower case
df.columns = df.columns.str.lower()
print(df.head())

# Split name into first and last names
df[["first_name", "last_name"]] = df.customer_name.str.split(expand=True)
print(df.head())

# Transform data string into date object
print(df.info())
df["new_purchase_date"] = pd.to_datetime(df.purchase_date)
print(df.info())
print(df.head())


# Group customers by age
def group_by_age(age: int) -> str:
    if age <= 30:
        return "<=30"
    elif age <= 40:
        return "31-40"
    elif age <= 50:
        return "41-50"
    elif age <= 60:
        return "51-60"
    else:
        return "61+"


df["age_group"] = df.age.map(group_by_age)
print(df.head())
