import pickle
import os
import shutil
from Logging.Logging import logger
from Data_Preprocessing import clustering
class File_Operation:
    """
                This class shall be used to save the model after training
                and load the saved model for prediction.

                Written By: Joydeep Ghosh
                Version: 1.0
                Revisions: None

                """
    def __init__(self):
        self.log_path=r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\General_Logging/File_Operation.log'
        self.file = open(self.log_path, 'a+')
        self.log = logger()
        self.model_directory=r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\models/'
        self.file.close()

    def save_model(self,model,filename):
        """
            Method Name: save_model
            Description: Save the model file to directory
            Outcome: File gets saved
            On Failure: Raise Exception

            Written By: Joydeep Ghosh
            Version: 1.0
            Revisions: None
"""
        self.file = open(self.log_path, 'a+')
        self.log.apply_log(self.file, 'Entered the save_model method of the File_Operation class')
        try:
            path = os.path.join(self.model_directory,filename) #create seperate directory for each cluster
            if os.path.isdir(path): #remove previously existing models for each clusters
                shutil.rmtree(self.model_directory)
                os.makedirs(path)
            else:
                os.makedirs(path) #
            with open(path +'/' + filename+'.sav','wb') as f:
                pickle.dump(model, f) # save the model to file
            message='Model File' + str(filename)+ 'saved. Exited the save_model method of the File_Operation class'
            self.log.apply_log(self.file,message)
            self.file.close()
            return 'success'
        except Exception as e:
            self.file = open(self.log_path, 'a+')
            self.log.apply_log(self.file,'Exception occured in save_model method of the Model_Finder class. Exception message: %s::' %e)
            message='Model File'+ str(filename)+ ' could not be saved.Exited the save_model method of the File_Operation class'
            self.log.apply_log(self.file,message)
            self.file.close()
            raise Exception()

    def load_model(self,filename):
        """
                    Method Name: load_model
                    Description: load the model file to memory
                    Output: The Model file loaded in memory
                    On Failure: Raise Exception

                    Written By: Joydeep Ghosh
                    Version: 1.0
                    Revisions: None
        """
        self.file = open(self.log_path, 'a+')
        self.log.apply_log(self.file, 'Entered the load_model method of the File_Operation class')
        try:
            with open(self.model_directory + filename + '/' + filename + '.sav','rb') as f:
                message='Model File'+ str(filename)+ ' loaded.Exited the load_model method of the File_Operation class'
                self.log.apply_log(self.file, message)
                self.file.close()
                return pickle.load(f)
        except Exception as e:
            self.file = open(self.log_path, 'a+')
            self.log.apply_log(self.file,'Exception occured in load_model method of the File_Operation class. Exception message:  %s::'%e)
            message='Model File'+ str(filename)+ 'could not be saved. Exited the load_model method of the File_Operation class'
            self.log.apply_log(self.file,message)
            self.file.close()
            raise Exception()

    def find_correct_model_file(self,cluster_number):
        """
                            Method Name: find_correct_model_file
                            Description: Select the correct model based on cluster number
                            Output: The Model file
                            On Failure: Raise Exception

                            Written By: Joydeep Ghosh
                            Version: 1.0
                            Revisions: None
                """
        self.file = open(self.log_path, 'a+')
        self.log.apply_log(self.file, 'Entered the find_correct_model_file method of the File_Operation class')
        try:
            self.cluster_number= cluster_number
            self.folder_name=self.model_directory
            self.list_of_model_files = []
            self.list_of_files = os.listdir(self.folder_name)
            for self.file_name in self.list_of_files:
                try:
                    if (self.file_name.index(str( self.cluster_number))!=-1):
                        self.model_name=self.file_name
                except:
                    continue
            self.model_name=self.model_name.split('.')[0]
            self.log.apply_log(self.file, 'Exited the find_correct_model_file method of the File_Operation class.')
            self.file.close()
            return self.model_name
        except Exception as e:
            self.file = open(self.log_path, 'a+')
            self.log.apply_log(self.file,'Exception occured in find_correct_model_file method of the File_Operation class. Exception message:%s::' %e)
            self.log.apply_log(self.file,'Exited the find_correct_model_file method of the File_Operation class with Failure')
            self.file.close()
            raise Exception()