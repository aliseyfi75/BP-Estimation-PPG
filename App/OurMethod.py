import shutil
import os
from Codes.pre_processing_features import pre_process_input
import numpy as np
from keras.models import load_model

# extract features and save them to a ./PPG/filename_features.csv
def extract_features(directory_name, file_name):
	ppg_data = np.genfromtxt('Codes/PPG/processed/' + directory_name + '/' + file_name + '.csv', delimiter=',')
	luna_roll = ppg_data[700:, 1]
	luna_roll_sub = ppg_data[700:, 2]
	luna_roll_sub_lpf = ppg_data[700:, 3]
	luna_roll_sub_lpf_cutstart = ppg_data[700:, 4]
	luna_cutstart_hpf = ppg_data[722:, 7]
	luna_cutstart_hpf_bpf_bmp = ppg_data[722:, 8]
	pre_process_input(luna_cutstart_hpf, 20, 'Codes/PPG/' + file_name + '_features.csv')

def function(video_path, vidoe_name):
	shutil.copyfile(video_path, 'Codes/PPG/videos/input/' + vidoe_name + '.mp4')
	os.system('Codes/Reading_PPG/signal_run_all.py')

	directory_name = 'input'
	file_name = vidoe_name
	extract_features(directory_name=directory_name, file_name= file_name)
	PPG_data = np.genfromtxt('Codes/PPG/' + file_name + '_features.csv', delimiter=',')

	loaded_ANN = load_model('Codes/model_1to6.h5')
	predictions = loaded_ANN.predict(PPG_data * 5)

	mean_pred = np.mean(predictions, axis=0)
	print("Estimated Blood Pressure :", mean_pred)

	H = mean_pred[1]
	L = mean_pred[0]

	return H, L