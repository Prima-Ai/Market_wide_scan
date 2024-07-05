from fastapi import FastAPI,HTTPException
from pydantic import BaseModel 
from market_wide_scan import market_wide_scan

scanner = market_wide_scan()

app = FastAPI()

class InputData(BaseModel):
    symbol:str
    # NOD:str
    # MA:int
    # column_name:str
@app.post('/get result')    
async def get_results(input_data:InputData):
    try:
        result = scanner.get_results(input_data.symbol)
        return {'result':result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))