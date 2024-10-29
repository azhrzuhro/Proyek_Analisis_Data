import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Load Data
bike_day = pd.read_csv("dashboard/new_bike_day.csv") 
datetime_columns = ["dteday"]
bike_day.sort_values(by="dteday", inplace=True)
bike_day.reset_index(inplace=True)
 
for column in datetime_columns:
    bike_day[column] = pd.to_datetime(bike_day[column])

min_date = bike_day["dteday"].min()
max_date = bike_day["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )


main_df = bike_day[(bike_day["dteday"] >= str(start_date)) & 
                (bike_day["dteday"] <= str(end_date))]

st.header('Dicoding Collection Dashboard :sparkles:')

st.subheader("Rental Demographics")
# Fungsi Helper untuk Visualisasi

def plot_monthly_rentals(df):
    # Mengubah tipe data kolom 'dteday' menjadi datetime
    df['registration_month'] = pd.to_datetime(df['dteday']).dt.month
    
    # Mengelompokkan data berdasarkan 'registration_month' dan menghitung jumlah pelanggan unik ('casual')
    monthly_customers = df.groupby('registration_month')['casual'].nunique()
    
    # Membuat line plot menggunakan Matplotlib
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(
        monthly_customers.index,
        monthly_customers.values,
        marker='o',
        linewidth=2,
        color="#72BCD4"
    )
    
    ax.set_title("Jumlah Penyewaan Per Bulan", loc="center", fontsize=18)
    ax.set_xticks(range(1, 13))  # Pastikan bulan 1-12 tampil dengan benar
    ax.set_xticklabels([
        "Jan", "Feb", "Mar", "Apr", "Mei", "Jun", 
        "Jul", "Agu", "Sep", "Okt", "Nov", "Des"
    ])
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    
    # Menampilkan plot di Streamlit
    st.pyplot(fig)

def plot_seasonal_and_weather_rentals(df):
    # Mengelompokkan data berdasarkan 'season' dan menjumlahkan total penyewaan ('cnt') untuk setiap musim
    seasonal_rentals = df.groupby('season')['cnt'].sum()

    # Mengelompokkan data berdasarkan 'weathersit', menghitung rata-rata 'cnt',
    # mengatur ulang indeks, dan mengurutkan berdasarkan 'cnt'
    weathersit_with_cnt = (
        df.groupby('weathersit')['cnt']
        .mean()
        .reset_index()
        .sort_values('cnt')
    )

    # Membuat figure dan dua axis untuk subplot
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))

    # Membuat barplot untuk jumlah penyewaan berdasarkan musim
    season_labels = ['Spring', 'Summer', 'Fall', 'Winter']
    sns.barplot(
        x=seasonal_rentals.index, 
        y=seasonal_rentals.values, 
        order=[1, 2, 3, 4], 
        palette='Greens', 
        ax=ax1
    )
    ax1.set_xticks([0, 1, 2, 3])
    ax1.set_xticklabels(season_labels)
    ax1.set_title('Jumlah Penyewaan Berdasarkan Musim', fontsize=18)
    ax1.set_xlabel('Season', fontsize=12)
    ax1.set_ylabel('Jumlah Penyewaan', fontsize=12)

    # Membuat barplot untuk jumlah penyewaan berdasarkan cuaca
    sns.barplot(
        x='cnt', 
        y='weathersit', 
        data=weathersit_with_cnt, 
        palette='Blues', 
        ax=ax2
    )
    ax2.set_title('Jumlah Penyewaan Berdasarkan Cuaca', fontsize=18)
    ax2.set_xlabel('Jumlah Sewa', fontsize=12)
    ax2.set_ylabel('Cuaca', fontsize=12)

    # Menampilkan plot di Streamlit
    st.pyplot(fig)

def plot_holiday_workingday_rentals(df):
    # Mengelompokkan data berdasarkan 'holiday' dan 'workingday'
    holiday_rentals = df.groupby('holiday')['cnt'].sum()
    workingday_rentals = df.groupby('workingday')['cnt'].sum()

    # Label untuk sumbu X
    holiday_labels = ['Non-Holiday', 'Holiday']
    workingday_labels = ['Non-Working Day', 'Working Day']

    # Membuat figure dan axis untuk subplot (2 barplot dalam 1 figure)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Plot untuk 'holiday'
    sns.barplot(x=holiday_rentals.index, y=holiday_rentals.values, palette='Reds', ax=ax1)
    ax1.set_xticks([0, 1])
    ax1.set_xticklabels(holiday_labels)
    ax1.set_title('Jumlah Penyewaan Berdasarkan Hari Libur', fontsize=18)
    ax1.set_xlabel('Holiday', fontsize=12)
    ax1.set_ylabel('Jumlah', fontsize=12)

    # Plot untuk 'workingday'
    sns.barplot(x=workingday_rentals.index, y=workingday_rentals.values, palette='Reds', ax=ax2)
    ax2.set_xticks([0, 1])
    ax2.set_xticklabels(workingday_labels)
    ax2.set_title('Jumlah Penyewaan Berdasarkan Hari Kerja', fontsize=18)
    ax2.set_xlabel('Working Day', fontsize=12)
    ax2.set_ylabel('Jumlah', fontsize=12)

    # Menyesuaikan layout agar lebih rapi
    plt.tight_layout()

    # Menampilkan plot di Streamlit
    st.pyplot(fig)
    
def plot_Analis_RFM_rentals(df):
    # Konversi 'dteday' ke datetime dan tambahkan 'registration_month'
    df['dteday'] = pd.to_datetime(df['dteday'])
    df['registration_month'] = df['dteday'].dt.month

    # Hitung recency untuk setiap pelanggan
    last_rental_date = df.groupby('casual')['dteday'].max()
    recency = (df['dteday'].max() - last_rental_date).dt.days


    # DataFrame untuk Recency
    recency_df = pd.DataFrame({
        'recency': recency, 
        'registration_month': df.groupby('casual')['registration_month'].first()
    })
    # Bandingkan recency antara pelanggan awal dan akhir tahun (misalnya, bulan 1 vs bulan 12)
    early_recency = recency_df[recency_df['registration_month'] == 1]['recency']
    late_recency = recency_df[recency_df['registration_month'] == 12]['recency']

    # Hitung total penyewaan dan bulan aktif per pelanggan
    total_rentals = df.groupby('casual')['cnt'].sum()
    active_months = df.groupby('casual')['registration_month'].nunique()
    avg_monthly_rentals = total_rentals / active_months

    # DataFrame untuk RFM dan segmentasi
    rfm_df = pd.DataFrame({
        'Recency': recency, 
        'Frequency': total_rentals, 
        'Monetary': total_rentals
    })
    rfm_df['R_Quartile'] = pd.qcut(rfm_df['Recency'], 4, labels=range(4, 0, -1))
    rfm_df['F_Quartile'] = pd.qcut(rfm_df['Frequency'], 4, labels=range(1, 5))
    rfm_df['M_Quartile'] = pd.qcut(rfm_df['Monetary'], 4, labels=range(1, 5))
    rfm_df['RFM_Segment'] = (
        rfm_df['R_Quartile'].astype(str) + 
        rfm_df['F_Quartile'].astype(str) + 
        rfm_df['M_Quartile'].astype(str)
    )

    # Total pendapatan per segmen
    segment_revenue = rfm_df.groupby('RFM_Segment')['Monetary'].sum()

    # Membuat figure dengan 1 baris dan 3 kolom
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Plot 1: Boxplot Recency
    sns.boxplot(
        x='registration_month', y='recency', 
        data=recency_df, ax=axes[0]
    )
    axes[0].set_title('Perbedaan Recency antara Pelanggan Awal dan Akhir Tahun')
    axes[0].set_xlabel('Bulan Registrasi')
    axes[0].set_ylabel('Recency (Hari)')

    # Plot 2: Histogram Frequency
    sns.histplot(avg_monthly_rentals, bins=20, ax=axes[1])
    axes[1].set_title('Distribusi Rata-rata Penyewaan per Bulan')
    axes[1].set_xlabel('Rata-rata Penyewaan per Bulan')
    axes[1].set_ylabel('Jumlah Pelanggan')

    # Plot 3: Barplot Monetary
    segment_revenue.plot(kind='bar', ax=axes[2])
    axes[2].set_title('Total Pendapatan per Segmen Pelanggan')
    axes[2].set_xlabel('Segmen Pelanggan (RFM)')
    axes[2].set_ylabel('Total Pendapatan')
    axes[2].tick_params(axis='x', rotation=45)

    # Menyesuaikan layout agar rapi
    plt.tight_layout()

    # Tampilkan plot di Streamlit
    st.pyplot(fig)

# Menampilkan Visualisasi
plot_Analis_RFM_rentals(bike_day)
plot_monthly_rentals(bike_day)
plot_seasonal_and_weather_rentals(bike_day)
plot_holiday_workingday_rentals(bike_day)




