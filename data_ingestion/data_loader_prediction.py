import os
import pandas as pd
from Logging.Logging import logger

class Data_Getter_Pred:
    """
    This class shall  be used for obtaining the data from the source for prediction.

    Written By: Joydeep Ghosh
    Version: 1.0
    Revisions: None

    """
    def __init__(self):

        self.directory_path=r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction/Prediction_FileFromDB'
        if os.path.isdir(self.directory_path) != True:
            os.mkdir(self.directory_path)
            print(os.getcwd())
        else:
            pass
        self.prediction_file=r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction/Prediction_FileFromDB/InputFile.csv'
        self.log_file_loc=r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\Prediction_Logs/Prediction_Logs.log'
        self.log=logger()
        self.file=open(self.log_file_loc, 'a+')
        self.log.apply_log(self.file,'Starting the Data_Getter_Pred')
        self.file.close()

    def get_data(self):
        """
        Method Name: get_data
        Description: This method reads the data from source.
        Output: A pandas DataFrame.
        On Failure: Raise Exception

         Written By: Joydeep Ghosh
        Version: 1.0
        Revisions: None

        """
        self.file = open(self.log_file_loc, 'a+')
        self.log.apply_log(self.file,'Entered the get_data method of the Data_Getter class')
        self.file.close()
        try:
            self.data= pd.read_csv(self.prediction_file) # reading the data file
            print(self.data)
            self.file = open(self.log_file_loc, 'a+')
            self.log.apply_log(self.file,'Data Load Successful.Exited the get_data method of the Data_Getter class')
            self.file.close()
            return self.data
        except Exception as e:
            self.file = open(self.log_file_loc, 'a+')
            self.log.apply_log(self.file,'Exception occured in get_data method of the Data_Getter class. Exception message: %s::'%e)
            self.log.apply_log(self.file,'Data Load Unsuccessful.Exited the get_data method of the Data_Getter class')
            self.file.close()
            raise Exception()


