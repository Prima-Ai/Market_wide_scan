from fastapi import FastAPI,HTTPException
from pydantic import BaseModel 
from market_wide_scan import market_wide_scan

scanner = market_wide_scan()

app = FastAPI()

class Symbol(BaseModel):
    symbol:str

class Paras(BaseModel):
    NOD:str
    MA:int
    column_name:str
    
    
@app.get('/get_data')
async def get_data():
    try:
        scanner.collect_data()
        return "data collected"
    except Exception as e:
        raise HTTPException(status_code=401,detail=str(e))

@app.get('/get_paths')
async def get_paths():
    try:
        scanner.get_csv_file_paths()
        return "retrived paths sucessfully"
    except Exception as e:
        raise HTTPException(status_code=402,detail=(str(e)))

@app.post('/give parameters')
async def get_paras(para:Paras):
    try:
        result = scanner.get_paras(para.NOD,para.MA,para.column_name)
        return {"message": "Processing", "result": result}
    except Exception as e:
        raise HTTPException(status_code=403,detail=str(e))

@app.post('/get result')    
async def get_results(input_data:Symbol):
    try:
        result = scanner.get_results(input_data.symbol)
        return {'result':result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))