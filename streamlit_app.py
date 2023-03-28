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


st.title("Credit Card Fraud Detection Web App")

st.image("image.jpg")



st.sidebar.header('Input Features of The Transaction')

sender_name = st.sidebar.text_input("""Input Sender ID""")
receiver_name = st.sidebar.text_input("""Input Receiver ID""")
step = st.sidebar.slider("""Number of Hours it took the Transaction to complete: """)
types = st.sidebar.subheader(f"""
                 Enter Type of Transfer Made:\n\n\n\n
                 0 for 'Cash In' Transaction\n 
                 1 for 'Cash Out' Transaction\n 
                 2 for 'Debit' Transaction\n
                 3 for 'Payment' Transaction\n  
                 4 for 'Transfer' Transaction\n""")
types = st.sidebar.selectbox("",(0,1,2,3,4))
x = ''
if types == 0:
    x = 'Cash in'
if types == 1:
    x = 'Cash Out'
if types == 2:
    x = 'Debit'
if types == 3:
    x = 'Payment'
if types == 4:
    x =  'Transfer'
    
amount = st.sidebar.number_input("Amount in $",min_value=0, max_value=110000)
oldbalanceorg = st.sidebar.number_input("""Sender Balance Before Transaction was made""",min_value=0, max_value=110000)
newbalanceorg= st.sidebar.number_input("""Sender Balance After Transaction was made""",min_value=0, max_value=110000)
oldbalancedest= st.sidebar.number_input("""Recipient Balance Before Transaction was made""",min_value=0, max_value=110000)
newbalancedest= st.sidebar.number_input("""Recipient Balance After Transaction was made""",min_value=0, max_value=110000)
isflaggedfraud = 0
if amount >= 200000:
  isflaggedfraud = 1
else:
  isflaggedfraud = 0



  
  
  
 
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

st.header(f'*Résultat de la demande de crédit pour le client {client_id}*')

# st.write(pred)
# st.write(type(pred))
# if pred == 1:
#   st.error('Crédit Refusé')
    
    
    
    
    
    
  
  
  



  
  
if st.button("Detection Result"):
    values = {
    "step": client_id,
    "types": types,
    "amount": amount,
    "oldbalanceorig": oldbalanceorg,
    "newbalanceorig": newbalanceorg,
    "oldbalancedest": oldbalancedest,
    "newbalancedest": newbalancedest,
    "isflaggedfraud": isflaggedfraud
    }


    st.write(f"""### These are the transaction details:\n
    Sender ID: {sender_name}
    Receiver ID: {receiver_name}
    1. Number of Hours it took to complete: {step}\n
    2. Type of Transaction: {x}\n
    3. Amount Sent: {amount}$\n
    4. Sender Balance Before Transaction: {oldbalanceorg}$\n
    5. Sender Balance After Transaction: {newbalanceorg}$\n
    6. Recepient Balance Before Transaction: {oldbalancedest}$\n
    7. Recepient Balance After Transaction: {newbalancedest}$\n
    8. System Flag Fraud Status(Transaction amount greater than $200000): {isflaggedfraud}
                """)

    res = re.post(f"https://creditcard2-production.up.railway.app/predict",json=values)
    json_str = json.dumps(res.json())
    resp = json.loads(json_str)
    
    if sender_name=='' or receiver_name == '':
        st.write("Error! Please input Transaction ID or Names of Sender and Receiver!")
    else:
        st.write(f"""### The '{x}' transaction that took place between {sender_name} and {receiver_name} is {resp[0]}.""")
