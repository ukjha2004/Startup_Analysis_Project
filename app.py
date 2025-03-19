import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.set_page_config(layout='wide',page_title='StartUp Analysis')
df =pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_overall_analysis():
    st.title('Overall Analysis')

    total = round(df['amount'].sum())

    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]

    avg_funding = df.groupby('startup')['amount'].sum().mean()

    num_startups = df['startup'].nunique()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric('Total', str(total) + ' Cr')
    with col2:
        st.metric('Max', str(max_funding) + ' Cr')

    with col3:
        st.metric('Avg', str(round(avg_funding)) + ' Cr')

    with col4:
        st.metric('Funded Startups', num_startups)

    st.header('MoM graph')
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'], temp_df['amount'])

    st.pyplot(fig3)

def load_investor_details(investor):
    st.title(investor)
    last5_df =df[df['investors'].str.contains(' investor')].head()[['date','startup','vertical','city','round','amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)
    big_series = df[df['investors'].str.contains(' investor')].groupby('startup')['amount'].sum().sort_values(
        ascending=False).head()
    st.subheader('Biggest Investments')
    fig, ax = plt.subplots()
    ax.bar(big_series.index, big_series.values)
    st.pyplot(fig)

    col1,col2=st.columns(2)



    with col1:
        vertical_series=df[df['investors'].str.contains(' investor')].groupby('startup')['amount'].sum().sort_values(
            ascending=False)
        st.subheader('Sectors invested in')
        fig, ax = plt.subplots()
        ax.pie(vertical_series,labels=vertical_series.index,autopct="%0.01f%%")

        st.pyplot(fig)
    with col2:
        round_series = df[df['investors'].str.contains(' investor')].groupby('round')['amount'].sum().sort_values(
            ascending=False)
        st.subheader('Stages invested in')
        fig2, ax2 = plt.subplots()
        ax2.pie(round_series, labels=round_series.index, autopct="%0.01f%%")

        st.pyplot(fig2)
    city_series=df[df['investors'].str.contains(' investor')].groupby('city')['amount'].sum().sort_values(ascending=False)
    st.subheader('Cities invested in')
    fig3, ax3 = plt.subplots()
    ax3.pie(city_series, labels=city_series.index, autopct="%0.01f%%")

    st.pyplot(fig3)


    df['year'] = df['date'].dt.year
    year_series=df[df['investors'].str.contains(' investor')].groupby('year')['amount'].sum()
    st.subheader('Year on Year Investments')
    fig4, ax4 = plt.subplots()
    ax4.plot(year_series.index,year_series.values)

    st.pyplot(fig4)

st.sidebar.title('Startup Funding Anaylsis')
option=st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])
if option == 'Overall Analysis':
    load_overall_analysis()

elif option == 'Startup':
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')

else:
    selected_investor= st.sidebar.selectbox('Select Startup',sorted(set(df['investors'].str.split(',').sum())))
    btn2=st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)



