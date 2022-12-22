'''
This file contains all the helper functions.
'''

# Importing required libraries.
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

# view-by dropdown function.
def view_by_dropdown():
    '''
    No parameters needed.
    Returns this list -> 
    ['Year', 'Month', 'Day of week', 'Day'].
    '''

    view_by_list = ['Year', 'Month', 'Day of week', 'Day']
    return view_by_list

# State list dropdown function.
def state_list(df):
    '''
    This function require one parameter.
    df -> Dataframe.

    Note :- 
    The dataframe must have ['State'] column or else it will not work.
    
    Returns a sorted list of states with the addition of "Overall" element.
    
    for example this list will look like this:-
    ['Overall', 'Alabama', 'Alaska', ..., 'Wyoming'].
    '''

    try:
        state = df['State'].unique().tolist()
        state.sort()
        state.insert(0, "Overall")

        return state

    except:
        st.error("Sorry for the Inconvenience. Please Reload the Page")    

# year list dropdown function.
def year_list(df):
    '''
    This function require one parameter.
    df -> Dataframe.

    Note :- 
    The dataframe must have ['Year'] column or else it will not work.
    
    Returns a descending list of Years with the addition of "Overall" element.
    
    for example this list will look like this:-
    ['Overall', 2022, 2021, ..., 1791].
    '''

    try:
        years = df['Year'].unique().tolist()
        years.sort(reverse=True)
        years.insert(0, "Overall")

        return years

    except:
        st.error("Sorry for the Inconvenience. Please Reload the Page")     

# month list dropdown function.
def month_list():
    '''
    No parameters needed.
    But adds "Overall" element.
    Returns this list -> 
    ['Overall', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'].
    '''

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    months.insert(0, "Overall")

    return months

# Day of Week list dropdown function.
def day_of_week_list():
    '''
    No parameters needed.
    But adds "Overall" element.
    Returns this list -> 
    ['Overall', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'].
    '''

    day_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    day_of_week.insert(0, "Overall")

    return day_of_week

# Days list dropdown function.
def days_list(df):
    '''
    This function require one parameter.
    df -> Dataframe.

    Note :- 
    The dataframe must have ['Day'] column or else it will not work.
    
    Returns a descending list of Years with the addition of "Overall" element.
    
    for example this list will look like this:-
    ['Overall', 1, 2, 3, ..., 31].
    '''

    try:
        days = df['Day'].unique().tolist()
        days.sort()
        days.insert(0, "Overall")

        return days

    except:
        st.error("Sorry for the Inconvenience. Please Reload the Page") 

# Fetch death tally data function.
def fetch_death_tally_data(df, view_by, year_month_dow_day, state):
    '''
    This function requires four parameters.

    1) df -> Dataframe,
    2) view_by -> The user can select one out of these option ['Year', 'Month', 'Day of week', 'Day'].
    3) year_month_dow_day -> This parameter depends on view_by parameter.
                             For example if view_by = 'Year' then year_month_dow_day = 1998 (A year).
                             For example if view_by = 'Month' then year_month_dow_day = "June" (A month).
                             For example if view_by = 'Day of week' then year_month_dow_day = 'Monday' (A day of week).
                             For example if view_by = 'Day' then year_month_dow_day = 29 (A Day).
    4) state -> A State which belongs to USA. 

    Default -> fetch_death_tally_data(df, 'Year', 'Overall', 'Overall')

    After passing all the parameters this function then filters the data based on the parameters selected by the user.
    
    This funtion returns a filtered dataframe which then can be used to display the death tally on the webapp,
    and it also returns a display title which can be used as a title on the webapp.                          
    '''

    # This will trigger by default.
    if year_month_dow_day == "Overall" and state == "Overall":
        try:
            temp_df = df[['Name', view_by]] # filters the df.
            temp_df = temp_df.groupby(view_by).count() # group by call.
            temp_df.rename(columns = {'Name' : 'Death Count'}, inplace=True) # renaming a column.
        
            # This if blocks decides what should be the display title and how the data should be filtered.
            # This are nothing but some data manipulation techniques.
            if view_by == "Year":
                temp_df = temp_df.reset_index()
                temp_df = temp_df[[view_by, 'Death Count']]
                temp_df = temp_df.sort_values(by=view_by, ascending=False).reset_index().drop('index', axis=1)
                display_title = "Overall Years Death Tally"
            
            elif view_by == "Day":
                temp_df = temp_df.reset_index()
                temp_df = temp_df[[view_by, 'Death Count']]
                temp_df = temp_df.sort_values(by=view_by).reset_index().drop('index', axis=1)
                display_title = "Overall Days Death Tally"
            
            elif view_by == "Month":
                temp_df = temp_df.reindex(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
                temp_df = temp_df.reset_index()
                temp_df = temp_df[[view_by, 'Death Count']]
                display_title = "Overall Months Death Tally"
            
            elif view_by == "Day of week":
                temp_df = temp_df.reindex(['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])
                temp_df = temp_df.reset_index()
                temp_df = temp_df[[view_by, 'Death Count']]  
                display_title = "Overall Day of Week Death Tally"  

        except:
            # If no records found then return an empty dataframe with the display tilte of "No Records Found".
            temp_df = pd.DataFrame(columns=[view_by, "Death Count"])   
            display_title = "No Records Found"         

    # This will trigger when year_month_dow_day will have a value other than "Overall".
    # For example :-
    # year_month_dow_day == 1998 and state == "Overall".
    # year_month_dow_day == "June" and state == "Overall".
    # year_month_dow_day == "Monday" and state == "Overall".
    # year_month_dow_day == 29 and state == "Overall".
    if year_month_dow_day != "Overall" and state == "Overall":
        try:
            # Data Manipulation
            temp_df = df[['State', view_by]]
            total_sum = len(temp_df[temp_df[view_by] == year_month_dow_day])
            temp_df = temp_df[temp_df[view_by] == year_month_dow_day].groupby('State').count()
            temp_df = temp_df.reset_index()
            temp_df.rename(columns={view_by : 'Death Count'}, inplace=True)
        
            # This if block will customize display title based on user selections.
            if view_by == "Year":
                display_title = f"In {view_by} {year_month_dow_day}, {total_sum} deaths were reported"
            
            elif view_by == "Month":
                display_title = f"Throughout the years. In the {view_by} of {year_month_dow_day}, {total_sum} deaths were reported"
            
            elif view_by == "Day of week":
                display_title = f"Throughout the years. On {year_month_dow_day}, {total_sum} deaths were reported"
            
            elif view_by == "Day":
                display_title = f"Throughout the years. On the Day {year_month_dow_day} of the months, {total_sum} deaths were reported"

        except:
            temp_df = pd.DataFrame(columns=[view_by, "Death Count"])   
            display_title = "No Records Found"        
    
    # This will trigger when state will have a value other than "Overall".
    # For example :-
    # year_month_dow_day == "Overall" and state == "Texas".
    if year_month_dow_day == "Overall" and state != "Overall":
        try:
            temp_df = df[['State', view_by]]
            total_sum = len(temp_df[temp_df['State'] == state])
            temp_df = temp_df[temp_df['State'] == state].groupby(view_by).count()
            temp_df.rename(columns={'State':'Death Count'}, inplace=True)
        
            # This if blocks decides what should be the display title and how the data should be filtered.
            # This are nothing but some data manipulation techniques.
            if view_by == "Year":
                temp_df = temp_df.reset_index()
                temp_df = temp_df.sort_values(by=view_by, ascending=False).reset_index()
                temp_df = temp_df[[view_by, 'Death Count']]
                display_title = f"{state} death tally by {view_by}, {total_sum} deaths were reported"
            
            elif view_by == "Day":
                temp_df = temp_df.reset_index()
                temp_df = temp_df.sort_values(by=view_by).reset_index()
                temp_df = temp_df[[view_by, 'Death Count']]
                display_title = f"{state} death tally by {view_by}, {total_sum} deaths were reported"
            
            elif view_by == "Month":
                temp_df = temp_df.reindex(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
                temp_df = temp_df.reset_index()
                temp_df = temp_df[[view_by, 'Death Count']]
                display_title = f"{state} death tally by {view_by}, {total_sum} deaths were reported"
            
            elif view_by == "Day of week":
                temp_df = temp_df.reindex(['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])
                temp_df = temp_df.reset_index()
                temp_df = temp_df[[view_by, 'Death Count']] 
                display_title = f"{state} death tally by {view_by}, {total_sum} deaths were reported"

        except:
            temp_df = pd.DataFrame(columns=[view_by, "Death Count"])
            display_title = "No Records Found"   

    # This will trigger when both params have a value other than "Overall".
    # For example :-
    # year_month_dow_day == 1998 and state == "Texas".
    # year_month_dow_day == "June" and state == "New York".
    # year_month_dow_day == "Monday" and state == "California".
    # year_month_dow_day == 29 and state == "Colorado".
    if year_month_dow_day != "Overall" and state != "Overall":
        try:
            # Data Manipulation.
            temp_df = df[['State', view_by]]
            temp_df = temp_df[(temp_df['State'] == state) & (temp_df[view_by] == year_month_dow_day)]
            temp_df = temp_df.reset_index()
            temp_df = temp_df.groupby(view_by).count()
            temp_df.rename(columns={'index':'Death Count'}, inplace=True)
            temp_df = temp_df.reset_index()
            temp_df.iloc[0,2] = state
            temp_df = temp_df[[view_by, 'State', 'Death Count']]
            display_title = f"{state} {view_by}:{year_month_dow_day} death tally"

        except:
            temp_df = pd.DataFrame(columns=[view_by, "State", "Death Count"])
            display_title = "No Records Found"   

    return temp_df, display_title

# Fetch death tally function
def fetch_death_tally(df, selected_view):
    '''
    This function activates when the user select "Death Tally" feature on the webapp.

    This function requires two parameters.

    1) df -> Dataframe,
    2) selected_view -> The user can select one out of these option ['Year', 'Month', 'Day of week', 'Day'].

    Default -> fetch_death_tally_data(df, 'Year')

    After passing all the parameters this function then filters the data based on the parameters selected by the user.
    
    This function shows the multiple dropdown list options to the user to select.
    
    Then calls the fetch_death_tally_data function to fetch the data.

    This funtion returns a filtered dataframe which then can be used to display the death tally on the webapp,
    then it also returns a display title which can be used as a title on the webapp,
    and it also return state value which can be used which depends on the use case.

    I needed this state value to display a message to the user whenever the user selects the state value = "United State".                          
    '''

    df = df[['Name', 'Year', 'Month', 'Day of week', 'Day', 'State']]
    if selected_view == "Year":
        years = year_list(df) # Fetching Year dropdown list.
        state = state_list(df) # Fetching State dropdown list.

        # Store values for year and state
        selected_year = st.sidebar.selectbox("Select Year", years)  # Display Year dropdown list.
        selected_state = st.sidebar.selectbox("Select State", state)  # Display State dropdown list.

        # Calling the fetch_death_tally_data function.
        death_tally, display_title = fetch_death_tally_data(df, selected_view, selected_year, selected_state)

        return death_tally, display_title, selected_state

    if selected_view == "Month":
        month = month_list() # Fetching Month dropdown list.
        state = state_list(df)

        selected_month = st.sidebar.selectbox("Select Month", month) # Display Month dropdown list.
        selected_state = st.sidebar.selectbox("Select State", state)

        death_tally, display_title = fetch_death_tally_data(df, selected_view, selected_month, selected_state)
        return death_tally, display_title, selected_state

    if selected_view == "Day of week":
        day_of_week = day_of_week_list() # Fetching Day of week dropdown list.
        state = state_list(df)

        selected_day_of_week = st.sidebar.selectbox("Select Day of Week", day_of_week)  # Display Day of week dropdown list.
        selected_state = st.sidebar.selectbox("Select State", state)

        death_tally, display_title = fetch_death_tally_data(df, selected_view, selected_day_of_week, selected_state)
        return death_tally, display_title, selected_state

    if selected_view == "Day":
        day = days_list(df)  # Fetching Day dropdown list.
        state = state_list(df)

        selected_day = st.sidebar.selectbox("Select Day", day)
        selected_state = st.sidebar.selectbox("Select State", state)  # Display Day dropdown list.

        death_tally, display_title = fetch_death_tally_data(df, selected_view, selected_day, selected_state)
        return death_tally, display_title, selected_state

# Deaths Distribution over the years function
def deaths_distribution_over_the_years(df, unit_menu, state=None):
    '''
    This function requires two parameters and third one is optional.

    1) df -> Dataframe,
    2) unit_menu -> The user can select one out of these option ['Human Unit', 'K9 Unit'],
    3) state -> If None then it gives the deaths distribution of the country.
                If state value is some [State] then it gives the deaths distribution of that specific state.
                For example ->
                state = "New York" gives the death distribution of New York throughout the years.

    Note :- The state value is useful for "State-Wise Analysis" feature.

    After passing all the parameters this fuction returns a plotly figure which can be used to display on the webapp.                         
    '''
    
    # Data Manipulation
    deaths_distribution = df[['Name','Year']]
    deaths_distribution = deaths_distribution.groupby("Year").count().reset_index()
    deaths_distribution = deaths_distribution.rename(columns={'Name':'Death Count'})

    # unit_menu is used to customize the title
    if unit_menu == "Human Unit":
        title = "Reported Police Deaths"

    elif unit_menu == "K9 Unit":
        title = "Reported K9 Deaths"    
    
    # This if block is also used to customize the title based on the user selections.
    if state == None:
        # Calling px.line for line plot.
        fig = px.line(deaths_distribution,
            x="Year",
            y="Death Count",
            title=f'{title} in USA <br><sup>From {deaths_distribution.iloc[0][0]} to {deaths_distribution.iloc[-1][0]}</sup>' 
        )

    else: 
        fig = px.line(deaths_distribution,
            x="Year",
            y="Death Count",
            title=f'{title} in {state} <br><sup>From {deaths_distribution.iloc[0][0]} to {deaths_distribution.iloc[-1][0]}</sup>'   
        )  

    # Updating plotly figure layout.
    fig.update_layout(
        autosize=False,
        width=1100,
        height=500,
        font=dict(size=20),
        font_color="#000000",
        title_font_color="#000000",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF"
    )

    return fig

# Age distribution function
def age_distribution(csv_path):
    '''
    This function requires one parameter.

    csv_path -> path of the csv file.

    Note :- I decided this parameter should be a csv path because the data needed some preprocessing and performing preprocessing
            in this function leading to more loading time in the webapp so I decided to preprocess data separately and then pass path of
            that preprocessed data and it reduced the load time.

    After passing all the parameters this fuction returns a plotly figure which can be used to display on the webapp.                         
    '''

    age_df = pd.read_csv(csv_path)

    # Making a cause list so that the user can interact and select a specific age distribution of a specific cause.
    causes_list = age_df['Cause'].unique().tolist()
    causes_list.remove("Other")
    causes_list.sort(reverse=True)
    causes_list.insert(0,"Other")
    causes_list.append("Overall")

    x1 = age_df[age_df['Cause'] == causes_list[0]]['Age']
    x2 = age_df[age_df['Cause'] == causes_list[1]]['Age']
    x3 = age_df[age_df['Cause'] == causes_list[2]]['Age']
    x4 = age_df[age_df['Cause'] == causes_list[3]]['Age']
    x5 = age_df[age_df['Cause'] == causes_list[4]]['Age']
    x6 = age_df[age_df['Cause'] == causes_list[5]]['Age']
    x7 = age_df[age_df['Cause'] == causes_list[6]]['Age']
    x8 = age_df[age_df['Cause'] == causes_list[7]]['Age']
    x9 = age_df[age_df['Cause'] == causes_list[8]]['Age']
    x10 = age_df['Age']

    # Calling plotly ff.creat_displot to create a distribution plot.
    fig = ff.create_distplot(
        [x1,x2,x3,x4,x5,x6,x7,x8,x9,x10],
        causes_list,
        show_hist=False,
        show_rug=False,
    )
    
    # Updating plotly figure layout.
    fig.update_layout(
        autosize=False,
        title='Age Distribution by Causes of Death<br><sup>Select causes of deaths by clicking them in the legend to compare</sup>',
        width=1100,
        height=500,
        font=dict(size=20),
        font_color="#000000",
        title_font_color="#000000",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF"
    )
    
    return fig 

# Heatmap year vs cause function.
def heatmap_year_vs_cause(csv_path, state=None):
    '''
    This function requires one parameter and one is optional.

    1) csv_path -> path of the csv file.
    2) state -> If None then it gives the heatmap year vs cause of the country.
                If state value is some [State] then it gives the heatmap year vs cause of that specific state.
                For example ->
                state = "New York" gives the heatmap year vs cause of New York throughout the years.

    Note :- I decided this parameter should be a csv path because the data needed some preprocessing and performing preprocessing
            in this function leading to more loading time in the webapp so I decided to preprocess data separately and then pass path of
            that preprocessed data and it reduced the load time.

    Note :- The state value is useful for "State-Wise Analysis" feature.        

    After passing all the parameters this fuction returns a seaborn figure which can be used to display on the webapp.                         
    '''

    df = pd.read_csv(csv_path)

    if state == None:
        fig, ax = plt.subplots(figsize=(20,20))
        ax = sns.heatmap(df.pivot_table(index='Cause', columns='Year', values='Name', aggfunc='count').fillna(0),annot=True,fmt="g")
        ax.set_title("Heatmap Year Vs Cause of Death", fontsize=30)

    else:
        df = df[df["State"] == state]
        fig, ax = plt.subplots(figsize=(20,20))
        ax = sns.heatmap(df.pivot_table(index='Cause', columns='Year', values='Name', aggfunc='count').fillna(0),annot=True,fmt="g")
        ax.set_title("Heatmap Year Vs Cause of Death", fontsize=30)

    return fig

# Month death count bar chart function.
def month_death_count_bar_chart(df):
    '''
    This function requires one parameter.

    df -> Dataframe.

    Note -> Make sure the dataframe have a 'Month' column. 

    After passing the parameter this function then filters the data based on the death count according to months and rank them
    from top to bottom and then returns a seaborn figure which can be used to display on the webapp.                          
    '''

    sorted_month_df = df[['Name', 'Month']]
    sorted_month_df = sorted_month_df.groupby("Month").count().sort_values(by='Name', ascending=False).reset_index()
    sorted_month_df.rename(columns={'Name':'Death Count'},inplace=True)

    fig, ax = plt.subplots(figsize=(20,10))
    ax = sns.barplot(data=sorted_month_df,x="Death Count", y="Month",palette="magma")
    
    plt.suptitle("Registered deaths",fontsize=30)
    plt.title("Month wise",fontsize=20)

    plt.xlabel("Death Count",fontsize=20)
    plt.ylabel("Months",fontsize=20)

    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)

    ax.bar_label(ax.containers[0],fontsize=20) # display the numbers

    return fig

# Day death count bar chart function.
def day_death_count_bar_chart(df):
    '''
    This function requires one parameter.

    df -> Dataframe.

    Note -> Make sure the dataframe have a 'Day of week' column. 

    After passing the parameter this function then filters the data based on the death count according to day of week and rank them
    from top to bottom and then returns a seaborn figure which can be used to display on the webapp.                          
    '''

    sorted_day_df = df[['Name', 'Day of week']]
    sorted_day_df = sorted_day_df.groupby("Day of week").count().sort_values(by='Name', ascending=False).reset_index()
    sorted_day_df.rename(columns={'Name':'Death Count'},inplace=True)

    fig, ax = plt.subplots(figsize=(20,10))
    ax = sns.barplot(data=sorted_day_df,x="Death Count", y="Day of week",palette="magma")
    
    plt.suptitle("Registered deaths",fontsize=30)
    plt.title("Day wise",fontsize=20)

    plt.xlabel("Death Count",fontsize=20)
    plt.ylabel("Day of Week",fontsize=20)

    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)

    ax.bar_label(ax.containers[0],fontsize=20) # display the numbers

    return fig    

# Rank tree map function.
def rank_tree_map(df):
    '''
    This function requires one parameter.

    df -> Dataframe.

    Note -> Make sure the dataframe have a 'Rank' column. 

    After passing the parameter this fuction returns a plotly figure which can be used to display on the webapp.                     
    '''

    fig = px.treemap(df,path=["Rank"])  

    fig.update_layout(
        autosize=False,
        title='Ranks With the Most Death',
        width=1100,
        height=600,
        font=dict(size=20),
        font_color="#000000",
        title_font_color="#000000",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF"
    )  
    
    return fig   

# State tree map function.
def state_tree_map(df):
    '''
    This function requires one parameter.

    df -> Dataframe.

    Note -> Make sure the dataframe have a 'State' column. 

    After passing the parameter this fuction returns a plotly figure which can be used to display on the webapp.                     
    '''

    temp_df = df[df['State'] != "United States"] # This step depends on the use case.
    fig = px.treemap(temp_df,path=["State"])  

    fig.update_layout(
        autosize=False,
        title='States With the Most Death',
        width=1100,
        height=600,
        font=dict(size=20),
        font_color="#000000",
        title_font_color="#000000",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF"
    )  
    
    return fig  

# Top ten dilter drop down list function.
def top_ten_filter_drop_down_list(unit_menu):
    '''
    This function requires one parameter.

    unit_menu -> The user can select one out of these option ['Human Unit', 'K9 Unit'],

    returns the list according to the unit_menu.
    '''
    if unit_menu == "Human Unit":
        filter_by_list = ['Ranks', 'Years', 'States',  'Departments', 'Murder Weapons', 'Days of Month', 'Cause of Deaths']

    elif unit_menu == "K9 Unit":   
        filter_by_list = ['Years', 'States', 'Departments', 'Murder Weapons', 'Days of Month', 'Cause of Deaths', 'Danger on Breeds'] 

    return filter_by_list

# Top ten rankings fig function
def top_ten_rankings_fig(df, selected_filter):
    '''
    This function requires two parameters.

    1) df -> Dataframe.
    2) selected_filter -> For Human Unit user can select one of this option :
                          ['Ranks', 'Years', 'States',  'Departments', 'Murder Weapons', 'Days of Month', 'Cause of Deaths']  
                          For K9 Unit user can select one of this option :
                          ['Years', 'States', 'Departments', 'Murder Weapons', 'Days of Month', 'Cause of Deaths', 'Danger on Breeds']      

    After passing all the parameters this fuction filter the data and ranks top 10 according to the selected filter and
    returns a seaborn bar plot figure.  

    Note -> There were some modifications needed for each type of filter that's why i decided to make if blocks rather than making only one function.                       
    '''

    # Ranking by Ranks.
    if selected_filter == "Ranks":
        temp_df = df[['Name', 'Rank']]
        temp_df = temp_df.groupby("Rank").count().sort_values(by='Name', ascending=False).reset_index()
        temp_df.rename(columns={'Name':'Death Count'},inplace=True)
        top_ten = temp_df.iloc[0:10]

        fig, ax = plt.subplots(figsize=(20,10))
        ax = sns.barplot(data=top_ten,x="Death Count", y="Rank",palette="YlOrRd_r")
    
        plt.suptitle("Top Ten Deadly Ranks",fontsize=30)

        plt.xlabel("Death Count",fontsize=20)
        plt.ylabel("Rank",fontsize=20)

        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)

        ax.bar_label(ax.containers[0],fontsize=20)
 
    # Ranking by Years.
    elif selected_filter == "Years":
        temp_df = df[['Name', 'Year']]
        temp_df = temp_df.groupby("Year").count().sort_values(by='Name', ascending=False).reset_index()
        temp_df.rename(columns={'Name':'Death Count'},inplace=True)
        top_ten = temp_df.iloc[0:10]
        top_ten['Year'] = top_ten['Year'].astype("str")

        fig, ax = plt.subplots(figsize=(20,10))
        ax = sns.barplot(data=top_ten,x="Death Count", y="Year",palette="Reds_r")
    
        plt.suptitle("Top Ten Deadly Years",fontsize=30)

        plt.xlabel("Death Count",fontsize=20)
        plt.ylabel("Year",fontsize=20)

        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)

        ax.bar_label(ax.containers[0],fontsize=20)

    # Ranking by States.
    elif selected_filter == "States":
        temp_df = df[['Name', 'State']]
        temp_df = temp_df.groupby("State").count().sort_values(by='Name', ascending=False).reset_index()
        temp_df.rename(columns={'Name':'Death Count'},inplace=True)
        temp_df = temp_df[temp_df['State'] != "United States"]
        top_ten = temp_df.iloc[0:10]

        fig, ax = plt.subplots(figsize=(20,10))
        ax = sns.barplot(data=top_ten,x="Death Count", y="State",palette="Oranges_r")
    
        plt.suptitle("Top Ten Deadly States",fontsize=30)

        plt.xlabel("Death Count",fontsize=20)
        plt.ylabel("State",fontsize=20)

        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)

        ax.bar_label(ax.containers[0],fontsize=20)

    # Ranking by Departments.
    elif selected_filter == "Departments":
        temp_df = df[['Name', 'Department']]
        temp_df = temp_df.groupby("Department").count().sort_values(by='Name', ascending=False).reset_index()
        temp_df.rename(columns={'Name':'Death Count'},inplace=True)
        top_ten = temp_df.iloc[0:10]

        fig, ax = plt.subplots(figsize=(20,10))
        ax = sns.barplot(data=top_ten,x="Death Count", y="Department",palette="OrRd_r")
    
        plt.suptitle("Top Ten Deadly Departments",fontsize=30)

        plt.xlabel("Death Count",fontsize=20)
        plt.ylabel("Department",fontsize=20)

        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)

        ax.bar_label(ax.containers[0],fontsize=20)

    # Ranking by Murder Weapons.
    elif selected_filter == "Murder Weapons":
        temp_df = df[['Name', 'Weapon']]
        temp_df = temp_df.groupby("Weapon").count().sort_values(by='Name', ascending=False).reset_index()
        temp_df.rename(columns={'Name':'Death Count'},inplace=True)
        top_ten = temp_df.iloc[0:10]

        fig, ax = plt.subplots(figsize=(20,10))
        ax = sns.barplot(data=top_ten,x="Death Count", y="Weapon",palette="Reds_r")
    
        plt.suptitle("Top Ten Deadly Murder Weapons",fontsize=30)

        plt.xlabel("Death Count",fontsize=20)
        plt.ylabel("Murder Weapon",fontsize=20)

        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)

        ax.bar_label(ax.containers[0],fontsize=20)

    # Ranking by Days of Month.
    elif selected_filter == "Days of Month":
        temp_df = df[['Name', 'Day']]
        temp_df = temp_df.groupby("Day").count().sort_values(by='Name', ascending=False).reset_index()
        temp_df.rename(columns={'Name':'Death Count'},inplace=True)
        top_ten = temp_df.iloc[0:10]
        top_ten['Day'] = top_ten['Day'].astype("str")

        fig, ax = plt.subplots(figsize=(20,10))
        ax = sns.barplot(data=top_ten,x="Death Count", y="Day",palette="YlOrRd_r")
    
        plt.suptitle("Top Ten Deadly Days of Month",fontsize=30)

        plt.xlabel("Death Count",fontsize=20)
        plt.ylabel("Day of Month",fontsize=20)

        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)

        ax.bar_label(ax.containers[0],fontsize=20)

    # Ranking by Cause of Deaths.
    elif selected_filter == "Cause of Deaths":
        temp_df = df[['Name', 'Cause']]
        temp_df = temp_df.groupby("Cause").count().sort_values(by='Name', ascending=False).reset_index()
        temp_df.rename(columns={'Name':'Death Count'},inplace=True)
        top_ten = temp_df.iloc[0:10]

        fig, ax = plt.subplots(figsize=(25,10))
        ax = sns.barplot(data=top_ten,x="Death Count", y="Cause",palette="OrRd_r")
    
        plt.suptitle("Top Ten Deadly Causes of Death",fontsize=30)

        plt.xlabel("Death Count",fontsize=20)
        plt.ylabel("Cause of Death",fontsize=20)

        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)

        ax.bar_label(ax.containers[0],fontsize=20) 

    # Ranking by Danger on Breeds.
    elif selected_filter == "Danger on Breeds":
        temp_df = df[['Name', 'Breed']]
        temp_df = temp_df.groupby("Breed").count().sort_values(by='Name', ascending=False).reset_index()
        temp_df.rename(columns={'Name':'Death Count'},inplace=True)
        top_ten = temp_df.iloc[0:10]

        fig, ax = plt.subplots(figsize=(20,10))
        ax = sns.barplot(data=top_ten,x="Death Count", y="Breed",palette="Reds_r")
    
        plt.suptitle("Top Ten Breeds with most deaths",fontsize=30)

        plt.xlabel("Death Count",fontsize=20)
        plt.ylabel("Breed",fontsize=20)

        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)

        ax.bar_label(ax.containers[0],fontsize=20)    

    return fig

# Cartogram function.
def cartogram(csv_path, year_range):
    '''
    This function requires two parameters.

    1) csv_path -> path of the csv file.
    2) year_range -> a years rang tuple for example (1791, 2022).

    Note :- I decided this parameter should be a csv path because the data needed some preprocessing and performing preprocessing
            in this function leading to more loading time in the webapp so I decided to preprocess data separately and then pass path of
            that preprocessed data and it reduced the load time.       

    After passing all the parameters this fuction returns a plotly map figure which can be changed on the basis on slider it can 
    be used to display on the webapp.                         
    '''

    usa_states_df = pd.read_csv("preprocessed data/us_states_code.csv")
    usa_states_df.rename(columns={'state':'State'}, inplace=True)

    temp_df = pd.read_csv(csv_path)
    temp_df = temp_df[(temp_df['Year'] >= year_range[0]) & (temp_df['Year'] <= year_range[1])] 
    temp_df = temp_df.groupby("State").count().reset_index()
    temp_df = temp_df[['State', 'Name']]
    temp_df.rename(columns={'Name':'Death Count'}, inplace=True)
    temp_df = temp_df.join(usa_states_df.set_index('State')[['code']], on='State')

    fig = go.Figure(data=go.Choropleth(
        locations=temp_df['code'],
        z = temp_df['Death Count'], 
        locationmode = 'USA-states',
        colorscale = 'Reds',
        colorbar_title = "Death Count",
        text = "Police Deaths in " + temp_df['State']
    ))

    fig.update_layout(
        autosize=False,
        geo_scope='usa',
        width=1000,
        height=600,
    )

    return fig
