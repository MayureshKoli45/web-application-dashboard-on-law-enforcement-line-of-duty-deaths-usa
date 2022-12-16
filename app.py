import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns
import helper 
import human_unit
import k9_unit

if __name__=="__main__":  

    try:
        st.set_page_config(layout='wide')
        st.sidebar.image("usa_flag.jpg")
        st.sidebar.title("United States of America Law Enforcement Line of Duty Deaths Analysis From 1791 to 2022")

        unit_menu = st.sidebar.radio(
            'Select a Unit',
            ('Human Unit', 'K9 Unit'),
            horizontal=True
        )

        user_menu = st.sidebar.radio(
            'Select an Option',
            ('Overall Analysis', 'Top Ten Deadly...', 'Death Tally', 'State-Wise Analysis', 'Cartogram')
        )

        if unit_menu == "Human Unit":
            df = pd.read_csv('police_deaths.csv') 
            human_unit.human_unit_analysis(df, user_menu, unit_menu)

        if unit_menu == "K9 Unit":
            df = pd.read_csv('k9_deaths.csv') 
            k9_unit.k9_unit_analysis(df, user_menu, unit_menu)  

    except:
        st.sidebar.title("Sorry for the Inconvenience. Please Reload the Page")          
