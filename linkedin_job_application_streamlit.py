# Importing libraries
import streamlit as st
import pandas as pd
from linkedin_job_application_analysis import process_linkedin_job_app_data, display_kpis, display_top_10_insights, display_daily_weekly_monthly_insights
import datetime
from streamlit_option_menu import option_menu

# ---------------------------------------------------------------------------------------------------------------------------------------------------

# Setting the page title and layout (make sure this is the first Streamlit command)
st.set_page_config(page_title = 'LinkedIn Job Application Tracker',
                   page_icon=None,
                   layout = 'centered', initial_sidebar_state="auto")

# ---------------------------------------------------------------------------------------------------------------------------------------------------

# Setting the sidebar options
with st.sidebar:
    selected_option = option_menu(
        menu_title = None,
        options = ['About', 'Application Tracker'],
        icons=['house', 'briefcase'],
        menu_icon='cast',
        default_index=0
    )

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
                \n 1. Go to the "Application Tracker" page.
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

# If the selected option is "Application Tracker", display the "LinkedIn Job Application Tracker" page
elif selected_option == 'Application Tracker':

    # Setting title of the page
    st.markdown('## LinkedIn Job Application Tracker')

    # Disabling the warning message
    st.set_option('deprecation.showfileUploaderEncoding', False)

    # Checkbox to load sample data
    load_sample_data_checkbox = st.sidebar.checkbox('Load Sample Data')

    # Reading sample csv data
    if load_sample_data_checkbox:
        df = pd.read_csv("sample_data.csv")  # Assuming sample_data.csv is in the same directory.

    # If the sample data checkbox is not selected, prompt for CSV upload
    uploaded_file = None
    if not load_sample_data_checkbox:
        uploaded_file = st.sidebar.file_uploader('Choose the Job Application CSV file', type='csv')

    if uploaded_file is not None:
        # Reading the uploaded file
        df = pd.read_csv(uploaded_file)

    # Show instructions if neither option is selected
    if uploaded_file is None and not load_sample_data_checkbox:
        st.markdown('''This dashboard works exclusively with job application data from LinkedIn.
                       \n You can download your LinkedIn data by following the instructions in this 
                       [link](https://www.linkedin.com/help/linkedin/answer/a1339364/downloading-your-account-data?lang=en).
                       \n Once you have the file, you can upload it by selecting the "Choose the Job Application CSV file" option.''')

    # Process data when uploaded
    if uploaded_file is not None or load_sample_data_checkbox:

        # Process the data
        data = process_linkedin_job_app_data(df)

        # Sidebar filters for date range
        st.sidebar.subheader('Filter by Date')

        # Determining the earliest date in the data
        min_date = data['Date'].min().date()

        # Sidebar date input
        start_date = st.sidebar.date_input("Select start date", value=min_date)
        end_date = st.sidebar.date_input("Select end date", value=data['Date'].max().date())

        # Converting the selected dates to datetime objects
        start_date = datetime.datetime.combine(start_date, datetime.datetime.min.time())
        end_date = datetime.datetime.combine(end_date, datetime.datetime.max.time())

        # Apply the date filter
        filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]

        # Display Key Performance Indicators (KPIs)
        display_kpis(filtered_data)

        # Display Top 10 Insights (Job roles and Companies)
        display_top_10_insights(filtered_data)

        # Display trends (daily, weekly, monthly)
        display_daily_weekly_monthly_insights(filtered_data)

        # Horizontal line and showing the filtered data
        st.write('---')

        st.write("###### Filtered Data:")
        st.write(filtered_data[['Date', 'Company Name', 'Job Title']])

# ---------------------------------------------------------------------------------------------------------------------------------------------------
