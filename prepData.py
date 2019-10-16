import pandas as pd
import numpy as np
import ddragon
from sklearn.preprocessing import MinMaxScaler

def clean(data):
    data = data.drop('gameId',axis=1)
    # Convert champion name into champion ID
    for col in data.columns:
        if col.endswith("_champion"):
            champIds = [ddragon.getChampionId(x) for x in data[col]]
            # print(champIds)
            data[col] = champIds

    # Convert win from bool to int
    data['win'] = [1 if x else 0 for x in data['win']]
    return data

def split():
    data = pd.read_csv("data_scaled.csv")
    data['split'] = np.random.randn(data.shape[0],1)
    msk = np.random.rand(len(data)) <= 0.7
    # print(msk)
    train = data[msk].drop("split",axis=1)
    test = data[~msk].drop("split",axis=1)

    train.to_csv("train.csv", index=False)
    test.to_csv("test.csv",index=False)

def scale():
    # Load raw data
    df = pd.read_csv("data.csv")
    df = clean(df)
    # Data needs to be scaled to a small range like 0 to 1 for the neural
    # network to work well.
    scaler = MinMaxScaler(feature_range=(0, 1))

    # Scale both the training inputs and outputs
    scaled = scaler.fit_transform(df)

    # Print out the adjustment that the scaler applied to the total_earnings column of data
    #print("Note: total_earnings values were scaled by multiplying by {:.10f} and adding {:.6f}".format(scaler.scale_[8], scaler.min_[8]))

    # Create new pandas DataFrame objects from the scaled data
    scaled_training_df = pd.DataFrame(scaled, columns=df.columns.values)
    # Save scaled data dataframes to new CSV files
    scaled_training_df.to_csv("data_scaled.csv", index=False)

scale()
split()