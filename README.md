# Aggregator of advertisements
An online system for aggregating and managing advertisements, facilitating efficient categorization and organization
## Features
*  Automated scraping of used car details from AutoRia using Selenium and BeautifulSoup.
* Implementation of endpoints or displaying parsed information, retrieving information by ID, displaying static information, and filtering information for a specific period.
*Automatic API documentation generation for http://127.0.0.1:8000/docs

##  Installation:
Python3 must be already installed

### 1.Clone the Repository:
```shell
git clone https://github.com/svitlana-savikhina/aggregator-of-advertisements.git
cd aggregator-of-advertisements
```
### 2.Environment Configuration: 
Create a .env file in the root directory with the following content, define environment variables in it (example you can find in .env_sample)
```shell
USERNAME=USERNAME
FULL_NAME=FULL_NAME
EMAIL=EMAIL
PASSWORD=PASSWORD
DISABLED=DISABLE
```
### 3.Activate venv:
```shell
python -m venv venv
source venv/bin/activate (Linux/Mac)
venv\Scripts\activate (Windows)
```
### 4.Install Dependencies:
```shell
pip install -r requirements.txt
```

### 5.Run:
```shell
uvicorn aggregator_of_advertisements.main:app --reload
```
