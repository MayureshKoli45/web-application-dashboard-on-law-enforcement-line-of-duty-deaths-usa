import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns

# default death tally
def death_tally(df):
    police_death_tally = df[['Name', 'Year', 'Month', 'Day of week', 'Day', 'State']]
    police_death_tally = police_death_tally.groupby('Year').count()
    police_death_tally.rename(columns = {'Name' : 'Death Count'}, inplace=True)
    police_death_tally = police_death_tally.reset_index()
    police_death_tally = police_death_tally[['Year', 'Death Count']]
    police_death_tally = police_death_tally.sort_values(by='Year', ascending=False).reset_index().drop('index', axis=1)
    return police_death_tally

# view-by dropdown
def view_by_dropdown():
    view_by_list = ['Year', 'Month', 'Day of week', 'Day']
    return view_by_list

# State list
def state_list(df):
    state = df['State'].unique().tolist()
    state.sort()
    state.insert(0, "Overall")

    return state

# year list
def year_list(df):
    years = df['Year'].unique().tolist()
    years.sort(reverse=True)
    years.insert(0, "Overall")

    return years

# month list
def month_list():
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    months.insert(0, "Overall")

    return months

# dow list
def day_of_week_list():
    day_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    day_of_week.insert(0, "Overall")

    return day_of_week

# days list
def days_list(df):
    days = df['Day'].unique().tolist()
    days.sort()
    days.insert(0, "Overall")

    return days        

def fetch_death_tally_data(df, view_by, year_month_dow_day, state):
    if year_month_dow_day == "Overall" and state == "Overall":
        temp_df = df[['Name', view_by]]
        temp_df = temp_df.groupby(view_by).count()
        temp_df.rename(columns = {'Name' : 'Death Count'}, inplace=True)
        
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
        

    if year_month_dow_day != "Overall" and state == "Overall":
        temp_df = df[['State', view_by]]
        total_sum = len(temp_df[temp_df[view_by] == year_month_dow_day])
        temp_df = temp_df[temp_df[view_by] == year_month_dow_day].groupby('State').count()
        temp_df = temp_df.reset_index()
        temp_df.rename(columns={view_by : 'Death Count'}, inplace=True)
        
        if view_by == "Year":
            display_title = f"In {view_by} {year_month_dow_day}, {total_sum} deaths were reported"
            
        elif view_by == "Month":
            display_title = f"Throughout the years. In the {view_by} of {year_month_dow_day}, {total_sum} deaths were reported"
            
        elif view_by == "Day of week":
            display_title = f"Throughout the years. On {year_month_dow_day}, {total_sum} deaths were reported"
            
        elif view_by == "Day":
            display_title = f"Throughout the years. On the Day {year_month_dow_day} of the months, {total_sum} deaths were reported"
    
    if year_month_dow_day == "Overall" and state != "Overall":
        temp_df = df[['State', view_by]]
        total_sum = len(temp_df[temp_df['State'] == state])
        temp_df = temp_df[temp_df['State'] == state].groupby(view_by).count()
        temp_df.rename(columns={'State':'Death Count'}, inplace=True)
        
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
    
    if year_month_dow_day != "Overall" and state != "Overall":
        temp_df = df[['State', view_by]]
        temp_df = temp_df[(temp_df['State'] == state) & (temp_df[view_by] == year_month_dow_day)]
        temp_df = temp_df.reset_index()
        temp_df = temp_df.groupby(view_by).count()
        temp_df.rename(columns={'index':'Death Count'}, inplace=True)
        temp_df = temp_df.reset_index()
        temp_df.iloc[0,2] = state
        temp_df = temp_df[[view_by, 'State', 'Death Count']]
        display_title = f"{state} {view_by}:{year_month_dow_day} death tally"
    
    return temp_df, display_title


def fetch_death_tally(df, selected_view):
    df = df[['Name', 'Year', 'Month', 'Day of week', 'Day', 'State']]
    if selected_view == "Year":
        years = year_list(df)
        state = state_list(df)
        selected_year = st.sidebar.selectbox("Select Year", years)
        selected_state = st.sidebar.selectbox("Select State", state)
        death_tally, display_title = fetch_death_tally_data(df, selected_view, selected_year, selected_state)
        return death_tally, display_title, selected_state

    if selected_view == "Month":
        month = month_list()
        state = state_list(df)
        selected_month = st.sidebar.selectbox("Select Month", month)
        selected_state = st.sidebar.selectbox("Select State", state)
        death_tally, display_title = fetch_death_tally_data(df, selected_view, selected_month, selected_state)
        return death_tally, display_title, selected_state

    if selected_view == "Day of week":
        day_of_week = day_of_week_list()
        state = state_list(df)
        selected_day_of_week = st.sidebar.selectbox("Select Day of Week", day_of_week)
        selected_state = st.sidebar.selectbox("Select State", state)
        death_tally, display_title = fetch_death_tally_data(df, selected_view, selected_day_of_week, selected_state)
        return death_tally, display_title, selected_state

    if selected_view == "Day":
        day = days_list(df)
        state = state_list(df)
        selected_day = st.sidebar.selectbox("Select Day", day)
        selected_state = st.sidebar.selectbox("Select State", state)
        death_tally, display_title = fetch_death_tally_data(df, selected_view, selected_day, selected_state)
        return death_tally, display_title, selected_state



def deaths_distribution_over_the_years(df, state=None):
    deaths_distribution = df[['Name','Year']]
    deaths_distribution = deaths_distribution.groupby("Year").count().reset_index()
    deaths_distribution = deaths_distribution.rename(columns={'Name':'Death Count'})

    if state == None:
        fig = px.line(deaths_distribution,
            x="Year",
            y="Death Count",
            title=f'Reported Police Deaths in USA <br><sup>From {deaths_distribution.iloc[0][0]} to {deaths_distribution.iloc[-1][0]}</sup>'    
        )

    else: 
        fig = px.line(deaths_distribution,
            x="Year",
            y="Death Count",
            title=f'Reported Police Deaths in {state} <br><sup>From {deaths_distribution.iloc[0][0]} to {deaths_distribution.iloc[-1][0]}</sup>'    
        )   

    fig.update_layout(
        autosize=False,
        width=1000,
        height=600,
        font=dict(
            size=20)
    )
    return fig


def age_distribution(csv_path):
    age_df = pd.read_csv(csv_path)
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

    fig = ff.create_distplot(
        [x1,x2,x3,x4,x5,x6,x7,x8,x9,x10],
        causes_list,
        show_hist=False,
        show_rug=False,
    )
    
    fig.update_layout(
        autosize=False,
        title='Age Distribution by Causes of Death',
        width=1000,
        height=600,
        font=dict(size=20)
    )
    
    return fig 


def heatmap_year_vs_cause(csv_path, state=None):
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


def month_death_count_bar_chart(df):
    sorted_month_df = df[['Name', 'Month']]
    sorted_month_df = sorted_month_df.groupby("Month").count().sort_values(by='Name', ascending=False).reset_index()
    sorted_month_df.rename(columns={'Name':'Death Count'},inplace=True)

    fig, ax = plt.subplots(figsize=(20,10))
    ax = sns.barplot(data=sorted_month_df,x="Death Count", y="Month",palette="magma")
    
    plt.suptitle("Registered police deaths",fontsize=30)
    plt.title("Month wise",fontsize=20)

    plt.xlabel("Death Count",fontsize=20)
    plt.ylabel("Months",fontsize=20)

    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)

    ax.bar_label(ax.containers[0],fontsize=20)

    return fig

def day_death_count_bar_chart(df):
    sorted_month_df = df[['Name', 'Day of week']]
    sorted_month_df = sorted_month_df.groupby("Day of week").count().sort_values(by='Name', ascending=False).reset_index()
    sorted_month_df.rename(columns={'Name':'Death Count'},inplace=True)

    fig, ax = plt.subplots(figsize=(20,10))
    ax = sns.barplot(data=sorted_month_df,x="Death Count", y="Day of week",palette="magma")
    
    plt.suptitle("Registered police deaths",fontsize=30)
    plt.title("Day wise",fontsize=20)

    plt.xlabel("Death Count",fontsize=20)
    plt.ylabel("Day of Week",fontsize=20)

    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)

    ax.bar_label(ax.containers[0],fontsize=20)

    return fig    

def rank_tree_map(df):
    fig = px.treemap(df,path=["Rank"])  

    fig.update_layout(
        autosize=False,
        title='Ranks With the Most Death',
        width=1000,
        height=600,
        font=dict(size=20)
    )  
    
    return fig   

def state_tree_map(df):
    temp_df = df[df['State'] != "United States"]
    fig = px.treemap(temp_df,path=["State"])  

    fig.update_layout(
        autosize=False,
        title='States With the Most Death',
        width=1000,
        height=600,
        font=dict(size=20)
    )  
    
    return fig      


def top_ten_filter_drop_down_list():
    filter_by_list = ['Ranks', 'Years', 'States',  'Departments', 'Murder Weapons', 'Days of Month', 'Cause of Deaths']

    return filter_by_list


def top_ten_rankings_fig(df, selected_filter):
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

    return fig
