import pandas as pd
import keras
from keras.models import Sequential
from keras.layers import *

RUN_NAME = "run 8 layers"

# Trainning data
training_data_df = pd.read_csv("train.csv")
X = training_data_df.drop('win', axis=1).values
Y = training_data_df[['win']].values

# Load the separate test data set
test_data_df = pd.read_csv("test.csv")
X_test = test_data_df.drop('win', axis=1).values
Y_test = test_data_df[['win']].values

# Define the model
model = Sequential()
model.add(Dense(50, input_dim=len(training_data_df.columns)-1, activation='relu', name='layer_1'))
model.add(Dense(100, activation='relu', name='layer_2'))
model.add(Dense(50, activation='relu', name='layer_3'))
model.add(Dense(50, activation='relu', name='layer_4'))
model.add(Dense(50, activation='relu', name='layer_5'))
model.add(Dense(50, activation='relu', name='layer_6'))
model.add(Dense(50, activation='relu', name='layer_7'))
model.add(Dense(50, activation='relu', name='layer_8'))
# model.add(Dense(50, activation='relu', name='layer_9'))
model.add(Dense(1, activation='linear', name='output_layer'))
model.compile(loss='mean_squared_error', optimizer='adam',metrics=['accuracy'])

# Create a TensorBoard logger
logger = keras.callbacks.TensorBoard(
    log_dir='logs/{}'.format(RUN_NAME),
    write_graph=True,
    histogram_freq=5
)

# Train the model
model.fit(
    X,
    Y,
    epochs=50,
    shuffle=True,
    verbose=2,
    validation_data=(X_test,Y_test),
    callbacks=[logger]
)

model.save(RUN_NAME+".h5")

test_error_rate = model.evaluate(X_test, Y_test, verbose=0)
print("accuracy is: {}".format(test_error_rate[1]))

