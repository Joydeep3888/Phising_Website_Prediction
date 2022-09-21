import pandas
import pandas as pd

from File_Operations import file_methods_v
from Data_Preprocessing.preprocessing import Preprocessor
from data_ingestion import data_loader_prediction
from Prediction_Raw_Data_Validation.predictionDataValidation import Prediction_Data_validation
from Logging.Logging import logger


class Prediction:

    def __init__(self):
        self.log_path=r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\Prediction_Logs\Prediction_Logs.log'
        self.file=open(self.log_path, 'a+')
        self.log=logger()
        self.log.apply_log(self.file,'Starting of Prediction Class')
        self.prediction_data_validation=Prediction_Data_validation(r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\Prediction_Batch_files')

    def prediction(self):

        """This method will going to do preprocessing and clustering of the file
        On Exception: Raise Error
        Written By: Joydeep Ghosh
        Revisions=1.0
        """

        try:
            self.log.apply_log(self.file, 'Starting of Data Preprocessing for Prediction')
            self.prediction_data_validation.deletePredictionFile()
            self.log.apply_log(self.file, 'The existing prediction file has been deleted')

            #Data loading

            data_getter = data_loader_prediction.Data_Getter_Pred()
            data=data_getter.get_data()
            self.log.apply_log(self.file, 'File loaded sucessfully in data veriable')

            preprocessor=Preprocessor()
            null_present,cols_with_missing_values= preprocessor.is_null_present(data)
            self.log.apply_log(self.file, 'Preprocessing: Missing Values Null Present='+str(null_present)+'Columns with missing values:'+str(cols_with_missing_values))
            if null_present==True:
                data=preprocessor.impute_missing_values(data,cols_with_missing_values)
                self.log.apply_log(self.file, 'Please find the data returned after replacing null values: '+ str(data.shape))

            file_loader = file_methods_v.File_Operation()
            KMeans= file_loader.load_model('KMeans')

            cluster=KMeans.predict(data)
            data['cluster']=cluster
            self.log.apply_log(self.file, 'Cluster created:'+str(data['cluster'].unique())+'Shape of the data file is: '+ str(data.shape))

            clusters = data['cluster'].unique()
            result = []

            for c in clusters:
                cluster_data=data[data['cluster']==c]
                cluster_data=cluster_data.drop(['cluster'], axis=1)
                model_name=file_loader.find_correct_model_file(c)
                model=file_loader.load_model(model_name)
                predictions=model.predict(cluster_data)
                print(predictions)
                for i in predictions:
                    result.append(i)
            result = pandas.DataFrame(result, columns=['Predictions'])
            print(result)
            data=pd.DataFrame(data)
            data['Predictions']=result
            path = "../Prediction_Output_File/Predictions.csv"
            data.to_csv(path, header=True)
            self.log.apply_log(self.file, 'prediction file generated and stored in:: '+str(path))
            return path
        except Exception as e:
            self.log.apply_log(self.file, str(e))
            raise e
        self.file.close()

