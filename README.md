# Generic Real Estate Consulting Project
Groups should generate their own suitable `README.md`. <br/>
Group number:43 <br/>
Group members:  <br/>
Jiahe Liu (jiahe3@student.unimelb.edu.au) <br/>
Hyunjin Park (hyunjinp@student.unimelb.edu.au) <br/>
Jongho Park (jonghop@student.unimelb.edu.au) <br/>
Nuo Chen (nc1@student.unimelb.edu.au) <br/>
Anzhe Cai (anzhec@student.unimelb.edu.au) <br/>

 



# 1. Data Downloading

## 1.1 Property Dataset Downloading

We retrieved data from `Domain.com` and `oldlisting.com` using API and web scraping respectively. We also applied web scraping to retrieve data from `Domain.com`. However, we realised that they are similar from API-retrieved ones and Web-scrapped Domain data contained more error messages and will result in big data loss after data cleaning. Hence, we decided to use API-retrieved Domain data.

To generate Domain's data using API, please run `/notebooks/Scraping/API_Retrieving.ipynb`. However, as you may need to apply for your own client key and secrete via https://developer.domain.com.au/ . If you have questions regarding this, please contact the team via jiahe3@student.unimelb.edu.au

To generate oldlisting's data use Web Scarping, please run `/notebooks/Scraping/Get_historical_url.ipynb`. Which will generate all the websites that contains historical rental information `/notebooks/Scraping/HIS_url_links`. It will generate the historical data retrieved from the first 100 URLs for example demonstration. This data will be stored at `/data/raw/historical_data\`. However, it is very likely to be blocked if we generate too many data at each time. Hence, the team devided the web scraping tasks and generated gradually using the notebook script `/notebooks/Scraping/Group_scraping_tasks.ipynb`. This script will generate all historical data (2006-2022) retrieved fro, oldlisting to `/data/raw/historical_data\`. In total, the team retrieved around 400k data from oldlisting.

As the historical web site monitor ip address with high levels of activity, we assume the website counts the number of access by tryring many access with reasonable breaks and check when it gets block. So there are few solution options and one of them is using api-rotator through AWS. It is shown in the file `/scripts/aws-scraping-tool.py`. AWS API key will be hidden in .env file.

If you want to see Domain's data retrieved using Web Scrping, please run `/notebooks/Scraping/BS_Scraping.ipynb`. However, these data will not be used in preliminary analysis or modeling to avoid redundancy.

## 1.2 External Dataset Downloading
We retrieved data of external attributes, such as crime cases, total personal income, estimated resident population, GDP from `abs.gov.au` and `hcrimestatistics.vic.gov.au`
**[Need to complete later] - katherine & jin**

## 1.3 External Dataset Downloading (Infrastructure Facility Locations Retrieved by API)
**[Need to complete later] - jin**


# 2. Data Preprocessing

## 2.1 Property Dataset Preprocessing

### 2.1.1 API-retrieved Data Preprocessing (rental price)

For API data rental price preprocessing, please see `/notebooks/Preprocessing/API_prepro.ipynb`. We kept the integer only for the rental price. This notebook also converted the API dataset to the same format as the Web Scraped dataset for future concatenation. 
### 2.1.2 Web-Scraping-retrieved Data Preprocessing (rental price, outlier detection for all features)

For Web Scraping + API data preprocessing please see `/notebooks/Preprocessing/History_prepro.ipynb`. We firstly cleaned Web-Scraped data's rental price and then combined it with API datasets. We classified the whole datset and re-saved them by year. This is because, there may be inflations every year and the variance of rental price calculated year by year may be more reasonable.

For number of rooms, we viewed the boxplot and mannually confirmed deleted some inituive outliers (large number of rooms, very low price). For the location (latitude and longitude), we ammended 3 badly scrapped location data. 

For the rental price, we removed outliers year by year. For each year, we removed the rental price vlaues out side of the 3 standard deviation. Each year, arounf 1 to 3 % of data were removed as outliers. Hence we suggest it is a reasonable outlier removal appraoch.

### 2.1.3 Adding SA2 Code for Cleaned Data
**[Need to complete later] - john & kathrine**

### 2.1.4 Adding Distance/Time to Places/CBD from Clean Property Data (Open Route Servive API)
See `/notebooks/Preprocessing/ors_iteration_add_rentalDistance`. At each iteration, a yearly subset of places csv and a year subset of property csv between 2013-2021 were called out and merged based on SA2 Code. Then, a list of clients registered with unique API keys was used to request distance/time for each merged yearly dataset. 

In the add_distance_time function, the requests were conducted by iterating SA2 codes. All properties in current SA2 code were computed as sources, each of which was mapped to all places defined by this SA2 code. So in total, (size of sources * count of places) routes of distances/time were computed for each SA2 district. 

For route number greater than 3500 which was prohibited by ORS, a slicing method that divided sources into smaller subsets based on the factor, by which route number exceeded 3500, replaced the original requests. Through this, the restriction could be solved by making additional calls for reduced sublists. For example for 206 sources * 35 places = 7210 > 3500, exceeding by a factor of 2, sources list was divided into \[0-68), \[68-136) and \[136-206) sublists, and 3 requests with route number 68 * 35, 68 * 35 and 70 * 35 were called to ensure all 7210 data was retrieved.

For exception such as exceeding API quota during processing, a back up API key with a capacity of 2500 calls was switched into to handle the exception. For other keys, the individual quota of 500 was mostly sufficient to process each merged yearly dataset given there were fewer than 500 SA2 codes in each year (except for 502 in 2022).  

### 2.1.5 Feature Engineering for Property Dataset

We engineered `residence type` as a binary feature (House or Apartment). This is because this project analyses resiential properties, hence we exlcuded rental properties for office, holidat, rural area etc. We calssified the rest residence type into `House` including townhouse, terrace, etc. and `Apartment` including unit, studio etc. for simplication so that we can ask our client for their rental residence type preference. 

However, we discovered that in total 42.66% of properties (231497 property data in total) do not have a residence type label. We assume that these properties are either House or Apartment. Hence, made a classification model to label them as either House or Apartment. 

To view these steps please see `/models/classify_property_type.ipynb`.

## 2.2 External Dataset Preprocessing
**[Need to complete later] - katherine**

## 2.3 Data Merging
**[Need to complete later] - ketherine**
### 2.3.X Adding SA2
There are many options to add SA2. 
First we add SA2 using suburb name as generally SA2 name refers to suburb in the residential address (see document  https://www.abs.gov.au/ausstats/abs@.nsf/lookup/by%20subject/1270.0.55.001~july%202016~main%20features~statistical%20area%20level%202%20(sa2)~10014) however there are many of them fail to match with SA2 name because of different formats, some of region added prefix or suffix (ex. -south, -north, the great-, etc...) and the regions that have different name to SA2 name.  

Second, we use location data to add SA2. This approach is genuine method as the all of data has location meta data in the website and API and the data loss is less than 0.5% (few data is located outside of victoria) and easy to process. We use shap file from ABS (https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files) and map polygon coordinates and check which region contains the residence locations. This will assign SA2 code to every residential locations.  



# 3. Data Analysis

## 3.1 Property Data Preliminary Analysis
**[Need to complete later] - jin & grace**
## 3.2 Property Data Geo Visual
**[Need to complete later] - jin & grace**

# 4. Modeling

## 4.1 Prediction Model for External Features
All models mentioned below are in `\models` file

### 4.1.1 Population
**[Need to complete later] john**

### 4.1.2 Averaged income per person for each SA2
**[Need to complete later] john**

### 4.1.3 Crime cases per each postcode region
A linear regression model was used to predict the crime cases per each postcode region from 2023 to 2027. 
prediction formula: `crime cases ~ year + postcode`
`year` was considered as numerical values and `postcode` was considered as categorical value

## 4.2 Rental Price Prediction
**[Need to complete later] philip, jin, katherine**

### 4.3 Rental Price Growth Rate Calculation
**[Need to complete later] philip, jin, katherine**

# 5. Liveability Scoring and Ranking Algorithm
**[Need to complete later] jon & grace**

# 6. Website Building
To put our model into practice and bridge the gap between the general population and our models, we built a web site that enables the general population to explore our models.

`/web/app.py` is an app object created using the Flask class. We have rendered our models including population density prediction, crime case prediction, income rate prediction, and rental price prediction models on our website. We also created a client-oriented section for our users get recommendations on the mostly liveable and affordable suburbs and properties based on their needs. Users can input the year and SA2 code in order to view the corresponding prediction result by our models.

We also included Suburb Name and SA2 code lookup tables for our users to get the SA2 code by suburb name. The html lookup table was transfered from the csv lookup table. The transferring process is included at the end of `/notebooks/preliminary_property.ipynb`.

To view the models, please visit the corresponidng notebooks in `/models`. At the end of each notebook, the model will be saved with `.pkl` format for the use of Flask. The `.pkl` model files are saved under `/web/models`.

To view the website, please run `/web/app.py` and go to `http://127.0.0.1:5000/ `.

To view the css styles of the website, please see`/web/static/style1.css` .

To view the html code of the website, please see `web/templates/index.html`.


