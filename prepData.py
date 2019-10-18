import pandas as pd
import numpy as np
import ddragon
import config
import os
from sklearn.preprocessing import MinMaxScaler

class DataPrep:
    def __init__(self,folder):
        self._folder = folder

    def clean(self,data):
        data = data.drop('gameId',axis=1)
        # Convert win from bool to int
        data['win'] = [1 if x else 0 for x in data['win']]
        print("data is cleaned")
        return data

    def split(self):
        data = pd.read_csv(os.path.join(self._folder,"data_scaled.csv"))
        data['split'] = np.random.randn(data.shape[0],1)
        msk = np.random.rand(len(data)) <= 0.7
        # print(msk)
        train = data[msk].drop("split",axis=1)
        test = data[~msk].drop("split",axis=1)

        train.to_csv(os.path.join(self._folder,"train.csv"), index=False)
        test.to_csv(os.path.join(self._folder,"test.csv"),index=False)
        print(f"trainning and test data sets are created in {self._folder}")

    def scale(self):
        # Load raw data
        df = pd.read_csv(os.path.join(self._folder,"data.csv"))
        df = self.clean(df)
        print("scaling data")
        # Data needs to be scaled to a small range like 0 to 1 for the neural
        # network to work well.
        scaler = MinMaxScaler(feature_range=(0, 1))

        # Scale both the training inputs and outputs
        scaled = scaler.fit_transform(df)

        # Create new pandas DataFrame objects from the scaled data
        scaled_training_df = pd.DataFrame(scaled, columns=df.columns.values)
        # Save scaled data dataframes to new CSV files
        scaled_training_df.to_csv(os.path.join(self._folder,"data_scaled.csv"), index=False)

if __name__ == "__main__":
    folder = os.path.join("analysis",config.playerName)
    prep = DataPrep(folder)
    prep.scale()
    prep.split()