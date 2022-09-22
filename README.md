# Internship for Ineuron

Problem Statement: Develop a Machine Learning Project to detect Phishing Websites. 

# Motivation

Website Phishing impacts billions of dollars per year. Phishers and Hackers steal valuable information leaving users helpless in the internet space. 

Hence, it is important to identify such Phishing websites to stop Phishers from stealing our valuable information. 

Hence this model has been developed to predict Phishing Websites based on the features such as Address Bar-based Features, Abnormal Address Bar-based Features, HTML and JavaScript-based Features, and Domain-based Features. 

# Dataset Information

This dataset contains information the phishing websites and normal websites based on the features such as Address Bar-based Features, Abnormal Address Bar-based Features, HTML and JavaScript-based Features, and Domain-based Features. 

# Approach and Models Used: 

1. Based on the training data, i have applied K-Means Clustering Algorithm to segregate the data into 4 clusters. 

2. Once the data had been segregated into 4 clusters, I applied the Naive Byes, Support Vector Machine, & XG Boost algorithm based on each cluster group. Plus, I also did the parameter hyper-tuning for each of the algorithms to identify the best parameters. 

3. Once that was done, I compared the Accuracy of each model in individual clusters and identified which model performed the best. 

4. We saved all the best-performing models inside a directory named Models. 

5. Then, I did the same step as step 2 for our prediction data. Once the clusters were created for the prediction data, I applied the best-fitted model for each cluster in that data and predicted based on the values present inside the Prediction dataset. 

# Best performing Model and the measure of Accuracy: 

It has been identified that the best-performing model is SVM with an AUC score of 0.9990808823529411, 0.9763940371860308, 0.9868701701201905, 1, for clusters 1, 2, 3, and 4. 

SVM best params: {'C': 10, 'gamma': 0.1, 'kernel': 'rbf', 'random_state': 101}

**C** =It is a hypermeter in SVM to control error

**gamma** = Higher value of gamma will mean that radius of influence is limited to only support vectors. This would essentially mean that the model tries and overfit. The model accuracy lowers with the increasing value of gamma. The lower value of gamma will mean that the data points have very high radius of influence.

**kernel** = Kernel takes data as input and transform it into the required form.

**random_state** = The lot number of the set generated randomly in any operation. 

So, we will be using SVM for prediction. 

# Installation

The Code is written in Python 3.7. 
If you don't have Python installed, you can find it here. 
If you are using a lower version of Python, you can upgrade using the pip package, ensuring you have the latest version of pip.
To install the required packages and libraries, run this command in the project directory after cloning the repository:

pip install -r requirements.txt

# Deployment

We deployed the model using docker and the CI-CD pipeline to Heroku. 

Credits
•	The original dataset can be found here at the UCI Machine Learning Repository (https://archive.ics.uci.edu/ml/datasets/phishing+websites) . This project wouldn't have been possible without this dataset.



