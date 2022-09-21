from datetime import datetime
import os
from Logging.Logging import logger
import pandas as pd


class dataTransform:

     """
               This class shall be used for transforming the Good Raw Training Data before loading it in Database!!.

               Written By: Joydeep Ghosh
               Version: 1.0
               Revisions: None

               """

     def __init__(self):
          self.goodDataPath = "../Training_Raw_files_validated/Good_Raw"
          self.log = logger()
          self.path_log=r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\General_Logging/Data_Transformation_Training.log'


     def addQuotesToStringValuesInColumn(self):
          """
                                           Method Name: addQuotesToStringValuesInColumn
                                           Description: This method converts all the columns with string datatype such that
                                                       each value for that column is enclosed in quotes. This is done
                                                       to avoid the error while inserting string values in table as varchar.

                                        Written By: Joydeep Ghosh
                                           Version: 1.0
                                           Revisions: None

                                                   """

          file = open(self.path_log, 'a+')
          message=('Start of addQuotesToStringValuesInColumn method outside try')
          self.log.apply_log(file, message)
          file.close()
          try:
               for file in os.listdir(r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\Training_Raw_files_validated\Good_Raw'):
                    df = pd.read_csv(r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\Training_Raw_files_validated\Good_Raw/' + file)
                    for column in df:
                         if df[column][df[column] == '?'].count() == 0:
                              file=open(self.path_log, 'a+')
                              message = ('The file values are all fine %s::' %file)
                              self.log.apply_log(file, message)
                              file.close()
                              #print('Values are ok')

                         else:
                              df[column] = df[column].replace('?', "'?'")
                              #print('Replaced the quotes value to string')
                              file = open(self.path_log, 'a+')
                              message = ('The file values were not fine, the program has changed the values from quotes to string %s::' % file)
                              self.log.apply_log(file, message)
                              file.close()
          except Exception as e:
               file = open(self.path_log, 'a+')
               self.log.apply_log(file, str(e))
               file.close()
               #print(str(e))

print('Succesful completion of DataTranformation_Training: DataTransformaton.py ')