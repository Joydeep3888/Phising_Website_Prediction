import pandas as pd
import matplotlib.pyplot as plt
#%matplotlib inline
import seaborn as sns
from scipy.io import arff
from Logging.Logging import logger


df = arff.loadarff(r"C:\Users\hp\OneDrive\Desktop\ineuron\Phising Website Prediction\Dataset\Training_Dataset.arff")
phishing = pd.DataFrame(df[0])
phishing1 = pd.DataFrame(df[1])
phishing=phishing.astype(int)

class DecodingFeaturesfromARFF:

    def __init__(self):
        self.phishing = phishing

    def DecodingFeaturesfromARFF(self):
        for feature in phishing.columns:
            phishing[feature] = phishing[feature].str.decode('utf-8')
        return phishing
class subplot:
    def __init__(self):
        self.log = logger()

    def plottingcountplot(self):
        plt.figure(figsize=(15, 60))
        plotnumber = 1
        for i in phishing.drop(columns='Result', axis=1).columns:
            ax = plt.subplot(15, 5, plotnumber)
            self.log.apply_log(file_name='../EDA_Logging.log', msg='Inside plottingcountplot method and countplot created')
            sns.countplot(data=phishing, x=phishing[i])
            plt.xlabel(i)
            plotnumber = plotnumber + 1
        plt.show()

    def violenplot(self):
        plt.figure(figsize=(15, 60))
        plot_number = 1
        for i in phishing.drop(columns='Result', axis=1).columns:
            ax = plt.subplot(12, 3, plot_number)
            self.log.apply_log(file_name='../EDA_Logging.log', msg='Inside Vilolenplot method')
            sns.violinplot(data=phishing, x=phishing[i], y=phishing['Result'], scale='area')
            plt.xlabel(i)
            plot_number = plot_number + 1
        #plt.show()

    def boxplot(self):
        plt.figure(figsize=(15, 60))
        plot_number = 1
        for i in phishing.drop(columns='Result', axis=1).columns:
            ax = plt.subplot(12, 3, plot_number)
            self.log.apply_log(file_name='../EDA_Logging.log', msg='Inside boxplot method')
            sns.boxplot(data=phishing, x=phishing[i])
            plt.xlabel(i)
            plot_number = plot_number + 1
        plt.show()

print('sucessful completion')