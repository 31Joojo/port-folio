### Importation des modules
import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import utils as ut

def app():
    ### Page title
    st.title("Welcome to my portfolio !")

    ### Subtitle
    st.subheader("Introduction", divider='green')

    ### Introduciton text
    st.write("""
        I'm currently doing a Master 1 in Data and Artificial Intelligence at EFREI Paris, and I'm passionate about data mining and creating powerful visual insights.
        The aim of this portfolio is to demonstrate my skills in data visualisation, by highlighting projects where I analyse my own music listening data.

        Through these visualisations, I seek to transform raw information into intuitive and interactive graphics, revealing trends, preferences and behaviours from a new angle.
        My approach combines analytical rigour and creativity to make the data accessible and aesthetically pleasing.
        """)
    
    ### Subtitle
    st.subheader("About me 🚀", divider='green')

    ### General information
    st.markdown("""
        <p>Name : Joris LARMAILARD-NOIREN</p>
        <p>Email : joris.larmaillard--noiren@efrei.net</p>
        <p>Cursus : on master degree Data & AI</p>
    """, unsafe_allow_html=True)

    ### Links to my social networks
    st.markdown("""
    <style>
        button {
            background-color: #D4E6B5;
            width: 100%;
            border: 2px solid white;
            border-radius: .25cm;
            padding: 10px;
            margin: 10px auto;
        }
        
        button:hover {
            color: #D4E6B5;
            background-color: white;
            border: 2px solid black;
        }
    </style>
    <a href="https://www.linkedin.com/in/joris-larmaillard-noiren/">
        <button>Linkedin</button>
    </a>
    <br>
    <a href="https://github.com/31Joojo">
        <button>GitHub</button>
    </a>
    """, unsafe_allow_html=True)