# Weather Data Visualization

This project processes weather data and visualizes it using a web application.

## Features

- Extracts temperature data from a text file and stores it in a database.
- Displays the temperature trend as a line chart using Streamlit.
- Shows statistics for maximum, minimum, and average temperatures.

## Requirements

- pandas
- streamlit

## How to Run

1.  **Process Data**

    Run `main.py` to read data from `data.txt` and save the processed results to `data.db`.

    ```bash
    python main.py
    ```

2.  **Launch the Web Application**

    Launch the web application using `streamlit`.

    ```bash
    streamlit run webapp.py
    ```

    Access the URL specified in your browser (usually http://localhost:8501) to see the weather data graph.

## File Structure

- `main.py`: Script for data processing.
- `webapp.py`: Web application for data visualization.
- `data.txt`: Contains the original weather data.
- `data.db`: Database file where the processed data is stored.
- `extract.yaml`: Configuration file for data extraction.
