from fastapi import FastAPI, Body
from fastapi.encoders import jsonable_encoder
from mangum import Mangum
from pydantic import BaseModel, Field
from joblib import load
import numpy as np

class MEAN_STD(BaseModel):
    Mean: float
    STD: float

class Item(BaseModel):
    Model: str
    HT: MEAN_STD 
    PPT: MEAN_STD 
    RRT: MEAN_STD 
    RPT: MEAN_STD 




app = FastAPI()
handler = Mangum(app)

classifier = {
    "SVM": load('svm.joblib'),
    "RF" : load('rf_clf.joblib'),
    "XGB" : load('xgb_clf.joblib')
}



@app.post("/")
async def add_book(req: Item):
    json_req = jsonable_encoder(req)
    features = np.array([[json_req['HT']['Mean'] , json_req['HT']['STD'],
        json_req['RPT']['Mean'],json_req['RPT']['Mean'],
        json_req['PPT']['Mean'],json_req['PPT']['Mean'],
        json_req['RRT']['Mean'],json_req['RRT']['Mean'],
    ]], dtype=np.float32)

    
    user_class = classifier[json_req['Model']].predict(features)

    return {"class": f'{user_class[0]+1}'}


