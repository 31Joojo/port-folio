### Importation des modules
import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
from utils import *

def app():
    ### Page title
    st.title("Government data analysis")

    ### Subtitle
    st.subheader("Introduction", divider=True)

    st.write("""
            In this section, I'll be analyzing government data on fuel prices in France, updated in an instant feed.
            Thanks to this data, I'll be able to track price trends in different regions and identify market trends or
            fluctuations.
            The aim is to provide a clear and accessible view of the current situation of the fuel market in France.
    """)

    ### Data cleaning
    df = load_data('data/prix-des-carburants-en-france-flux-instantane-v2.csv', delimiter=';')

    df = clean_data(df,
                    columns_to_drop=['horaires', 'horaires_automate_24_24',
                                     'horaires_jour', 'services', 'services_service'])
