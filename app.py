'''
This is main app file. To implement this webapp dashboard run this file.
'''

# Importing required libraries.
import streamlit as st 
import pandas as pd
import human_unit # This library includes the manipulation of the data w.r.t police human_unit.
import k9_unit # This library includes the manipulation of the data w.r.t police k9_unit.

if __name__=="__main__":  

    st.set_page_config(layout='wide') # Setting up the page config to wide.

    with open('style.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

    st.sidebar.image("image folder/usa_flag.jpg") # Uploading an image to the webapp.

    st.sidebar.title('United States of America Law Enforcement Line of Duty Deaths Analysis From 1791 to 2022') # Setting up the title.

    # This radio button gives choice to analyze the data for Human Unit or K9 Unit.
    unit_menu = st.sidebar.radio(
        'Select a Unit', # Title.
        ('Human Unit', 'K9 Unit'), # Options.
        horizontal=True # Alignment default is vertical.
    )

    # This radio button gives choice to view the following features.
    user_menu = st.sidebar.radio(
        'Select an Option',
        ('Overall Analysis', 'Top Ten Deadly...', 'Death Tally', 'State-Wise Analysis', 'Cartogram') # Features.
    )

    # If user select Human Unit section then it will trigger this if block.
    if unit_menu == "Human Unit":
        df = pd.read_csv('main data files/police_deaths.csv') # Storing human unit dataset.
            
        # Calling human_unit_analysis function from human_unit.py file (More info about this is in their respective files).
        human_unit.human_unit_analysis(df, user_menu, unit_menu)

    # If user select K9 Unit section then it will trigger this if block.
    if unit_menu == "K9 Unit":
        df = pd.read_csv('main data files/k9_deaths.csv') # Storing K9 unit dataset.

        # Calling human_unit_analysis function from k9_unit.py file (More info about this is in their respective files).
        k9_unit.k9_unit_analysis(df, user_menu, unit_menu)          
