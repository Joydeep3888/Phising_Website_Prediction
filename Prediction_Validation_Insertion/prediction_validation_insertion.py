from Logging.Logging import logger

from Prediction_Raw_Data_Validation.predictionDataValidation import Prediction_Data_validation
#the above one just validates file checks from the schema

from DataTransformation_Prediction.DataTransformationPrediction import dataTransformPredict
#the above one changes the missing values in data with Null

from DataTypeValidation_Insertion_Prediction.DataTypeValidationPrediction import dBOperation
#used for creating database files such as tables and etc from the prediction file

class pred_validation:

    def __init__(self,path):
        self.raw_data = Prediction_Data_validation(path)
        self.dataTransform = dataTransformPredict()
        self.dBOperation = dBOperation()
        self.log = logger()
        self.log_path=r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\Prediction_Logs/Prediction_Logs.log'
        self.file=open(self.log_path, 'a+')
        self.log.apply_log(self.file, '*1-starting of Prediction Validation')

    def prediction_validation(self):
        """ This method will going to call all the predictionDataValidation,DataTransformationPrediction and
        DataTypeValidationPrediction methods and will going validate the data and the missing values

        On Error Raise Exception

        Written By: Joydeep Ghosh
        Revision: 1.0

        """
        self.log.apply_log(self.file, 'Calling predictionDataValidation file method and Prediction_Data_validation Class, Inside valuesFromSchema')
        try:
            # Start of Prediction_Data_validation
            LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, NumberofColumns=self.raw_data.valuesFromSchema()

            self.log.apply_log(self.file,'Data Reading sucessful, retrieved the data from valuesFromSchema')
            self.log.apply_log(self.file, 'Values are as follows-->LengthOfDateStampInFile :' +str(LengthOfDateStampInFile)+'LengthOfTimeStampInFile :'+str(LengthOfTimeStampInFile)+'column_names :'+str(column_names)+'NumberofColumns :'+ str(NumberofColumns))

            regex=self.raw_data.manualRegexCreation()
            self.log.apply_log(self.file, 'regex value validated:' +str(regex))

            self.raw_data.createDirectoryForGoodBadRawData()
            self.log.apply_log(self.file, 'Directory for good bad raw data created')

            self.raw_data.moveBadFilesToArchiveBad()
            self.log.apply_log(self.file, 'Bad files are moved to archive path')

            self.raw_data.validationFileNameRaw()
            self.log.apply_log(self.file, 'Validation of the file names has been sucessful')

            self.raw_data.validateColumnLength(NumberofColumns)
            self.log.apply_log(self.file, 'Validated column number: '+str(NumberofColumns))

            self.log.apply_log(self.file, '***End of Prediction_Data_validation***')

            #Start of DataTransformationPrediction
            self.log.apply_log(self.file, 'Start of DataTransformationPrediction')
            self.dataTransform.addQuotesToStringValuesInColumn()
            self.log.apply_log(self.file, 'Sucessful completion of DataTransformationPrediction')
            self.log.apply_log(self.file, '***End of DataTransformationPrediction***')

            #Start of DB operation
            self.log.apply_log(self.file, 'Start of DB operation')

            self.dBOperation.createTableDb('Prediction', column_names)

            self.log.apply_log(self.file, 'Sucessfully created the Prediction DB')

            self.dBOperation.insertIntoTableGoodData('Prediction')

            self.log.apply_log(self.file, 'Sucessfully created the Table')

            self.dBOperation.insertIntoTableGoodData('Prediction')
            self.log.apply_log(self.file, 'Data inserted into Table')

            self.dBOperation.selectingDatafromtableintocsv('Prediction')
            self.log.apply_log(self.file, 'CSV exported sucessfully')

            self.raw_data.deleteExistingBadDataTrainingFolder()
            self.log.apply_log(self.file, 'Bad Data folder deleted sucessfully')
            self.raw_data.deleteExistingGoodDataTrainingFolder()
            self.log.apply_log(self.file, 'Good Data folder deleted sucessfully')
            #self.raw_data.deletePredictionFile()

        except Exception as e:
            self.log.apply_log(self.file, str(e))
            raise e
        self.file.close()