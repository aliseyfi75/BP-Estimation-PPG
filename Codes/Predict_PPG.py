import numpy as np
import matplotlib.pyplot as pp
from pre_processing_features import pre_process_input
import joblib
from keras.models import load_model


# extract features and save them to a ./PPG/filename_features.csv
def extract_features(directory_name, file_name):
    ppg_data = np.genfromtxt('./PPG/processed/' + directory_name + '/' + file_name + '.csv', delimiter=',')
    luna_roll = ppg_data[700:, 1]
    luna_roll_sub = ppg_data[700:, 2]
    luna_roll_sub_lpf = ppg_data[700:, 3]
    luna_roll_sub_lpf_cutstart = ppg_data[700:, 4]
    luna_cutstart_hpf = ppg_data[722:, 7]
    luna_cutstart_hpf_bpf_bmp = ppg_data[722:, 8]

    pre_process_input(luna_cutstart_hpf, 20, './PPG/' + file_name + '_features.csv')

    # pp.plot(luna_cutstart_hpf)
    # pp.show()

direct = '6_3'
filename = 'IMG_6553'
extract_features(direct,file_name=filename)

PPG_data = np.genfromtxt('./PPG/' + filename + '_features.csv', delimiter=',')
# #
# loaded_regressor = joblib.load("./random_forest_1to4.joblib")
# predictions = loaded_regressor.predict(PPG_data)

loaded_ANN = load_model('model_1to6.h5')
predictions = loaded_ANN.predict(PPG_data * 5)

print(predictions)
print("Estimated Blood Pressure :", np.mean(predictions, axis= 0))




































