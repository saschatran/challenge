#https://data.worldbank.org/indicator/SI.POV.GINI?end=2023&start=2023&view=bar

df_Gini = pd.read_csv(csv_filepath, skiprows=4) 
df_Gini.head()

#find the unique country vaues in the read data set in domicile_country_name
#drop nan values
df_real['domicile_country_name'] = df_real['domicile_country_name'].replace('United States of America', 'United States')
df_real['domicile_country_name'] = df_real['domicile_country_name'].replace('Hong Kong', 'Hong Kong SAR, China')
df_real['domicile_country_name'] = df_real['domicile_country_name'].replace('ChinaHong Kong', 'Hong Kong SAR, China')
df_real['domicile_country_name'] = df_real['domicile_country_name'].replace('United Kingdom of Great Britain and Northern Ireland', 'United Kingdom')


df_real.dropna(subset=['domicile_country_name'], inplace=True)

#reduce the size of the data set df_Gini to only the countrys in the df_real data set
df_Gini = df_Gini[df_Gini['Country Name'].isin(df_real['domicile_country_name'].unique())]

#if a country has all nan value in 2014-2023 column drop the row
df_Gini.dropna(subset=['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023'], how='all', inplace=True)
df_Gini
