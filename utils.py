import pandas as pd

### Function to load the data
def load_data(filepath, delimiter: str = None):
    return pd.read_csv(filepath, delimiter=delimiter)

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
def group_data(df: pd.DataFrame, columns_to_group: list, column_referred: str, agg_func: str = 'sum') -> pd.DataFrame:
    """
    Function to group the data according to specified columns and apply an aggregation function

    :param df: The DataFrame to work on
    :param columns_to_group: The columns that will be used to group the data
    :param column_referred: The column on which to apply the aggregation function
    :param agg_func: The aggregation function to apply ('sum', 'mean', 'count', etc.)
    :return: A DataFrame with grouped columns and aggregated results
    """
    # Perform the groupby operation
    grouped = df.groupby(columns_to_group)[column_referred]

    # Apply the aggregation function
    if agg_func == 'sum':
        return grouped.sum().reset_index()
    elif agg_func == 'mean':
        return grouped.mean().reset_index()
    elif agg_func == 'count':
        return grouped.count().reset_index()
    else:
        raise ValueError("Invalid agg_func. Use 'sum', 'mean', 'count', or other valid pandas aggregation functions.")
