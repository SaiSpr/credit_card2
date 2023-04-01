#-----------------------#
# IMPORT DES LIBRAIRIES #
#-----------------------#

import streamlit as st
import joblib
import plotly.graph_objects as go
import matplotlib as plt
import plotly.express as px
st.set_option('deprecation.showPyplotGlobalUse', False)
import shap
import requests as re
import numpy as np
import pickle
import json
import pandas as pd


st.title("Bank Loan Detection Web App")

st.image("image.jpg")



st.sidebar.header('Input Features of The Transaction')

sender_name = 1
receiver_name = 2

types = 4

    
amount = 4
oldbalanceorg = 5
newbalanceorg= 6
oldbalancedest=7
newbalancedest= 8
isflaggedfraud = 0




  
st.title("****Calculating the probability that a customer will repay their credit or not****")  
  
 
# Read 
list_file = open('cols_shap_local.pickle','rb')
cols_shap_local = pickle.load(list_file)
print(cols_shap_local)



#df_test_prod = pd.read_csv('df_test_ok_prod_100.csv', index_col=[0])
df_test_prod = pd.read_csv('df_test_ok_prod_100_V7.csv', index_col=[0])
df_test_prod['LOAN_DURATION'] = 1/df_test_prod['PAYMENT_RATE']
df_test_prod.drop(columns=['TARGET'], inplace=True)
df_test_prod_request  = df_test_prod.set_index('SK_ID_CURR')



df_train = pd.read_csv('df_train_prod_1.csv', index_col=[0])
df_train['LOAN_DURATION'] = 1/df_train['PAYMENT_RATE']

# Liste clients id sidebar 
list_client_prod = df_test_prod['SK_ID_CURR'].tolist()
client_id = st.sidebar.selectbox("Client Id list",list_client_prod)
client_id = int(client_id)

st.header(f'Credit request result for client {client_id}')

# st.write(pred)
# st.write(type(pred))
# if pred == 1:
#   st.error('Crédit Refusé')
    
step = client_id  
    
    
    
    
  
  
  



  
  
if st.button("Detection Result"):
    values = {
    "step": step,
    }


    st.write(f"""### These are the details:\n

    Client Id is: {step}\n
    
    type of client_id is : {type(step)}
    
    Values is : {values}
    
    Values tyep is : {type(values)}

                """)

    res = re.post( url ="https://creditcard2-production.up.railway.app/predict", data = json.dumps(values))

    json_str = json.dumps(res.json())
    
        
    st.write(json_str)
    st.write(type(json_str))
    resp = json.loads(json_str)
    
#     prediction = res

    st.write(res)
    st.write(type(res))
    
    st.write(resp)
    st.write(type(resp))
    
    pred = prediction["prediction"]

    probability_value_0 = round(prediction["probability_0"] * 100,2)
    probability_value_1 = round(prediction["probability_1"] * 100,2)


    st.header(f'*Résultat de la demande de crédit pour le client {client_id}*')

    st.write(pred)
    st.write(type(pred))
    if pred == 1:
      st.error('Crédit Refusé')
      option_1 = {
            "tooltip": {"formatter": "{a} <br/>{b} : {c}%"},
            "series": [
                {
                    "name": "Pressure",
                    "type": "gauge",
                    "axisLine": {
                        "lineStyle": {
                            "width": 10,
                        },
                    },
                    "progress": {"show": "true", "width": 10},
                    "detail": {"valueAnimation": "true", "formatter": "{value}"},
                    "data": [{"value": probability_value_1, "name": "Probabilité %"}],
                }
            ],
        }

      st_echarts(options=option_1, width="100%", key=0)
      st.header(f'*Les données qui ont le plus influencé le calcul de la prédiction pour le client {client_id}*')

      explain_plot(client_id, pred)
    else:
        st.success('Crédit Accordé')
        option = {
            "tooltip": {"formatter": "{a} <br/>{b} : {c}%"},
            "series": [
                {
                    "name": "Pressure",
                    "type": "gauge",
                    "axisLine": {
                        "lineStyle": {
                            "width": 10,
                        },
                    },
                    "progress": {"show": "true", "width": 10},
                    "detail": {"valueAnimation": "true", "formatter": "{value}"},
                    "data": [{"value": probability_value_0, "name": "Probabilité %"}],
                }
            ],
        }

        st_echarts(options=option, width="100%", key=0)

        st.header(f'*Les données qui ont le plus influencé le calcul de la prédiction pour le client {client_id}*')
        explain_plot(client_id, pred)



    st.header("*Les variables les plus significatives par ordre décroissant et qui ont un pouvoir prédictif élevé.*")

    st.image("Shap_features_global.png", use_column_width=True)

#     st.header(f'*Résultat de la demande de crédit pour le client {client_id}*')



#     st.write(f"""### Result score is: {res}.""")
