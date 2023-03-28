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
    "types": types,
    "amount": amount,
    "oldbalanceorig": oldbalanceorg,
    "newbalanceorig": newbalanceorg,
    "oldbalancedest": oldbalancedest,
    "newbalancedest": newbalancedest,
    "isflaggedfraud": isflaggedfraud
    }


    st.write(f"""### These are the details:\n

    Client Id is: {step}\n

                """)

    res = re.post(f"https://creditcard2-production.up.railway.app/predict",json=values)
    
    prediction = res

    st.write(prediction)
    st.write(type(prediction))
    
#     pred = prediction["prediction"]

#     probability_value_0 = round(prediction["probability_0"] * 100,2)
#     probability_value_1 = round(prediction["probability_1"] * 100,2)


    st.header(f'*Résultat de la demande de crédit pour le client {client_id}*')

    st.write(pred)
    st.write(type(pred))

    st.write(f"""### Result score is: {res}.""")
