# ad-test
Exposing SQL db as HTTP api    
    
Usage:    
1. Add project to pythonpath    
    `export PYTHONPATH="${PYTHONPATH}:/my/other/path"`
2. Install dependencies:    
    `pip install -r requirements.txt`
3. (Optional) Run *the test*    
    `pytest test/`
4. Run app    
    `uvicorn server:app --reload`    


    
URLs for common usecases:    
1. Show the number of impressions and clicks that occurred before the 1st of June 2017, broken down by channel and country, sorted by clicks in descending order.    
    
    http://127.0.0.1:8000/?col=impressions&col=clicks&date_to=2017-06-01&group_col=channel&group_col=country&order_by=clicks
    
2. Show the number of installs that occurred in May of 2017 on iOS, broken down by date, sorted by date in ascending order.    
    
    http://127.0.0.1:8000/?date_from=2017-05-01&date_to=2017-05-31&group_col=date&order_by=date&desc=false
    
3. Show revenue, earned on June 1, 2017 in US, broken down by operating system and sorted by revenue in descending order.    
    http://127.0.0.1:8000/?date_from=2017-06-01&date_to=2017-06-01&group_col=os&order_by=revenue    
    
4. Show CPI and spend for Canada (CA) broken down by channel ordered by CPI in descending order. Please think carefully which is an appropriate aggregate function for CPI.    
    
    http://127.0.0.1:8000/?metric=cpi&group_col=country&order_by=cpi    
    
