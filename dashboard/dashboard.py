import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
sns.set(style='whitegrid')

# Load the dataset
df_day = pd.read_csv('day.csv')
df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_day['year'] = df_day['dteday'].dt.year

# Sidebar settings
st.header('Analisis Dataset Bike Sharing :sparkles:')
st.sidebar.image("https://storage.googleapis.com/kaggle-datasets-images/3556223/6194875/c51f57d9f027c00fc8d573060eef197b/dataset-cover.jpeg", width=300)
min_date = df_day['dteday'].min().date()
max_date = df_day['dteday'].max().date()

# Date range filter
start_date, end_date = st.sidebar.date_input(
    label='Rentang Waktu',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Convert date objects to datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filtering data based on selected date range
filtered_data = df_day[(df_day['dteday'] >= start_date) & (df_day['dteday'] <= end_date)]

# Calculate today's count and yesterday's count
todays_cnt = int(filtered_data['cnt'].iloc[-1])
yesterdays_cnt = int(filtered_data['cnt'].iloc[-2])

# Display the metric in the sidebar with thousand separators
st.sidebar.metric(
    label="Pertumbuhan harian pengguna",
    value=todays_cnt,
    delta=yesterdays_cnt
)


# Daily User
daily_users_data = filtered_data.groupby('dteday').agg({
    'casual': 'sum',
    'registered': 'sum',
    'cnt': 'sum'
}).reset_index()

st.subheader('Total Users')

col1, col2, col3 = st.columns(3)

def format_number(number):
    return f"{number:,}"

with col1:
    total_casual = daily_users_data.casual.sum()
    st.metric("Total Casual Users", value=format_number(total_casual))

with col2:
    total_registered = daily_users_data.registered.sum()
    st.metric("Total Registered Users", value=format_number(total_registered))

with col3:
    total_cnt = daily_users_data.cnt.sum()
    st.metric("Total Users", value=format_number(total_cnt))


# PLOT 1
user_counts_data = df_day[['casual', 'registered']].sum()

# Plotting pie plot
fig_pie, ax_pie = plt.subplots()
ax_pie.pie(user_counts_data, labels=user_counts_data.index, autopct='%2.1f%%', startangle=90, colors=['#FFA07A', '#90CAF9'])
ax_pie.axis('equal')
ax_pie.set_title("User Percentages (Casual vs Registered)")

# Display the plot in Streamlit
st.pyplot(fig_pie)


#PLOT 2
st.subheader('Daily Users')
# set figure size
fig_fh3, ax_fh3 = plt.subplots(figsize=(16, 8))
# Plotting
sns.lineplot(x='dteday', y='casual', data=daily_users_data, ax=ax_fh3, label='Casual', marker='o', color="#FFA07A")
sns.lineplot(x='dteday', y='registered', data=daily_users_data, ax=ax_fh3, label='Registered', marker='o', color="#90CAF9")
ax_fh3.set_ylabel("User Counts")
ax_fh3.set_xlabel("Order Date")
ax_fh3.set_title("Casual and Registered Users Counts per Day")
ax_fh3.tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better readability
ax_fh3.legend(["Casual", "Registered"])

# Display the plot in Streamlit
st.pyplot(fig_fh3)


#PLOT 3

st.subheader('Users vs Temperature')

# Map numeric season values to labels
season_mapping = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Autumn'}
filtered_data['season'] = filtered_data['season'].map(season_mapping)

# Plotting
fig_temp, ax_temp = plt.subplots(figsize=(12, 6))
ax_temp.scatter(filtered_data['casual'], filtered_data['temp'], label='Casual')
ax_temp.scatter(filtered_data['registered'], filtered_data['temp'], label='Registered')
ax_temp.set_xlabel('Jumlah Pengguna')
ax_temp.set_ylabel('Suhu (normalize)')
ax_temp.legend()
ax_temp.set_title('Relationship Between Bike User and Temperature')

# Display the plot in Streamlit
st.pyplot(fig_temp)

# Aggregated data
season_data = filtered_data.groupby('season').agg({
    'registered': 'sum',
    'casual': 'sum'
}).reset_index()

# Aggregated data for plotting
plot_data = filtered_data.groupby(['temp', 'atemp']).agg({
    'cnt': 'sum'
}).reset_index()

#subplot 1
fig, ax = plt.subplots()
sns.regplot(x='cnt', y='temp', data=plot_data, ax=ax, label='temp', color="#FFA07A", line_kws={'color': 'red'})
ax.set_ylabel("User Counts")
ax.set_xlabel("Temperature")
ax.set_title("Total User vs Temperature")
ax.legend()

#subplot 2
fig2, ax = plt.subplots()
sns.regplot(x='cnt', y='atemp', data=plot_data, ax=ax, label='atemp', color="#90CAF9", line_kws={'color': 'red'})
ax.set_ylabel("User Counts")
ax.set_xlabel("Temperature")
ax.set_title("Total User vs ATemperature")
ax.legend()

# Display the plot in Streamlit
col1, col2 = st.columns(2)
with col1:
    st.pyplot(fig)

with col2:
    st.pyplot(fig2)

# Expander for additional information
with st.expander("Informasi Tambahan"):
    st.write("""
    Secara umum, semakin tinggi temperatur udara (temp dan atemp), maka semakin banyak pengguna Bike Sharing.\n
    Ket:\n
    - **casual**: jumlah pengguna casual
    - **registered**: jumlah pengguna terdaftar
    - **temp**: suhu normal dalam Celsius. Nilai-nilai ini diperoleh melalui (t-t_min)/(t_max-t_min), t_min=-8, t_max=+39 (hanya dalam skala per jam)
    - **atemp**: suhu rasa normal dalam Celsius. Nilai-nilai ini diperoleh melalui (t-t_min)/(t_max-t_min), t_min=-16, t_max=+50 (hanya dalam skala per jam)
    """)


#PLOTTING 4

st.subheader('Users vs Season')

fig_fh1, ax_fh1 = plt.subplots()
sns.barplot(x='season', y='registered', data=season_data, ax=ax_fh1, label='Registered', color="#90CAF9")
sns.barplot(x='season', y='casual', data=season_data, ax=ax_fh1, label='Casual', color="#FFA07A")
ax_fh1.set_ylabel("Count")
ax_fh1.set_title(f"Casual and Registered User by Season")
ax_fh1.legend()

# Display the plot in Streamlit
st.pyplot(fig_fh1)


#PLOTTING 5

st.subheader('Users vs Weather')

season_data= df_day.groupby('weathersit').agg({
    'casual':'sum',
    'registered':'sum'
}).reset_index()
fig_fh1, ax_fh1 = plt.subplots()
sns.barplot(x='weathersit', y='registered', data=season_data, ax=ax_fh1, label='Registered', color="#90CAF9")
sns.barplot(x='weathersit', y='casual', data=season_data, ax=ax_fh1, label='Casual', color="#FFA07A")
ax_fh1.set_ylabel("Count")
ax_fh1.set_title(f"Casual and Registered User by Weather")
ax_fh1.legend()

# Display the plot in Streamlit
st.pyplot(fig_fh1)

with st.expander("Informasi Tambahan"):
    st.write("""
    Angka 1e6 pada plot yang tertampil adalah notasi ilmiah untuk bilangan 1.000.000.\n
    Secara umum, semakin baik cuacanya, semakin banyak pula pengguna Bike Sharing dengan 1 cuaca paling baik dan 3 cuaca paling buruk.\n
    Ket:\n
    - **1**: Clear, Few clouds, Partly cloudy, Partly cloudy
    - **2**:  Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist
    - **3**: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds
    """)


# PLOTTING 6

st.subheader('Users vs Hour')

# Hourly user counts
cnt_hour = [39130, 24164, 16352, 8174, 4428, 14261, 55132, 154171, 261001, 159438,
            126257, 151320, 184414, 184919, 175652, 183149, 227748, 336860, 309772, 226789,
            164550, 125445, 95612, 63941]


# PLOTTING 6
# Hourly user counts
cnt_hour = [39130, 24164, 16352, 8174, 4428, 14261, 55132, 154171, 261001, 159438,
            126257, 151320, 184414, 184919, 175652, 183149, 227748, 336860, 309772, 226789,
            164550, 125445, 95612, 63941]

# Plotting
fig_fh2, ax_fh2 = plt.subplots(figsize=(12, 6))
hours = np.arange(24)
sns.lineplot(x=hours, y=cnt_hour, ax=ax_fh2, marker='o', color="#90CAF9")
ax_fh2.set_ylabel("Count")
ax_fh2.set_xlabel("Hour")
ax_fh2.set_title("Hourly Users")
ax_fh2.set_xticks(hours)  # Mengatur posisi sumbu x sesuai dengan jumlah jam dalam sehari
ax_fh2.tick_params(axis='x', rotation=45)

# Tambahkan garis vertikal pada jam 5, 10, 15, dan 20
for hour in [5, 10, 15, 20]:
    plt.axvline(x=hour, linestyle='--', color='red')

# Display the plot in Streamlit
st.pyplot(fig_fh2)


with st.expander("Informasi Tambahan"):
    st.write("""
            Perhatikan bahwa data yang digunakan adalah total pengguna dari Januari 2011 hingga 2013 untuk jam 0 hingga 23. 
            Data ini tidak disinkronkan dengan filter "Rentang Waktu" yang diggunakan.\n
            Plot Di atas adalah klasterisasi sederhana untuk membagi jam pelayanan Bike Sharing dalam beberapa kategori. Kategori yang digunakan adalah:\n
            - **Jam sepi pengguna**:  Untuk jam sepi pengguna dari tabel diatas adalah dari jam 0 hingga 5
            - **Jam sedang pengguna**: Untuk jam sedang pengguna dari tabel diatas adalah jetelah jam 10 hingga jam 15, lalu diikuti oleh jam 20 hingga sebelum jam 0.
            - **Jam ramai pengguna**: Untuk jam sedang pengguna dari tabel diatas adalah jetelah jam 5 hingga jam 10, lalu diikuti oleh jam 15 hingga sebelum jam 20.\n
            Asumsi yang bisa diambil dari klasterisasi tersebut adalah bahwa Bike Sharing ramai pengguna pada jam berangkat kerja dan saat pulang kerja. Pada siang hari, 
            pengguna cenderung "standar" atau tidak terlalu ramai. Sedangkan pada saat larut malam hingga pagi saat masih istirahat, pengguna sangat sedikit.
    """)