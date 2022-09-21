from datetime import datetime
import os
from Logging.Logging import logger
import pandas as pd


class dataTransformPredict:

     """
                  This class shall be used for transforming the Good Raw Training Data before loading it in Database!!.

                  Written By: Joydeep Ghosh
                  Version: 1.0
                  Revisions: None

                  """

     def __init__(self):
          self.goodDataPath = r"C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\Prediction_Raw_Files_Validated/Good_Raw"
          self.log = logger()
          self.log_path=r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\Prediction_Logs/Prediction_Logs.log'
          self.file=open(self.log_path, 'a+')
          self.log.apply_log(self.file,'Starting of Data Transformation Predict')
          self.file.close()

     def addQuotesToStringValuesInColumn(self):
          self.file = open(self.log_path, 'a+')
          """
                                  Method Name: addQuotesToStringValuesInColumn
                                  Description: This method replaces the missing values in columns with "NULL" to
                                               store in the table. We are using substring in the first column to
                                               keep only "Integer" data for ease up the loading.
                                               This column is anyways going to be removed during prediction.

                                   Written By: Joydeep Ghosh
                                  Version: 1.0
                                  Revisions: None

                                          """
          try:

               for file in os.listdir(self.goodDataPath):
                    df = pd.read_csv(self.goodDataPath + "/" + file)
                    c = 0
                    for column in df:
                         c = c + 1
                         if df[column][df[column] == '?'].count() == 0:
                              message = 'processing for:'+ str(c)+ str(column) +':The file values are all fine'+ str(file)
                              self.log.apply_log(self.file, message)
                              print(str(c)+':'+ str(df.shape) +' processing : '+ str(column)+ ' Values are ok ')

                         else:
                              df[column] = df[column].replace('?', "'?'")
                              print('Replaced the quotes value to string')
                              message = 'The file values were not fine, the program has changed the values from quotes to string %s::' %file
                              self.log.apply_log(self.file, message)
          except Exception as e:
               self.log.apply_log(self.file, str(e))
          self.file.close()

     print('Succesful completion of DataTranformation_Prediction: DataTransformatonPrediction.py ')