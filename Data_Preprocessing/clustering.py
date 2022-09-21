import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator
from File_Operations import file_methods_v
from Logging.Logging import logger
import csv
class KMeansClustering:
    """
            This class shall  be used to divide the data into clusters before training.

            Written By: Joydeep Ghosh
            Version: 1.0
            Revisions: None

            """

    def __init__(self):
        self.file_log=r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\General_Logging/Clustering.log'
        self.file = open(self.file_log, 'a+')
        self.log = logger()
        self.log.apply_log(self.file,'Starting of Clsuter: __init__ method of KMeansClustering class')
        self.file.close()

    def elbow_plot(self,data):
        """
                        Method Name: elbow_plot
                        Description: This method saves the plot to decide the optimum number of clusters to the file.
                        Output: A picture saved to the directory
                        On Failure: Raise Exception

                        Why this method is required?

                        Inertia measures how well a dataset was clustered by K-Means.
                        It is calculated by measuring the distance between each data point and its centroid,
                        squaring this distance, and summing these squares across one cluster.
                        A good model is one with low inertia AND a low number of clusters (K).
                        However, this is a tradeoff because as K increases, inertia decreases.
                        To find the optimal K for a dataset, we have used the Elbow method to
                        find the point where the decrease in inertia begins to slow.
                        As observed K=4 is the “elbow” of this graph.

                        Written By: Joydeep Ghosh
                        Version: 1.0
                        Revisions: None

                """
        self.file = open(self.file_log, 'a+')
        self.log.apply_log(self.file, 'Entered the elbow_plot method of the KMeansClustering class')
        wcss=[] # initializing an empty list to store the inertia points
        try:
            for i in range (1,11):
                kmeans=KMeans(n_clusters=i,init='k-means++',random_state=101) # initializing the KMeans object
                kmeans.fit(data) # fitting the data to the KMeans Algorithm
                wcss.append(kmeans.inertia_)
            plt.plot(range(1,11),wcss) # creating the graph between WCSS and the number of clusters
            plt.title('The Elbow Method')
            plt.xlabel('Number of clusters')
            plt.ylabel('WCSS')
            plt.show()
            plt.savefig(r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\Data_Preprocessing/K-Means_Elbow.PNG') # saving the elbow plot locally
            # finding the value of the optimum cluster programmatically
            self.kn = KneeLocator(range(1, 11), wcss, curve='convex', direction='decreasing')
            self.log.apply_log(self.file, 'The optimum number of clusters is: %s::'%self.kn.knee)
            self.log.apply_log(self.file, 'Exited the elbow_plot method of the KMeansClustering class')
            self.file.close()
            return self.kn.knee

        except Exception as e:
            self.file=open(self.file_log, 'a+')
            self.log.apply_log(self.file,'Exception occured in elbow_plot method of the KMeansClustering class. Exception message:%s::'%e)
            self.log.apply_log(self.file,'Finding the number of clusters failed. Exited the elbow_plot method of the KMeansClustering class')
            self.file.close()
            raise Exception()

    def create_clusters(self,data,number_of_clusters):
        """
                                Method Name: create_clusters
                                Description: Create a new dataframe consisting of the cluster information.
                                Output: A datframe with cluster column
                                On Failure: Raise Exception

                                Written By: Joydeep Ghosh
                                Version: 1.0
                                Revisions: None

                        """
        self.file = open(self.file_log, 'a+')
        self.log.apply_log(self.file, 'Entered the create_clusters method of the KMeansClustering class')
        self.data=data
        try:
            self.kmeans = KMeans(n_clusters=number_of_clusters, init='k-means++', random_state=101)
            #self.data = self.data[~self.data.isin([np.nan, np.inf, -np.inf]).any(1)]
            self.y_kmeans=self.kmeans.fit_predict(data) #  divide data into clusters

            self.file_op = file_methods_v.File_Operation()
            self.save_model = self.file_op.save_model(self.kmeans, 'KMeans') # saving the KMeans model to directory                                                                      # passing 'Model' as the functions need three parameters
            self.data['Cluster']=self.y_kmeans  # create a new column in dataset for storing the cluster information
            print('Inside Clustering.py-create_clusters', self.data['Cluster'].shape)
            #print(self.data['Cluster'])

            '''Just to check if the file is getting written correct through CSV reader'''
            #self.fileFromDb=r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\Training_File_from_DB/'
            #self.filenameToWrite=r'InputFile - Copy.csv'
            #csvFile = csv.writer(open(self.fileFromDb + self.filenameToWrite, 'w', newline=''), delimiter=',',lineterminator='\r\n', quoting=csv.QUOTE_ALL, escapechar='\\')

            self.log.apply_log(self.file, 'Succesful clusters created :: %s' %self.kn.knee)
            self.log.apply_log(self.file, 'Exited the create_clusters method of the KMeansClustering class')
            self.file.close()
            return self.data

        except Exception as e:
            self.file = open(self.file_log, 'a+')
            self.log.apply_log(self.file,'Exception occured in create_clusters method of the KMeansClustering class. Exception message:%s::' %e)
            self.log.apply_log(self.file,'Fitting the data to clusters failed. Exited the create_clusters method of the KMeansClustering class')
            self.file.close()
            raise Exception()