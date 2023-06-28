# Function that creates a df filtered with a specific province
def get_province_df(df, province):
    df = df.copy()
    df = df.loc[df['Province'] == province]
    return df


# Function that creates a df filtered with a specific region
def get_region_df(df, region):
    df = df.copy()
    df = df.loc[df['Region'] == region]
    return df


# Function that creates a df filtered with a specific macro-area
def get_zone_df(df, area):
    df = df.copy()
    df = df.loc[df['Area'] == area]
    return df


# Function that finds the increasing crimes over the years (returns a dict with type of crime and variation percentage)
def find_increasing_rates(df):
    df = df.copy()
    crimes = list(df['Crime'].unique())
    increasing_crimes = []
    increasing_crimes_with_values = {}
    for crime in crimes:
        value_2006 = df.loc[(df['Crime'] == crime) & (df['Year'] == 2006), 'Value'].values
        value_2021 = df.loc[(df['Crime'] == crime) & (df['Year'] == 2021), 'Value'].values
        if value_2006.size > 0 and value_2021.size > 0:
            if value_2021 > value_2006 and value_2006 != 0:
                increasing_crimes.append(crime)
                percentage_increase = ((value_2021 - value_2006) / value_2006)
                percentage_increase_format = "{:.2%}".format(percentage_increase[0])
                increasing_crimes_with_values[crime] = percentage_increase_format 
    return increasing_crimes_with_values


# Function that finds the most decreasing crimes over the years, under a certain threshold (returns a dict with type of crime and variation percentage)
def find_decreasing_rates(df, threshold):
    df = df.copy()
    crimes = list(df['Crime'].unique())
    decreasing_crimes = []
    decreasing_crimes_with_rates = {}
    for crime in crimes:
        value_2006 = df.loc[(df['Crime'] == crime) & (df['Year'] == 2006), 'Value'].values
        value_2021 = df.loc[(df['Crime'] == crime) & (df['Year'] == 2021), 'Value'].values
        if value_2006.size > 0:
            if value_2021 < value_2006:
                decreasing_crimes.append(crime)
                percentage_decrease = ((value_2021 - value_2006) / value_2006)
                if percentage_decrease < threshold:
                    percentage_decrease_formatted = "{:.2%}".format(percentage_decrease[0])
                    decreasing_crimes_with_rates[crime] = percentage_decrease_formatted
    return decreasing_crimes_with_rates