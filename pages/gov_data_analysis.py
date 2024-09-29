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

    ### CSS for the gear animation
    st.markdown(
        """
        <style>
        .gear-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 400px;
        }

        .gear {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: #6c757d;
            position: relative;
            animation: spin 2s linear infinite;
        }

        .gear:before, .gear:after {
            content: "";
            position: absolute;
            background: #6c757d;
            border-radius: 50%;
        }

        .gear:before {
            width: 25%;
            height: 25%;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
        }

        .gear:after {
            width: 15%;
            height: 15%;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .under-construction-text {
            margin-top: 20px;
            font-size: 20px;
            font-weight: bold;
            color: #6c757d;
        }
        </style>
        """, unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="gear-container">
            <div class="gear"></div>
            <div class="under-construction-text">This section is under construction.</div>
        </div>
        """, unsafe_allow_html=True
    )

