# Importing libraries
import streamlit as st
import pandas as pd
from linkedin_job_application_analysis import process_linkedin_job_app_data, display_kpis, display_top_10_insights, display_daily_weekly_monthly_insights
import datetime

# ---------------------------------------------------------------------------------------------------------------------------------------------------

# Setting the page title and layout
st.set_page_config(page_title = 'LinkedIn Job Application Tracker',
                   page_icon=None,
                   layout = 'centered', initial_sidebar_state="auto")

# ---------------------------------------------------------------------------------------------------------------------------------------------------

# Setting the sidebar options
options = ['About','LinkedIn Job Application Tracker']
selected_option = st.sidebar.selectbox('Select an option', options)

st.sidebar.write("\n\n\n")
st.sidebar.write("\n\n\n")

# ---------------------------------------------------------------------------------------------------------------------------------------------------

# If the selected option is "About", display the 'About the app' page
if selected_option == 'About':

    # Setting title of the page
    st.markdown('## About LinkedIn Job Application Tracker')

    st.markdown('#### Goal:')

    st.write('''The LinkedIn Job Application Tracker is a tool deployed to help job seekers keep track of their job applications on LinkedIn. 
                It allows users to track their progress, and get insights into their job search. 
                The goal of the tool is to help job seekers stay organized throughout their job search process.''')

    st.markdown('#### How to use:')
    
    st.write('''**Note** The LinkedIn Job Applications will automatically track easy applied jobs. However, to
                track applications that you apply for on external career websites or job boards through LinkedIn, 
                you will need to manually mark them as "Applied".
                \n 1. Go to the "LinkedIn Job Application Tracker" page.
                \n 2. Click on the "Browse files" button.
                \n 3. Select the CSV file that contains your job application data.
                \n 4. The data will be uploaded, processed, and displayed in the "LinkedIn Job Application Tracker" page.''')

    st.markdown('#### Links:')

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write('##### [Github](https://github.com/VishakBaburaj/)')

    with col2:
        st.write('##### [LinkedIn](https://www.linkedin.com/in/vishakbaburaj/)')

    with col3:
        st.write('##### [Portfolio](https://vishakbaburaj.carrd.co/)')

# ---------------------------------------------------------------------------------------------------------------------------------------------------

# If the selected option is "LinkedIn", display the "LinkedIn Job Application Tracker" page
elif selected_option == 'LinkedIn Job Application Tracker':

    # Setting title of the page
    st.markdown('## LinkedIn Job Application Tracker')

    # Disabling the warning message
    st.set_option('deprecation.showfileUploaderEncoding', False)

    # Checkbox to load sample data
    load_sample_data_checkbox = st.sidebar.checkbox('Load Sample Data')

    # Reading sample csv data
    df = pd.read_csv("sample_data.csv") 

    # If the sample data checkbox is selected upload the sample data
    if load_sample_data_checkbox:
        uploaded_file = df  # Display the sample data in the app

    # If the sample data checkbox is not selected upload the csv data
    elif uploaded_file := st.sidebar.file_uploader('Choose the Job Application CSV file', type = 'csv'):

        # Reading the CSV file
        uploaded_file = pd.read_csv(uploaded_file)

    elif st.markdown('#### Upload Job Application CSV file or Load Sample Data'):

        st.markdown('''This dashboard is designed to work exclusively with the Job Application data from LinkedIn. 
                       \n To access your data, you will need to request an archive from LinkedIn by following the instructions 
                       provided in this [link](https://www.linkedin.com/help/linkedin/answer/a1339364/downloading-your-account-data?lang=en).
                       \n It usually takes approximately 24 hours to receive your data. However, in the interim, 
                       you can experiment with the job application sample data that is readily available on the app. 
                       Simply load the sample data by clicking on the "Load Sample Data" checkbox in the sidebar.''')

    # When either data has been input
    if uploaded_file is not None:

        # Precessing the data
        data = process_linkedin_job_app_data(uploaded_file)

        st.sidebar.subheader('Filter dates')

        # Determining the earliest date in the data
        min_date = data['Date'].min().date()

        # Adding a date filter
        start_date = st.sidebar.date_input("Select start date", value=min_date)
        end_date = st.sidebar.date_input("Select end date")

        # Converting start_date and end_date to datetime objects
        start_date = datetime.datetime.combine(start_date, datetime.datetime.min.time())
        end_date = datetime.datetime.combine(end_date, datetime.datetime.max.time())

        # Apply date filter to the data frame
        filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]

# # ---------------------------------------------------------------------------------------------------------------------------------------------------

        display_kpis(filtered_data)
        display_top_10_insights(filtered_data)
        display_daily_weekly_monthly_insights(filtered_data)

# # ---------------------------------------------------------------------------------------------------------------------------------------------------

