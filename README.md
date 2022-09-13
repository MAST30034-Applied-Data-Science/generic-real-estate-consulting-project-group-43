# Generic Real Estate Consulting Project
Groups should generate their own suitable `README.md`.
Group number:43
Group members:  \n
Jiahe Liu (jiahe3@student.unimelb.edu.au) \n
Hyunjin Park (hyunjinp@student.unimelb.edu.au) \n
Jongho Park (jonghop@student.unimelb.edu.au) \n
Nuo Chen (nc1@student.unimelb.edu.au) \n
Anzhe Cai (anzhec@student.unimelb.edu.au) \n

 \n



# 1. Data Downloading

## 1.1 Property Dataset Downloading

We retrieved data from `Domain.com` and `oldlisting.com` using API and web scraping respectively. We also applied web scraping to retrieve data from `Domain.com`. However, we realised that they are similar from API-retrieved ones and Web-scrapped Domain data contained more error messages and will result in big data loss after data cleaning. Hence, we decided to use API-retrieved Domain data.

To generate Domain's data using API, please run `/notebooks/Scraping/API_Retrieving.ipynb`. However, as you may need to apply for your own client key and secrete via https://developer.domain.com.au/ . If you have questions regarding this, please contact the team via jiahe3@student.unimelb.edu.au

To generate oldlisting's data use Web Scarping, please run `/notebooks/Scraping/Get_historical_url.ipynb`. Which will generate all the websites that contains historical rental information `/notebooks/Scraping/HIS_url_links`. It will generate the historical data retrieved from the first 100 URLs for example demonstration. This data will be stored at `/data/raw/historical_data\`. However, it is very likely to be blocked if we generate too many data at each time. Hence, the team devided the web scraping tasks and generated gradually using the notebook script `/notebooks/Scraping/Group_scraping_tasks.ipynb`. This script will generate all historical data (2006-2022) retrieved fro, oldlisting to `/data/raw/historical_data\`. In total, the team retrieved around 400k data from oldlisting.

If you want to see Domain's data retrieved using Web Scrping, please run `/notebooks/Scraping/BS_Scraping.ipynb`. However, these data will not be used in preliminary analysis or modeling to avoid redundancy.

## 1.2 External Dataset Downloading
[Need to complete later]

# 2. Data Preprocessing

## 2.1 Property Dataset Preprocessing

### 2.1.1 API-retrieved Data Preprocessing (rental price)

For API data rental price preprocessing, please see `/notebooks/Preprocessing/API_prepro.ipynb`. We kept the integer only for the rental price. This notebook also converted the API dataset to the same format as the Web Scraped dataset for future concatenation. 
### 2.1.2 Web-Scraping-retrieved Data Preprocessing (rental price, outlier detection for all features)

For Web Scraping + API data preprocessing please see `/notebooks/Preprocessing/History_prepro.ipynb`. We firstly cleaned Web-Scraped data's rental price and then combined it with API datasets. We classified the whole datset and re-saved them by year. This is because, there may be inflations every year and the variance of rental price calculated year by year may be more reasonable.

For number of rooms, we viewed the boxplot and mannually confirmed deleted some inituive outliers (large number of rooms, very low price). For the location (latitude and longitude), we ammended 3 badly scrapped location data. 

For the rental price, we removed outliers year by year. For each year, we removed the rental price vlaues out side of the 3 standard deviation. Each year, arounf 1 to 3 % of data were removed as outliers. Hence we suggest it is a reasonable outlier removal appraoch.

### 2.1.2 Adding SA2 Code for Cleaned Data
[Need to complete later]

## 2.2 External Dataset Preprocessing
[Need to complete later]

## 2.3 Data Merging
[Need to complete later]

# 3. Data Analysis

## 3.1 Property Data Preliminary Analysis
[Need to complete later]
## 3.2 Property Data Geo Visual
[Need to complete later]

# 4. Modeling

