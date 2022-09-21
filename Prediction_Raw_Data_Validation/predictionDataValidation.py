import sqlite3
from datetime import datetime
from os import listdir
import os
import re
import json
import shutil
import pandas as pd
from Logging.Logging import logger

class Prediction_Data_validation:
    """
               This class shall be used for handling all the validation done on the Raw Prediction Data!!.

               Written By: Joydeep Ghosh
               Version: 1.0
               Revisions: None

               """
    def __init__(self,path):
        self.Batch_Directory = path
        self.schema_path = r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction/schema_prediction.json'
        self.logger = logger()
        self.log_path= r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\Prediction_Logs/Prediction_Logs.log'
        self.file=open(self.log_path, 'a+')
        self.logger.apply_log(self.file,'Starting of Prediction_Data_validation')
        self.file.close()
    def valuesFromSchema(self):
        self.file = open(self.log_path, 'a+')
        """
                                Method Name: valuesFromSchema
                                Description: This method will extract the relevant information from the pre-defined "Schema" file.
                                Output: LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, Number of Columns
                                On Failure: Raise ValueError,KeyError,Exception

                                 Written By: Joydeep Ghosh
                                Version: 1.0
                                Revisions: None

                                        """
        try:

            with open(self.schema_path, 'r') as f:
                dic = json.load(f)
                f.close()
            pattern = dic['SampleFileName']
            LengthOfDateStampInFile = dic['LengthOfDateStampInFile']
            LengthOfTimeStampInFile = dic['LengthOfTimeStampInFile']
            column_names = dic['ColName']
            NumberofColumns = dic['NumberofColumns']

            message ="LengthOfDateStampInFile:: %s" %LengthOfDateStampInFile + "\t" + "LengthOfTimeStampInFile:: %s" % LengthOfTimeStampInFile +"\t " + "NumberofColumns:: %s" % NumberofColumns + "\n"
            self.logger.apply_log(self.file,message)

        except ValueError:
            self.logger.log(self.file,"ValueError:Value not found inside schema_training.json")
            raise ValueError

        except KeyError:
            self.logger.apply_log(self.file, "KeyError:Key value error incorrect key passed")
            raise KeyError

        except Exception as e:
            self.logger.apply_log(self.file, str(e))
            raise e

        return LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, NumberofColumns

        self.file.close()

    def manualRegexCreation(self):
        self.file = open(self.log_path, 'a+')

        """
                                      Method Name: manualRegexCreation
                                      Description: This method contains a manually defined regex based on the "FileName" given in "Schema" file.
                                                  This Regex is used to validate the filename of the prediction data.
                                      Output: Regex pattern
                                      On Failure: None

                                       Written By: Joydeep Ghosh
                                      Version: 1.0
                                      Revisions: None

                                              """
        regex = "['phising']+['\_'']+[\d_]+[\d]+\.csv"
        return regex

        self.file.close()

    def createDirectoryForGoodBadRawData(self):
        self.file = open(self.log_path, 'a+')

        """
                                        Method Name: createDirectoryForGoodBadRawData
                                        Description: This method creates directories to store the Good Data and Bad Data
                                                      after validating the prediction data.

                                        Output: None
                                        On Failure: OSError

                                         Written By: Joydeep Ghosh
                                        Version: 1.0
                                        Revisions: None

                                                """
        try:
            path = os.path.join(r"C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\Prediction_Raw_Files_Validated/", "Good_Raw/")
            if os.path.isdir(path)!=True:
                os.makedirs(path)
            path = os.path.join(r"C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\Prediction_Raw_Files_Validated/", "Bad_Raw/")
            if os.path.isdir(path)!=True:
                os.makedirs(path)

        except OSError as e:
            self.logger.apply_log(self.file,"Error while creating Directory %s:" %e)
            raise OSError
        self.file.close()

    def deleteExistingGoodDataTrainingFolder(self):
        self.file = open(self.log_path, 'a+')
        """
                                            Method Name: deleteExistingGoodDataTrainingFolder
                                            Description: This method deletes the directory made to store the Good Data
                                                          after loading the data in the table. Once the good files are
                                                          loaded in the DB,deleting the directory ensures space optimization.
                                            Output: None
                                            On Failure: OSError

                                             Written By: Joydeep Ghosh
                                            Version: 1.0
                                            Revisions: None

                                                    """
        try:
            path = r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\Prediction_Raw_Files_Validated/'

            if os.path.isdir(path + 'Good_Raw/')==True:
                shutil.rmtree(path + 'Good_Raw/')
                self.logger.apply_log(self.file,"GoodRaw directory deleted successfully, check log file for details")
        except OSError as s:
            self.logger.apply_log(self.file,"Error while Deleting Directory : %s" %s)
            raise OSError
        self.file.close()

    def deleteExistingBadDataTrainingFolder(self):
        self.file = open(self.log_path, 'a+')

        """
                                            Method Name: deleteExistingBadDataTrainingFolder
                                            Description: This method deletes the directory made to store the bad Data.
                                            Output: None
                                            On Failure: OSError

                                             Written By: Joydeep Ghosh
                                            Version: 1.0
                                            Revisions: None

                                                    """

        try:
            path = r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\Prediction_Raw_Files_Validated/'

            if os.path.isdir(path + 'Bad_Raw/')==True:
                shutil.rmtree(path + 'Bad_Raw/')
                self.logger.apply_log(self.file,"BadRaw directory deleted before starting validation, check log file for details")

        except OSError as ose:
            self.logger.apply_log(self.file,"Error while Deleting Directory : %s" %ose)
            raise OSError
        self.file.close()

    def moveBadFilesToArchiveBad(self):
        self.file = open(self.log_path, 'a+')


        """
                                            Method Name: moveBadFilesToArchiveBad
                                            Description: This method deletes the directory made  to store the Bad Data
                                                          after moving the data in an archive folder. We archive the bad
                                                          files to send them back to the client for invalid data issue.
                                            Output: None
                                            On Failure: OSError

                                             Written By: Joydeep Ghosh
                                            Version: 1.0
                                            Revisions: None

                                                    """
        now = datetime.now()
        date = now.date()
        time = now.strftime("%H%M%S")
        try:
            path= r"C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\PredictionArchivedBadData"
            if os.path.isdir(path)!=True:
                os.makedirs(path)
            source = r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\Prediction_Raw_Files_Validated/Bad_Raw/'
            dest = path+'/BadData_' + str(date)+"_"+str(time)
            if not os.path.isdir(dest):
                os.makedirs(dest)
            files= os.listdir(source)
            for f in files:
                if f not in os.listdir(dest):
                    shutil.move(source + f, dest)
            self.logger.apply_log(self.file,"Bad files moved to archive folder")
            path = r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\Prediction_Raw_Files_Validated/'
            if os.path.isdir(path + 'Bad_Raw/')==True:
                shutil.rmtree(path + 'Bad_Raw/')
            self.logger.apply_log(self.file,"Bad Raw Data Folder Deleted successfully, check log file for details")
        except OSError as e:
            self.logger.apply_log(self.file, "Error while moving bad files to archive:: %s" % e)
            raise OSError
        self.file.close()




    def validationFileNameRaw(self):
        self.file = open(self.log_path, 'a+')
        """
            Method Name: validationFileNameRaw
            Description: This function validates the name of the prediction csv file as per given name in the schema!
                         Regex pattern is used to do the validation.If name format do not match the file is moved
                         to Bad Raw Data folder else in Good raw data.
            Output: None
            On Failure: Exception

             Written By: Joydeep Ghosh
            Version: 1.0
            Revisions: None

        """
        # delete the directories for good and bad data in case last run was unsuccessful and folders were not deleted.
        self.deleteExistingBadDataTrainingFolder()
        self.deleteExistingGoodDataTrainingFolder()
        self.createDirectoryForGoodBadRawData()
        self.regex=self.manualRegexCreation()
        onlyfiles = [f for f in listdir(self.Batch_Directory)]
        try:
            self.file = open(self.log_path, 'a+')
            for filename in onlyfiles:
                if (re.match(self.regex, filename)):
                    splitAtDot = re.split('.csv', filename)
                    splitAtDot = (re.split('_', splitAtDot[0]))
                    if len(splitAtDot[1]) == 8:
                        if len(splitAtDot[2]) == 6:
                            shutil.copy("../Prediction_Batch_files/" + filename, "../Prediction_Raw_Files_Validated/Good_Raw")
                            self.logger.apply_log(self.file,"Valid File name!! File moved to GoodRaw Folder :: %s" % filename)

                        else:
                            shutil.copy("../Prediction_Batch_files/" + filename, "../Prediction_Raw_Files_Validated/Bad_Raw")
                            self.logger.apply_log(self.file,"Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
                    else:
                        shutil.copy("../Prediction_Batch_files/" + filename, "../Prediction_Raw_Files_Validated/Bad_Raw")
                        self.logger.apply_log(self.file,"Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
                else:
                    shutil.copy("../Prediction_Batch_files/" + filename, "../Prediction_Raw_Files_Validated/Bad_Raw")
                    self.logger.apply_log(self.file, "Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)

        except Exception as e:
            self.logger.apply_log(self.file, "Error occured while validating FileName %s" % e)
            self.file.close()
            raise e



    def validateColumnLength(self,NumberofColumns):
        """
                    Method Name: validateColumnLength
                    Description: This function validates the number of columns in the csv files.
                                 It is should be same as given in the schema file.
                                 If not same file is not suitable for processing and thus is moved to Bad Raw Data folder.
                                 If the column number matches, file is kept in Good Raw Data for processing.
                                The csv file is missing the first column name, this function changes the missing name to "Wafer".
                    Output: None
                    On Failure: Exception

                     Written By: Joydeep Ghosh
                    Version: 1.0
                    Revisions: None

             """
        try:
            self.file = open(self.log_path, 'a+')
            self.logger.apply_log(self.file,"Column Length Validation Started!!")
            for file in listdir('../Prediction_Raw_Files_Validated/Good_Raw/'):
                csv = pd.read_csv("../Prediction_Raw_Files_Validated/Good_Raw/" + file)
                if csv.shape[1] == NumberofColumns:
                    print('column validated sucessfully!!!')
                    self.logger.apply_log(self.file,'column validated sucessfully!!!, The column length is: '+ str(csv.shape[1]))

                    csv.to_csv("../Prediction_Raw_Files_Validated/Good_Raw/" + file, index=None, header=True)
                else:
                    shutil.move("../Prediction_Raw_Files_Validated/Good_Raw/" + file, "../Prediction_Raw_Files_Validated/Bad_Raw")
                    self.logger.apply_log(self.file, "Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file)

            self.logger.apply_log(self.file, "Column Length Validation Completed!!")
        except OSError:
            self.logger.apply_log(self.file, "Error Occured while moving the file :: %s" % OSError)
            raise OSError
        except Exception as e:
            self.logger.apply_log(self.file, "Error Occured:: %s" % e)
            self.file.close()
            raise e


    def deletePredictionFile(self):
        self.file = open(self.log_path, 'a+')

        path=r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\Prediction_Output_File/Predictions.csv'
        if os.path.exists(path)==True:
            os.remove(path)
        self.file.close()

    def validateMissingValuesInWholeColumn(self):

        """
                                  Method Name: validateMissingValuesInWholeColumn
                                  Description: This function validates if any column in the csv file has all values missing.
                                               If all the values are missing, the file is not suitable for processing.
                                               SUch files are moved to bad raw data.
                                  Output: None
                                  On Failure: Exception

                                   Written By: Joydeep Ghosh
                                  Version: 1.0
                                  Revisions: None

                              """
        try:
            self.file = open(self.log_path, 'a+')
            self.logger.apply_log(self.file, "Missing Values Validation Started!!")
            path=r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\Prediction_Raw_Files_Validated/'
            for file in listdir(path+'Good_Raw/'):
                csv = pd.read_csv(path+'Good_Raw/' + file)
                count = 0
                for columns in csv:
                    if (len(csv[columns]) - csv[columns].count()) == len(csv[columns]):
                        count+=1
                        shutil.move("../Prediction_Raw_Files_Validated/Good_Raw/" + file,
                                    "../Prediction_Raw_Files_Validated/Bad_Raw")
                        self.logger.apply_log(self.file,"Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file)
                        break
                    else:
                        print('The file abosolutely fine, no issues')
                        self.logger.apply_log(self.file, 'The File is fine there is no missing column')
                if count==0:
                    csv.rename(columns={"Unnamed: 0": "Wafer"}, inplace=True)
                    csv.to_csv("../Prediction_Raw_Files_Validated/Good_Raw/" + file, index=None, header=True)
        except OSError:
            self.logger.apply_log(self.file, "Error Occured while moving the file :: %s" % OSError)
            raise OSError
        except Exception as e:
            self.logger.apply_log(self.file, "Error Occured:: %s" % e)
            self.file.close()
            raise e














