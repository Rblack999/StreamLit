"""
Streamlit Application for Auto-updating DataFrame Plotting with Matplotlib

This application allows users to upload a CSV file, and it will automatically
read and plot the data from the uploaded file. The application periodically refreshes
the data and plot every 10 seconds to reflect any updates made to the CSV file.

Features:
- User uploads a CSV file using the Streamlit file uploader.
- Data is loaded and cached for 10 seconds to reduce unnecessary reloads.
- The DataFrame is displayed in the Streamlit app.
- The data is plotted using Matplotlib and displayed in the Streamlit app.
- The plot title is dynamically set based on the file name.
- A manual refresh button allows users to refresh the data on demand.
- The app automatically refreshes every 10 seconds to update the plot with the latest data.

Usage:
1. Upload a CSV file using the file uploader.
2. The application will display the DataFrame and plot the data.
3. Any updates to the uploaded CSV file will be reflected in the app every 10 seconds.
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

def save_uploaded_file(uploaded_file):
    """Save the uploaded file and return the file path."""
    with open(os.path.join("uploads", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    return os.path.join("uploads", uploaded_file.name)

# Create uploads directory if it doesn't exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Title
st.title('Auto-updating DataFrame Plotting in Streamlit with Matplotlib')

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
if uploaded_file is not None:
    file_path = save_uploaded_file(uploaded_file)
    st.session_state['file_path'] = file_path
    st.session_state['file_name'] = uploaded_file.name

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
    st.write("Please upload a CSV file to start plotting.")
