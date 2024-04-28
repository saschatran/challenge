import pandas as pd


def process_gini(df):
    df_Gini = pd.read_csv("../data/API_SI.POV.GINI_DS2_en_csv_v2_213326.csv", skiprows=4) 
    df_real = df.copy()

    df_Gini['Country Name'] = df_Gini['Country Name'].replace('United States', 'united states of america')
    df_Gini['Country Name'] = df_Gini['Country Name'].replace('Hong Kong SAR, China', 'hong kong')
    df_Gini['Country Name'] = df_Gini['Country Name'].replace('United Kingdom', 'united kingdom of great britain and northern ireland')

    df_real.dropna(subset=['domicile_country_name'], inplace=True)

    # remove leading and trailing whitespaces and convert to lowercase
    #df_Gini = df_Gini.map(lambda x: x.strip().lower() if isinstance(x, str) else x)
    for varname in df.columns:
        # 1. remove leading and trailing whitespaces and convert to lowercase
        df[varname] = df[varname].apply(lambda x: x.strip().lower() if isinstance(x, str) else x)

   
    #reduce the size of the data set df_Gini to only the countrys in the df_real data set
    df_Gini = df_Gini[df_Gini['Country Name'].isin(df_real['domicile_country_name'].unique())]
  

    #if a country has all nan value in 2014-2023 column drop the row
    df_Gini.dropna(subset=['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023'], how='all', inplace=True)

    # drop irrelevant columns
    df_Gini.drop(columns=["Country Code", "Indicator Name", "Indicator Code", "Unnamed: 68"], inplace=True)

    # Reshape df1 to have 'Year' and 'value' columns
    df_Gini = pd.melt(df_Gini, id_vars=['Country Name'], var_name='Year', value_name='Gene Index')

    # Convert 'Year' to int (if necessary)
    df_Gini['Year'] = df_Gini['Year'].astype(int)

    return df_Gini
