from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from market_wide_scan import market_wide_scan

scanner = market_wide_scan()

app = FastAPI()

# Define the origins that should be allowed to make requests to your API
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",  # Add your frontend domain if different
    "https://yourdomain.com",  # Replace with your actual domain
    "http://localhost:5173"
]

# Add the CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # Allow cookies to be included in requests
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

class Symbol(BaseModel):
    symbol: str

class Paras(BaseModel):
    NOD: str
    MA: int
    column_name: str

@app.get('/get_data')
async def get_data():
    try:
        scanner.collect_data()
        return "data collected"
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@app.get('/get_paths')
async def get_paths():
    try:
        scanner.get_csv_file_paths()
        return "retrieved paths successfully"
    except Exception as e:
        raise HTTPException(status_code=402, detail=str(e))

@app.post('/give_parameters')
async def get_paras(para: Paras):
    try:
        result = scanner.get_paras(para.NOD, para.MA, para.column_name)
        return {"message": "Processing", "result": result}
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

@app.post('/get_result')
async def get_results(input_data: Symbol):
    try:
        result = scanner.get_results(input_data.symbol)
        return {'result': result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
