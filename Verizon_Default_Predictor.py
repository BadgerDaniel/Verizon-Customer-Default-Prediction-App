#!/usr/bin/env python
# coding: utf-8




#import will2live
import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler








model=pickle.load(open('xgb_model_verizon.pkl','rb'))



def get_credit_score_bin(given_score):
    # bin the credit score
    if given_score >= 300 and given_score < 362:
        return 0
    elif given_score >= 362 and given_score < 424:
        return 1
    elif given_score >= 424 and given_score < 486:
        return 2
    elif given_score >= 486 and given_score < 548:
        return 3
    elif given_score >= 548 and given_score < 610:
        return 4
    elif given_score >= 610 and given_score < 672:
        return 5
    elif given_score >= 672 and given_score < 734:
        return 6
    elif given_score >= 734 and given_score < 796:
        return 7
    elif given_score >= 796:
        return 8


# In[4]:


def get_model_prediction(df):
    prediction = model.predict(df)[0]
    return "Predicted to Pay" if prediction == 0 else "Predicted to Default"


# In[5]:


#!pip freeze > requirements_verizon_default_tool.txt


# In[6]:



st.title('Customer Default Predictor')

# the inputs here 
age = st.number_input('Age', min_value=18, max_value=100, value=30)
gender = st.selectbox('Gender', ['M', 'F'])
price = st.number_input('Price', value=0.0)
down_payment = st.number_input('Down Payment', value=0.0)
payment_type = st.selectbox('Payment Type', ['Credit Card', 'Cash', 'Check', 'Debit Card'])



credit_score_option = st.radio('Credit Score Option', ['Enter exact score',
                                                       'Select score range'])

if credit_score_option == 'Enter exact score':
    credit_score = st.number_input('Credit Score', min_value=300, max_value=850, value=550)
else:
    credit_score_range = st.selectbox('Credit Score Range', ['300-399',
                                                             '400-499',
                                                             '500-599',
                                                             '600-699',
                                                             '700-799',
                                                             '800-850'])
    credit_score = int(credit_score_range.split('-')[0])



payment_option = st.radio('Payment Plan Options', ['Set Monthly Payment',
                                                   'Set Number of Months'])

if payment_option == 'Set Monthly Payment':
    monthly_payment = st.number_input('Monthly Payment', min_value=0.0, value=0.0)
    month_due = (price - down_payment) / monthly_payment if monthly_payment else 0
    
else:
    
    month_due = st.number_input('Number of Months', min_value=0, value=0)
    monthly_payment = (price - down_payment) / month_due if month_due else 0

if st.button('Submit'):
    credit_bin = get_credit_score_bin(credit_score)
    data = {
        'price': [price],
        'downpmt': [down_payment],
        'monthdue': [month_due],
        'payment_left': [price - down_payment],
        'monthly_payment': [monthly_payment],
        'credit_score': [credit_bin],
        'age': [age],
        'gender_female': [gender == "F"],
        'gender_male': [gender == "M"],
        'pmttype_Cash': [payment_type == "Cash"],
        'pmttype_Check': [payment_type == "Check"],
        'pmttype_Credit Card': [payment_type == "Credit Card"],
        'pmttype_Debit Card': [payment_type == "Debit Card"]
    }
    df = pd.DataFrame(data)
    result = get_model_prediction(df)
    st.success(f'Result: {result}')


# In[6]:





# In[6]:





# In[ ]:




