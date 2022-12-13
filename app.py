import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns
import helper 

if __name__=="__main__":

    df = pd.read_csv('police_deaths.csv')   

    st.set_page_config(layout='wide')
    st.sidebar.title("Law Enforcement Line of Duty Deaths Analysis From 1791 to 2022")

    user_menu = st.sidebar.radio(
        'Select an Option',
        ('Overall Analysis', 'Top Ten Deadly...', 'Death Tally', 'State-Wise Analysis', 'Cartogram')
    )

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


        deaths_distribution_fig = helper.deaths_distribution_over_the_years(df)
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


    if user_menu == "Top Ten Deadly...":
        st.title("Top Ten Deadly...")
        filter_by_list = helper.top_ten_filter_drop_down_list()
        selected_filter = st.selectbox("Filter By", filter_by_list)

        filtered_bar_plot_fig = helper.top_ten_rankings_fig(df, selected_filter)
        st.pyplot(filtered_bar_plot_fig)


    if user_menu == "Death Tally":
        st.sidebar.header("Death Tally")

        view_by_list = helper.view_by_dropdown()
        selected_view = st.sidebar.selectbox("View By", view_by_list)

        represent_death_tally_df, represent_title = helper.fetch_death_tally(df, selected_view)

        st.title(represent_title)
        st.table(represent_death_tally_df)   


