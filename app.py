from fastapi import FastAPI, File, Query, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse, PlainTextResponse
import uvicorn
import joblib
import numpy as np
from pydantic import BaseModel



app = FastAPI(
    title="Credit Card Fraud Detection API",
    description="""An API that utilises a Machine Learning model that detects if a credit card transaction is fraudulent or not based on the following features: hours, amount, transaction type etc.""",
    version="1.0.0", debug=True)


model = joblib.load('credit_fraud.pkl')

@app.get("/", response_class=PlainTextResponse)
async def running():
  note = """
Credit Card Fraud Detection API 🙌🏻

Note: add "/docs" to the URL to get the Swagger UI Docs or "/redoc"
  """
  return note

favicon_path = 'favicon.png'
@app.get('/favicon.png', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)
																	
class fraudDetection(BaseModel):
    step:int
    types:int
    amount:float	
    oldbalanceorig:float	
    newbalanceorig:float	
    oldbalancedest:float	
    newbalancedest:float	
    isflaggedfraud:float


@app.post('/predict')
def predict(data : fraudDetection):
                                                                                                                                                                                                                                
    features = np.array([[data.step, data.types, data.amount, data.oldbalanceorig, data.newbalanceorig, data.oldbalancedest, data.newbalancedest, data.isflaggedfraud]])
#     model = joblib.load('credit_fraud.pkl')

#     predictions = model.predict(features)
#     if predictions == 1:
#         return {"Bad"}
#     elif predictions == 0:
#         return {"not Bad"}

    id = data.step

    if id not in clients_id:
        raise HTTPException(status_code=404, detail="client's id not found")
    
    else:
        
        
        pipe_prod = joblib.load('LGBM_pipe_version7.pkl')
    
        values_id_client = df_test_prod_request.loc[[id]]
       
        # Définir le best threshold
        prob_preds = pipe_prod.predict_proba(values_id_client)
        
        #Fast_API_prob_preds
        threshold = 0.332# definir threshold ici
        y_test_prob = [1 if prob_preds[i][1]> threshold else 0 for i in range(len(prob_preds))]
        
       
        return {
            "prediction": y_test_prob[0],
            "probability_0" : prob_preds[0][0],
            "probability_1" : prob_preds[0][1],}
