import os
import pandas as pd
from Logging.Logging import logger

class Get_Data:
    """
    This class shall  be used for obtaining the data from the source for training.

    Written By: Joydeep Ghosh
    Version: 1.0
    Revisions: None

    """
    def __init__(self):
        self.training_file_location=r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction/Training_File_from_DB/InputFile.csv'
        self.log_file=r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\General_Logging/Data_Loader.log'
        self.log=logger()

        self.file=open(self.log_file, 'a+')
        self.log.apply_log(self.file,'Starting data loading Training')
        self.file.close()
    def get_data_from_source(self):
        """
        Method Name: get_data_from_source
        Description: This method reads the data from source.
        Output: A pandas DataFrame.
        On Failure: Raise Exception

        Written By: Joydeep Ghosh
        Version: 1.0
        Revisions: None

        """
        self.file = open(self.log_file, 'a+')
        message='Entered the get_data_from_source method of the Data_Getter class'
        self.log.apply_log(self.file,message)
        self.file.close()

        try:
            self.data=pd.read_csv(self.training_file_location) #reading the data file

            #print(self.data.shape)

            self.file = open(self.log_file, 'a+')
            message='Data Load Successful.Exited the get_data method of the Data_Getter class'
            self.log.apply_log(self.file,message)
            self.file.close()
            #print('Sucessful extraction')
            return self.data
        except Exception as e:

            self.file = open(self.log_file, 'a+')
            self.log.apply_log(self.file,'Exception occured in get_data method of the Data_Getter class. Exception message: %s::' %e)
            self.log.apply_log(self.file,'Data Load Unsuccessful.Exited the get_data method of the Data_Getter class')
            self.file.close()
            #print('Exception not reached')
            raise Exception




