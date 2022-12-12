import plotly.express as px
import plotly.figure_factory as ff

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


def deaths_distribution_over_the_years(df):
    deaths_distribution = df[['Name','Year']]
    deaths_distribution = deaths_distribution.groupby("Year").count().reset_index()
    deaths_distribution = deaths_distribution.rename(columns={'Name':'Death Count'})
    fig = px.line(deaths_distribution,
        x="Year",
        y="Death Count",
        title=f'Reported Police Deaths in USA <br><sup>From {deaths_distribution.iloc[0][0]} to {deaths_distribution.iloc[-1][0]}</sup>'    
    )

    fig.update_layout(
        autosize=False,
        width=1000,
        height=600,
        font=dict(
            size=20)
    )
    return fig


def age_distribution(df):
    age_df = df[['Name','Age','Cause']]
    age_df = age_df.dropna()
    age_df = age_df[age_df['Age'] < 100]

    causes_list = age_df.groupby('Cause').count().sort_values(by='Age',ascending=False)
    causes_list = causes_list.index.to_list()
    causes_list = causes_list[0:8]
    causes_list.insert(0, "Overall")
    causes_list.append("Other")
    causes_list = causes_list[::-1]

    for i in range(len(age_df)):
        if age_df.iloc[i][2] not in causes_list:
            age_df.iloc[i,2] = 'Other'

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
        font=dict(
            size=20)
    )
    
    return fig    
    
