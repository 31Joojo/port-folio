import pandas as pd
import json
import plotly.express as px
from matplotlib import pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go

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
def group_data(df: pd.DataFrame, columns_to_group: list,
               column_referred: str = None, agg_func: str = 'sum', name: str = None) -> pd.DataFrame:
    """
    Function to group the data according to specified columns and apply an aggregation function

    :param df: The DataFrame to work on
    :param columns_to_group: The columns that will be used to group the data
    :param column_referred: The column on which to apply the aggregation function
    :param agg_func: The aggregation function to apply ('sum', 'mean', 'count', etc.)
    :param name: The name of the group
    :return: A DataFrame with grouped columns and aggregated results
    """
    ### Perform the groupby operation
    grouped = df.groupby(columns_to_group)[column_referred]

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
def transform_into_dummies(df: pd.DataFrame, ref_column: str, seperator: str = None) -> pd.DataFrame:
    """
    Function to transform data into dummy variables

    :param df: The DataFrame to work on
    :param ref_column: The column on which to apply the aggregation function
    :param seperator: Separator to use
    :return: New DataFrame with dummy variables
    """
    return df[ref_column].str.get_dummies(seperator=seperator)

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

def merge_dataframes(df1: pd.DataFrame, df2: pd.DataFrame, on, how: str ='inner', *args, **kwargs):
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
    df_concatenated = pd.concat(df1, df2, axis=1)

    return df_concatenated

### Function to make a simple plot
def simple_plot(df: pd.DataFrame, type: str, path_geojson_file: str = None, loc: str = None,
                color: str = None, hover_name: str = None, hover_data: str = None, label: dict = None, title: str = None) -> None:
    """
    Function to plot a scatter plot of a DataFrame

    :param df: The DataFrame to work on
    :param type: The type of plot to create (Ex: mapbox or choropleth)
    :param path_geojson_file: Geojson from which location data are loaded
    :param loc: Column to use as location
    :param color: Column to use as color
    :param hover_name: Name to display while hovering
    :param hover_data: Data to display when hovering
    :param label: Corresponding label for the corresponding data
    :param title: Title of the plot
    """
    if type == 'choropleth':
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

        fig.update_layout(fitbounds="locations", visible=False)
        ### Final plot
        fig.show()

    elif type == 'mapbox':
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
        fig.update_layout(mapboxstyle="open-street-map",
                          title=title,
                          height=800)

### Function to make subplots
def subplots(df: pd.DataFrame, path_geojson_file: str, subtitles: tuple = None,
             loc: str = None, hover_infor: str = None, color1: str = None, color2: str = None,
             label1: dict = None, label2: dict = None, title: str = None
             ) -> None:
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
    """

    ### Creating a figure with two columns
    fig = make_subplots(rows=1, cols=2,
                        subplot_titles=subtitles,
                        specs=[[{"type": "choropleth"}, {"type": "choropleth"}]])

    ### First column : 1
    fig.add_trace(
        px.choropleth(
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
    fig.show()

### Function to make a boxplot
def make_boxplot(df: pd.DataFrame, list_columns: list, list_names: list,
                 title: str = None, x_axis: str = None, y_axis: str = None) -> None:
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

    fig.show()

### Function to make a bar plot
def make_barplot(df: pd.DataFrame, feature_name: str, reference: str,
                 title: str, labels: dict = None, color: str = None, mode: str = None) -> None:
    """
    Function to make a bar plot of different features from a DataFrame

    :param df: The DataFrame to work on
    :param feature_name: The feature we want to analyse
    :param reference: What we study the data against
    :param title: Title of the plot
    :param labels: Dictionary of labels to use
    :param color: Specific column to use as color
    :param mode: How to display the bars
    """
    fig = px.bar(df,
                 x=feature_name,
                 y=reference,
                 color=color,
                 barmode=mode,
                 title=title,
                 labels=labels)

    fig.show()

### Function to generate a heatmap
def make_heatmap(df: pd.DataFrame, labels:dict, title: str = None) -> None:
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

    fig.show()

