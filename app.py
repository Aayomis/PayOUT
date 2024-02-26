import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

#reading the data from csv
df = pd.read_csv('~/Downloads/Streamlit App/Transfer.csv')
df['time'] = pd.to_datetime(df['time'], unit='s')
df['date'] = df['time'].dt.date
st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
image  = Image.open('marasoft.jpeg')



col1, col2 = st.columns([0.1,0.9])
with col1:
    st.image(image, width=100)

html_title = """
    <style>
    .title-test {
    font-weight:bold;
    padding:5px;
    border-radius:6px;
    }
    </style>
    <center><h1 class="title-test"> Payout Success and Failure Rate</h1></center>
    """
with col2:
    st.markdown(html_title, unsafe_allow_html=True)


transaction_counts = df['status'].value_counts()


total_success = transaction_counts.get('success')
total_failed = transaction_counts.get('fail')
total_transactions = total_success + total_failed


percentage_success = ((total_success / total_transactions) * 100).round(2)
percentage_failed = ((total_failed / total_transactions) * 100).round(2)

data = {
    'Transaction Status': ['Success', 'Failure'],
    'Percentage (%)': [percentage_success, percentage_failed]
}
da = pd.DataFrame(data)

col1, col2 = st.columns(2)
df['date'] = pd.to_datetime(df['date'])

startDate = pd.to_datetime(df["date"]).min()
endDate = pd.to_datetime(df["date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))
with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["date"] >= date1) & (df["date"] <= date2)].copy()


col3, col4, col5 = st.columns([0.1,0.45, 0.55])
#with col3:
   # box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    #st.write(f"Last updated:   \n{box_date}")


with col4:
    fig = px.bar(da, x = "Transaction Status", y = "Percentage (%)", title = "Success and Failure Rate for the Week",
                  hover_data= ["Percentage (%)"], text='Percentage (%)',template= "gridon", height=500, color = 'Transaction Status',range_y=[0, 100])
    st.plotly_chart(fig, use_container_width=True)
_, view1, dwn1, view2, dwn2 = st.columns([0.15, 0.20, 0.20, 0.20, 0.20])
with view1:
    expander = st.expander("Rate of Transactions")
    data = da
    expander.write(data)
with dwn1:
    st.download_button("Get Data", data = data.to_csv().encode("utf-8"), 
                       file_name = "Success and Failure rate for the week.csv", mime = "text/csv")
    

grouped_data = df.groupby(['date', 'status']).size().unstack(fill_value=0)
grouped_data['total'] = grouped_data.sum(axis=1)
grouped_data['percentage_success'] = (grouped_data['success'] / grouped_data['total']) * 100
grouped_data['percentage_failed'] = (grouped_data['fail'] / grouped_data['total']) * 100

visualization_data = pd.DataFrame({
    'Date': grouped_data.index,
    'Percentage Success': grouped_data['percentage_success'].round(1),
    'Percentage Failed': grouped_data['percentage_failed'].round(1)
})

vn_data = visualization_data.reset_index(drop=True)
df_melted = pd.melt(vn_data, id_vars=['Date'], value_vars=['Percentage Success', 'Percentage Failed'],
                    var_name='Transaction Status', value_name='Percentage (%)')
with col5:
    fig1 = px.bar(df_melted, x='Date', y='Percentage (%)', color='Transaction Status',
             title='Success and Failure Rate per day', hover_data=['Percentage (%)'],text='Percentage (%)',
             template='gridon', height=500, range_y=[0, 100])

    st.plotly_chart(fig1, use_container_width=True)
with view2:
    expander = st.expander("Rate of Transactions per day")
    data = vn_data
    expander.write(data)
with dwn2:
    st.download_button("Get Data", data = data.to_csv().encode("utf-8"), 
                       file_name = "Success and Failure rate per day.csv", mime = "text/csv")
st.divider()

# create a tree map based on userId and amount
st.subheader("Hierarchical view of payout amount by userID")
fig3 = px.treemap(df, path = ['userId','status'], values= "amount", hover_data=["amount"], color ='status')
fig3.update_layout(width= 800, height = 650)
st.plotly_chart(fig3, use_container_width= True)