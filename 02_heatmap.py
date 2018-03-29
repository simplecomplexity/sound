#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

df_flights = sns.load_dataset('flights')
df_flights.head(5)

df_flights_pivot = pd.pivot_table(data=df_flights, values='passengers',
                                  columns='year', index='month', aggfunc=np.mean)

sns.heatmap(df_flights_pivot)
plt.show()
