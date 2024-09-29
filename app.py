"""
    Author : Joris LARMAILLARD-NOIREN
    Email : joris.larmaillard--noiren@efrei.net
"""

import streamlit as st
from streamlit_option_menu import option_menu

### Pages importation
from pages import home_page, music_data_analysis, gov_data_analysis

### Setting the navigation bar
st.set_page_config(page_title="My Portfolio", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

### Remove default sidebar
st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

### Navigation bar with the different pages
selected = option_menu(
    menu_title="Navigation", 
    options=["Home page", "Music Data analysis", "Government Data Analysis"], 
    icons=["house", "graph-up", "bar-chart"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

### Displaying the corresponding page
if selected == "Home page":
    home_page.app()
elif selected == "Music Data analysis":
    music_data_analysis.app()
elif selected == "Government Data Analysis":
    gov_data_analysis.app()
