# This is Heroku Deployment Lectre
from flask import Flask, request, render_template
import os
import pickle

print("working dir:", os.getcwd())
path = os.getcwd()

with open('Models/LR_Model.pkl', 'rb') as f:
    logistic = pickle.load(f)

with open('Models/RF_Model.pkl', 'rb') as f:
    randomforest = pickle.load(f)

with open('Models/SVM_Model.pkl', 'rb') as f:
    svm_model = pickle.load(f)


def get_predictions(age, gender, cp, trest_bps, chol, fbs, restecg, thalach, exang,
                    old_peak, slope, ca, thal, req_model):
    mylist = [age, gender, cp, trest_bps, chol, fbs, restecg,
              thalach, exang, old_peak, slope, ca, thal]
    mylist = [float(i) for i in mylist]
    vals = [mylist]

    if req_model == 'Logistic':
        return logistic.predict(vals)[0]
    elif req_model == 'RandomForest':
        return randomforest.predict(vals)[0]
    elif req_model == 'SVM':
        return svm_model.predict(vals)[0]
    else:
        return "Cannot Predict"


app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/', methods=['POST', 'GET'])
def my_form_post():
    if request.method == 'POST':
        age = request.form['age']
        gender = request.form['gender']
        cp = request.form['cp']
        trest_bps = request.form['trest_bps']
        chol = request.form['chol']
        fbs = request.form['fbs']
        restecg = request.form['restecg']
        thalach = request.form['thalach']
        exang = request.form['exang']
        old_peak = request.form['old_peak']
        slope = request.form['slope']
        ca = request.form['ca']
        thal = request.form['thal']
        req_model = request.form['req_model']

        target = get_predictions(age, gender, cp, trest_bps, chol, fbs,
                                 restecg, thalach, exang, old_peak, slope,
                                 ca, thal, req_model)

        if target == 1:
            sale_making = 'Presence of Heart Disease'
        else:
            sale_making = 'Absence of Heart Disease'

        return render_template('index.html', target=target,
                               sale_making=sale_making)
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)