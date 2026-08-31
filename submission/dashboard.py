import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(
    page_title="Dashboard Bike Sharing",
    page_icon="🚲",
    layout="wide"
)

@st.cache_data
def load_data():
    day = pd.read_csv("data_main.csv")
    day["dteday"] = pd.to_datetime(day["dteday"])
    return day

day_df = load_data()

weather_label = {1: "Cerah", 2: "Mendung/Berkabut", 3: "Hujan/Salju Ringan", 4: "Cuaca Ekstrem"}
season_label = {1: "Semi", 2: "Panas", 3: "Gugur", 4: "Dingin"}

day_df["weather_label"] = day_df["weathersit"].map(weather_label)
day_df["season_label"] = day_df["season"].map(season_label)

st.sidebar.header("Filter Data")

season_options = st.sidebar.multiselect(
    "Pilih Musim",
    options=day_df["season_label"].unique(),
    default=day_df["season_label"].unique()
)

weather_options = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca",
    options=day_df["weather_label"].unique(),
    default=day_df["weather_label"].unique()
)

date_range = st.sidebar.date_input(
    "Rentang Tanggal",
    value=(day_df["dteday"].min(), day_df["dteday"].max()),
    min_value=day_df["dteday"].min(),
    max_value=day_df["dteday"].max()
)

filtered_df = day_df[
    (day_df["season_label"].isin(season_options)) &
    (day_df["weather_label"].isin(weather_options)) &
    (day_df["dteday"] >= pd.to_datetime(date_range[0])) &
    (day_df["dteday"] <= pd.to_datetime(date_range[1]))
]

st.title("🚲 Dashboard Analisis Bike Sharing")
st.markdown("Dashboard ini menampilkan hasil analisis pengaruh **cuaca** dan **musim** terhadap jumlah penyewaan sepeda.")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Penyewaan", f"{filtered_df['cnt'].sum():,.0f}")
col2.metric("Rata-rata Harian", f"{filtered_df['cnt'].mean():,.0f}")
col3.metric("Penyewaan Tertinggi", f"{filtered_df['cnt'].max():,.0f}")
col4.metric("Jumlah Hari (data)", f"{filtered_df.shape[0]:,}")

st.markdown("---")

st.header("1. Bagaimana Pengaruh Kondisi Cuaca (Cerah, Mendung, dan Hujan Ringan) terhadap Jumlah Penyewaan Sepeda Selama Periode 2011-2012?")

col_a, col_b = st.columns([2, 1])

with col_a:
    weather_summary = (
        filtered_df.groupby("weather_label")["cnt"]
        .mean()
        .reindex(["Cerah", "Mendung/Berkabut", "Hujan/Salju Ringan", "Cuaca Ekstrem"])
        .dropna()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=weather_summary, x="weather_label", y="cnt", ax=ax, palette="Blues_d")
    ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Rata-rata Jumlah Penyewaan")
    st.pyplot(fig)

with col_b:
    st.markdown("**Insight:**")
    st.markdown(
        """
        - Semakin buruk cuaca, semakin rendah rata-rata penyewaan sepeda.
        - Penurunan dari cuaca **Cerah** ke **Hujan Ringan** mencapai lebih dari **60%**.
        - Kategori **Cuaca Ekstrem** sangat jarang terjadi pada data harian.
        """
    )

st.markdown("---")

st.header("2. Bagaimana Pola Jumlah Penyewaan Sepeda pada Tiap Musim (Semi, Panas, Gugur, Dingin) Selama Periode 2011-2012, dan Musim Mana yang Memiliki Rata-rata Penyewaan Tertinggi?")

col_c, col_d = st.columns([2, 1])

with col_c:
    season_summary = (
        filtered_df.groupby("season_label")["cnt"]
        .mean()
        .reindex(["Semi", "Panas", "Gugur", "Dingin"])
        .dropna()
        .reset_index()
        .sort_values("cnt", ascending=False)
    )

    fig2, ax2 = plt.subplots(figsize=(7, 4))
    sns.barplot(data=season_summary, x="season_label", y="cnt", ax=ax2, palette="Oranges_d")
    ax2.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Musim")
    ax2.set_xlabel("Musim")
    ax2.set_ylabel("Rata-rata Jumlah Penyewaan")
    st.pyplot(fig2)

with col_d:
    top_season = season_summary.iloc[0]["season_label"]
    st.markdown("**Insight:**")
    st.markdown(
        f"""
        - Musim dengan rata-rata penyewaan **tertinggi**: **{top_season}**.
        - Musim **Semi** memiliki rata-rata penyewaan **terendah**.
        - Selisih rata-rata antara musim tertinggi dan terendah mencapai **>50%**, menunjukkan pengaruh musim yang signifikan.
        """
    )

st.markdown("---")

st.header("3. Analisis Lanjutan: Kombinasi Musim dan Cuaca")

combo = (
    filtered_df.groupby(["season_label", "weather_label"])["cnt"]
    .mean()
    .reset_index()
)

fig3, ax3 = plt.subplots(figsize=(9, 4.5))
sns.barplot(
    data=combo,
    x="season_label",
    y="cnt",
    hue="weather_label",
    order=["Semi", "Panas", "Gugur", "Dingin"],
    ax=ax3
)
ax3.set_title("Rata-rata Penyewaan Berdasarkan Kombinasi Musim dan Cuaca")
ax3.set_xlabel("Musim")
ax3.set_ylabel("Rata-rata Jumlah Penyewaan")
ax3.legend(title="Cuaca", bbox_to_anchor=(1.02, 1), loc="upper left")
st.pyplot(fig3)

st.markdown(
    """
    **Insight:** Efek cuaca buruk konsisten menurunkan penyewaan di semua musim,
    namun besarnya penurunan berbeda antar musim — cuaca hujan pada musim panas
    tampak menurunkan penyewaan lebih tajam dibanding cuaca hujan pada musim gugur.
    """
)

st.markdown("---")

with st.expander("Lihat Data Mentah (setelah difilter)"):
    st.dataframe(filtered_df)

st.caption("Dashboard dibuat dengan Streamlit — Dataset: Bike Sharing (Capital Bikeshare, 2011-2012)")
