import pandas as pd
import numpy as np


def impute_followers(data):
    brand = "business_entity_doing_business_as_name"
    data = data.sort_values(by=[brand, 'period_end_date'])

    # drop the following columns
    drop_cols = ["period_end_date",	"compset_group", "compset", "Country Name", "lag_1_date", "lag_1_company",
                "legal_entity_name",	"domicile_country_name",	"ultimate_parent_legal_entity_name",	"primary_exchange_name"]
    df = data.drop(drop_cols, axis=1)

     # Get unique brands
    brands = df[brand].unique()
    print(brands)

    columns = ["followers"]

    for cols in columns:
        if cols == brand:
            continue

        for b in brands:
            # Select rows for the brand
            brand_df = df[df[brand] == b]
            # Indices for the brand in original df
            indices = brand_df.index

            # Forward fill then backward fill to handle first and last missing values
            df.loc[indices, cols] = brand_df[cols].fillna(method='ffill').fillna(method='bfill')

            # Impute missing values between known values by averaging adjacent values
            missing_mask = pd.isnull(df.loc[indices, cols])
            while missing_mask.any():
                df.loc[indices, cols] = df.loc[indices, cols].fillna((df[cols].shift(-1) + df[cols].shift(1)) / 2)
                missing_mask = pd.isnull(df.loc[indices, cols])
    df["period_end_date"] = data["period_end_date"]
    return df

def impute_by_mean(df):
    # group by brand and impute missing values by mean
    brand = "business_entity_doing_business_as_name"
    df = df.sort_values(by=[brand, 'period_end_date'])

    # drop period_end_date
    df = df.drop("period_end_date", axis=1)

    # get mean of values ignoring nan
    numeric_cols = df.select_dtypes(include='number').columns
    df[numeric_cols] = df.groupby(brand)[numeric_cols].transform(lambda x: x.fillna(x.mean()))


    return df