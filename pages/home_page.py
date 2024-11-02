### Importation des modules
import streamlit as st
import base64

def app():
    ### Page title
    st.title("Welcome to my portfolio !")

    ### Subtitle
    st.subheader("About me 🚀", divider='green')

    ### General information
    st.markdown("""
            <style>
            .img-circle {
                border-radius: 50%;
                width: 200px;
            }
            </style>
            <img src="Users/Jorislarmaillard/Downloads/IMG_6376.JPG" class="img-circle"/>
            <p>Joris LARMAILARD-NOIREN</p>
            <p>Email : joris.larmaillard--noiren@efrei.net</p>
            <p>Cursus : on Master degree Data & AI</p>
            <p>
                I'm currently doing a Master 1 in Data and Artificial Intelligence at EFREI Paris, and I'm passionate about data 
                mining and creating powerful visual insights.
                The aim of this portfolio is to demonstrate my skills in data visualisation, by highlighting projects where I 
                analyse my own music listening data, and governmental data.
            </p>
        """, unsafe_allow_html=True)

    ### Skills section
    st.markdown("""
            <p>
                In this section, I present my various IT skills, organized into several categories to give you a complete
                overview of my technical and personal abilities.
            </p>
            <ul style="list-style-type: circle;">
                <li>&#x1F4BB; Programming:
                    <ul style="list-style-type: square;">
                        <li>&#128013; Python</li>
                        <li>&#9749; Java</li>
                        <li>&#x1F310; HTML/CSS</li>
                        <li>&#128189; SQL, PL/SQL</li>
                    </ul>
                </li>
                <li>&#x1F64B;&#127997; Soft skills:
                    <ul style="list-style-type: square;">
                        <li>&#x1F465; Teamwork</li>
                        <li>🦸🏽‍♂️ Autonomy</li>
                        <li>&#128295; Adaptability</li>
                        <li>&#x1F5E3; Communication</li>
                        <li>&#129425; Multitasking</li>
                        <li>&#128373;&#127997; Curiosity</li>
                        <li>&#128119;&#127997; Enthusiasm for taking on new challenges</li>
                        <li>&#128196; Strong writing skills</li>
                    </ul>
                </li>
                <li>&#x1F310; Web Framework :
                    <ul style="list-style-type: square;">
                        <li>Django</li>
                        <li>Node.js</li>
                        <li>Vue.js</li>
                    </ul>
                </li>
            </ul>
        """, unsafe_allow_html=True)

    ### Links to my social networks
    button_style = """
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
        """

    st.markdown(button_style, unsafe_allow_html=True)

    st.markdown("""
        <a href="https://www.linkedin.com/in/joris-larmaillard-noiren/">
            <button>Linkedin</button>
        </a>
        <br>
        <a href="https://github.com/31Joojo">
            <button>GitHub</button>
        </a>
        """, unsafe_allow_html=True)

    with open("assets/CV_Base2_Joris_LARMAILLARD-NOIREN copie.pdf", "rb") as file:
        pdf_bytes = file.read()
        b64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')

    st.markdown(f"""
        <a href="data:application/octet-stream;base64,{b64_pdf}" 
           download="CV_Joris_LARMAILLARD.pdf">
            <button>Download Resume</button>
        </a>
        """, unsafe_allow_html=True)

    ### Subtitle
    st.subheader("Introduction", divider='green')

    ### Introduciton text
    st.markdown("""
        <h4>
            Technologies and tools used :
        </h4>
        <ul>
            <li>Streamlit for the web application</li>
            <li>Python (libraries: pandas, matplotlib/plotly, folium, prince).</li>
            <li>Interactive visualization (maps, graphs).</li>
        </ul>
        <p>
            Through these visualisations, I seek to transform raw information into intuitive and interactive graphics, 
            revealing trends, preferences and behaviours from a new angle.
            My approach combines analytical rigour and creativity to make the data accessible and aesthetically pleasing.
        </p>
        <h4>
            Site structure :
        </h4>
        <ol style="list-style: number;">
            <li>Home page :
                <ul>
                    <li>Introduction to my site and projects.</li>
                    <li>Links to my LinkedIn and GitHub for a quick overview of my background.</li>
                </ul>
            </li>
            <li>Analysis of my personal music data :
                <ul>
                    <li>This section presents an analysis of my music-listening habits (e.g. favorite genres, most-listened-to artists).</li>
                    <li>The aim is to provide a personalized, interactive visualization of my own music data.</li>
                </ul>
            </li>
            <li>Analysis of government data on fuel prices :
                <ul>
                    <li>This page explores fuel prices in France using government data in instantaneous flow.</li>
                    <li>The analysis compares prices between regions, fuel types and brands, with dynamic visualizations (graphs, maps).</li>
                </ul>
            </li>
        </ol>
        <h5>
            Code structure :
        </h5>
        <ul>
            <li>Parent file :
                <ul>
                    <li>This file is the gateway to the site, providing access to the various pages via a simple navigation menu.</li>
                    <li>It also manages the logic required to organize the routes and display the content of each page.</li>
                </ul>
            </li>
            <li>Page files :
                <ul>
                    <li>Three separate files contain the code specific to each page (Home, Music Analysis, Fuel Price Analysis).</li>
                    <li>This separation helps to better organize the code, making the project more modular and easier to maintain.</li>
                </ul>
            </li>
        </ul>
        <h5>
            Choice of structure
        </h5>
        <p>
            I opted for this structure to facilitate navigation and guarantee a fluid user experience. Each page has a clear 
            purpose, and users can quickly access the information they need via the menu.
        </p>
        <h4>
            Reflections and future improvements :
        </h4>
        <ul>
            <li>Project limitations :
                <ul style="list-style-type: square;">
                    <li>No historical data → Difficult to study price trends.</li>
                    <li>Possible anomalies in local prices → Influence of unmeasured external factors (promotions, input error).</li>
                </ul>
            </li>
            <li>Possible improvements :
                <ul style="list-style-type: square;">
                    <li>Integration of new data sources (price history, weather data, etc.)</li>
                    <li>Addition of more advanced interactive filters in Streamlit (by region, city).</li>
                    <li>Additional visualizations to aid decision-making.</li>
                </ul>
            </li>
    """, unsafe_allow_html=True)

    st.markdown("""
            [📂 View source code on GitHub](https://github.com/31Joojo/port-folio/blob/main/pages/home_page.py)
    """)
