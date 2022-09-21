import pandas as pd
import numpy as np
from Logging.Logging import logger
from DataTypeValidation_Insertion_Training.DataTypeValidation import dBOperation
from Training_Raw_data_validation.rawValidation import Raw_Data_Validation
from DataTransform_Training.DataTransformation import dataTransform

class train_validation:

    def __init__(self, path):

        self.raw_data=Raw_Data_Validation(path)
        self.dataTransform=dataTransform()
        self.dBOperation=dBOperation()
        self.file_=open(r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\General_Logging/train_validation_insertion.log', 'a+')
        self.log=logger()

    def train_validation(self):

        try:

            self.log.apply_log(self.file_, 'start of train_validation')

            print('starting with rawValidation')

            LengthOfDateStampInFile, LengthOfDateStampInFile, ColName, NumberofColumns=self.raw_data.Read_Values_from_Schema()
            self.log.apply_log(self.file_, 'reading values from rawValidation: Read_Values_from_Schema')

            file_1=self.raw_data.validating_file_name_format('../Training_Batch_File/')

            self.log.apply_log(self.file_, 'reading values from rawValidation: validating_file_name_format')

            ValidateColumnLength=self.raw_data.validating_file_name_format(31)

            self.log.apply_log(self.file_, 'reading values from rawValidation: validating_file_name_format')

            self.raw_data.validateMissingValuesInWholeColumn()

            self.log.apply_log(self.file_, 'reading values from rawValidation: validateMissingValuesInWholeColumn')

            self.raw_data.CreateDirectoryForGoodData()

            self.log.apply_log(self.file_, 'reading values from rawValidation: CreateDirectoryForGoodData')

            self.raw_data.CreateDirectoryForBadData()

            self.log.apply_log(self.file_, 'reading values from rawValidation: CreateDirectoryForBadData')

            self.raw_data.deleteExistingBadDataTrainingFolder()

            self.log.apply_log(self.file_, 'reading values from rawValidation: deleteExistingBadDataTrainingFolder')

            self.raw_data.moveBadFilesToArchiveBad()

            self.log.apply_log(self.file_, 'reading values from rawValidation: moveBadFilesToArchiveBad')

            print('End of rawValidation, The Raw Data Validation has been completed sucessfully')

            self.log.apply_log(self.file_, 'start of Data Transformation')

            print('starting with Data Transformation')

            self.dataTransform.addQuotesToStringValuesInColumn()

            self.log.apply_log(self.file_, 'Data Transformation has been completed sucessfully')
            print('End of Data Transformation')

            print('start of DatatypeValidation: DB Operations')

            self.log.apply_log(self.file_, 'DatatypeValidation: dBOperation: start of DB Operations')

            self.dBOperation.dataBaseConnection('Training')

            self.log.apply_log(self.file_, 'Inside DatatypeValidation: dBOperation: dataBaseConnection')

            self.dBOperation.createTableDb('Training')

            self.log.apply_log(self.file_, 'DatatypeValidation: dBOperation: Inside createTableDb')

            self.dBOperation.insertIntoTableGoodData('Training')

            self.log.apply_log(self.file_, 'DatatypeValidation: dBOperation: Inside insertIntoTableGoodData')

            self.dBOperation.selectingDatafromtableintocsv('Training')

            self.log.apply_log(self.file_, 'DatatypeValidation: dBOperation: Inside selectingDatafromtableintocsv')

            print('End of DB Operations')

        except Exception as e:
            self.log.apply_log(self.file_, 'There is some Exception happened ::%s' %e)
            self.file_.close()










