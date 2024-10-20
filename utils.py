import pandas as pd
import json
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import folium
from folium.plugins import MarkerCluster
from prince import MCA

### Function to load the data
def load_data(filepath: str, delimiter: str = None) -> pd.DataFrame:
    """
    Loads data from csv file

    :param filepath: File path that will be loaded
    :param delimiter: File parser
    :return: A DataFrame with data loaded from the csv file
    """
    return pd.read_csv(filepath, delimiter=delimiter)

### Function to load a file
def load_json(jsonfile: str) -> dict:
    """
    Loads data from json file

    :param jsonfile: File path that will be loaded
    :return: Json data loaded from the json file
    """
    with open(jsonfile, 'r') as f:
        return json.load(f)

### Function to select columns from a DataFrame
def select_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Selects columns from a dataframe

    :param df: The DataFrame to select columns from
    :param columns: List of columns to select
    :return: DataFrame with selected columns
    """
    return df[columns]

### Function to drop columns
def drop_columns(df: pd.DataFrame, columns_to_drop: list) -> pd.DataFrame:
    """
    Deletes specific columns from the DataFrame.
    
    :param df: The DataFrame to work on
    :param columns_to_drop: List of columns to be deleted
    :return: DataFrame with deleted columns
    """
    return df.drop(columns=columns_to_drop, axis=1)

### Function to create new columns
def create_columns(df: pd.DataFrame, new_col_name: str, function) -> pd.DataFrame:
    """
    Creates a new column in the DataFrame based on a function.

    :param df: The DataFrame to work on
    :param new_col_name: The name of the new column to be added
    :param function: A function to be applied to generate the new column
    :return: DataFrame with the new column added
    """
    df[new_col_name] = df.apply(function, axis=1)
    return df

### Function to rename a column
def rename_columns(df: pd.DataFrame, columns_dict: dict) -> pd.DataFrame:
    """
    Renames DataFrame columns according to a matching dictionary.
    
    :param df: The DataFrame to work on
    :param columns_dict: Dictionary {old_column: new_column}
    :return: DataFrame with renamed columns
    """
    return df.rename(columns=columns_dict)

### Function to convert the data format
def convert_data(df: pd.DataFrame, column_to_convert: str) -> pd.Series:
    """
    Converts data unit.

    :param df: The DataFrame to work on
    :param column_to_convert: The name of the column to be converted
    :return: Series with converted data
    """
    return df[column_to_convert].apply(lambda x: x * 10 ** (-3))

### Function to set up date format
def set_date_format(df: pd.DataFrame, date_column: str, date_format: str) -> pd.DataFrame:
    """
    Formats a date column in a DataFrame according to the specified format.
    
    :param df: The DataFrame containing the column to be formatted
    :param date_column: The name of the column to be formatted
    :param date_format: The target date format ('%Y-%m-%d')
    :return: DataFrame with formatted date column
    """
    try:
        df[date_column] = pd.to_datetime(df[date_column], format=date_format)
    except Exception as e:
        print(f"Error setting date format: {e}")
    
    return df

### Function to split information
def split_data(df: pd.DataFrame, column_to_separate: str, seperator: str, position: int) -> pd.Series:
    """
    Splits data into a series according to the specified seperator.
    :param df: The DataFrame to work on
    :param column_to_separate: The name of the column to be split
    :param seperator: The separator to split the data
    :param position: The position we want to keep
    :return: Series with the split data
    """
    return df[column_to_separate].str.split(seperator).str[position]

### Function to clean the data
def clean_data(df: pd.DataFrame, columns_to_drop: list = None,
               columns_to_rename: dict = None,
               new_column_info: dict = None,
               date_column: str = None,
               date_format: str = None) -> pd.DataFrame:
    """
    Main function for cleaning data with various operations.
    
    :param df: The DataFrame to be cleaned
    :param columns_to_drop: List of columns to delete
    :param columns_to_rename: Dictionary for renaming columns {old_column: new_column}.
    :param new_column_info: Dictionary where keys are new column names and values are either:
                            - A tuple ('date_split', column_name) for date-based splits
                            - A function to apply to the DataFrame to create the new column
    :param date_column: Name of the column to be formatted
    :param date_format: Target date format
    :return: DataFrame cleaned
    """
    if date_column and date_format:
        df = set_date_format(df, date_column, date_format)

    if new_column_info:
        for new_col, value in new_column_info.items():
            if isinstance(value, tuple) and value[0] == 'date_split':
                ### Special case: Split date into separate year, month, day, etc.
                date_column = value[1]
                df['Year'] = df[date_column].dt.year
                df['Month'] = df[date_column].dt.month
                df['Day'] = df[date_column].dt.day
                df['Day Name'] = df[date_column].dt.day_name()
            elif callable(value[0]):
                ### Apply the custom function to create the new column
                df[new_col] = value[0](df, *value[1:])

    if columns_to_drop:
        df = drop_columns(df, columns_to_drop)
    
    if columns_to_rename:
        df = rename_columns(df, columns_to_rename)
    return df

### Function to filter the data
def filter_data(df: pd.DataFrame, condition: str) -> pd.DataFrame:
    """
    Selecting the data according to a provided query

    :param df: The DataFrame to work on
    :param condition: The condition the data must comply with
    :return: DataFrame filtered
    """
    return df.query(condition)

### Function to count the data based on values or index
def count_data(df: pd.DataFrame, columns_to_count, sort_type: str) -> pd.Series:
    """
    Function to count the occurrences of values in a specified column and sort the result

    :param df: The DataFrame to work on
    :param columns_to_count: The column that will be counted
    :param sort_type: The sorting type that will be applied
    :return: A Series with counts sorted by index or values
    """
    counts = df[columns_to_count].value_counts()
    if sort_type == 'index':
        return counts.sort_index()
    if sort_type == 'value':
        return counts.sort_values(ascending=False)
    else:
        raise ValueError("Invalid sort_by value. Use 'index' or 'values'.")

### Function to group data
def group_data(df: pd.DataFrame, columns_to_group,
               columns_referred=None, agg_func: str = 'sum', name: str = None) -> pd.DataFrame:
    """
    Function to group the data according to specified columns and apply an aggregation function

    :param df: The DataFrame to work on
    :param columns_to_group: The columns that will be used to group the data
    :param columns_referred: The column on which to apply the aggregation function
    :param agg_func: The aggregation function to apply ('sum', 'mean', 'count', etc.)
    :param name: The name of the group
    :return: A DataFrame with grouped columns and aggregated results
    """
    ### Perform the groupby operation
    if columns_referred is not None:
        grouped = df.groupby(columns_to_group)[columns_referred]
    else:
        grouped = df.groupby(columns_to_group)

    ### Apply the aggregation function
    if agg_func == 'sum':
        return grouped.sum().reset_index()
    elif agg_func == 'mean':
        return grouped.mean().reset_index(name=name)
    elif agg_func == 'median':
        return grouped.median().reset_index()
    elif agg_func == 'count':
        return grouped.count().reset_index()
    elif agg_func == 'size':
        return grouped.size().reset_index(name=name)
    else:
        raise ValueError("Invalid agg_func. Use 'sum', 'mean', 'count', or other valid pandas aggregation functions.")

### Function to generate crosstab
def cross_df(df: pd.DataFrame, col1: str, col2: str) -> pd.DataFrame:
    """
    Function to cross the data according to a specified column

    :param df: The DataFrame to work on
    :param col1: First column that will be crossed
    :param col2: Second column that will be crossed
    :return: A DataFrame with crossed columns
    """
    return pd.crosstab(df[col1], df[col2])

### Function to melt a transformed DataFrame
def melt_dataframe(df: pd.DataFrame, columns_to_save: list,
                   columns_to_melt: list, var_name: str, value_name: str) -> pd.DataFrame:
    """
    Function to melt the data according to the specified columns

    :param df: The DataFrame to work on
    :param columns_to_save: Columns that won't change
    :param columns_to_melt: The columns that will be melted
    :param var_name: New column melted name
    :param value_name: New name for the column that contains the values
    :return: New melted DataFrame
    """
    df_melted = pd.melt(df, id_vars=columns_to_save, value_vars=columns_to_melt,
                        var_name=var_name, value_name=value_name)
    return df_melted

### Function for transforming values into dummies
def transform_into_dummies(df: pd.DataFrame, ref_column: str, sep: str = None) -> pd.DataFrame:
    """
    Function to transform data into dummy variables

    :param df: The DataFrame to work on
    :param ref_column: The column on which to apply the aggregation function
    :param sep: Separator to use
    :return: New DataFrame with dummy variables
    """
    return df[ref_column].str.get_dummies(sep=sep)

### Function to compute percentage
def percentage(df: pd.DataFrame, new_col_name: str, col1: str, col2: str) -> pd.Series:
    """
    Function to calculate a percentage between two columns

    :param df: The DataFrame to work on
    :param new_col_name: Name of the new column
    :param col1: First column as numerator
    :param col2: Second column as denominator
    :return: A Series with percentage between two columns
    """
    df[new_col_name] = (df[col1] / df[col2]) * 100
    return df[new_col_name]

### Function to merge two DataFrames

def merge_dataframes(df1: pd.DataFrame, df2: pd.DataFrame, on, how: str = 'inner', *args, **kwargs):
    """
    Function for merging several DataFrames based on specified columns


    :param df1: First DataFrame
    :param df2: Second DataFrame
    :param on: The columns or index on which to merge the DataFrames
    :param how: Merge type ('inner', 'outer', 'left', 'right'), default 'inner'
    :return: Resulting merged DataFrame
    """
    ### Merge df1 and df2 first
    df_merged = pd.merge(df1, df2, on=on, how=how, **kwargs)

    ### Merge additional DataFrames passed in *args
    for df in args:
        df_merged = pd.merge(df_merged, df, on=on, how=how, **kwargs)

    return df_merged

### Function to concatenate DataFrame
def concat_dataframes(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """
    Function to concatenate several DataFrames based on specified columns

    :param df1: First DataFrame to concatenate
    :param df2: Seconde DataFrame to concatenate
    :return: New DataFrame with concatenated DataFrames
    """
    df_concatenated = pd.concat([df1, df2], axis=1)

    return df_concatenated

### Function to fill nan values
def fill_na(df1: pd.DataFrame, df2: pd.DataFrame, col_to_fill: list, on, suffixes) -> pd.DataFrame:
    """
    Function to fill NaN values in a DataFrame

    :param df1: First DataFrame
    :param df2: Second DataFrame
    :param col_to_fill: List of columns to fill
    :param on: Columns to use a reference for merging DataFrame
    :param suffixes: List of suffixes to use
    :return: New filled DataFrame
    """
    df_filled = df1.merge(df2, on=on, suffixes=suffixes, how='left')

    for col in col_to_fill:
        df_filled[col] = df_filled[col].fillna(df_filled[f'{col}_median'])

    df_filled = df_filled.drop([f'{col}_median' for col in col_to_fill], axis=1)
    return df_filled

### Function to make MCA analysis
def make_mca(df: pd.DataFrame, index_ref: str) -> plt.Figure:
    """
    Function to make MCA analysis

    :param df: The DataFrame to work on
    :param index_ref: Column to use as the index
    :return: Plot
    """
    if index_ref:
        df = df.set_index(index_ref)

    mca = MCA(n_components=2)
    mca = mca.fit(df)
    mca_results = mca.transform(df)

    fig = px.scatter(mca_results, 0, 1, text=mca_results.index, width=600, height=600)

    fig.update_traces(textposition='top center')

    fig.update_layout(title_text="MCA Analysis",
                      xaxis=dict(
                          showgrid=True,
                          gridwidth=1
                      ),
                      yaxis=dict(
                          showgrid=True,
                          gridwidth=1
                      ))
    fig.update_xaxes(title_text="Component 1")
    fig.update_yaxes(title_text="Component 2")

    return fig

### Function to create a pie chart
def make_pie(df: pd.DataFrame, title: str = None) -> go.Figure:
    """
    Function to make a pie chart

    :param df: The DataFrame to work on
    :param title: Title of the pie chart
    :return: Plot
    """
    fig = px.pie(df,
                 names=df.index,
                 values=df.values,
                 title=title)

    return fig

### Function to make a simple plot
def simple_plot(df: pd.DataFrame, plot_type: str, path_geojson_file: str = None, loc: str = None,
                color: str = None, hover_name: str = None, hover_data=None, label: dict = None, title: str = None) -> go.Figure:
    """
    Function to plot a scatter plot of a DataFrame

    :param df: The DataFrame to work on
    :param plot_type: The type of plot to create (Ex: mapbox or choropleth)
    :param path_geojson_file: Geojson from which location data are loaded
    :param loc: Column to use as location
    :param color: Column to use as color
    :param hover_name: Name to display while hovering
    :param hover_data: Data to display when hovering
    :param label: Corresponding label for the corresponding data
    :param title: Plot title
    :return: Plot
    """
    if plot_type == 'choropleth':
        fig = px.choropleth(
            df,
            geojson=load_json(path_geojson_file),
            locations=loc,
            featureidkey="properties.code",
            color=color,
            hover_name=hover_name,
            hover_data=hover_data,
            color_continuous_scale="Plasma",
            labels=label,
            title=title
        )

        fig.update_geos(fitbounds="locations", visible=False)
        ### Final plot
        return fig

    elif plot_type == 'mapbox':
        fig = px.choropleth_mapbox(
            df,
            geojson=load_json(path_geojson_file),
            locations=loc,
            featureidkey="properties.code",
            color=color,
            hover_name=hover_name,
            hover_data=hover_data,
            color_continuous_scale="Reds",
            mapbox_style="carto-positron",
            zoom=5,
            center={"lat": 46.603354, "lon": 1.888334},
            opacity=0.5
        )
        fig.update_layout(mapbox_style="open-street-map",
                          title=title,
                          height=800)
        return fig

### Function to make subplots
def subplots(df: pd.DataFrame, path_geojson_file: str, subtitles: tuple = None,
             loc: str = None, hover_infor: str = None, color1: str = None, color2: str = None,
             label1: dict = None, label2: dict = None, title: str = None
             ) -> go.Figure:
    """
    Function to display subplots on one plot

    :param df: The DataFrame to work on
    :param subtitles: Tuples of the two subtitles to display on the subplots
    :param path_geojson_file: Geojson from which location data are loaded
    :param loc: Column to use as location
    :param hover_infor: Column to use as hover information
    :param color1: First color
    :param color2: Second color
    :param label1: Label for first subplot
    :param label2: Label for second subplot
    :param title: Title of the final plot
    :return: Plot
    """

    ### Creating a figure with two columns
    fig = make_subplots(rows=1, cols=2,
                        subplot_titles=subtitles,
                        specs=[[{"type": "choropleth"}, {"type": "choropleth"}]])

    ### First column : 1
    fig.add_trace(
        px.choropleth(
            df,
            geojson=load_json(path_geojson_file),
            locations=loc,
            featureidkey="properties.code",
            color=color1,
            hover_name=hover_infor,
            color_continuous_scale="Plasma",
            labels=label1
        ).data[0],
        row=1, col=1
    )

    ### Second column : 2
    fig.add_trace(
        px.choropleth(
            df,
            geojson=load_json(path_geojson_file),
            locations=loc,
            featureidkey="properties.code",
            color=color2,
            hover_name=hover_infor,
            color_continuous_scale="Plasma",
            labels=label2
        ).data[0],
        row=1, col=2
    )

    ### Setting appearance and geographical boundaries
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title_text=title,
                      height=800)

    ### Displaying the final plot
    return fig

### Function to make a boxplot
def make_boxplot(df: pd.DataFrame, list_columns: list, list_names: list,
                 title: str = None, x_axis: str = None, y_axis: str = None) -> go.Figure:
    """
    Function to make a box plot of different features from a DataFrame

    :param df: The DataFrame to work on
    :param list_columns: List of columns to plot
    :param list_names: Liste of names for each feature
    :param title: Title of the plot
    :param x_axis: Label to use as x axis
    :param y_axis: Label to use as y axis
    """
    fig = go.Figure()
    for column, name in zip(list_columns, list_names):
        fig.add_trace(go.Box(y=df[column], name=name))

    fig.update_layout(
        title=title,
        yaxis_title=y_axis,
        xaxis_title=x_axis
    )

    return fig

### Function to make a bar plot
def make_barplot(df: pd.DataFrame, feature_name: str, reference: str,
                 title: str, labels: dict = None, color: str = None, mode: str = None) -> go.Figure:
    """
    Function to make a bar plot of different features from a DataFrame

    :param df: The DataFrame to work on
    :param feature_name: The feature we want to analyse
    :param reference: What we study the data against
    :param title: Title of the plot
    :param labels: Dictionary of labels to use
    :param color: Specific column to use as color
    :param mode: How to display the bars
    :return: Plot
    """
    fig = px.bar(df,
                 x=feature_name,
                 y=reference,
                 color=color,
                 barmode=mode,
                 title=title,
                 labels=labels)

    return fig

### Function to generate a heatmap
def make_heatmap(df: pd.DataFrame, labels: dict, title: str = None) -> go.Figure:
    """
    Function to make a heatmap of different features from a DataFrame

    :param df: The DataFrame to work on
    :param labels: The labels to use
    :param title: Title of the plot
    """
    fig = px.imshow(df.T,
                    labels=labels,
                    color_continuous_scale="Viridis",
                    aspect="auto",
                    title=title)

    return fig

### Function to display a map with clusters

def disp_clusters(df: pd.DataFrame, feature_info: list, location_col: str, popup_pattern: str) -> folium.Map:
    """
    Function to display the clusters of features from a DataFrame

    :param df: The DataFrame to work on
    :param feature_info: Name of the feature information we want to display
    :param location_col: Name of the column that contains geographical information
    :param popup_pattern: Pattern that will be applied for displaying information
    :return: Map
    """
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

    marker_cluster = MarkerCluster().add_to(m)

    for i, row in df.iterrows():
        popup_text = popup_pattern.format(
            **{col: row[col] for col in feature_info},
            ville=row['ville']
        )

        folium.Marker(
            location=row[location_col].split(','),
            popup=popup_text,
            icon=folium.Icon(color='red', icon="info-sign")
        ).add_to(marker_cluster)

    return m

### Function to display the corresponding commentary
def get_commentary(option: str = None) -> str:
    """
    Function to get the commentary of a given option

    :param option: Option selected from option selector to be displayed
    :return: The commentary corresponding to the chosen option
    """
    comments = {
        'Median price analysis': """
        """,
        'Gasoline price analysis': """
        <p>
            As we can, most of the west departments have a lower price than the rest of France, especially l'Île-de-France.
            Generally speaking, we can see that prices in France for sp98 are around 1.80€ and 1.85€ : this distribution is
            fairly uniform throughout the country, except for Paris, which has a median value over 1.90€ per liter.
            In the case of sp95, the average price range is between 1.70€ and 1.80€ across the country, except in Paris,
            where the price per liter is around 2.0€.
        </p>
        
        <p>
            This price difference between Paris and the rest of the country can be due to several factors :
        </p>
        <ul>
            <li>Higher operating costs in Paris: high rents and property taxes, higher salaries</li>
            <li>Less competition between stations in Paris: fewer large low-cost stations, supermarket stations are rare.</li>
            <li>Delivery and logistics</li>
            <li>Demand effect</li>
        </ul>
        <p>
            Fuel prices in Paris are higher due to a combination of additional costs (logistics, operations, taxes) and
            weaker competition. In addition, local policies and the demand effect play a role. In other regions, the
            presence of supermarket stations and larger supermarkets reduces prices through increased competition.
        </p>
        """,
        'Ethanol price analysis': """
        <p>
            This case is impressive because we see a complete contrast in average prices between e10 and e85 superethanol.
            E10 ethanol is much more expensive nationwide, with an  average price of 1.70€, compared with 0.83€ for e85.
            However, in both cases, there is no real significant difference from one region to another: prices are fairly
            uniform. This may be due to the fact that there aren't as many ethanol-powered vehicles throughout the country
            as there are for other types of vehicle.
        </p>
        """,
        'Gazole price analysis': """
        <p>
            As we can see, the price of diesel is around 1.63€ nationwide. For Corsica and Paris, we see higher costs:
            around 1.75€ for Corsica, and 1.80€ for Paris.
        </p>
        """,
        'GPLc price analysis': """
        <p>
            On average, prices in the region are around €1.0. There is no real variation in price from one département to
            another, except for Corsica, where the average price is around 1.30€. This difference may be due to the cost
            of transporting cLPG between France and Corsica: the cost of transport is therefore included in the price per
            liter of cLPG.
        </p>
        """,
        'E85 & E10 shortage': """
        <p>
            The map above shows the definitive discontinuation rate for each département for superethanol e85, also compared 
            with e10.
            Each rate is represented as a function of the total number of stations per department no longer selling these
            fuels permanently.
            As we can see, this fuel has a fairly high rate of permanent discontinuation across the board, with rates
            approaching **60%** for some departments (such as Aveyron, Haute-Loire, etc.).
            On the other hand, we can see that some départements have low final breakage rates for superethanol e85:
            Essonne, Vaucluse and Haute-Garonne, for example. These departments are mainly located on the outskirts of major 
            cities, which encourages the presence of all types of vehicles, and therefore a need for this fuel.
            Compared with superethanol e10, the shortage rate is a little lower: between **10% and 20%**, except for
            Corsica, of course, because of its geographical location.
            This information can help carmakers to orientate their market, and find out which type of vehicle will be most
            interesting for the populations living in these areas.
        </p>
        """,
        'SP95 & SP98 shortage': """
        <p>
            In the case of unleaded 95, such a high level of permanent discontinuation can be explained by the gradual
            cessation of use of this fuel by private consumers. In fact, the higher the octane rating of gasoline, the
            better combustion is controlled, protecting your engine's performance and longevity. Unleaded 98 therefore
            offers better performance and engine protection than unleaded 95. As a result, fewer and fewer service
            stations will be offering this type of fuel, which has a higher ultimate breakage rate.
        </p>
        """,
        'Gazole shortage': """
        <p>
            As we can see, diesel has a definitive break rate throughout the country. This is perfectly normal, given that 
            the proportion of French vehicles running on diesel is almost **53%**.
        </p>
        """,
        'GPLc shortage': """
        <p>
            There is also a marked shortage in several central and western départements: for example, in the Massif
            Central and around Bordeaux. Departments in the north and east seem less affected overall, with lower
            shortage rates, indicated by lighter colors (around 30-40%). There is considerable variability between
            departments. Some are extremely hard hit, while others show a more stable situation. This heterogeneity
            could be explained by logistical or supply differences.
            To sum up, there is a more severe shortage of cLPG in the south-east and west of the country, while the
            north seems relatively better supplied.
        </p>
        """,
        'Heatmap analysis': """
        As we can see, among the list of fuels, the one with the most definitive break is GPLc, with rates reaching 80% 
        for some departments. And, as we saw earlier, the fuel with the lowest rate of permanent rupture is diesel.
        """,
        'Gas stations distribution analysis': """
        As we can see, **95.5%** of service stations are located on roadsides, which is normal in the case of towns and
        cities, given that most motorists travel in towns and cities: more traffic means more turnover for the station
        owners. In particular, there are far more needs in town than on the motorways: going to work or shopping, so
        there are far more service stations in town.
        Whereas **4.5%** of service stations are located on the edge of France's motorways. That's a total of 453
        gas stations located along motorways throughout the country. Excluding holiday periods, this means fewer
        people passing through, and therefore less need.
        """
    }
    return comments.get(option, "No commentary available for this option.")
