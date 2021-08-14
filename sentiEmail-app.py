import os
import funcs as main
import numpy as np
import pandas as pd
import streamlit as st
import datetime
import db_connect as db


# load in database
table_name = "sentiment"
df = db.connect(table_name)
# set up customer list
new_customer_lst = []
customer_lst = df['customer'].unique()
customer_lst = np.sort(np.append(customer_lst, values='All'))

# INTRO
st.title('Customer Sentiment Dashboard')
st.markdown("""
    The following dashboard analyses and displays customer sentiment towards the organisation.

    To add a new email to the database click the button below!
""")

# add email button
if st.checkbox('Add email'):
    st.sidebar.markdown('**Add customer email**')
    # input locations
    if st.sidebar.checkbox('Add customer'):
        customer_add = st.sidebar.text_input("Customer")
    else:
        customer_lst_copy = list(customer_lst.copy())
        customer_lst_copy.remove('All')
        customer_add = st.sidebar.selectbox('Customer', customer_lst_copy)
    date_add = st.sidebar.date_input("Email date", value=datetime.date.today())
    
    email = st.sidebar.text_area("Copy and paste email here")
    st.sidebar.caption('* Only copy and paste body of email, remove signature and greeting!')
    # st.write("TEMP HOLDING FOR UPLOAD BUTTON")
    pressed = st.sidebar.button('Add')
    if pressed:
        scores = main.run(email)
        st.sidebar.title("Results")
        sentiment = main.sentiment_func(scores)
        st.sidebar.markdown(f'The overall sentiment is **{sentiment}**!\n\n')
        st.sidebar.write(pd.DataFrame.from_dict(scores, orient="index"))
        # create dataframe
        add_dict = {
            'date': date_add,
            'customer': customer_add,
            'negative': scores['neg'],
            'neutral': scores['neu'],
            'positive': scores['pos'],
            'compound': scores['compound'],
            'overall': sentiment  
        }
        add_df = pd.DataFrame(data=add_dict, index=[0])
        df = df.append(add_df, ignore_index=True)
        final_row = df.iloc[[-1][:]]
        db.append_email(table_name, final_row)
        
        # display success message
        st.sidebar.success("Successfully added sentiment to database!")


# DASHBOARD
col1, col2, col3 = st.columns(3)
# set up date inputs
###############################
df['date'] = pd.to_datetime(df['date']).dt.date
start_date_datetime = min(df['date'])
###############################
start_date = col1.date_input("Start date", value=start_date_datetime)  # earliest dates
end_date = col2.date_input("End date", value=datetime.date.today())

placeholder = col3.empty()  # makes placeholder, can all a st func to fill
# placeholder.selectbox("View customer", customer_lst)
view_customer = placeholder.selectbox("View customer", customer_lst)

# return data for selected dates
df_scores = df
mask = (df_scores['date'] >= start_date) & (df_scores['date'] <= end_date)
df_scores = df.loc[mask]
# return data for selected customer
if view_customer == 'All':
    df_scores = df_scores
else:
    df_scores = df.loc[df['customer']==view_customer]
# earliest email date
earliest_date = min(df_scores['date'])
st.caption(f"Earliest email from {view_customer}: {earliest_date}")

# create total positive, negative and neutral
total_series = df_scores['overall'].value_counts(normalize=True) * 100
total_series = total_series.to_dict()

# plot total scores
st.markdown("""---""")
st.markdown(f"**Total customer sentiment - {view_customer}**")
fig_total = main.plot_totals_px(total_series)
st.write(fig_total)

# tidy up data frame into scores func input
df_scores = df_scores.drop(columns=['date', 'customer', 'overall'])
df_scores = np.mean(df_scores, axis=0)
scores = df_scores.to_dict()
# create plot of scores
st.markdown(f"**Average sentiment scores - {view_customer}**")
fig = main.plot_scores_px(scores)
st.write(fig)
