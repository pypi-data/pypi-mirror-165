import matplotlib.pyplot as plt
from simba.read_config_unit_tests import (read_config_entry,
                                          read_config_file,
                                          check_file_exist_and_readable)
from simba.misc_tools import get_fn_ext, find_video_of_file
from simba.labelling_aggression import choose_folder2, load_frame2
import cv2
from simba.rw_dfs import read_df
import os
import threading
from copy import copy


class InteractiveProbabilityGrapher(object):
    def __init__(self,
                 config_path: str=None,
                 file_path: str=None,
                 model_path: str=None):

        if file_path == 'No file selected':
            print('SIMBA ERROR: No feature file path selected. Please select a path to a valid SimBA file containing machine learning features. They are by default located in the `project_folder/csv/features_extracted` directory')
            raise FileNotFoundError('SIMBA ERROR: No feature file path selected. Please select a path to a valid SimBA file containing machine learning features. They are by default located in the `project_folder/csv/features_extracted` directory')
        elif model_path == 'No file selected':
            print('SIMBA ERROR: No model file path selected. Please select a path to a valid machine learning model file.')
            raise FileNotFoundError('SIMBA ERROR: No model file path selected. Please select a path to a valid machine learning model file. They are by default located in a subdirectory of the `models` folder within your project directory tree')
        self.click_counter = 0
        self.config = read_config_file(config_path)
        self.project_path = self.config.get('General settings', 'project_path')
        self.in_dir = os.path.join(self.project_path, 'csv')
        self.videos_path = os.path.join(self.project_path, 'videos')
        self.file_type = read_config_entry(self.config, 'General settings', 'workflow_file_type', 'str', 'csv')
        self.file_path, self.model_path = file_path, model_path
        self.clf_name = str(os.path.basename(self.model_path)).split(".")[0]
        self.data_path = os.path.join(self.in_dir, "validation", os.path.basename(self.file_path))
        check_file_exist_and_readable(self.data_path)
        self.data_df = read_df(self.data_path, self.file_type)
        self.p_arr = self.data_df[['Probability_{}'.format(self.clf_name)]].to_numpy()
        dir_name, file_name, ext = get_fn_ext(self.data_path)
        current_video_file_path = find_video_of_file(video_dir=self.videos_path, filename=file_name)
        self.cap = cv2.VideoCapture(current_video_file_path)
        self.master_window = choose_folder2(current_video_file_path, config_path)



    @staticmethod
    def click_event(event):
        global current_x_cord
        if (event.dblclick) and (event.button == 1) and (type(event.xdata) != None):
            current_x_cord = int(event.xdata)

    def create_plots(self):
        import matplotlib
        matplotlib.use('TkAgg')

        probability = "Selected frame: {}, {} probability: {}".format(str(0), self.clf_name, str(self.p_arr[0][0]))
        plt_title = 'Click on the points of the graph to display the corresponding video frame. \n {}'.format(str(probability))
        global current_x_cord
        current_x_cord, prior_x_cord = None, None
        fig, ax = plt.subplots()
        ax.plot(self.p_arr)
        plt.xlabel('frame #', fontsize=16)
        plt.ylabel(str(self.clf_name) + ' probability', fontsize=16)
        plt.title(plt_title)
        plt.grid()
        line = None
        fig.canvas.draw()
        fig.canvas.flush_events()

        while True:
            _ = fig.canvas.mpl_connect('button_press_event', lambda event: self.click_event(event))
            if current_x_cord != prior_x_cord:
                prior_x_cord = copy(current_x_cord)
                probability = "Selected frame: {}, {} probability: {}".format(str(current_x_cord), self.clf_name, str(self.p_arr[current_x_cord][0]))
                plt_title = 'Click on the points of the graph to display the corresponding video frame. \n {}'.format(str(probability))
                load_frame2(current_x_cord, self.master_window.guimaster(), self.master_window.Rfbox())
                if line != None:
                    line.remove()
                plt.title(plt_title)
                line = plt.axvline(x=current_x_cord, color='r')
            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.ion()
            threading.Thread(plt.show()).start()
            plt.pause(.0001)

# test = InteractiveProbabilityGrapher(config_path=r'/Users/simon/Desktop/troubleshooting/train_model_project/project_folder/project_config.ini', file_path='/Users/simon/Desktop/troubleshooting/train_model_project/project_folder/csv/features_extracted/Together_1.csv', model_path='/Users/simon/Desktop/troubleshooting/train_model_project/models/generated_models/Attack.sav')
# test.create_plots()


# #
# if click_counter == 0:
#     vertical_line = plt.axvline(x=0, color='r')
# else:
#     vertical_line.remove()
# click_counter += 1
# probability = p_arr[int(event.xdata)].astype(str)
# load_frame2(int(event.xdata), master.guimaster(), master.Rfbox())
# print("Selected frame has a probability of", probability,
#       ", please enter the threshold into the entry box and validate.")
# vertical_line.set_xdata(x=int(event.xdata))
# fig.canvas.draw()
# fig.canvas.flush_events()
# # a.remove()
#
#
#
#
#
#
#
#
#
#
#
# from configparser import ConfigParser, NoSectionError, NoOptionError
# import os
# import pandas as pd
#
# import cv2
# from simba.labelling_aggression import *
# import threading
# from simba.rw_dfs import *
# from simba.drop_bp_cords import get_fn_ext
# import os
# from simba.misc_tools import find_video_of_file
#
#
#
# def updateThreshold_graph(inifile, csv ,model):
#     global click_counter
#     global vertical_line
#     configFile = str(inifile) ## get ini file
#     config = ConfigParser()
#     config.read(configFile)
#     project_path = config.get('General settings', 'project_path')
#     csv_dir = os.path.join(project_path, 'csv')
#     videos_path = os.path.join(project_path, 'videos')
#
#     currFile = os.path.join(csv_dir,"validation",(os.path.basename(csv)))
#     classifierName = str(os.path.basename(model)).split(".")[0]
#     try:
#         wfileType = config.get('General settings', 'workflow_file_type')
#     except NoOptionError:
#         wfileType = 'csv'
#     currDf = read_df(currFile, wfileType)
#     probabilityColumnName = 'Probability_' + classifierName
#     probs = currDf[[probabilityColumnName]].to_numpy()
#
#     # get frame dir
#     frames_dir_in = os.path.join(project_path, 'frames', 'input')
#
#
#     # frames_dir_in = config.get('Frame settings', 'frames_dir_in')
#     currFrameFolder = os.path.basename(currFile).replace('.' + wfileType, '')
#
#     # get video file
#     dir_name, file_name, ext = get_fn_ext(currFile)
#     current_video_file_path = find_video_of_file(video_dir=videos_path, filename=file_name)
#     cap = cv2.VideoCapture(current_video_file_path)
#     master = choose_folder2(current_video_file_path, inifile) ## open up label gui
#
#
#     ### gets mouse click on graph to open up the frames
#     def onclick(event):
#         global click_counter
#         global vertical_line
#         if event.dblclick:
#             if event.button == 1: ##get point 1 on double left click
#                 if click_counter == 0:
#                     vertical_line = plt.axvline(x=0, color='r')
#                 click_counter += 1
#                 probability = probs[int(event.xdata)].astype(str)
#                 load_frame2(int(event.xdata),master.guimaster(),master.Rfbox())
#                 print("Selected frame has a probability of",probability, ", please enter the threshold into the entry box and validate.")
#                 vertical_line.set_xdata(x=int(event.xdata))
#                 fig.canvas.draw()
#                 fig.canvas.flush_events()
#                 #a.remove()
#
#
#     #plot graphs
#
#     fig, ax = plt.subplots()
#     ax.plot(probs)
#     plt.xlabel('frame #', fontsize=16)
#     plt.ylabel(str(classifierName) + ' probability', fontsize=16)
#     plt.title('Click on the points of the graph to display the corresponding frames.')
#     plt.grid()
#     cid = fig.canvas.mpl_connect('button_press_event', onclick) ##incoporate mouse click event
#     plt.ion()
#     threading.Thread(plt.show()).start()
#     plt.pause(.001)
#
#
#
#
#
#
#
#
#
#
#
