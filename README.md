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

If you want to see Domain's data retrieved using Web Scrping, please run `/notebooks/Scraping/BS_Scraping.ipynb`. However, these data will not be used in preliminary analysis or modeling to avoid redundancy.

## 1.2 External Dataset Downloading
We retrieved data of external attributes, such as crime cases, total personal income, population, GDP from `abs.gov.au` and `hcrimestatistics.vic.gov.au`
[Need to complete later]

# 2. Data Preprocessing

## 2.1 Property Dataset Preprocessing

### 2.1.1 API-retrieved Data Preprocessing (rental price)

For API data rental price preprocessing, please see `/notebooks/Preprocessing/API_prepro.ipynb`. We kept the integer only for the rental price. This notebook also converted the API dataset to the same format as the Web Scraped dataset for future concatenation. 
### 2.1.2 Web-Scraping-retrieved Data Preprocessing (rental price, outlier detection for all features)

For Web Scraping + API data preprocessing please see `/notebooks/Preprocessing/History_prepro.ipynb`. We firstly cleaned Web-Scraped data's rental price and then combined it with API datasets. We classified the whole datset and re-saved them by year. This is because, there may be inflations every year and the variance of rental price calculated year by year may be more reasonable.

For number of rooms, we viewed the boxplot and mannually confirmed deleted some inituive outliers (large number of rooms, very low price). For the location (latitude and longitude), we ammended 3 badly scrapped location data. 

For the rental price, we removed outliers year by year. For each year, we removed the rental price vlaues out side of the 3 standard deviation. Each year, arounf 1 to 3 % of data were removed as outliers. Hence we suggest it is a reasonable outlier removal appraoch.

### 2.1.3 Adding SA2 Code for Cleaned Data
[Need to complete later]

### 2.1.4 Adding Distance/Time to Places/CBD from Clean Property Data (Open Route Servive API)
See `/notebooks/Preprocessing/ors_iteration_add_rentalDistance`. At each iteration, a yearly subset of places csv and a year subset of property csv between 2013-2021 were called out and merged based on SA2 Code. Then, a list of clients registered with unique API keys was used to request distance/time for each merged yearly dataset. 

In the add_distance_time function, the requests were conducted by iterating SA2 codes. All properties in current SA2 code were computed as sources, each of which was mapped to all places defined by this SA2 code. So in total, (size of sources * count of places) routes of distances/time were computed for each SA2 district. 

For route number greater than 3500 which was prohibited by ORS, a slicing method that divided sources into smaller subsets based on the factor, by which route number exceeded 3500, replaced the original requests. Through this, the restriction could be solved by making additional calls for reduced sublists. For example for 206 sources * 35 places = 7210 > 3500, exceeding by a factor of 2, sources list was divided into \[0-68), \[68-136) and \[136-206) sublists, and 3 requests with route number 68 * 35, 68 * 35 and 70 * 35 were called to ensure all 7210 data was retrieved.

For exception such as exceeding API quota during processing, a back up API key with a capacity of 2500 calls was switched into to handle the exception. For other keys, the individual quota of 500 was mostly sufficient to process each merged yearly dataset given there were fewer than 500 SA2 codes in each year (except for 502 in 2022).  

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

