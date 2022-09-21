from wsgiref import simple_server
from wsgiref.simple_server import make_server
from flask import Flask, request, render_template
#importing flask module
from flask import Response
import os
from flask_cors import CORS, cross_origin
from Prediction_Validation_Insertion import prediction_validation_insertion
from Training_Model import Training_Model
from Training_Raw_data_validation import rawValidation
import flask_monitoringdashboard as dashboard
from Predict_from_Model import predict_from_model
from Prediction_Raw_Data_Validation import predictionDataValidation
from training_validation_insertion import train_validation

app = Flask(__name__)
#object of the flask
@app.route("/", methods =['GET'])
@cross_origin()
def home_page():
    return render_template('index.html')

@app.route("/predict/json", methods =['POST', 'GET'])
@cross_origin()

def predict_the_result_from_json():

    try:
        if request.json is not None:
            path=request.json['filepath']
            os.chdir(path)
            pred_val=prediction_validation_insertion.pred_validation(path)
            pred_val.prediction_validation()
            prediction_object=predict_from_model.Prediction()
            path=prediction_object.prediction()
            return Response('The Prediction files has been genrated, and moved to %s::' %path)
    except ValueError:
        return Response("Error Occurred! %s" % ValueError)

    except KeyError:
        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:
        return Response('There is some exception %s::' %e)

@app.route("/predict", methods=['POST', 'GET'])
@cross_origin()

def predict_from_html():
    try:
        if request.form is not None:
                path = request.form['path']
                os.chdir(path)
                print(path)
                pred_val = prediction_validation_insertion.pred_validation(path)
                pred_val.prediction_validation()
                prediction_object = predict_from_model.Prediction()
                path_final = prediction_object.prediction()
                return render_template('results.html', path_final='Result stored in :'+str(path_final))

    except ValueError:
        return Response("Error Occurred! %s" % ValueError)

    except KeyError:
        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:
        return Response('There is some exception %s::' %e)

@app.route("/training/json", methods=['POST'])
@cross_origin()

def training_model_json():
    try:
        if request.json['filepath_testing'] is not None:
            path=request.json['filepath_testing']
            os.chdir(path)
            test_val=train_validation(path)
            #initializing the object
            test_val.train_validation()
            #calling the method

            train_Model=Training_Model()
            trainModel=train_Model.Preprocessing_Training()

            return Response('Training Sucessfully completed')
    except ValueError:
        return Response("Error Occurred! %s" % ValueError)

    except KeyError:
        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:
        return Response('There is some exception %s::' % e)

@app.route("/training", methods=['POST', 'GET'])
@cross_origin()
def training_model():
    try:
        if request.form['path_train'] is not None:
                path_train = request.form['path_train']
                os.chdir(path_train)
                test_val = train_validation(path_train)
                # initializing the object
                test_val.train_validation()
                # calling the method
                train_Model = Training_Model()
                trainModel = train_Model.Preprocessing_Training()
                directory_stored_models=r'C:\Users\hp\OneDrive\Desktop\ineuron\Phising_Website_Prediction\models'
                return render_template('result_training.html',message='Training sucessfully completed, training models are stored in:: '+str(directory_stored_models))

    except ValueError:
        return Response("Error Occurred! %s" % ValueError)

    except KeyError:
        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:
        return Response('There is some exception %s::' %e)

if __name__ == "__main__":

    app.run(debug=True)




