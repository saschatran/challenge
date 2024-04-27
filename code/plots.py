import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def total_aggregate(df, agg_by):
    # Aggregating likes per date
    aggregated_data = df.groupby('period_end_date')[agg_by].sum().reset_index()

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(aggregated_data['period_end_date'], aggregated_data[agg_by], marker='o')
    plt.title(f'Total {agg_by} Over Time')
    plt.xlabel('Date')
    plt.ylabel(f'Total {agg_by}')
    plt.grid(True)
    plt.xticks(rotation=45)  # Rotate date labels for better readability
    plt.tight_layout()
    plt.show()