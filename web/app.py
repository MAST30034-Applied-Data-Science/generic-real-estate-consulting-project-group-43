# https://youtu.be/bluclMxiUkA

import numpy as np
from flask import Flask, request, render_template, json
import pickle
import os
import pandas as pd
 
#Create an app object using the Flask class. 
app = Flask(__name__)


#Load the trained model. (Pickle file)

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
print(dname)

model1 = pickle.load(open('../web/models/population_model.pkl', 'rb'))
model2 = pickle.load(open('../web/models/crimecase_model.pkl', 'rb'))
model3 = pickle.load(open('../web/models/income_model.pkl', 'rb'))


#Define the route to be home. 
#The decorator below links the relative route of the URL to the function it is decorating.
#Here, home function is with '/', our root directory. 
#Running the app sends us to index.html.
#Note that render_template means it looks for the file in the templates folder. 

#use the route() decorator to tell Flask what URL should trigger our function.
@app.route('/')
def home():
    return render_template('index.html')

#You can use the methods argument of the route() decorator to handle different HTTP methods.
#GET: A GET message is send, and the server returns data
#POST: Used to send HTML form data to the server.
#Add Post method to the decorator to allow for form submission. 
#Redirect to /predict page with the output
@app.route('/predict',methods=['POST'])

def predict():
    int_features = [x for x in request.form.values()] #Convert string inputs to float.
    features = [np.array(int_features)]  #Convert to the form [[a, b]] for input to the 
    if (features[0][0].isdigit() & features[0][1].isdigit()):
        year = int(features[0][0])
        sa2 = int(features[0][1])
    else:
        return render_template('index.html', error1='Please enter valid values.')
    result = pd.read_csv('../data/curated/feature_prediction/22_27_population.csv')
    sa2_df = pd.read_csv('../data/curated/sa2_vic_2021.csv')
    print(sa2)
    suburb = sa2_df.loc[sa2_df.SA2_CODE21 == sa2].SA2_NAME21.values
    if suburb:
        suburb = suburb[0]
    SA2_lst = list(set(result['SA2 code']))
    year_lst = list(set(result['year']))
    if ((sa2 in SA2_lst) & (year in year_lst)):
        df_sa2 = pd.DataFrame(SA2_lst)
        df_sa2.columns = ['SA2 code']
        df_sa2_dum = pd.get_dummies(df_sa2, columns=['SA2 code'])
        row = df_sa2_dum[df_sa2_dum['SA2 code_'+str(sa2)] == 1]
        row.insert(0, 'year',year)
        pred = int(model1.predict(row))
        #prediction = model.predict(features)  # features Must be in the form [[a, b]]
        output = pred
        return render_template('index.html', prediction_text1='In {}, the population density of {} is predicted to be {} per kilometer square'.format(year, suburb,output))
    return render_template('index.html', error2='Sorry, we do not have enough information to make prediction.')

@app.route('/predict_crime',methods=['POST'])

def predict_crime():
    int_features = [x for x in request.form.values()] #Convert string inputs to float.
    features = [np.array(int_features)]
    if (features[0][0].isdigit() & features[0][1].isdigit() ):
        print(len( features[0][1]))
        year_crime = int(features[0][0])
        post = int(features[0][1])
    else:
        return render_template('index.html', error3='Please enter valid values.')
    result = pd.read_csv('../data/curated/feature_prediction/23_27_crime_case.csv')
    post_lst = list(set(result['Postcode']))
    year_lst = list(set(result['Year']))
    if ((post in post_lst) & (year_crime in year_lst)):

        df_post = pd.DataFrame(post_lst)
        df_post.columns = ['Postcode']
        df_post_dum = pd.get_dummies(df_post, columns=['Postcode'])
        row = df_post_dum[df_post_dum['Postcode_'+str(post)] == 1]
        row.insert(0, 'Year',year_crime)
        pred = int(model2.predict(row))
        #prediction = model.predict(features)  # features Must be in the form [[a, b]]
        output_crime = pred
        return render_template('index.html', prediction_text2='In {}, the crime cases of {} is predicted to be {}'.format(year_crime, post,output_crime))
    return render_template('index.html', error4='Sorry, we do not have enough information to make the prediction.')

@app.route('/predict_income',methods=['POST'])

def predict_income():
    int_features = [x for x in request.form.values()] #Convert string inputs to float.
    features = [np.array(int_features)]
    if (features[0][0].isdigit() & features[0][1].isdigit() ):
        print(len( features[0][1]))
        year_income = int(features[0][0])
        sa2 = int(features[0][1])
    else:
        return render_template('index.html', error5='Please enter valid values.')
    result = pd.read_csv('../data/curated/feature_prediction/20_27_income_per_person_2016sa2.csv')
    sa2_df = pd.read_csv('../data/curated/sa2_vic_2016.csv')
    suburb = sa2_df.loc[sa2_df.SA2_MAIN16 == sa2].SA2_NAME16.values
    if suburb:
        suburb = suburb[0]
    sa2_lst = list(set(result['sa2_2016']))
    year_lst = list(set(result['Year']))
    if ((sa2 in sa2_lst) & (year_income in year_lst)):
        df_sa2 = pd.DataFrame(sa2_lst)
        df_sa2.columns = ['SA2']
        df_sa2_dum = pd.get_dummies(df_sa2, columns=['SA2'])
        row = df_sa2_dum[df_sa2_dum['SA2_'+str(sa2)] == 1]
        row.insert(0, 'Year',year_income)
        pred = int(model3.predict(row))
        #prediction = model.predict(features)  # features Must be in the form [[a, b]]
        output_crime = pred
        return render_template('index.html', prediction_text3='In {}, the income of {} is predicted to be {} AUD per year'.format(year_income, suburb,output_crime))
    return render_template('index.html', error6='Sorry, we do not have enough information to make the prediction.')

#When the Python interpreter reads a source file, it first defines a few special variables. 
#For now, we care about the __name__ variable.
#If we execute our code in the main program, like in our case here, it assigns
# __main__ as the name (__name__). 
#So if we want to run our code right here, we can check if __name__ == __main__
#if so, execute it here. 
#If we import this file (module) to another file then __name__ == app (which is the name of this python file).

if __name__ == '__main__':
    app.run(debug=True)

'''if __name__=="__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 4444)))'''