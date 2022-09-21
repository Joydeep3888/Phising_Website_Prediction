from datetime import datetime
import os
from Logging.Logging import logger
import json
import pandas as pd
import re
import shutil

class Raw_Data_Validation:

    """This class shall be used for handling all the validation done on the Raw Training Data!!.
    Written By: Joydeep Ghosh."""
    def __init__(self, path):
        self.Batch_Directory_Path=path
        '''Directory is Training_Batch_Files directory'''
        self.schema_path='schema_training.json'
        self.log=logger()
        self.path_log = r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\General_Logging/Raw_Data_Validation.log'

    def Read_Values_from_Schema(self):

        """Method Name: valuesFromSchema
        Description: This method extracts all the relevant information from the pre-defined "Schema" file.
        Output: LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, Number of Columns
        On Failure: Raise ValueError,KeyError,Exception
        Written By: Joydeep Ghosh"""
        try:
            with open(self.schema_path, 'r+') as f:
                dic = json.load(f)
                f.close()
            file_name_pattern=dic['SampleFileName']
            LengthOfDateStampInFile=dic['LengthOfDateStampInFile']
            LengthOfTimeStampInFile=dic['LengthOfTimeStampInFile']
            ColName = dic['ColName']
            NumberofColumns = dic['NumberofColumns']
            file=open(self.path_log, 'a+')
            message='LengthOfDateStampInFile:: %s'%LengthOfDateStampInFile+ 'LengthOfDateStampInFile :: %s' %LengthOfDateStampInFile + 'LengthOfTimeStampInFile :: %s' %LengthOfTimeStampInFile + 'NumberofColumns:: %s' %NumberofColumns+'\n'
            self.log.apply_log(file,message)
            file.close()

        except ValueError as v:
            file = open(self.path_log, 'a+')
            self.log.apply_log(self.path_log, str(v))
            file.close()
            raise ValueError()
        except KeyError as s:
            file = open(self.path_log, 'a+')
            self.log.apply_log(file, str(s))
            file.close()
            raise KeyError()
        except Exception as e:
            file = open(self.path_log, 'a+')
            self.log.apply_log(file, str(e))
            file.close()
            raise Exception()
        return LengthOfDateStampInFile, LengthOfDateStampInFile, ColName, NumberofColumns

    def validating_file_name_format(self,path):
        '''This method is used to validate the file_name
        Written By: Joydeep Ghosh
        Version: 1'''

        try:
            path=r'../Training_Batch_Files'
            os.chmod(path, 0o666)
            for i in os.listdir(path):
                regex=re.compile(r"['phising']+['\_']+[\d_]+[\d]+[\.csv]")
                mo = regex.search(i)
                file = open(self.path_log, 'a+')
                message = ('math found in Training_Batch_Files File Name ::%s' %i)
                self.log.apply_log(file, message)
                file.close()
                splitatdot = re.split('.csv', i)
                #print(splitatdot)
                splitatdot_1 = re.split('_', splitatdot[0])
                #print(splitatdot_1[1], splitatdot_1[2])
                if len(splitatdot_1[1]) == 8 and len(splitatdot_1[2]) == 6:
                    #print('correct values')
                    #src=os.path.abspath(i)
                    #head, tail = os.path.split(src)
                    os.chmod('../Training_Batch_Files',mode= 0o777)
                    shutil.copy("../Training_Batch_Files/"+i ,"../Training_Raw_files_validated/Good_Raw/")
                    file = open(self.path_log, 'a+')
                    message = ('file format is correct file moved to : Training_Raw_files_validated/Good_Raw %s::' %i)
                    self.log.apply_log(file,message)
                    file.close()
                else:
                    shutil.copy("../Training_Batch_Files/"+i , '../Training_Raw_files_validated/Bad_Raw/')
                    file = open(self.path_log, 'a+')
                    message = ('file format is incorrect file moved to : Training_Raw_files_validated/Bad_Raw %s::' %i)
                    self.log.apply_log(file, message)
                    file.close()
                return (mo.group())
        except Exception as e:
            file = open(self.path_log, 'a+')
            return str(e)
            message=('There is some other error %s::' %e)
            self.log.apply_log(file, message)
            file.close()

    def ValidateColumnLength(self, NumberofColumns):
        try:
            file = open(self.path_log, 'a+')
            message = ('ValidateColumnLength method started ::%s' %file)
            self.log.apply_log(file, message)
            file.close()
            for file in os.listdir(r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\Training_Raw_files_validated\Good_Raw'):
                df=pd.read_csv(r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\Training_Raw_files_validated\Good_Raw/' + file)
                if df.shape[1]==NumberofColumns:
                    file = open(self.path_log, 'a+')
                    message = ('Colum Number verified file is in Good_Raw directory')
                    self.log.apply_log(file, message)
                    file.close()
                    pass
                else:
                    file=open(self.path_log, 'a+')
                    message=('file moved to Training_Raw_files_validated/Bad_Raw')
                    self.log.apply_log(file,message)
                    file.close()
        except OSError:
            f = open(self.path_log, 'a+')
            self.log.apply_log(f, "Error Occured while moving the file :: %s" % OSError)
            f.close()
        except Exception as e:
            file = open(self.path_log, 'a+')
            self.log.apply_log(file, str(e))
            file.close()
            raise Exception()

    def validateMissingValuesInWholeColumn(self):
        try:
            file=open(self.path_log, 'a+')
            message=('starting of validation to see if there is any missing values')
            self.log.apply_log(file, message)
            file.close()

            for file in os.listdir(r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\Training_Raw_files_validated\Good_Raw'):
                df = pd.read_csv(r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\Training_Raw_files_validated\Good_Raw/' + file)
                count=0
                for column in df:
                    #print(len(df[column]))
                    #print(df[column].count())
                    if len(df[column])-df[column].count()!=0:
                        shutil.move('../Training_Raw_files_validated/Good_Raw','../Training_Raw_files_validated/Good_Raw')
                        file = open(self.path_log, 'a+')
                        message = ('file moved to bad_raw folder %s::' %file)
                        self.log.apply_log(file, message)
                        file.close()
                        count = count + 1
                    elif len(df[column])-df[column].count()==0:
                        file = open(self.path_log, 'a+')
                        message = ('The file has no missing value it is good to be processed %s ::' %file)
                        self.log.apply_log(file, message)
                        file.close()
        except Exception as e:
            file = open(self.path_log, 'a+')
            self.log.apply_log(file, '%s::' %e)
            file.close()


    def CreateDirectoryForGoodData(self):
        '''Method Name: CreateDirectoryForGoodData
                                            Description: This method deletes the directory made  to store the Good Data
                                                          after loading the data in the table. Once the good files are
                                                          loaded in the DB,deleting the directory ensures space optimization.
                                            Output: None
                                            On Failure: OSError
                                             Written By: Joydeep Ghosh
                                            Version: 1.0
                                            Revisions: None'''
        try:
            os.chdir(r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction')
            print(os.getcwd())
            path_final_good = os.path.join("Training_Raw_files_validated/", "Good_Raw/")
            if os.path.isdir(path_final_good):
                print(path_final_good, 'path exist')
            else:
                print(path_final_good, 'does not exist and needs to be created')
                os.mkdir(path_final_good, mode=0o666)
                print(path_final_good, 'created')
        except OSError as e:
            file=open('../General_Logging/CreateDirectoryForGoodandBadData/log', 'a+')
            message='The directory %s::' %path_final_good + 'has not been created there is some issue'
            self.log.apply_log(file, str(message))
            print(str(e))
            file.close()


    def CreateDirectoryForBadData(self):
        '''Method Name: CreateDirectoryForGoodData
                                                    Description: This method deletes the directory made  to store the Bad Data
                                                                  after loading the data in the table. Once the good files are
                                                                  loaded in the DB,deleting the directory ensures space optimization.
                                                    Output: None
                                                    On Failure: OSError
                                                     Written By: Joydeep Ghosh
                                                    Version: 1.0
                                                    Revisions: None'''
        try:
            os.chdir(r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction')
            print(os.getcwd())
            path_final_bad = os.path.join("Training_Raw_files_validated/", "Bad_Raw/")
            if os.path.isdir(path_final_bad):
                print(path_final_bad, 'path exist')
            else:
                print(path_final_bad, 'does not exist and needs to be created')
                os.mkdir(path_final_bad, mode=0o666)
                print(path_final_bad, 'created')

        except OSError as e:
            file=open('../General_Logging/CreateDirectoryForGoodandBadData.log', 'a+')
            message='The directory %s::' %path_final_bad + 'has not been created there is some issue'
            self.log.apply_log(file, str(message))
            print(str(e))
            file.close()

    def deleteExistingBadDataTrainingFolder(self):
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
            path='../Training_Raw_files_validated/'
            if os.path.isdir(path+'Good_Raw')==True:
                shutil.rmtree(path+'Good_Raw')
                file = open('../General_Logging/deleteExistingBadDataTrainingFolder.log', 'a+')
                message = 'directory :: %s' %path+'Good_Raw' +' '+ 'has been deleted'
                print('directory :: %s' % path + 'Good_Raw' + ' ' + 'has been deleted')
                self.log.apply_log(file, message)
                file.close()
            elif os.path.isdir(path+'Bad_Raw')==True:
                shutil.rmtree(path + 'Bad_Raw')
                file = open('../General_Logging/deleteExistingBadDataTrainingFolder.log', 'a+')
                message = 'directory :: %s' % path + 'Bad_Raw' + ' ' + 'has been deleted'
                print('directory :: %s' % path + 'Bad_Raw' + ' ' + 'has been deleted')
                self.log.apply_log(file, message)
                file.close()
        except OSError as OS:
            file=open('../General_Logging/deleteExistingBadDataTrainingFolder.log', 'a+')
            self.log.apply_log(file,str(OS))
            file.close()
            raise OSError()

    def moveBadFilesToArchiveBad(self):
        date_now = datetime.now()
        Date = date_now.date()
        time = date_now.strftime("%H%M%S")
        try:
            source_path = '..Training_Raw_files_validated/Bad_Raw'
            if os.path.isdir(source_path) == True:
                path = 'TrainingArchiveBadData'
                if os.path.isdir(path) != True:
                    os.makedirs(path)
                destination_path = path + '/BadData_' + str(Date) + '_' + str(time)
                if not os.path.isdir(destination_path):
                    os.makedirs(destination_path)
                for files in os.listdir(source_path):
                    if files not in os.listdir(destination_path):
                        shutil.move(source_path + files, destination_path)
                file = open("Training_Logs/moveBadFilesToArchiveBad.log", 'a+')
                self.log.apply_log(file, "Bad files moved to archive")
                path = 'Training_Raw_files_validated/'
                if os.path.isdir(path + 'Bad_Raw'):
                    shutil.rmtree(path + 'Bad_Raw')
                self.log.apply_log(file, "Bad Raw Data Folder Deleted successfully!!")
                file.close()
        except Exception as e:
            file = open("Training_Logs/moveBadFilesToArchiveBad.log", 'a+')
            self.log.apply_log(file, "Error while moving bad files to archive:: %s" % str(e))
            file.close()



print('Succesful completion of rawValidation.py')
