# ad-test 
    
Usage:    
1. Add project to pythonpath    
    `export PYTHONPATH="${PYTHONPATH}:/my/other/path"`
2. Install dependencies:    
    `pip install -r requirements.txt`
3. Edit `src/config.py` and add (absolute) path to `dataset.csv`    
4. (Optional) Run *the test*    
    `pytest test/`
5. Run app    
    `uvicorn server:app --reload`    
