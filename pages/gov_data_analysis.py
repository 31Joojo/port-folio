### Importation des modules
import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
from utils import *
from streamlit_folium import st_folium

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

    st.write("""
            In order to analyse the data correctly, we'll divide the dataset into several different sets.
            A subset of the dataset will be linked to a specific piece of information we wish to analyse. To do this,
            we'll first perform a preliminary data cleansing (on the dataset as a whole), then we'll go through the
            datasets.
    """)

    st.markdown("""
        <p>
        We will have the following subsets of data :
        </p>
        <ul style="list-style-type:circle">
            <li>`df_price` : fuel price analysis
                <ul style="list-style-type:square">
                    <li>Visualize price trends in different regions or cities, compare prices by fuel type, or analyze
                    the impact of price fluctuations over specific periods.</li>
                </ul>
            </li>
            <li>`df_geo`: geographical analysis
                <ul style="list-style-type:square">
                    <li>Explore regional or local disparities in fuel availability and prices.</li>
                </ul>
            </li>
            <li>`df_shortage` : fuel availability and outage management
                <ul style="list-style-type:square">
                    <li>Analyze the frequency and duration of fuel unavailability</li>
                </ul>
            </li>
            <li>`df_availability` : General fuel availability
                <ul style="list-style-type:square">
                    <li>Comparative analysis of fuel availability and non-availability</li>
                </ul>
            </li>
        </ul>
        """, unsafe_allow_html=True)

    ### Data importation
    df = load_data('data/prix-des-carburants-en-france-flux-instantane-v2.csv', delimiter=';')

    df = drop_columns(df, ['horaires', 'horaires_automate_24_24', 'horaires_jour', 'services',
                           'services_service'])

    st.dataframe(df.head(100), height=600)

    ### Price distribution analysis
    st.write("""
            In the next section, we'll move on to an in-depth analysis of the available data. To do this, we'll use a variety of
            interactive graphics to better understand the key trends, correlations and insights that emerge from our dataset.
            These visualizations will enable us to present the results in a clear and intuitive way.
    """)

    ### Analysis of each variable distribution
    df_price = select_columns(df, ['cp', 'ville', 'latitude', 'longitude', 'departement', 'code_departement',
                                   'geom', 'prix', 'e10_prix', 'e85_prix', 'sp95_prix', 'sp98_prix', 'gazole_prix',
                                   'gplc_prix'])

    fig = make_boxplot(df_price,
                       ['e10_prix', 'e85_prix', 'sp95_prix', 'sp98_prix', 'gazole_prix', 'gplc_prix'],
                       ['E10', 'E85', 'SP95', 'SP98', 'Gazole', 'GPLC'],
                       title='Distribution of prices',
                       x_axis='Fuels type',
                       y_axis='Prices (€)')

    st.plotly_chart(fig)

    ### Commentary
    st.markdown("""
        <p>
            We observe that for all fuel types there is a strong presence of outliers. Our dataset presents missing values
            due to several factors :
        </p>
        <ul>
            <li>Some stations don't sell certain types of fuel, so fuel prices are not updated.</li>
            <li>Some values are simply missing, so I think they've just not been recorded, or these outlets don't sell
            these fuels.</li>
        </ul>
        <p>
            Next, we'll calculate the median by department, as it's more robust for asymmetrical distributions or those
            containing extreme values, as in our case. For example, an isolated station with a much higher price could
            affect the average.
        </p>
    """, unsafe_allow_html=True)

    ### Gas stations distributions
    df_crossed = cross_df(df, 'code_departement', 'pop').sum()

    st.plotly_chart(make_pie(df_crossed, 'Populations distribution by type'))

    st.write("""
            As we can see, **95.5%** of service stations are located on roadsides, which is normal in the case of towns
            and cities, given that most motorists travel in towns and cities: more traffic means more turnover for the
            station owners. In particular, there are far more needs in town than on the motorways: going to work or
            shopping, so there are far more service stations in town.
            Whereas **4.5%** of service stations are located on the edge of France's motorways. That's a total of 453
            service stations located along motorways throughout the country. Excluding holiday periods, this means fewer 
            people passing through, and therefore less need.
    """)

    ### Price analysis
    price_per_departement = group_data(df_price,
                                       ['departement', 'code_departement'],
                                       ['sp98_prix', 'sp95_prix', 'gazole_prix', 'e10_prix', 'e85_prix', 'gplc_prix'],
                                       'median')

    price_per_departement_melted = melt_dataframe(price_per_departement,
                                                  ['departement', 'code_departement'],
                                                  ['sp98_prix', 'sp95_prix', 'gazole_prix', 'e10_prix', 'e85_prix'],
                                                  'Fuels type',
                                                  'Median Price')

    st.plotly_chart(
        make_barplot(price_per_departement_melted,
                     'departement',
                     'Median Price',
                     'Median price by department',
                     {'departement': 'Departement',
                      'Median Price': 'Median Price (€/L)',
                      'Fuels type': 'Fuels type'},
                     'Fuels type',
                     'group')
    )

    st.markdown("""
        <p>
            Let's do some visualisation with our data displayed onto the French map.
            We'll use a geoson file of France in order to use a map already split by departement, and display the
            corresponding data to each corresponding departement.
        </p>
        <p>
            To do this, we need to display our map according to each type of fuel. We'll proceed as follows :
        </p>
        <ul>
            <li>First : sp98 and sp95</li>
            <li>Second : e10 and e85</li>
            <li>Third : diesel</li>
            <li>Fourth : gplc</li>
         </ul>
    """, unsafe_allow_html=True)

    st.subheader("Data Visualisation", divider=True)

    st.write("**Service station locations**")

    st.write("""
            The map below shows the geographical location of our service stations. Each station is marked with
            additional information that can be accessed by clicking on the corresponding icons. This interactive map
            makes it easy to explore the distribution of stations, and provides useful details for each outlet.
    """)

    pattern = """
        {ville} :
        \nE10 : {e10_prix} €/L
        \nE85 : {e85_prix} €/L
        \nSP95 : {sp95_prix} €/L
        \nSP98 : {sp98_prix} €/L
        \nGazole : {gazole_prix} €/L
        \nGPLc : {gplc_prix} €/L
    """

    ### Filling NaN values
    df_filled = fill_na(df_price, price_per_departement,
                        ['sp98_prix', 'sp95_prix', 'gazole_prix', 'e10_prix', 'e85_prix', 'gplc_prix'],
                        ['departement', 'code_departement'],
                        ('', '_median'))

    with st.container():
        m = disp_clusters(df_filled,
                  ['e10_prix', 'e85_prix', 'gplc_prix', 'sp98_prix', 'sp95_prix', 'gazole_prix'],
                  'geom',
                  pattern
                  )
        st_folium(m, width=725, height=600)

    st.write("""
                In the following section, we will analyze the prices of different types of fuel by department. For easier
                viewing, you can select the fuels to be compared using the selector. Note that some fuels have been grouped 
                in pairs: unleaded 95 and 98, and ethanol E10 and E85. This grouping is explained by their similarity of use 
                and composition, enabling a more coherent and relevant analysis.
        """)

    ### Selector to choose analysis
    option = st.selectbox(
        "Choose an analysis to display : ",
        ('Gasoline', 'Ethanol', 'Gazole', 'GPLc')
    )

    if option == 'Gasoline':
        st.plotly_chart(subplots(price_per_departement,
                                 'data/departements.geojson',
                                 ("SP98 Price by Department", "SP95 Price by Department"),
                                 'code_departement',
                                 'departement',
                                 'sp98_prix',
                                 'sp95_prix',
                                 {'sp98_prix': 'SP98 Price (€/L)'},
                                 {'sp95_prix': 'SP95 Price (€/L)'},
                                 "SP98 vs SP95 Fuel Prices by Department"))
        st.markdown(get_commentary('Gasoline price analysis'), unsafe_allow_html=True)

    if option == 'Ethanol':
        st.plotly_chart(subplots(price_per_departement,
                                 'data/departements.geojson',
                                 ("E10 Price by Department", "E85 Price by Department"),
                                 'code_departement',
                                 'departement',
                                 'e10_prix',
                                 'e85_prix',
                                 {'e10_prix': 'E10 Price (€/L)'},
                                 {'e85_prix': 'E85 Price (€/L)'},
                                 "E10 vs E85 Fuel Prices by Department"))
        st.markdown(get_commentary('Ethanol price analysis'), unsafe_allow_html=True)

    if option == 'Gazole':
        st.plotly_chart(simple_plot(price_per_departement,
                                    'choropleth',
                                    'data/departements.geojson',
                                    'code_departement',
                                    'gazole_prix',
                                    'departement',
                                    label={'gazole_prix': 'Diesel Price (€/L)'},
                                    title='Median fuel prices by department (diesel)'
                                    ))
        st.markdown(get_commentary('Gazole price analysis'), unsafe_allow_html=True)

    if option == 'GPLc':
        st.plotly_chart(simple_plot(price_per_departement,
                                    'choropleth',
                                    'data/departements.geojson',
                                    'code_departement',
                                    'gplc_prix',
                                    'departement',
                                    label={'gplc_prix': 'GPLC Price (€/L)'},
                                    title='Median fuel prices by department (GPLc)'
                                    ))
        st.markdown(get_commentary('GPLc price analysis'), unsafe_allow_html=True)

    ### Geographical analysis
    st.subheader('Geographical exploration of fuel shortages', divider=True)

