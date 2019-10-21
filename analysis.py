import pandas as pd
import keras
import config
import os
from keras.models import Sequential
from keras.constraints import unit_norm
from keras.layers import Dense, Dropout
from keras.callbacks import EarlyStopping

class Analysis():
    RUN_NAME = "run 5 layers"

    def __init__(self,folder):
        self._folder = folder
        # Create a TensorBoard logger
        self._logger = keras.callbacks.TensorBoard(
            log_dir='logs/{}'.format(self.RUN_NAME),
            write_graph=True,
            histogram_freq=5
        )

    def loadData(self,filename):
        df = pd.read_csv(os.path.join(self._folder,filename))
        output = {}
        X = df.drop('win', axis=1).values
        Y = df[['win']].values
        output['df'] = df
        output['X'] = X
        output['Y'] = Y
        return output

    def build(self):
        # load data
        train = self.loadData("train.csv")
        test = self.loadData("test.csv")

        # Define the model
        model = Sequential()
        model.add(Dense(50, input_dim=len(train['df'].columns)-1, activation='relu', name='layer_1'))
        model.add(Dropout(0.4))
        # model.add(Dense(100, activation='relu', name='layer_2'))
        model.add(Dense(100, activation='relu', name='layer_2', kernel_constraint=unit_norm()))
        model.add(Dense(50, activation='relu', name='layer_3'))
        model.add(Dense(50, activation='relu', name='layer_4'))
        model.add(Dense(50, activation='relu', name='layer_5'))
        # model.add(Dense(50, activation='relu', name='layer_6'))
        # model.add(Dense(50, activation='relu', name='layer_7'))
        # model.add(Dense(50, activation='relu', name='layer_8'))
        # model.add(Dense(50, activation='relu', name='layer_9'))
        model.add(Dense(1, activation='sigmoid', name='output_layer'))
        model.compile(loss='logcosh', optimizer='adam',metrics=['accuracy'])

        # early stop
        early_stop = EarlyStopping(monitor='val_loss', min_delta=0,patience=3,verbose=1,mode='auto')

        # Train the model
        model.fit(train['X'],train['Y'],epochs=250,shuffle=True,verbose=2, validation_split=0.2,batch_size=5
        # ,validation_data=(test['X'],test['Y']),callbacks=[self._logger]
        ,callbacks=[early_stop]
        )

        # save model
        # model.save(config.playerName+".h5")

        test_error_rate = model.evaluate(test['X'], test['Y'], verbose=0)
        print("accuracy is: {}".format(test_error_rate[1]))

if __name__ == "__main__":
    folder = os.path.join("analysis","all")
    a = Analysis(folder)
    a.build()