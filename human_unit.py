'''
This file contains the data manipulation and data visualization w.r.t police deaths of Human Unit.
This file contains main functionalities of the webapp dashboard.
'''

# Importing required libraries.
import streamlit as st
import numpy as np
import helper # This is the helper module which helps to implement all the requirements.


def human_unit_analysis(df, user_menu, unit_menu):
    '''
    This function requires three parameters.

    1) df -> Dataframe,
    2) user_menu -> In app.py user_menu stands for feature selection that is available in webapp,
    3) unit_menu -> unit_menu is the selection of the section on whether the user wants to analyze the data of Human Unit or K9 Unit.
    
    This function take those parameters and perform data manipulation and also present data visualizations as per the feature selected by the user.
    
    Warning :-
    This function is especially made for the dataframe which can be acquired from "police_deaths.csv".
    It will not work on any other dataframes.

    The police_deaths df contains this columns ->
    ['Rank', 'Name', 'Age', 'End of watch', 'Day of week', 'Cause', 'Department', 'State', 'Tour', 'Badge', 'Weapon', 'Offender', 'Summary', 'Year', 'Month', 'Day'].
    
    So addition of any other columns might disrupt the flow of this program.
    
    But the viewer can modify this program as per needed for his/her requirements. 
    '''

    # This if block triggers the feature "Overall Analysis".
    # This feature gives the user an overall analysis of the dataframe.
    if user_menu == "Overall Analysis":

        total_deaths = len(df) # Total deaths reported till death.

        avg_deaths_per_year = round(len(df)/len(df['Year'].unique())) # Average deaths per year.

        deadly_year = df['Year'].value_counts().sort_values(ascending=False).reset_index()
        deadly_year = deadly_year.iloc[0][0] # The year which have highest deaths reported.

        causes_of_deaths = df['Cause'].unique().tolist()
        causes_of_deaths.remove(np.nan)  
        unique_cod = len(causes_of_deaths) # Number of Unique types of causes of deaths.

        deadly_cod = df['Cause'].value_counts().sort_values(ascending=False).reset_index()
        deadly_cod = deadly_cod.iloc[0][0] # Highest number of deaths by this cause of death.

        types_of_weapons = df['Weapon'].unique().tolist()
        types_of_weapons.remove(np.nan)  
        unique_weapons = len(types_of_weapons) # Number of Unique types of murder weapons.

        deadly_weapon = df['Weapon'].value_counts().sort_values(ascending=False).reset_index()
        deadly_weapon = deadly_weapon.iloc[0][0] # Highest number of deaths by this murder weapon.

        total_departments = len(df['Department'].unique())  # Number of Unique types of Departments in USA throughout the years.

        deadly_state = df['State'].value_counts().sort_values(ascending=False).reset_index()
        deadly_state = deadly_state.iloc[0][0] # Highest number of deaths in this state.


        st.title("Top Statistics") # Streamlit title for this feature

        # Since I have 9 various important statistics to show I wanted to present this info in the 3*3 grid form.
        # For that you have to declare 3 columns each time and pass the stat variable info through title, header, subheader or markdown. 
        # Grid first row.
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Total Deaths Reported")
            st.header(total_deaths)

        with col2:
            st.subheader("Average Deaths/Year")
            st.header(avg_deaths_per_year) 

        with col3:
            st.subheader("Deadly Year")
            st.header(deadly_year)  

        # Grid second row.
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Unique Causes of Death")
            st.header(unique_cod)

        with col2:
            st.subheader("Unique Murder Weapons")
            st.header(unique_weapons) 

        with col3:
            st.subheader("Unique Departments")
            st.header(total_departments) 

        # Grid third row.
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Deadly Cause of Death")
            st.header(deadly_cod)

        with col2:
            st.subheader("Deadly Murder Weapon")
            st.header(deadly_weapon) 

        with col3:
            st.subheader("Deadly State")
            st.header(deadly_state)        

        # This variable contains plotly figure which is aquired from a helper function.
        deaths_distribution_fig = helper.deaths_distribution_over_the_years(df, unit_menu)
        st.plotly_chart(deaths_distribution_fig) # Display the figure.

        # Same strategy is applied below except some functions takes path of the csv file.

        age_distribution_fig = helper.age_distribution("preprocessed data/human_unit_age_distribution_df.csv")
        st.plotly_chart(age_distribution_fig)

        heatmap_fig = helper.heatmap_year_vs_cause("preprocessed data/human_unit_heatmap_year_vs_cause.csv")
        st.pyplot(heatmap_fig)

        month_bar_chart_fig = helper.month_death_count_bar_chart(df)
        st.pyplot(month_bar_chart_fig)

        day_bar_chart_fig = helper.day_death_count_bar_chart(df)
        st.pyplot(day_bar_chart_fig)

        rank_death_fig = helper.rank_tree_map(df)
        st.plotly_chart(rank_death_fig)

        state_death_fig = helper.state_tree_map(df)
        st.plotly_chart(state_death_fig)


    # This if block triggers the feature "Top Ten Deadly...".
    # This feature presents the top ten to the user as per the selection of the filter.
    if user_menu == "Top Ten Deadly...":
        st.title("Top Ten Deadly...")

        # Presents a list to select a filter [Rank, Year, State, etc.].
        filter_by_list = helper.top_ten_filter_drop_down_list(unit_menu)

        # Store the value of the selected feature by the user.
        selected_filter = st.selectbox("Filter By", filter_by_list)

        # Store the bar plot of the top ten [feature] by ranking them from top to bottom.
        filtered_bar_plot_fig = helper.top_ten_rankings_fig(df, selected_filter)

        # Display the figure.
        st.pyplot(filtered_bar_plot_fig)


    # This if block triggers the feature "Death Tally".
    # This feature presents the Death Tally by Year, Month, Day of Week, Day and States.
    if user_menu == "Death Tally":
        st.sidebar.header("Death Tally")

        # Presents a list to select a filter [Year, Month, Day of Week, Day].
        view_by_list = helper.view_by_dropdown()

        # Store the value of the selected feature by the user.
        selected_view = st.sidebar.selectbox("View By", view_by_list)

        # represent_death_tally_df stores the dataframe.
        # represent_title stores the title.
        # represent_state stores the selected state.
        # Then we will display to the user based on their selections.
        represent_death_tally_df, represent_title, represent_state = helper.fetch_death_tally(df, selected_view)

        # This is note that I wanted to show to the user if he/she selects state = United States.
        if represent_state == "United States":
            st.markdown('''**Note :- The state United States refers to police officers who were directly working for US Department of Justice. 
            It needed to be included because during scraping the data, many officer department states were assigned as US or United States.**''')

        # The title will change according to the selections of the user.
        st.title(represent_title)

        # This radio button is created to add sort table feature so that the user can sort the tally.
        sort_by_menu = st.radio(
            'Sort By',
            ('None', 'High to Low', 'Low to High'),
            horizontal=True
            )

        # Represents Tally in true form.
        if sort_by_menu == "None":    
            st.table(represent_death_tally_df)

        # Represents Tally in Descending order.
        elif sort_by_menu == "High to Low":
            sorted_df = represent_death_tally_df.sort_values(by="Death Count", ascending=False) 
            st.table(sorted_df)

        # Represents Tally in Ascending order.
        elif sort_by_menu == "Low to High":
            sorted_df = represent_death_tally_df.sort_values(by="Death Count") 
            st.table(sorted_df)         


    # This if block triggers the feature "State-Wise Analysis".
    # This feature is same as overall analysis but focusses mainly on a State at a time.
    if user_menu == "State-Wise Analysis":
        st.title("State-Wise Analysis")

        state_selection_list = df['State'].unique().tolist()
        state_selection_list.sort()

        # Presents a list to select of States (default -> "Texas").
        selected_state = st.selectbox("Select a State", state_selection_list, index=state_selection_list.index("Texas"))

        # This is note that I wanted to show to the user if he/she selects state = United States.
        if selected_state == "United States":
            st.markdown('''**Note :- The state United States refers to police officers who were directly working for US Department of Justice. 
            It needed to be included because during scraping the data, many officer department states were assigned as US or United States.**''')

        # Filtering Dataframe w.r.t State
        state_selected_temp_df = df[df["State"] == selected_state] 

        # This variable contains plotly figure which is aquired from a helper function.
        state_deaths_distribution_fig = helper.deaths_distribution_over_the_years(state_selected_temp_df, unit_menu, state=selected_state)
        st.plotly_chart(state_deaths_distribution_fig) # Display the figure.

        # Same strategy is applied below except some functions takes path of the csv file.

        state_heatmap_fig = helper.heatmap_year_vs_cause("preprocessed data/human_unit_heatmap_year_vs_cause.csv", selected_state)
        st.pyplot(state_heatmap_fig)

        state_month_bar_chart_fig = helper.month_death_count_bar_chart(state_selected_temp_df)
        st.pyplot(state_month_bar_chart_fig)

        state_day_bar_chart_fig = helper.day_death_count_bar_chart(state_selected_temp_df)
        st.pyplot(state_day_bar_chart_fig)

        state_rank_death_fig = helper.rank_tree_map(state_selected_temp_df)
        st.plotly_chart(state_rank_death_fig)  


    # This if block triggers the feature "Cartogram".
    # This feature shows the death count by state on the map and user can also select the range of the years from 1791 to 2022.
    if user_menu == "Cartogram":
        st.title("Police Deaths in USA Cartogram")

        s_date = int(df["Year"].min()) # For slider min range.
        e_date = int(df['Year'].max()) # For slider min range.

        # Streamlit slder.
        year_range = st.slider(
            'Select a range of years', # Title.
            min_value = s_date, # Min range value of the slider.
            max_value = e_date, # Max range value of the slider.
            value = [s_date, e_date] # Range.
        ) 

        # This variable store a map figure.
        map_fig = helper.cartogram("preprocessed data/human_unit_filtered_states_for_map.csv", year_range)

        # Displaying the figure.
        st.plotly_chart(map_fig)
