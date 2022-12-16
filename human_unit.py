import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns
import helper 

def human_unit_analysis(df, user_menu, unit_menu):
    if user_menu == "Overall Analysis":
        total_deaths = len(df)
        avg_deaths_per_year = round(len(df)/len(df['Year'].unique()))
        deadly_year = df['Year'].value_counts().sort_values(ascending=False).reset_index()
        deadly_year = deadly_year.iloc[0][0]

        causes_of_deaths = df['Cause'].unique().tolist()
        causes_of_deaths.remove(np.nan)  
        unique_cod = len(causes_of_deaths)
        deadly_cod = df['Cause'].value_counts().sort_values(ascending=False).reset_index()
        deadly_cod = deadly_cod.iloc[0][0]

        types_of_weapons = df['Weapon'].unique().tolist()
        types_of_weapons.remove(np.nan)  
        unique_weapons = len(types_of_weapons)
        deadly_weapon = df['Weapon'].value_counts().sort_values(ascending=False).reset_index()
        deadly_weapon = deadly_weapon.iloc[0][0]

        total_departments = len(df['Department'].unique())
        deadly_state = df['State'].value_counts().sort_values(ascending=False).reset_index()
        deadly_state = deadly_state.iloc[0][0]


        st.title("Top Statistics")

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


        deaths_distribution_fig = helper.deaths_distribution_over_the_years(df, unit_menu)
        st.plotly_chart(deaths_distribution_fig)

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


    if user_menu == "Top Ten Deadly...":
        st.title("Top Ten Deadly...")
        filter_by_list = helper.top_ten_filter_drop_down_list(unit_menu)
        selected_filter = st.selectbox("Filter By", filter_by_list)

        filtered_bar_plot_fig = helper.top_ten_rankings_fig(df, selected_filter)
        st.pyplot(filtered_bar_plot_fig)


    if user_menu == "Death Tally":
        st.sidebar.header("Death Tally")

        view_by_list = helper.view_by_dropdown()
        selected_view = st.sidebar.selectbox("View By", view_by_list)

        represent_death_tally_df, represent_title, represent_state = helper.fetch_death_tally(df, selected_view)

        if represent_state == "United States":
            st.markdown('''**Note :- The state United States refers to police officers who were directly working for US Department of Justice. 
            It needed to be included because during scraping the data, many officer department states were assigned as US or United States.**''')

        st.title(represent_title)

        sort_by_menu = st.radio(
            'Sort By',
            ('None', 'High to Low', 'Low to High'),
            horizontal=True
            )

        if sort_by_menu == "None":    
            st.table(represent_death_tally_df)

        elif sort_by_menu == "High to Low":
            sorted_df = represent_death_tally_df.sort_values(by="Death Count", ascending=False) 
            st.table(sorted_df)

        elif sort_by_menu == "Low to High":
            sorted_df = represent_death_tally_df.sort_values(by="Death Count") 
            st.table(sorted_df)         


    if user_menu == "State-Wise Analysis":
        st.title("State-Wise Analysis")

        state_selection_list = df['State'].unique().tolist()
        state_selection_list.sort()
        selected_state = st.selectbox("Select a State", state_selection_list, index=state_selection_list.index("Texas"))

        if selected_state == "United States":
            st.markdown('''**Note :- The state United States refers to police officers who were directly working for US Department of Justice. 
            It needed to be included because during scraping the data, many officer department states were assigned as US or United States.**''')

        state_selected_temp_df = df[df["State"] == selected_state] 

        state_deaths_distribution_fig = helper.deaths_distribution_over_the_years(state_selected_temp_df, unit_menu, state=selected_state)
        st.plotly_chart(state_deaths_distribution_fig)

        state_heatmap_fig = helper.heatmap_year_vs_cause("preprocessed data/human_unit_heatmap_year_vs_cause.csv", selected_state)
        st.pyplot(state_heatmap_fig)

        state_month_bar_chart_fig = helper.month_death_count_bar_chart(state_selected_temp_df)
        st.pyplot(state_month_bar_chart_fig)

        state_day_bar_chart_fig = helper.day_death_count_bar_chart(state_selected_temp_df)
        st.pyplot(state_day_bar_chart_fig)

        state_rank_death_fig = helper.rank_tree_map(state_selected_temp_df)
        st.plotly_chart(state_rank_death_fig)  


    if user_menu == "Cartogram":
        st.title("Police Deaths in USA Cartogram")

        s_date = int(df["Year"].min())
        e_date = int(df['Year'].max())

        year_range = st.slider(
            'Select a range of years',
            min_value = s_date,
            max_value = e_date,
            value = [s_date, e_date]
        ) 

        map_fig = helper.cartogram("preprocessed data/human_unit_filtered_states_for_map.csv", year_range)
        st.plotly_chart(map_fig)
