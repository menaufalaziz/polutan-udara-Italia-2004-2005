import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title = "Dashboard kualitas udara",
    page_icon = "🌫️",
    layout = "wide"
)

# Load data
@st.cache_data
def load_data():
    dfudara = pd.read_csv("AirQualityUCI.csv", sep=";", decimal=",")
    dfudara = dfudara.dropna(how="all", axis=1)
    dfudara = dfudara[dfudara["Date"].notna()]

    dfudara["Datetime"] = pd.to_datetime(
        dfudara["Date"] + " " + dfudara["Time"],
        format="%d/%m/%Y %H.%M.%S"
    )

    dfudara = dfudara.drop(columns=["Date", "Time"])

    dfudara = dfudara.replace(-200, pd.NA)
    return dfudara


dfudara = load_data()

# Sidebar
with st.sidebar:
    st.title("Filter")

    polutan_options = ["CO(GT)", "NOx(GT)","NO2(GT)","C6H6(GT)"]
    polutan = st.selectbox("Pilih polutan:", polutan_options)

    # Slider bulan
    dfudara["Bulan"] = dfudara["Datetime"].dt.month
    bulan_min, bulan_max  = int(dfudara["Bulan"].min()), int(dfudara["Bulan"].max())
    rentang = st.slider(
        "Rentang bulan: ",
        min_value = bulan_min,
        max_value = bulan_max,
        value=(bulan_min, bulan_max)
    )

# Filter based input
mask = dfudara["Bulan"].between(rentang[0], rentang[1])
dfudara_filtered = dfudara[mask].dropna(subset=[polutan])

# Header
st.title("Dashboard Kualitas udara Italia 2004-2005")
st.caption("Menampilkan: **{polutan}** | Bulan {rentang[0]}-{rentang[1]}")

# Metrics cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Rata-rata", f"{dfudara_filtered[polutan].mean():.2f}")
col2.metric("Maksimum",  f"{dfudara_filtered[polutan].max():.2f}")
col3.metric("Minimum",   f"{dfudara_filtered[polutan].min():.2f}")
col4.metric("Jumlah data", f"{len(dfudara_filtered):,}")

st.divider()

# Tabs
tab1, tab2, tab3 = st.tabs(["Tren Waktu", "Distribusi", "Data Mentah"])

with tab1:
    fig = px.line(
        dfudara_filtered.sort_values("Datetime"),
        x="Datetime", y=polutan,
        title=f"Tren {polutan} dari waktu ke waktu",
        labels={"Datetime": "Waktu", polutan: polutan}
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig2 = px.histogram(
        dfudara_filtered, x=polutan,
        nbins=50,
        title=f"Distribusi nilai {polutan}",
        color_discrete_sequence=["#378ADD"]
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.dataframe(
        dfudara_filtered[["Datetime", polutan]].sort_values("Datetime"),
        use_container_width=True,
        height=400
    )
    # Tombol download CSV
    csv = dfudara_filtered.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download CSV", csv, "data_filtered.csv", "text/csv")
