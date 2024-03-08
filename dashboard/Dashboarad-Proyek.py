import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

def create_byseason(df):
    byseason_df = daily_df.groupby(by=['season', 'weekday']).agg({

    'total': 'sum'
    })
    
    return byseason_df

def create_bymonth(df):
    monthly_totals = daily_df.groupby(by=['year', 'month']).agg({
        'total': 'sum'
    })

    return monthly_totals

def create_bydaily(df):
    daily_totals = daily_df.groupby(by=['workingday', 'year']).agg({'total': 'sum'})

    return daily_totals

def create_byweather(df):
    weather_hour_totals = hours_df.groupby(by=['weathersit', 'hour']).agg({

    'total': ['sum', 'max', 'min'],

    })
    
    return weather_hour_totals

daily_df = pd.read_csv('daily_data.csv')
hours_df = pd.read_csv('hours_data.csv')

byseason_df = create_byseason(daily_df)
monthly_totals = create_bymonth(daily_df)
daily_totals = create_bydaily(daily_df)
weather_hour_totals = create_byweather(hours_df)

st.header('Bike Sharing Dashboard :sparkles:')

st.subheader("Penyewaan Harian Sepeda By Season")

fig, ax = plt.subplots(figsize=(15, 5))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    y="total",  
    x="season",  
    data=byseason_df.sort_values(by="total", ascending=False),  
    palette=colors,
    ax=ax 
)

ax.set_title("Total Count by Season", loc="center", fontsize=25)  
ax.set_ylabel("Total Count")  
ax.set_xlabel("Season") 
ax.tick_params(axis='x', labelsize=12)  
st.pyplot(fig)

st.subheader("Penyewaan harian sepeda Tertinggi Pertahun berdasarkan Bulan")

# Buat heatmap
fig, ax= plt.subplots(figsize=(10, 5))
sns.heatmap(monthly_totals.pivot_table(index='month', columns='year', values='total'), cmap='Blues')

ax.set_xlabel('Tahun')
ax.set_ylabel('Bulan')
ax.set_title('Total jumlah peminjaman per Bulan dan Tahun')
st.pyplot(fig)

st.subheader("Penyewaan Sepeda di Hari Libur Vs Hari Kerja")
fig, ax= plt.subplots(figsize=(10, 5))
colors = ["#D3D3D3", "#72BCD4"]
sns.barplot(daily_totals.pivot_table(index='year', columns='workingday', values='total'), palette=colors)

ax.set_xlabel('Hari Kerja')
ax.set_ylabel(None)
ax.set_title('Total Peminjaman per Hari Kerja')
st.pyplot(fig)

st.subheader('Maksimal dan Minimal jam peminjaman sepeda berdasarkan cuaca')
fig, ax= plt.subplots(figsize=(10, 5))
sns.barplot(x=weather_hour_totals.index.get_level_values('weathersit'), y=weather_hour_totals['total']['sum'], color='skyblue')

ax.set_xlabel('Cuaca')
ax.set_ylabel('Total Penyewaan')
ax.set_title('Total Penyewaan Sepeda per Jam (Berdasarkan Cuaca)')
ax.set_xticks(weather_hour_totals.index.get_level_values('weathersit'))
st.pyplot(fig)
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(18, 6))

sns.barplot(x=weather_hour_totals.index.get_level_values('hour'), y=weather_hour_totals['total']['min'], ax=ax[0], color='skyblue')
ax[0].set_xlabel('Jam')
ax[0].set_ylabel('Penyewaan Minimum')
ax[0].set_title('Penyewaan Sepeda Minimum per Jam')
ax[0].set_xticks(weather_hour_totals.index.get_level_values('hour'))

# Buat grafik batang untuk maksimum penyewaan
sns.barplot(x=weather_hour_totals.index.get_level_values('hour'), y=weather_hour_totals['total']['max'], ax=ax[1], color='skyblue')
ax[1].set_xlabel('Jam')
ax[1].set_ylabel('Penyewaan Maksimum')
ax[1].set_title('Penyewaan Sepeda Maksimum per Jam')
ax[1].set_xticks(weather_hour_totals.index.get_level_values('hour'))

st.pyplot(fig)