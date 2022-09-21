from sklearn.model_selection import train_test_split
from Logging.Logging import logger
from data_ingestion import data_loader
from Data_Preprocessing import preprocessing
from Data_Preprocessing import clustering
from File_Operations import file_methods_v
from best_model_finder import tuner
class Training_Model:

    def __init__(self):
        self.log_path=r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\General_Logging/Training_Model.log'
        self.log = logger()
        self.file=open(self.log_path, 'a+')
        message='Starting of Training Model Pre processing'
        self.log.apply_log(self.file,message)
        self.file.close()

    def Preprocessing_Training(self):


        try:

            self.file = open(self.log_path, 'a+')
            message = 'Inside Training Model: Preprocessing_Training method'
            self.log.apply_log(self.file, message)


            data_getter=data_loader.Get_Data()
            data=data_getter.get_data_from_source()

            self.file = open(self.log_path, 'a+')
            message = 'Got the data from data_loader.py file'
            self.log.apply_log(self.file, message)


            '''Starting Preprocessing of the data'''

            self.file = open(self.log_path, 'a+')
            message = 'Starting the preprocessing'
            self.log.apply_log(self.file, message)


            '''#####1 Calling get_useful_data_label_data method'''

            preprocessor_=preprocessing.Preprocessor()
            X, Y=preprocessor_.get_useful_data_label_data(data, 'Result')
            print(X.shape)
            print(Y.shape)
            self.file = open(self.log_path, 'a+')
            message = 'Successfully separated the of label column and the rest of the data'
            self.log.apply_log(self.file, message)


            '''#####2 dropping Unnecessary column'''
            #self.file = open(self.log_path, 'a+')
            #message = 'Dropping Unnecessary column'
            #data = preprocessor_.dropUnnecessaryColumns(data, ['Unnecessary_Column'])
            #self.log.apply_log(self.file, message)
            #self.file.close()

            '''#####3 Replace Invalid Values with Null'''

            self.file = open(self.log_path, 'a+')
            message = 'Replace Invalid values with Null'
            data = preprocessor_.replaceInvalidValuesWithNull(data)
            self.log.apply_log(self.file, message)


            '''#####4 Check if Null Values are present'''

            self.file = open(self.log_path, 'a+')
            message = 'is_null_present: Check if null value present'
            null_present,cols_with_missing_values = preprocessor_.is_null_present(data)
            message = 'Completed the validation of: If null value present, Check the Preprocessing.log for the details'
            self.log.apply_log(self.file, message)


            self.file = open(self.log_path, 'a+')
            if(null_present):
                data=preprocessor_.impute_missing_values(data,cols_with_missing_values)
                message = 'If only null value is present go inside impute_missing_values class'
                self.log.apply_log(self.file, message)

            else:
                message = 'No need to go inside impute_missing_values class, the data has no missing values'
                self.log.apply_log(self.file, message)


            '''#####5 Check if columns with 0 standard deviation are present'''

            self.file = open(self.log_path, 'a+')
            message = 'Check if columns with 0 standard deviation are present: get_columns_with_zero_std_deviation'
            self.log.apply_log(self.file, message)


            col_to_drop=preprocessor_.get_columns_with_zero_std_deviation(data)
            print(col_to_drop)

            self.file = open(self.log_path, 'a+')
            message = 'End of get_columns_with_zero_std_deviation'
            self.log.apply_log(self.file, message)
            message= 'End of **********Preprocessing***************'

            '''#####6 *******Clustering***********'''

            self.log.apply_log(self.file, message)
            message='Start of *********Clustering**************'
            self.log.apply_log(self.file, message)

            message='Clustering KMEANS start: Calling KMeansClustering class'
            self.log.apply_log(self.file, message)

            kmeans = clustering.KMeansClustering()

            message = 'Clustering KMEANS End-Sucessfully called KMeansClustering class'
            self.log.apply_log(self.file, message)

            number_of_clusters=kmeans.elbow_plot(X)
            message = 'Clustering: Elbow has been plotted'
            self.log.apply_log(self.file, message)

            message = 'Clustering: Creating Clusters'
            self.log.apply_log(self.file, message)
            X=kmeans.create_clusters(X,number_of_clusters)
            print('Created Cluster', X.shape)
            message = 'Clustering: Clusters created'
            self.log.apply_log(self.file, message)
            print('Calling from Training_Model.py', X.shape)

            '''#####7 *******Training Model***********'''

            # create a new column in the dataset consisting of the corresponding cluster assignments.
            X['Labels'] = Y
            print('Before Parsing',X.shape)

            # getting the unique clusters from our dataset
            print(X['Cluster'].unique())
            list_of_clusters=X['Cluster'].unique()

            """parsing all the clusters and looking for the best ML algorithm to fit on individual cluster"""
            for i in list_of_clusters:
                cluster_data = X[X['Cluster'] == i]  # filter the data for one cluster
                #Prepare the feature and Label columns
                cluster_features = cluster_data.drop(['Cluster', 'Labels'], axis=1)
                print(cluster_features.shape)
                cluster_label = cluster_data['Labels']
                print(cluster_label.shape)

                # splitting the data into training and test set for each cluster one by one

                x_train, x_test, y_train, y_test = train_test_split(cluster_features, cluster_label, test_size=1 / 3,random_state=101)
                model_finder = tuner.Model_Finder()

                # getting the best model for each of the clusters

                best_model_name, best_model = model_finder.get_best_model(x_train, y_train, x_test, y_test)

                # saving the best model to the directory.
                file_op = file_methods_v.File_Operation()
                save_model = file_op.save_model(best_model, best_model_name + str(i))

            self.log.apply_log(self.file, 'Successful End of Training')
            self.file.close()

        except Exception as e:
            self.file = open(self.log_path, 'a+')
            self.log.apply_log(self.file,str(e))
            self.file.close()







