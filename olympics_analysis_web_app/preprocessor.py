import pandas as pd

athlete_df = pd.read_csv("athlete_events.csv")
region_df = pd.read_csv("noc_regions.csv")


# here we preprocessed our data to make it ready for each menus of webpage

def preprocess():
    global athlete_df, region_df #these tables are defined outside the function and wtv changes made in this function will reflect in the tables outside the func.

    athlete_df = athlete_df[athlete_df["Season"]=="Summer"] # will focus in summer season only

    df = athlete_df.merge(region_df, on="NOC",how="left") # merge region_df and athlete_df

    df.drop_duplicates(inplace=True) # dropping duplicates

    df = pd.concat([df,pd.get_dummies(df["Medal"])],axis=1) # one hot encoding
    return df