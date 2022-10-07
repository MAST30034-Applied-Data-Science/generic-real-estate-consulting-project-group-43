# Generic Real Estate Consulting Project
Groups should generate their own suitable `README.md`. <br/>
Group number:43 <br/>
Group members:  <br/>
Jiahe Liu (jiahe3@student.unimelb.edu.au) <br/>
Hyunjin Park (hyunjinp@student.unimelb.edu.au) <br/>
Jongho Park (jonghop@student.unimelb.edu.au) <br/>
Nuo Chen (nc1@student.unimelb.edu.au) <br/>
Anzhe Cai (anzhec@student.unimelb.edu.au) <br/>

 
* Note: file named beginning with "test_" are approaches we tried but seemed not useful or we found alternative way to optimise. 




# 1. Data Downloading

## 1.1 Property Dataset Downloading

We retrieved data from `Domain.com` and `oldlisting.com` using API and web scraping respectively. We also applied web scraping to retrieve data from `Domain.com`. However, we realised that they are similar from API-retrieved ones and Web-scrapped Domain data contained more error messages and will result in big data loss after data cleaning. Hence, we decided to use API-retrieved Domain data.

0. `/notebooks/Scraping/0.BS_Scraping.ipynb`: This notebook will scrape data at Domain using beautiful soup. However, these data will not be used in preliminary analysis or modeling to avoid redundancy.

1. `/notebooks/Scraping/1.API_Retrieving.ipynb`:  This notebook will retrieve data at Domain using API.However, as you may need to apply for your own client key and secrete via https://developer.domain.com.au/ . If you have questions regarding this, please contact the team via jiahe3@student.unimelb.edu.au

2. `/notebooks/Scraping/2.Get_historical_url.ipynb`: This notebook  will generate all the URL links that contains historical rental information into `/notebooks/Scraping/HIS_url_links`
It will generate the historical data retrieved from the first 100 URLs for example demonstration. However, it is very likely to be blocked if we generate too many data at each time. Hence, the team devided the web scraping tasks and generated gradually using the notebook script.

3. `/notebooks/Scraping/3.Group_scraping_tasks.ipynb`: Hence, this notebook will generate all historical data (2006-2022) retrieved fro, oldlisting to `/data/raw/historical_data/`.We retrieved around 572k data from oldlisting.

4. `/notebooks/Scraping/4.Scraping_whole.ipynb`: this notebook will using api-rotator through AWSAs to prevent web scrapping from being blocked. The historical web site monitor ip address with high levels of activity, we assume the website counts the number of access by trying many access with reasonable breaks and check when it gets block. So there are few solution options and one of them is using api-rotator through AWS. It is shown in the file `/scripts/aws-scraping-tool.py`. AWS API key will be hidden in .env file.

5. `/notebooks/Scraping/5.facility_data_retreiving`: this notebook will retrieve facility data using API. Facility dataset include the facility name, location, year in which these facilitie exist. Facilities include primary and secondary schools, hospital, train station, police station, market, shopping mall.

## 1.2 External Dataset Downloading
We retrieved data of external attribute by urls, such as crime cases, total personal income, estimated resident population, GDP, saving rate from `abs.gov.au`, `hcrimestatistics.vic.gov.au` and `data.oecd.org/natincome/saving-rate.htm`. The notebook script `/notebooks/External/0.external_dataset_download.ipynb` is used to download those external dataset, and store into the raw folder in the data folder.

## 1.3 External Dataset Downloading (Infrastructure Facility Locations Retrieved by API)
We retreieved data of features of interest in Victoria state by retreiving query in GeoJson format through `https://services6.arcgis.com/GB33F62SbDxJjwEL/ArcGIS/rest/services/Vicmap_Features_of_Interest/FeatureServer/8/query`. The selected features of interest that we deicded to include were primary/secondary schools, parks, train stations, hospitals, market places, police stations and shopping malls. By querying them by each year with their registered data on the dataset of `https://www.arcgis.com/home/webmap/viewer.html?url=https://services6.arcgis.com/GB33F62SbDxJjwEL/ArcGIS/rest/services/Vicmap_Features_of_Interest/FeatureServer/8&source=sd`, we could retrieve each year's features of interest locations that is used to calculate the distance between a feature of interest and a rental property from the historical rental property dataset. <br/>
### Structure of features of interest dataset for each year
The way of producing one feature of interest for a particular year is cumulative. 
eg) To retrieve the data for **market places in 2014**, all the market places registered before 2013 + market places registered in 2013 + market places registered in 2014 are combined. <br/>
### The reasons of choosing these particular features
We have chosen these 8 features of interest to put into our model as inputs out of many other features of interest in Victoria, since we consider them to have a significant relevant to livability, which is one of the main topic questions. According to Global livability Index 2021 Report `https://www.eiu.com/n/campaigns/global-liveability-index-2021/`, they stated 5 factors that compose liveability as "stability, healthcare, culture and environment, education and infrastructure". 
**By referring to these five factors, we have chosen the 8 features with the following reasons:** <br/>
- Primary/secondary schools: Education
- Parks, Shopping malls: Culture and environment
- Hospitals: Healthcare
- Markets, Police stations, Train stations: Stability, Infrastructure

# 2. Data Preprocessing

## 2.1 Property Dataset Preprocessing

### 2.1.1 API-retrieved Data Preprocessing (rental price)

0. `/notebooks/Preprocessing/0.API_prepro.ipynb`: this notebook will preprocess API data rental price. We kept the integer only for the rental price. This notebook also converted the API dataset to the same format as the Web Scraped dataset for future concatenation. 

### 2.1.2 Web-Scraping-retrieved Data Preprocessing (rental price, outlier detection for all features)

1. `/notebooks/Preprocessing/1.History_prepro.ipynb`:this notebook will preproces Web Scraping + API data preprocessing. We firstly cleaned Web-Scraped data's rental price and then combined it with API datasets. We classified the whole datset and re-saved them by year. This is because, there may be inflations every year and the variance of rental price calculated year by year may be more reasonable.

For number of rooms, we viewed the boxplot and mannually confirmed deleted some inituive outliers (large number of rooms, very low price). For the location (latitude and longitude), we ammended 3 badly scrapped location data. 

For the rental price, we removed outliers year by year. For each year, we removed the rental price vlaues out side of the 3 standard deviation. Each year, arounf 1 to 3 % of data were removed as outliers. Hence we suggest it is a reasonable outlier removal appraoch.


### 2.1.3 Adding SA2 Code for Cleaned Data
There are many options to add SA2. 
First we add SA2 using suburb name as generally SA2 name refers to suburb in the residential address (see document  https://www.abs.gov.au/ausstats/abs@.nsf/lookup/by%20subject/1270.0.55.001~july%202016~main%20features~statistical%20area%20level%202%20(sa2)~10014) however there are many of them fail to match with SA2 name because of different formats, some of region added prefix or suffix (ex. -south, -north, the great-, etc...) and the few regions that have totally different name to SA2 name.  

Second, we use location data to add SA2. This approach is genuine method as the all of data has location meta data in the website and API and the data loss is less than 0.5% (few data is located outside of victoria) and easy to process. For the process, we use shap file from ABS (https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files) and map polygon coordinates and check which region contains the residence locations. This will assign SA2 code to every residential locations.  

2. `/notebooks/Preprocessing/2.add_SA2_coordinate_API.`: this notebook will add 2021 SA2 code for each property instance retrieved by Domain API. This is done by checking whether the location point (longitude, latitude) is within the SA2 polygon by from shape file. 

3. `/notebooks/Preprocessing/3.add_SA2_coordinate_WS_and_facilities`: this notebook will add 2021 SA2 code for each property instance retrieved oldlisting web scraping and facility (school, parks, hospital etc.) dataset. Approaches are the same as the above.

### 2.1.4 Adding Distance/Time to Places/CBD from Clean Property Data (Open Route Servive API)
4. `/notebooks/Preprocessing/4.ors_add_rentalDistance.ipynb`. At each iteration, a yearly subset of places csv and a year subset of property csv between 2013-2021 were called out and merged based on SA2 Code. Then, a list of clients registered with unique API keys was used to request distance/time for each merged yearly dataset. 

In the add_distance_time function, the requests were conducted by iterating SA2 codes. All properties in current SA2 code were computed as sources, each of which was mapped to all places defined by this SA2 code. So in total, (size of sources * count of places) routes of distances/time were computed for each SA2 district. 

For route number greater than 3500 which was prohibited by ORS, a slicing method that divided sources into smaller subsets based on the factor, by which route number exceeded 3500, replaced the original requests. Through this, the restriction could be solved by making additional calls for reduced sublists. For example for 206 sources * 35 places = 7210 > 3500, exceeding by a factor of 2, sources list was divided into \[0-68), \[68-136) and \[136-206) sublists, and 3 requests with route number 68 * 35, 68 * 35 and 70 * 35 were called to ensure all 7210 data was retrieved.

For exception such as exceeding API quota during processing, a back up API key with a capacity of 2500 calls was switched into to handle the exception. For other keys, the individual quota of 500 was mostly sufficient to process each merged yearly dataset given there were fewer than 500 SA2 codes in each year (except for 502 in 2022).  

5. `/notebooks/Preprocessing/5.ors_iteration_add_rentalDistance.ipynb`: this notebook will perform the mentioned steps iteratively to retrieve the (2013-2022) data we need. `/notebooks/Preprocessing/5.ors_add_rentalDistance.ipynb`: this notebook will retrieve 2022 data individually due to large data size.

6. `/notebooks/Preprocessing/6.get_minDistance.ipynb`: this notebook will compare distances each facility within a SA2 suburb for each property and only keep the minimal distance i.e. distance to the cloesest facility. NA value will be applied if there is no a type of facility within a SA2 suburb. These NA values will be filled later by the maximum number within a column. 

### 2.1.5 Feature Engineering for Property Dataset

We engineered `residence type` as a binary feature (House or Apartment). This is because this project analyses resiential properties, hence we exlcuded rental properties for office, holidat, rural area etc. We calssified the rest residence type into `House` including townhouse, terrace, etc. and `Apartment` including unit, studio etc. for simplication so that we can ask our client for their rental residence type preference. 

However, we discovered that in total 42.66% of properties (231497 property data in total) do not have a residence type label. We assume that these properties are either House or Apartment. Hence, made a classification model to label them as either House or Apartment. 

To view these steps please see `/models/classify_property_type.ipynb`.

## 2.2 External Dataset Preprocessing
The notebook script `/notebooks/External/1.external_preprocess.ipynb` is used to do preprocessing on those external dataset (estimated resident population, total income, crime cases, GDP, saving rate), and store into the curated folder in the data folder. We calculated the population density for each sa2 region (2021), income per person for each sa2 region (2016) based on the dataset of estimated resident population and total income respectively. We tried to convert the 2016 sa2 of income to 2021 sa2, but this would lead to lots of data missing. Therefore, we decide to use 2016 sa2 for later merging. There are also some plots for different types of offence.

## 2.3 Data Merging

### 2.3.1 Adding SA2 2016
There were issues arised that the statistic data (including population, income, etc...) before 2021 has different SA2 code standard established at 2016. Every five year the SA2 code standard gradually changes so we need to add more SA2 code standard to the instance. As the name and area of SA2 codes change, we need stable data to match the code. The using location data is decided as an fitable method because is is stable and can be point directly what SA2 region, it was used to belong in the past.
To view these steps please see `/notebooks/Preprocessing/7.add_SA2_2016.ipynb` and `/notebooks/Preprocessing/8.organising.ipynb`.

### 2.3.2 Adding External Features
For merging external data of 2013 to 2022, the notebook script `/notebooks/External/2.external_merge.ipynb` is used to merge external attributes (GDP and saving rate, income per person for each sa2, population density and crime cases) with the data in the min_distance_sa2_organised folder in curated folder, and also drop months to get values of all attributes based on year. If the values of external attributes (GDP and saving rate, income per person for each sa2, population density and crime cases) are missing, the predicted values for the external attributes (in the features_prediction folder in curated folder) are used to merge.

For merging predicted values of external attributes of 2023 to 2027, the notebook script `/notebooks/External/3.2023_2027_merge.ipynb` is used to merge predicted values of external attributes (GDP and saving rate, income per person for each sa2, population density and crime cases) with the postcode of Local Government Area (LGA), 2016 sa2 codes and 2021 sa2 codes from 2022 dataset. Since 2022 dataset has the most values of postcode, sa2 2021 and sa2 2016, and includes all values from previous years of those attributes, postcode, sa2 2021 and sa2 2016 from 2022 dataset will be used for further prediction. The predicted values of the external attributes, that used for merging, are from the features_prediction folder in curated folder.

`/notebooks/External/4.external_geo.ipynb`: this notebook visualize the population density of sa2 (2021) regions with geo plots.

# 3. Data Analysis

## 3.1 Property Data Preliminary Analysis
`/notebooks/preliminary_property.ipynb`: this notebook performs analysis through analysis houses and apartments together and respectively. Plots drawn by this were saved to `/plots/figure/`. 

## 3.2 Property Data Geo Visual
`/notebooks/preliminary_property.ipynb`: This notebook also contains geo visual for houses and apartments per SA2 respectively. More imporatantly, this notebook uses simplified geo shape file to improve graph-drawn efficiency. The simplification process was down through `https://mapshaper.org/`. `notebooks/Liveability/scoring.ipynb` has clearer explanation of this. And the number of houses and apartments rental records per SA2 respectively. Geo plots were saved to `/plots/aggregated_geo`

# 4. Modeling

## 4.1 Prediction Model for External Features
All feature prediction models mentioned below are in `\models` file. The output of predicted features' values will be stored into the features_prediction folder in curated folder.

### 4.1.1 Population
`/models/1a.bootstrap-population.ipynb`: this notebook predicts population from 2022 to 2027 using bootstrapping and linear regression, with `population density  ~ year + sa2 code(2021)`.

### 4.1.2 Averaged income per person for each SA2
The notebook script `/models/1b.income_predict.ipynb` is used to model the income per person for each sa2 (2016) with a linear regression model, and it is used to predict the income per person for each sa2 (2016) region from 2020 to 2027, with `income per person ~ year + sa2 code(2016)`.
`year` is considered as numerical value and `sa2 code(2016)` is considered as categorical value.

### 4.1.3 Crime cases per each postcode region
`/models/1c.crimecase_predict.ipynb`:A linear regression model was used to predict the crime cases per each postcode region from 2023 to 2027. 
prediction formula: `crime cases ~ year + postcode`
`year` was considered as numerical value and `postcode` was considered as categorical value

### 4.1.4 GDP and Saving rate
`/models/1d.gdp_saving_predict.ipynb`: this notebook predicts the GDP and saving rate from 2021 to 2027. The GDP is predicted by a linear regression model with `log(GDP) ~ log(year)`. And the saving rate is predicted by a quadratic regression model with `Saving rate ~ year^2`

## 4.2 Rental Price Prediction

### 4.2.1 OLS Model
Ordinary Least Square Regression is implemented in `/models/LR_prediction_all.ipynb`. In this notebook, forward selection based on lowest AIC is first conducted, which takes around an hour to run. Then the resulting features are selected from the training set to train and test the model at a ratio of 7:3. Subsequently, the Linear Regression model in `/models/LR_future_prediction.ipynb` is trained by the full 2013-2022 merged dataset containing the selected features, which is then used to make future 2023-2027 predictions.

### 4.2.2 XGboost Model
Due to the lack of historical data, the dataset is biased. Therefore, the XGboost model is used for the rent price prediction, referring to the `/models/rent_price_xgboost.ipynb`. With using holdout method for train test split, the XGboost regression model is trained, and the training accuracy is 0.718 while the test accuracy is 0.688. A feature importance graph is also plotted by XGboost built-in function. Further, this notebook predicts the rent prices for 2023 - 2027. 

### 4.2.3 Random Forest


**[Need to complete later] jin**

### 4.3 Rental Price Growth Rate Calculation
Based on prediction results from 2023-2027, rental prices are aggregated to average per SA2 district per year. The same aggregation is applied to year 2022 rental dataset, which is then concatenated to the prediction set. Growth rate of a district in current year is calculated by (average rental price of district in current year)-(average rental price of district in past year) / (average rental price of district in past year). The average future growth rate for a district is then calculated by sum of yearly growth rates from 2023 to 2027 of the district / 5. 

# 5. Liveability Scoring and Ranking Algorithm
`notebooks/Liveability/scoring.ipynb`: this notebook developed a ranking system for liveability scoring (0-100). The notebook firstly checked distribution of each feature to see whether standardisation can be applied. Unfortunately, data were not normally distributed. Hence we used score = rank / len(df) to perform the score for each liveability criterion and sum them with weight specified by our user. 

# 6. Website Building
To put our model into practice and bridge the gap between the general population and our models, we built a web site that enables the general population to explore our models.

`/web/app.py` is an app object created using the Flask class. We have rendered our models including population density prediction, crime case prediction, income rate prediction, and rental price prediction models on our website. We also created a client-oriented section for our users get recommendations on the mostly liveable and affordable suburbs and properties based on their needs. Users can input the year and SA2 code in order to view the corresponding prediction result by our models.

We also included Suburb Name and SA2 code lookup tables for our users to get the SA2 code by suburb name. The html lookup table was transfered from the csv lookup table. The transferring process is included at the end of `/notebooks/preliminary_property.ipynb`.

To view the models, please visit the corresponidng notebooks in `/models`. At the end of each notebook, the model will be saved with `.pkl` format for the use of Flask. The `.pkl` model files are saved under `/web/models`.

To view the website, please run `/web/app.py` and go to `http://127.0.0.1:5000/ `.

To view the css styles of the website, please see`/web/static/style1.css` .

To view the html code of the website, please see `web/templates/index.html`.


