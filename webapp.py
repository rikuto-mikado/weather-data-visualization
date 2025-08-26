import streamlit as st
import plotly.express as px
import psycopg2
import pandas as pd
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://admin:password@localhost:5432/weather_db"
)


def get_db_connection():
    # Get connection from PostgreSQL
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None


def load_data():
    # Get connection from Database
    conn = get_db_connection()
    if conn is None:
        return None, None

    try:
        # Get the data
        query = "SELECT date, temperature FROM temperatures ORDER BY created_at"
        df = pd.read_sql(query, conn)

        dates = df["date"].tolist()
        temperatures = df["temperature"].tolist()

        conn.close()
        return dates, temperatures

    except Exception as e:
        st.error(f"Data connection error: {e}")
        conn.close()
        return None, None


# Streamlit app
st.title("Weather Data Visualization")
st.write("Visualisation of temperature data in a PostgreSQL + Docker environment")

dates, temperatures = load_data()


if dates and temperatures:
    # Making graphs
    fig = px.line(
        x=dates,
        y=temperatures,
        labels={"x": "Date", "y": "Temperature (°C)"},
        title="Temperature Trend Over Time",
    )

    fig.update_traces(line_color="#FF6B6B", line_width=3)
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(size=14)
    )

    st.plotly_chart(fig, use_container_width=True)

    # Statistics infomation
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Highest temperature", f"{max(temperatures)}°C")

    with col2:
        st.metric("Lowest temperature", f"{min(temperatures)}°C")

    with col3:
        st.metric("Average temperature", f"{sum(temperatures)/len(temperatures):.1f}°C")

    # Data table
    if st.checkbox("Display data table"):
        df = pd.DataFrame({"Date": dates, "Temperature (°C)": temperatures})
        st.dataframe(df, use_container_width=True)

else:
    st.error("Data could not be read. Please check the database connection")

# Displaying database connection status
st.sidebar.write("### System Information")
conn = get_db_connection()
if conn:
    st.sidebar.success("✅ PostgreSQL Connected")
    conn.close()
else:
    st.sidebar.error("❌ PostgreSQL Connection Failed")
