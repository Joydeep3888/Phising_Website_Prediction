import os

import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
#from sklearn_pandas import CategoricalImputer
from sklearn.impute import SimpleImputer
from Logging.Logging import logger

class Preprocessor:
    def __init__(self):
        self.log = logger()
        self.log_path=r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\General_Logging/Preprocessing.log'
        self.file=open(self.log_path, 'a+')
        message='starting with preprocessing'
        self.log.apply_log(self.file, message)
        self.file.close()

    def get_useful_data_label_data(self,data, columns):
        """
                Method Name: remove_columns
                Description: This method removes the given columns from a pandas dataframe.
                Output: A pandas DataFrame after removing the specified columns.
                On Failure: Raise Exception

                Written By: Joydeep Ghosh
                Version: 1.0
                Revisions: None

        """
        try:
            self.data=data
            self.columns=columns
            print(self.columns)
            self.X=self.data.drop(self.columns, axis=1)
            self.Y=self.data[self.columns]
            # drop the labels specified in the columns
            self.file=open(self.log_path, 'a+')
            self.log.apply_log(self.file,'Successful separated target column and the actual data.Exited the get_useful_data_label_data method of the Preprocessor class %s::' %self.Y %self.X)
            self.file.close()
            return self.X, self.Y
        except Exception as e:
            self.file=open(self.log_path, 'a+')
            self.log.apply_log(self.file,'Exception occured in get_useful_data_label_data method of the Preprocessor class. Exception message:  ::%s' %e)
            self.log.apply_log(self.file,'Column removal Unsuccessful. Exited the get_useful_data_label_data method of the Preprocessor class')
            self.file.close()
        raise Exception()

    def dropUnnecessaryColumns(self,data,columnNameList):
        """
                        Method Name: is_null_present
                        Description: This method drops the unwanted columns as discussed in EDA section.

                        Written By: Joydeep Ghosh
                        Version: 1.0
                        Revisions: None

                                """
        data = data.drop(columnNameList,axis=1)
        self.file = open(self.log_path, 'a+')
        self.log.apply_log(self.file, 'Dropped Unncessary columns')
        self.file.close()
        return data


    def replaceInvalidValuesWithNull(self,data):

        """
                               Method Name: is_null_present
                               Description: This method replaces invalid values i.e. '?' with null, as discussed in EDA.

                               Written By: Joydeep Ghosh
                               Version: 1.0
                               Revisions: None

                                       """

        for column in data.columns:
            count = data[column][data[column] == '?'].count()
            if count != 0:
                self.file = open(self.log_path, 'a+')
                self.log.apply_log(self.file, 'There are null values')
                data[column] = data[column].replace('?', np.nan)
                self.log.apply_log(self.file, 'Null Values replaced')
                self.file.close()

        return data


    def is_null_present(self,data):
        """
                                Method Name: is_null_present
                                Description: This method checks whether there are null values present in the pandas Dataframe or not.
                                Output: Returns True if null values are present in the DataFrame, False if they are not present and
                                        returns the list of columns for which null values are present.
                                On Failure: Raise Exception

                                Written By: Joydeep Ghosh
                                Version: 1.0
                                Revisions: None

                        """
        self.file = open(self.log_path, 'a+')
        self.log.apply_log(self.file, 'Entered the is_null_present method of the Preprocessor class')
        self.file.close()
        self.null_present = False
        self.cols_with_missing_values=[]
#        self.cols = data.columns
        self.data=data
        try:

            self.null_counts=self.data.isna().sum() # check for the count of null values per column

            for i in range(len(self.null_counts)):
                if self.null_counts[i]>0:
                    self.null_present=True
                    self.cols_with_missing_values.append(self.cols[i])

            if(self.null_present==True): # write the logs to see which columns have null values
                self.dataframe_with_null = pd.DataFrame()
                self.dataframe_with_null['columns'] = self.data.columns
                self.dataframe_with_null['missing values count'] = np.asarray(self.data.isna().sum())
                self.dataframe_with_null.to_csv('../Data_Preprocessing/null_values.csv') # storing the null column information to file

            self.file = open(self.log_path, 'a+')
            self.log.apply_log(self.file,'Finding missing values is a success.Data written to the null values file. Exited the is_null_present method of the Preprocessor class')
            self.file.close()
            return self.null_present, self.cols_with_missing_values
        except Exception as e:
            self.file = open(self.log_path, 'a+')
            self.log.apply_log(self.file,'Exception occured in is_null_present method of the Preprocessor class. Exception message: %s::' %e)
            self.log.apply_log(self.file,'Finding missing values failed. Exited the is_null_present method of the Preprocessor class')
            self.file.close()
            raise Exception()

    '''def encodeCategoricalValues(self,data):
     """
                                        Method Name: encodeCategoricalValues
                                        Description: This method encodes all the categorical values in the training set.
                                        Output: A Dataframe which has all the categorical values encoded.
                                        On Failure: Raise Exception

                                        Written By: Joydeep Ghosh
                                        Version: 1.0
                                        Revisions: None
                     """
     data["class"] = data["class"].map({'p': 1, 'e': 2})

     for column in data.drop(['class'],axis=1).columns:
            data = pd.get_dummies(data, columns=[column])

     return data'''


    '''def encodeCategoricalValuesPrediction(self,data):
        """
                                               Method Name: encodeCategoricalValuesPrediction
                                               Description: This method encodes all the categorical values in the prediction set.
                                               Output: A Dataframe which has all the categorical values encoded.
                                               On Failure: Raise Exception

                                               Written By: Joydeep Ghosh
                                               Version: 1.0
                                               Revisions: None
                            """

        for column in data.columns:
            data = pd.get_dummies(data, columns=[column])

        return data'''

    '''def handleImbalanceDataset(self,X,Y):
       """
                                                     Method Name: handleImbalanceDataset
                                                      Description: This method handles the imbalance in the dataset by oversampling.
                                                     Output: A Dataframe which is balanced now.
                                                      On Failure: Raise Exception

                                                     Written By: Joydeep Ghosh
                                                       Version: 1.0
                                                      Revisions: None
                                   """
    
    
    
          rdsmple = RandomOverSampler()
          x_sampled, y_sampled = rdsmple.fit_sample(X, Y)
          return x_sampled,y_sampled '''

    def impute_missing_values(self, data, cols_with_missing_values):
        """
                                        Method Name: impute_missing_values
                                        Description: This method replaces all the missing values in the Dataframe using KNN Imputer.
                                        Output: A Dataframe which has all the missing values imputed.
                                        On Failure: Raise Exception

                                        Written By: Joydeep Ghosh
                                        Version: 1.0
                                        Revisions: None
                     """
        self.file = open(self.log_path, 'a+')
        self.log.apply_log(self.file, 'Entered the impute_missing_values method of the Preprocessor class')
        self.file.close()
        self.data= data
        self.cols_with_missing_values=cols_with_missing_values
        try:
            self.imputer = SimpleImputer()
            for col in self.cols_with_missing_values:
                self.data[col] = self.imputer.fit_transform(self.data[col])
            self.file = open(self.log_path, 'a+')
            self.log.apply_log(self.file, 'Imputing missing values Successful. Exited the impute_missing_values method of the Preprocessor class')
            self.file.close()
            return self.data
        except Exception as e:
            self.file = open(self.log_path, 'a+')
            self.log.apply_log(self.file,'Exception occured in impute_missing_values method of the Preprocessor class. Exception message:  ' + str(e))
            self.log.apply_log(self.file,'Imputing missing values failed. Exited the impute_missing_values method of the Preprocessor class')
            self.file.close()
            raise Exception()

    def get_columns_with_zero_std_deviation(self,data):
        """
                                                Method Name: get_columns_with_zero_std_deviation
                                                Description: This method finds out the columns which have a standard deviation of zero.
                                                STD=0 means columns which are having all the same values.
                                                Output: List of the columns with standard deviation of zero
                                                On Failure: Raise Exception

                                                Written By: Joydeep Ghosh
                                                Version: 1.0
                                                Revisions: None
                             """
        self.file = open(self.log_path, 'a+')
        self.log.apply_log(self.file, 'Entered the get_columns_with_zero_std_deviation method of the Preprocessor class')
        self.file.close()
        self.columns=data.columns
        self.data_n = data.describe()
        self.col_to_drop=[]
        try:
            for x in self.columns:
                if (self.data_n[x]['std'] == 0): # check if standard deviation is zero
                    self.col_to_drop.append(x)  # prepare the list of columns with standard deviation zero
            self.file = open(self.log_path, 'a+')
            self.log.apply_log(self.file, 'Column search for Standard Deviation of Zero Successful. Exited the get_columns_with_zero_std_deviation method of the Preprocessor class')
            self.file.close()
            return self.col_to_drop
        except Exception as e:
            self.file = open(self.log_path, 'a+')
            self.log.apply_log()(self.file,'Exception occured in get_columns_with_zero_std_deviation method of the Preprocessor class. Exception message: %s::'%e)
            self.logger_object.log(self.file, 'Column search for Standard Deviation of Zero Failed. Exited the get_columns_with_zero_std_deviation method of the Preprocessor class')
            self.file.close()
            raise Exception()

print('succesful completion of preprocessing.py')