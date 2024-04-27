import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def total_aggregate(df, agg_by, ignore_first=False):

    if ignore_first:
        df = df.sort_values(by=['business_entity_doing_business_as_name', 'period_end_date'])
        # remove for each business the first entry
        df = df.groupby('business_entity_doing_business_as_name').apply(lambda x: x.iloc[1:]).reset_index(drop=True)


    # Aggregating likes per date
    aggregated_data = df.groupby('period_end_date')[agg_by].sum().reset_index()

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(aggregated_data['period_end_date'], aggregated_data[agg_by], marker='o')
    plt.title(f'Relative {agg_by} Over Time')
    plt.xlabel('Date')
    plt.ylabel(f'Relative {agg_by}')
    plt.grid(True)
    plt.xticks(rotation=45)  # Rotate date labels for better readability
    plt.tight_layout()
    plt.show()

def pca_plot(df):
    # Standardize the data
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df)  # Assuming 'date' is not part of the numeric features

    # Apply PCA
    pca = PCA(n_components=2)  # Reduce to two components for easy visualization
    principal_components = pca.fit_transform(df_scaled)
    principal_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])

    # Add anomaly labels from Isolation Forest
    principal_df['anomaly'] = df['anomaly']

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.scatter(principal_df['PC1'][principal_df['anomaly'] == 1], principal_df['PC2'][principal_df['anomaly'] == 1], color='blue', label='Normal')
    plt.scatter(principal_df['PC1'][principal_df['anomaly'] == -1], principal_df['PC2'][principal_df['anomaly'] == -1], color='red', label='Anomaly')

    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title('PCA of Dataset (2D Projection)')
    plt.legend()
    plt.grid(True)
    plt.show()