# reference https://youtu.be/bluclMxiUkA

from lib2to3.pgen2.pgen import DFAState
import string
import numpy as np
from flask import Flask, request, render_template, json, jsonify
import pickle
import os
import pandas as pd
import folium

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

@app.route('/liveability',methods=['POST'])
def liveability():
    df = pd.read_csv('../data/curated/merged_dataset/2022_merged_data.csv')
    type = request.form['residence_type']
    budget = request.form['budget']
    if type != 'idm':
        df = df[df.residence_type == type]
    if budget != 'idm':
        budget = float(request.form['budget'])
        df = df[df.weekly_rent <= budget]
    crime = request.form['crime']
    poli = request.form['poli']
    primary = request.form['primary']
    secondary = request.form['secondary']
    trans = request.form['trans']
    health = request.form['health']
    park = request.form['park']
    city = request.form['city']
    shop = request.form['shop']
    lst = [int(crime), int(poli), int(primary),int(secondary), int(trans), int(health),int(park), int(city), int(shop)]
    weight = [int(crime)/sum(lst), int(poli)/sum(lst), int(primary)/sum(lst), int(secondary)/sum(lst), int(trans)/sum(lst), int(health)/sum(lst), int(park)/sum(lst), int(city)/sum(lst), int(shop)/sum(lst)]
    COLS = ["residence_type","weekly_rent","address","sa2_2021",
        'min_distance_to_poli', 'crime_cases',  'min_distance_to_prim',
       'min_distance_to_second', 'min_distance_to_train',
       'min_distance_to_hosp','min_distance_to_park',
       'min_distance_to_cbd', 'min_distance_to_shop']
    COL = [
        'min_distance_to_poli', 'crime_cases',  'min_distance_to_prim',
       'min_distance_to_second', 'min_distance_to_train',
       'min_distance_to_hosp','min_distance_to_park',
       'min_distance_to_cbd', 'min_distance_to_shop']
    ranking = pd.DataFrame()
    for col in COLS:
        if col not in ["address","sa2_2021","residence_type","weekly_rent"]:
            ranking[col] = df[col].rank(ascending=False)
        else:
            ranking[col] = df[col]
    for col in COL:
        if col not in ["address","sa2_2021","residence_type","weekly_rent"]:
            ranking[col] = ranking[col]/len(ranking[col])
    score = ranking
    def liveability_scoring(scores, cols, weights):
        """Takes score data, list of weights and column names, return the total liveability score based on the weights"""
        score_lst = []
        for i in range(len(cols)):
            col_score = (1+ df[cols[i]].rank(ascending=False))/len(scores) # +1 as rank starts from 0
            df[f'{cols[i]}_score'] = col_score * weights[i]
            score_lst.append(f'{cols[i]}_score')
            df['total_liveability_score'] = df[score_lst].sum(axis=1)
        return df
    total_score = liveability_scoring(score, COL, weight)
    # liveable property
    total_score =total_score.sort_values(by=['total_liveability_score'], ascending=False)
    result = list(total_score.address.head(10))
    r1 = result[0]
    r2 = result[1]
    r3 = result[2]
    r4 = result[3]
    r5 = result[4]
    price = list(total_score.weekly_rent.head(5))
    p1 = price[0]
    p2 = price[1]
    p3 = price[2]
    p4 = price[3]
    p5 = price[4]
    type = list(total_score.residence_type.head(5))
    t1 = type[0]
    t2 = type[1]
    t3 = type[2]
    t4 = type[3]
    t5 = type[4]
    score = list(round(total_score.total_liveability_score.head(10)*100,2))
    s1 = score[0]
    s2 = score[1]
    s3 = score[2]
    s4 = score[3]
    s5 = score[4]
    # liveable suburb
    sa2_name = pd.read_csv('../data/curated/sa2_vic_2021.csv')
    df2 = total_score[['sa2_2021', 'total_liveability_score','address']]\
        .groupby(['sa2_2021'],as_index = False) \
        .agg(
            {\
                'total_liveability_score': 'mean', # count number of instances from sample
                'address': 'count',
            }
        ) \
        .rename({'address': 'num','total_liveability_score': 'averaged_total_liveability_score' }, axis=1)
    df2 = df2.sort_values(by=['averaged_total_liveability_score'], ascending=False)
    df2['averaged_total_liveability_score'] = round(df2['averaged_total_liveability_score']*100,2)
    df33 = df2.merge(sa2_name, how="left",left_on="sa2_2021",right_on = "SA2_CODE21").drop(columns = ['Unnamed: 0','SA2_CODE21'])
    df3 = list(df33.SA2_NAME21.head(5))
    score = list(df33.averaged_total_liveability_score.head(10))
    R1 = df3[0]
    R2 = df3[1]
    R3 = df3[2]
    R4 = df3[3]
    R5 = df3[4]

    S1 = score[0]
    S2 = score[1]
    S3 = score[2]
    S4 = score[3]
    S5 = score[4]

    with open('../data/curated/geo.json', 'r') as f:
        geoJSON = json.load(f)
    gsdf_pd = pd.read_csv('../data/curated/gsdf_pd.csv')
    m = folium.Map(location=[-37.81, 144.96], tiles="Stamen Terrain", zoom_start=10, color='white')
    svg_style = '<style>svg {background-color: rgb(255, 255, 255,0.5);}</style>'
    m.get_root().header.add_child(folium.Element(svg_style))

    c = folium.Choropleth(
        geo_data=geoJSON,
        name='choropleth',
        data=df33.reset_index(), 
        columns=['SA2_NAME21','averaged_total_liveability_score'],
        key_on='properties.SA2_NAME21', 
        fill_color='PiYG', 
        nan_fill_color='black',
        legend_name='averaged livability score per sa2',
    )
    c.add_to(m)

    return render_template('index.html',result = 'The top 5 recommended properties for you to rent are', \
            red = '(with liveability score out of 100):',\
            r1='1. {}'.format(r1),r2='2. {}'.format(r2),r3='3. {}'.format(r3),r4='4. {}'.format(r4),r5='5. {}'.format(r5),\
            result2 = 'The top 5 recommended suburbs for you to rent at are',\
            R1='1. {},'.format(R1),R2='2. {},'.format(R2),R3='3. {},'.format(R3),R4='4. {},'.format(R4),R5='5. {},'.format(R5),\
            p1=', ${} per week,'.format(p1),p2=', ${} per week,'.format(p2),p3=', ${} per week,'.format(p3),p4=', ${} per week,'.format(p4),p5=', ${} per week,'.format(p5),\
            t1=', {}'.format(t1),t2=', {}'.format(t2),t3=', {}'.format(t3),t4=', {}'.format(t4),t5=', {}'.format(t5),\
            s1=' {}'.format(s1),s2=' {}'.format(s2),s3=' {}'.format(s3),s4=' {}'.format(s4),s5=' {}'.format(s5),\
            S1=' {}'.format(S1),S2=' {}'.format(S2),S3=' {}'.format(S3),S4=' {}'.format(S4),S5=' {}'.format(S5),\
            contact = 'Contact us at jiahe3@student.unimelb.edu.au if you are interested in how we performed the ranking steps.',\
            map=m._repr_html_(),map1 = 'Averaged Liveability Score Based on Your Criteria')


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