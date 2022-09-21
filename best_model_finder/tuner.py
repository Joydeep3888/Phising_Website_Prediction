from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier
from sklearn.metrics  import roc_auc_score,accuracy_score
from Logging.Logging import logger
from sklearn.naive_bayes import BernoulliNB

class Model_Finder:
    """
                This class shall  be used to find the model with best accuracy and AUC score.
                Written By: Joydeep Ghosh
                Version: 1.0
                Revisions: None

                """

    def __init__(self):
        self.log_path=r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\General_Logging/Model_Tuner.log'
        self.file_object = open(self.log_path, 'a+')
        self.log = logger()
        self.log.apply_log(self.file_object ,'Parent: Starting of Tuner.py of Model_Finder Class')
        self.sv_classifier=SVC()
        self.xgb = XGBClassifier(objective='binary:logistic',n_jobs=-1)
        self.cnvb = BernoulliNB()
        #self.file_object.close()

    def get_best_params_for_naive_byes(self, train_x, train_y):
        """
                Method Name: get_best_params_for_naive_bayes
                Description: get the parameters for the Naive Byes Algorithm which give the best accuracy.
                             Use Hyper Parameter Tuning.
                Output: The model with the best parameters
                On Failure: Raise Exception

                Written By: Joydeep Ghosh
                Version: 1.0
                Revisions: None """
        try:

            #self.file_object = open(self.log_path, 'a+')
            self.log.apply_log(self.file_object, '1: get_best_params_for_naive_byes Entered the get_best_params_for_naive_byes method of the Model_Finder class')

            self.param_grid_NV = {
                "alpha": [0.1, 0.01, 1]
                                  }
            self.grid = GridSearchCV(estimator=self.cnvb, param_grid=self.param_grid_NV, verbose=3, cv=5)

            message = '2-get_best_params_for_naive_byes: Creating an object of an Grid Search Class' + str(self.grid)
            self.log.apply_log(self.file_object, message)

            message = '3-get_best_params_for_naive_byes: Fitting Grid Object with x_train and y_train' + str(self.grid)

            self.grid.fit(train_x, train_y)
            self.log.apply_log(self.file_object, message)

            message = '4-get_best_params_for_naive_byes: Extracting the best parameters from Grid object'
            self.log.apply_log(self.file_object, message)

            self.alpha = self.grid.best_params_['alpha']

            message = '5-get_best_params_for_naive_byes: Extracting the best parameters from Grid object'
            self.log.apply_log(self.file_object, message)

            self.cnvb = BernoulliNB(alpha=self.alpha)

            message = '6-get_best_params_for_naive_byes: creating a new model with the best parameters: kernel: '+ str(self.alpha)
            self.log.apply_log(self.file_object, message)

            self.cnvb.fit(train_x, train_y)
            message = '7-get_best_params_for_naive_byes: Naive Byes best params: ' + str(self.grid.best_params_) + '. Exited the get_best_params_for_svm method of the Model_Finder class'
            self.log.apply_log(self.file_object, message)
            #self.file_object.close()
            return self.cnvb

        except Exception as e:
            #self.file_object = open(self.log_path, 'a+')
            message='Exception occured in get_best_params_for_svm method of the Model_Finder class. Exception message:  ' + str(e)
            self.log.apply_log(self.file_object,message)

            message='SVM training  failed. Exited the get_best_params_for_svm method of the Model_Finder class'
            self.log.apply_log(self.file_object,message)
            #self.file_object.close()
            raise Exception()


    def get_best_params_for_svm(self,train_x,train_y):
        """
        Method Name: get_best_params_for_naive_bayes
        Description: get the parameters for the SVM Algorithm which give the best accuracy.
                     Use Hyper Parameter Tuning.
        Output: The model with the best parameters
        On Failure: Raise Exception

        Written By: Joydeep Ghosh
        Version: 1.0
        Revisions: None

                        """

        try:
            #self.file_object = open(self.log_path, 'a+')
            self.log.apply_log(self.file_object,'1-get_best_params_for_svm: Entered the get_best_params_for_svm method of the Model_Finder class')

            # initializing with different combination of parameters

            self.param_grid_svm = {
                "C": [1, 0.1, 10, 0.5],
                "kernel": ['rbf', 'sigmoid'],
                "gamma": [0.1, 0.2, 0.5, 1],
                "random_state": [101, 32, 200, 300]
            }
            self.grid = GridSearchCV(estimator=self.sv_classifier, param_grid=self.param_grid_svm, verbose=3, cv=5)

            message='2-get_best_params_for_svm: Creating an object of an Grid Search Class'+ str(self.grid)
            self.log.apply_log(self.file_object, message)

            #finding the best parameters

            message = '3-get_best_params_for_svm: Fitting Grid Object with x_train and y_train' + str(self.grid)
            self.grid.fit(train_x, train_y)
            self.log.apply_log(self.file_object, message)

            #extracting the best parameters

            message = '4-get_best_params_for_svm: Extracting the best parameters from Grid object'
            self.log.apply_log(self.file_object, message)

            self.kernel = self.grid.best_params_['kernel']
            self.C = self.grid.best_params_['C']
            self.random_state = self.grid.best_params_['random_state']
            self.gamma=self.grid.best_params_['gamma']

            message = '5-get_best_params_for_svm: Extracting the best parameters from Grid object'
            self.log.apply_log(self.file_object, message)

            #creating a new model with the best parameters
            self.sv_classifier = SVC(kernel=self.kernel,C=self.C,random_state=self.random_state,gamma= self.gamma)
            message = '6-get_best_params_for_svm: creating a new model with the best parameters: kernel: ' +str(self.kernel)+ '--C:'+ str(self.C)+ '--random_state: '+str(self.random_state)+ '--gamma:'+str(self.gamma)
            self.log.apply_log(self.file_object, message)
            # training the mew model

            self.sv_classifier.fit(train_x, train_y)
            message='7-get_best_params_for_svm: SVM best params: '+str(self.grid.best_params_)+'. Exited the get_best_params_for_svm method of the Model_Finder class'
            self.log.apply_log(self.file_object,message)

            #self.file_object.close()

            return self.sv_classifier

        except Exception as e:
            #self.file_object = open(self.log_path, 'a+')
            message='Exception occured in get_best_params_for_svm method of the Model_Finder class. Exception message:  ' + str(e)
            self.log.apply_log(self.file_object,message)

            message='SVM training  failed. Exited the get_best_params_for_svm method of the Model_Finder class'
            self.log.apply_log(self.file_object,message)
            #self.file_object.close()
            raise Exception()

    def get_best_params_for_xgboost(self,train_x,train_y):

        """
                                        Method Name: get_best_params_for_xgboost
                                        Description: get the parameters for XGBoost Algorithm which give the best accuracy.
                                                     Use Hyper Parameter Tuning.
                                        Output: The model with the best parameters
                                        On Failure: Raise Exception

                                        Written By: Joydeep Ghosh
                                        Version: 1.0
                                        Revisions: None

                                """
        try:
            #self.file_object = open(self.log_path, 'a+')
            self.log.apply_log(self.file_object,'1: get_best_params_for_xgboost-->Entered the get_best_params_for_xgboost method of the Model_Finder class')
            # initializing with different combination of parameters
            self.param_grid_xgboost = {

                "n_estimators": [100, 130, 120, 110],
                "criterion": ['gini', 'entropy'],
                "max_depth": range(8, 10, 1)

            }
            # Creating an object of the Grid Search class
            self.grid= GridSearchCV(XGBClassifier(objective='binary:logistic'),self.param_grid_xgboost, verbose=3,cv=5)
            # finding the best parameters
            self.grid.fit(train_x, train_y)

            # extracting the best parameters
            self.criterion = self.grid.best_params_['criterion']
            self.max_depth = self.grid.best_params_['max_depth']
            self.n_estimators = self.grid.best_params_['n_estimators']

            # creating a new model with the best parameters
            self.xgb = XGBClassifier(criterion=self.criterion, max_depth=self.max_depth,n_estimators= self.n_estimators, n_jobs=-1 )
            # training the mew model
            self.xgb.fit(train_x, train_y)
            message='XGBoost best params: ' + str(self.grid.best_params_)+ '--Exited the get_best_params_for_xgboost method of the Model_Finder class'
            self.log.apply_log(self.file_object,message)
            #self.file_object.close()
            return self.xgb

        except Exception as e:
            #self.file_object = open(self.log_path, 'a+')
            self.log.apply_log(self.file_object,
                                   'Exception occured in get_best_params_for_xgboost method of the Model_Finder class. Exception message:  ' + str(
                                       e))
            self.log.apply_log(self.file_object,
                                   'XGBoost Parameter tuning  failed. Exited the get_best_params_for_xgboost method of the Model_Finder class')
            #self.file_object.close()
            raise Exception()


    def get_best_model(self,train_x,train_y,test_x,test_y):
        """
                                                Method Name: get_best_model
                                                Description: Find out the Model which has the best AUC score.
                                                Output: The best model name and the model object
                                                On Failure: Raise Exception

                                                Written By: Joydeep Ghosh
                                                Version: 1.0
                                                Revisions: None

                                        """

        # create best model for XGBoost
        try:
            #self.file_object = open(self.log_path, 'a+')
            self.log.apply_log(self.file_object, 'Entered the get_best_model method of the Model_Finder class')

            self.xgboost= self.get_best_params_for_xgboost(train_x,train_y)
            self.prediction_xgboost = self.xgboost.predict(test_x) # Predictions using the XGBoost Model

            if len(test_y.unique()) == 1: #if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                self.xgboost_score = accuracy_score(test_y, self.prediction_xgboost)
                self.log.apply_log(self.file_object, 'Accuracy for XGBoost:' + str(self.xgboost_score))  # Log AUC
            else:
                self.xgboost_score = roc_auc_score(test_y, self.prediction_xgboost) # AUC for XGBoost
                self.log.apply_log(self.file_object, 'AUC for XGBoost:' + str(self.xgboost_score)) # Log AUC

            # create best model for SVM

            self.svm=self.get_best_params_for_svm(train_x,train_y)
            self.prediction_svm=self.svm.predict(test_x) # prediction using the SVM Algorithm

            if len(test_y.unique()) == 1:#if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                self.svm_score = accuracy_score(test_y,self.prediction_svm)
                self.log.apply_log(self.file_object, 'Accuracy for SVM:' + str(self.svm_score))
            else:
                self.svm_score = roc_auc_score(test_y, self.prediction_svm) # AUC for Random Forest
                self.log.apply_log(self.file_object, 'AUC for SVM:' + str(self.svm_score))

                  #Naive Byes

            self.naive_byes = self.get_best_params_for_svm(train_x, train_y)
            self.prediction_naive_byes = self.naive_byes.predict(test_x)

            if len(test_y.unique()) == 1:#if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                self.naive_byes_score= accuracy_score(test_y,self.prediction_naive_byes)
                self.log.apply_log(self.file_object, 'Accuracy for Naive Byes:' + str(self.svm_score))
            else:
                self.naive_byes_score = roc_auc_score(test_y, self.prediction_naive_byes) # AUC for Random Forest
                self.log.apply_log(self.file_object, 'AUC for SVM:' + str(self.naive_byes_score))

            #self.file_object.close()

            #comparing the three models

            if (self.naive_byes_score < self.svm_score < self.xgboost_score):
                return 'XGBoost',self.xgboost

            elif (self.svm_score < self.naive_byes_score < self.xgboost_score):
                return 'XGBoost', self.xgboost

            elif (self.xgboost_score< self.svm_score <  self.naive_byes_score):
                return 'Naive Byes',self.naive_byes

            elif (self.svm_score< self.xgboost_score < self.naive_byes_score):
                return 'Naive Byes', self.naive_byes

            elif (self.naive_byes_score< self.xgboost_score< self.svm_score):
                return 'SVM', self.svm
            else:
                return 'SVM', self.svm

        except Exception as e:
            #self.file_object = open(self.log_path, 'a+')
            self.log.apply_log(self.file_object,'Exception occured in get_best_model method of the Model_Finder class. Exception message:  ' + str(e))
            self.log.apply_log(self.file_object,'Model Selection Failed. Exited the get_best_model method of the Model_Finder class')
            raise Exception()

        self.file_object.close()

print('Last: Sucessful Completion of Tuner.py')