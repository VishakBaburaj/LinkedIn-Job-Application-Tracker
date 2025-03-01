# Importing libraries
import pandas as pd
import streamlit as st
import altair as alt

#------------------------------------------------------------------------------------------------------------------------------------------------
# Processing the data
def process_linkedin_job_app_data(data):
    # Processing the data
    # Droping sensitive data
    data = data[['Application Date', 'Company Name', 'Job Title']]
    # Droping duplicate rows
    data = data.drop_duplicates(keep='first')
    # Splitting the date and time column into separate columns
    split_df = data['Application Date'].str.split(' ', expand=True)
    # Assigning new column names
    split_df.columns = ['Date', 'Time', 'AM/PM']
    # Replacing missing or null values with NaN
    split_df = split_df.replace('', pd.NA)
    # Concatenating the split DataFrame with the original DataFrame
    data = pd.concat([data, split_df], axis=1)
    # Droping the 'Application Date', 'Time' and 'AM/PM' columns in place
    data = data.drop(columns=['Application Date', 'Time', 'AM/PM'])
    # Converting the 'Date' column to a datetime data type
    data['Date'] = pd.to_datetime(data['Date'])
    # Droping the index from the DataFrame
    data = data.reset_index(drop=True)
    # Extracting weekday, month and year from Date into separate columns
    data['Weekday'] = data['Date'].dt.day_name()
    data['Month'] = data['Date'].dt.strftime('%B')
    data['Year'] = data['Date'].dt.year
    # Sort the dataframe by "Application Date"
    data = data.sort_values('Date')
    return data

#------------------------------------------------------------------------------------------------------------------------------------------------
# Displaying the KPIs
def display_kpis(data):
    #-----------------------------------------------------------------------------------------
    # Total jobs applied KPI
    total_jobs_applied = len(data)

    # Calculating the number of unique companies applied as a KPI in the second column
    unique_companies_applied = len(data['Company Name'].unique())
    #-----------------------------------------------------------------------------------------

    # Average jobs applied per day KPI
    # Calculating the number of days over which the jobs were applied
    num_days = (data['Date'].max() - data['Date'].min()).days + 1

    # Calculating the average jobs applied per week
    applications_per_week = total_jobs_applied // (num_days // 7)

    # Calculating the average jobs applied per month
    applications_per_month = total_jobs_applied // (num_days // 30)
    #-----------------------------------------------------------------------------------------

    st.write(f"###### Key metrics:")

    # a 3x3 grid the long way to display the KPIs
    col1, col2, col3 = st.columns(3)
    with col1:
        interview_calls_received = st.number_input('''Enter total jobs interviewed to calculate **Application Response Rate**:''', value=0, min_value=0)
    with col2:
        if total_jobs_applied > 0:
            application_response_rate = round((interview_calls_received / total_jobs_applied) * 100, 2)
            st.metric(f"**Application Response Rate:**", application_response_rate)
    with col3:
        st.metric(f"**Total Unique Companies Applied:**", unique_companies_applied)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(f"**Total Jobs Applied:**", total_jobs_applied)
    with col2:
        st.metric(f"**Average Jobs Applied Per Week:**", applications_per_week)
    with col3:
        st.metric(f"**Average Jobs Applied Per Month:**", applications_per_month)

    # Adding a horizontal line
    st.write('---')

#------------------------------------------------------------------------------------------------------------------------------------------------
# Displaying the top 10 insights
def display_top_10_insights(data):
    #-----------------------------------------------------------------------------------------
    # Selecting the job roles and companies
    top_10_options = ['Top 10 Job Roles Applied', 'Top 10 Companies Applied']
    selected_top_10_options = st.radio('###### Select an insight:', top_10_options, horizontal=False)

    #-----------------------------------------------------------------------------------------
    # Displaying the selected options
    if selected_top_10_options == 'Top 10 Job Roles Applied':
        # Grouping the data by job title and counting the number of occurrences
        jobs_applied = data.groupby('Job Title').size().reset_index(name='count')

        # Sorting the data by count in descending order and selecting the top 10 rows
        top_jobs_applied = jobs_applied.sort_values("count", ascending=False).head(10)

        # Creating the chart
        top_jobs_applied_chart = alt.Chart(top_jobs_applied).mark_bar().encode(
            x=alt.X('count:Q', title='Count of Jobs Applied'),
            y=alt.Y('Job Title:O', title='Job Titles', sort='-x'),
            color=alt.Color('count:Q', legend=None),
            tooltip=['Job Title:O', 'count:Q']
        )

        # Adding labels for the count of jobs applied
        top_jobs_applied_text = top_jobs_applied_chart.mark_text(
            align='left',
            baseline='middle',
            dx=5,
            fontSize=18
        ).encode(
            text='count:Q'
        )

        # Displaying the chart and the count of jobs applied
        st.altair_chart(top_jobs_applied_chart + top_jobs_applied_text, use_container_width=True)

        # Adding a horizontal line
        st.write('---')

    #-----------------------------------------------------------------------------------------
    elif selected_top_10_options == 'Top 10 Companies Applied':

        # Grouping the data by company name and counting the number of occurrences
        companies_applied = data.groupby('Company Name').size().reset_index(name='count')

        # Sorting the data by count in descending order and selecting the top 10 rows
        top_companies_applied = companies_applied.sort_values("count", ascending=False).head(10)

        # Creating the chart
        top_companies_applied_chart = alt.Chart(top_companies_applied).mark_bar().encode(
            x=alt.X('count:Q', title='Count of Companies Applied'),
            y=alt.Y('Company Name:O', title='Company Names', sort='-x'),
            color=alt.Color('count:Q', legend=None),
            tooltip=['Company Name:O', 'count:Q']
        )

        # Adding labels for the count of companies applied
        top_companies_applied_text = top_companies_applied_chart.mark_text(
            align='left',
            baseline='middle',
            dx=5,
            fontSize=18
        ).encode(
            text='count:Q'
        )

        # Displaying the chart and the count of companies applied
        st.altair_chart(top_companies_applied_chart + top_companies_applied_text, use_container_width=True)

        # Adding a horizontal line
        st.write('---')

#------------------------------------------------------------------------------------------------------------------------------------------------
# Displaying daily, weekly and monthly insights
def display_daily_weekly_monthly_insights(data):
    #-----------------------------------------------------------------------------------------
    # Selecting the insights
    daily_weekly_monthly_options = ['Daily Application Trend', 'Weekly Application Trend', 'Monthly Application Trend']
    selected_daily_weekly_monthly_options = st.radio('###### Select an insight:', daily_weekly_monthly_options, layout="horizontal")

    #-----------------------------------------------------------------------------------------
    # Displaying the selected options
    if selected_daily_weekly_monthly_options == 'Daily Application Trend':
        # Grouping the data by date and counting the number of occurrences
        daily_jobs_applied = data.groupby('Date').size().reset_index(name='count')

        # Sorting the data by count in descending order
        daily_jobs_applied = daily_jobs_applied.sort_values("count", ascending=False)

        # Creating the chart
        # Daily trend line chart
        source = daily_jobs_applied
        x = 'Date'
        y = 'count'
        selector = alt.selection_single(encodings=['x', 'y'])
        hover = alt.selection_single(
            fields=[x],
            nearest=True,
            on="mouseover",
            empty="none",
        )

        lines = (
            alt.Chart(source).mark_line(point="transparent").encode(
                x=alt.X(x, title="Date", axis=alt.Axis(labelFontSize=15, titleFontSize=15)), 
                y=alt.Y(y, title="Count of Applications sent", axis=alt.Axis(labelFontSize=15, titleFontSize=15))
                ).transform_calculate(color='datum.delta < 0 ? "red" : "lightblue"')
        )
        points = (
            lines.transform_filter(hover).mark_circle(size=50).encode(
            color=alt.Color("color:N", scale=None))
        )
        tooltips = (
            alt.Chart(source).mark_rule(opacity=0).encode(
                x=x,
                y=y,
                tooltip=[x, y],
            ).add_selection(hover)
        )

        daily_application_chart = (lines + points + tooltips).interactive().configure_view(strokeWidth=0)

        st.altair_chart(daily_application_chart, use_container_width=True)

    #-----------------------------------------------------------------------------------------
    elif selected_daily_weekly_monthly_options == 'Weekly Application Trend':
        # Define custom sort order for weekdays
        weekday_order = pd.CategoricalDtype(categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ordered=True)

        # Group the data by year and month, and count the number of applications per month
        weekly_jobs_applied = data.groupby(['Year', 'Weekday'])['Date'].count().reset_index()
        weekly_jobs_applied = weekly_jobs_applied.rename(columns={'Date': 'Count'})

        # Sort by weekday
        weekly_jobs_applied['Weekday'] = weekly_jobs_applied['Weekday'].astype(weekday_order)
        weekly_jobs_applied = weekly_jobs_applied.sort_values(['Weekday', 'Year'])

        # Creating a dropdown filters for year
        weekly_jobs_applied_selected_year = st.selectbox('Select year:', options=weekly_jobs_applied['Year'].unique(), index=0)

        # Creating the year filters
        weekly_jobs_applied_year_filter = weekly_jobs_applied[weekly_jobs_applied['Year'] == weekly_jobs_applied_selected_year]

        # Creating the bar chart
        weekly_application_chart = alt.Chart(weekly_jobs_applied_year_filter).mark_bar().encode(
            x=alt.X('Weekday:N', title='Weekday', sort=None),
            y=alt.Y('Count:Q', title='Count of Applications Sent'),
            tooltip=['Year:N', 'Weekday:N', 'Count:Q']
        )
            
        # Add labels to the bars
        weekly_application_text = weekly_application_chart.mark_text(
            align='center',
            baseline='bottom',
            dy=-5,
            fontSize=18,
            color='white'
        ).encode(
            text='Count:Q'
        )

        # Displaying the chart
        st.altair_chart((weekly_application_chart + weekly_application_text), use_container_width=True)

    #-----------------------------------------------------------------------------------------
    elif selected_daily_weekly_monthly_options == 'Monthly Application Trend':
        # Group the data by year and month, and count the number of applications per month
        monthly_jobs_applied = data.groupby(['Year', 'Month'])['Date'].count().reset_index()
        monthly_jobs_applied = monthly_jobs_applied.rename(columns={'Date': 'Count'})

        # Create a new column that combines the Year and Month columns
        monthly_jobs_applied['YearMonth'] = pd.to_datetime(monthly_jobs_applied['Year'].astype(str) + ' ' + monthly_jobs_applied['Month'], format='%Y %B')
        monthly_jobs_applied = monthly_jobs_applied.sort_values('YearMonth')

        # Creating a dropdown filters for year
        monthly_jobs_applied_selected_year = st.selectbox('Select year:', options=monthly_jobs_applied['Year'].unique(), index=0)

        # Creating the year filters
        monthly_jobs_applied_year_filter = monthly_jobs_applied[monthly_jobs_applied['Year'] == monthly_jobs_applied_selected_year]

        # Creating the bar chart
        monthly_application_chart = alt.Chart(monthly_jobs_applied_year_filter).mark_bar().encode(
            x=alt.X('Month:N', title='Month', sort=None),
            y=alt.Y('Count:Q', title='Count of Applications Sent'),
            tooltip=['Year:N', 'Month:N', 'Count:Q']
        )
            
        # Add labels to the bars
        monthly_application_text = monthly_application_chart.mark_text(
            align='center',
            baseline='bottom',
            dy=-5,
            fontSize=18,
            color='white'
        ).encode(
            text='Count:Q'
        )

        # Displaying the chart
        st.altair_chart((monthly_application_chart + monthly_application_text), use_container_width=True)
