"""
Streamlit Application for Auto-updating DataFrame Plotting with Matplotlib

This application allows users to input the path to a CSV file, and it will automatically
read and plot the data from the specified file. The application periodically refreshes
the data and plot every 10 seconds to reflect any updates made to the CSV file.

Features:
- User inputs the full path to the CSV file.
- Data is loaded and cached for 10 seconds to reduce unnecessary reloads.
- The DataFrame is displayed in the Streamlit app.
- The data is plotted using Matplotlib and displayed in the Streamlit app.
- The plot title is dynamically set based on the file name.
- A manual refresh button allows users to refresh the data on demand.
- The app automatically refreshes every 10 seconds to update the plot with the latest data.

Usage:
1. Enter the full path to your CSV file in the text input field.
2. The application will display the DataFrame and plot the data.
3. Any updates to the CSV file at the specified path will be reflected in the app every 10 seconds.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import os

@st.cache_data(ttl=10)  # Cache the data with a time-to-live (TTL) of 10 seconds
def load_data(file_path):
    """Load data from a CSV file at the specified file path."""
    data_file = pd.read_csv(file_path)
    return data_file

# Title
st.title('Auto-updating DataFrame Plotting in Streamlit with Matplotlib')

# User inputs the file path directly
file_path = st.text_input("Enter the full path to your CSV file:")

if file_path:
    st.session_state['file_path'] = file_path
    file_name = os.path.basename(file_path)
    st.session_state['file_name'] = file_name

if 'file_path' in st.session_state:
    file_path = st.session_state['file_path']
    file_name = st.session_state['file_name']

    st.write(f"### Plotting data from: {file_name}")

    # Check if the file exists
    if os.path.exists(file_path):
        # Load data
        df = load_data(file_path)

        if not df.empty:
            # Display the DataFrame
            st.write('## DataFrame')
            st.dataframe(df)

            # Plotting with Matplotlib
            st.write('## Matplotlib Plot')
            fig, ax = plt.subplots()
            ax.plot(df['Data1'], df['Data3'], label='Data3')
            ax.set_title(f'Line Plot of DataFrame Columns from {file_name}')
            ax.set_xlabel('Index')
            ax.set_ylabel('Values')
            ax.legend()

            # Display the plot in Streamlit
            st.pyplot(fig)

            # Add a button to manually refresh data
            if st.button('Refresh Data'):
                st.cache_data.clear()  # Clear cache to force reload data
                st.experimental_rerun()  # Re-run the app to update data

            # Auto-refresh every 10 seconds
            st.write('Updating in 10 seconds...')
            time.sleep(10)
            st.experimental_rerun()
        else:
            st.write("The uploaded file is empty or could not be read. Please upload a valid CSV file.")
    else:
        st.write(f"The file at path {file_path} does not exist. Please provide a valid path.")
else:
    st.write("Please enter the path to a CSV file to start plotting.")
