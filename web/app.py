# https://youtu.be/bluclMxiUkA

import numpy as np
from flask import Flask, request, render_template
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
    int_features = [float(x) for x in request.form.values()] #Convert string inputs to float.
    features = [np.array(int_features)]  #Convert to the form [[a, b]] for input to the model
    year = int(features[0][0])
    sa2 = int(features[0][1])
    result = pd.read_csv('../data/curated/feature_prediction/22_27_population.csv')
    sa2_df = pd.read_csv('../data/curated/sa2_vic.csv')
    suburb = sa2_df[sa2_df.SA2_CODE21 == 201011001].SA2_NAME21
    suburb = suburb[0]
    SA2_lst = list(set(result['SA2 code']))
    df_sa2 = pd.DataFrame(SA2_lst)
    df_sa2.columns = ['SA2 code']
    df_sa2_dum = pd.get_dummies(df_sa2, columns=['SA2 code'])
    row = df_sa2_dum[df_sa2_dum['SA2 code_'+str(sa2)] == 1]
    row.insert(0, 'year',year)
    pred = int(model1.predict(row))
    #prediction = model.predict(features)  # features Must be in the form [[a, b]]
    output = pred
    return render_template('index.html', prediction_text1='In {}, the population of {} is predicted to be {}'.format(year, suburb,output))

@app.route('/predict_crime',methods=['POST'])

def predict_crime():
    year_crime = 2023
    post = 3000
    result = pd.read_csv('../data/curated/feature_prediction/23_27_crime_case.csv')
    post_lst = list(set(result['Postcode']))
    df_post = pd.DataFrame(post_lst)
    df_post.columns = ['Postcode']
    df_post_dum = pd.get_dummies(df_post, columns=['Postcode'])
    row = df_post_dum[df_post_dum['Postcode_'+str(post)] == 1]
    row.insert(0, 'Year',year_crime)
    pred = int(model2.predict(row))
    #prediction = model.predict(features)  # features Must be in the form [[a, b]]
    output_crime = pred
    return render_template('index.html', prediction_text2='In {}, the crime cases of {} is predicted to be {}'.format(year_crime, post,output_crime))



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