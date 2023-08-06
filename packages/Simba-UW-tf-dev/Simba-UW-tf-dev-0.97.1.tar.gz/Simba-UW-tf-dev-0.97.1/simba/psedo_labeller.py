from simba.read_config_unit_tests import (read_config_entry, read_config_file, check_file_exist_and_readable, check_that_column_exist)
from simba.misc_tools import get_fn_ext, find_video_of_file, check_multi_animal_status
from simba.rw_dfs import read_df
from simba.drop_bp_cords import getBpNames, createColorListofList, create_body_part_dictionary
import os

class PseduLabeller(object):
    def __init__(self,
                 config_path: str=None,
                 input_file_path: str=None,
                 targets: list=None,
                 thresholds: list=None):

        self.config_path, self.input_file_path = config_path, input_file_path
        self.targets_lst, self.threshold_lst = targets, thresholds
        self.config = read_config_file(config_path)
        self.project_path = read_config_entry(self.config, 'General settings', 'project_path', data_type='str')
        self.file_type = read_config_entry(self.config, 'General settings', 'workflow_file_type', 'str', 'csv')
        self.animal_cnt = read_config_entry(self.config, 'General settings', 'animal_no', 'int')
        self.videos_path = os.path.join(self.project_path, 'videos')
        self.machine_results_path = os.path.join(self.project_path, 'csv', 'machine_results')
        _, self.in_file_name, _ = get_fn_ext(input_file_path)
        self.results_df_path = os.path.join(self.machine_results_path, self.in_file_name + '.' + self.file_type)
        self.video_path = find_video_of_file(video_dir=self.videos_path, filename=self.in_file_name)
        self.threshold_dict = dict(zip(targets, thresholds))
        check_file_exist_and_readable(self.results_df_path)
        self.data_df = read_df(self.results_df_path, self.file_type)
        self.multi_animal_status, self.multi_animal_ids = check_multi_animal_status(self.config, self.animal_cnt)
        self.x_cols, self.y_cols, self.pcols = getBpNames(self.config_path)
        self.clr_lst_of_lst = createColorListofList(self.animal_cnt, int(len(self.x_cols) / self.animal_cnt) + 1)
        for k, v in self.threshold_dict.items():
            check_that_column_exist(df=self.data_df, column_name='Probability_{}'.format(k),file_name=self.results_df_path)
            self.data_df[k] = [1 if x >= v else 0 for x in self.data_df['Probability_{}'.format(k)]]
        self.animal_bp_dict = create_body_part_dictionary(self.multi_animal_status, self.multi_animal_ids, self.animal_cnt, self.x_cols, self.y_cols, [], self.clr_lst_of_lst)






test = PseduLabeller(config_path='/Users/simon/Desktop/troubleshooting/train_model_project/project_folder/project_config.ini',
                 input_file_path='/Users/simon/Desktop/troubleshooting/train_model_project/project_folder/csv/machine_results/Together_1.csv',
                 targets=['Attack', 'Sniffing'],
                 thresholds=[0.5, 0.3])




