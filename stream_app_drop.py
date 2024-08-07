import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import os

@st.cache_data(ttl=10)  # Cache the data with a time-to-live (TTL) of 10 seconds
def load_data(file_name):
    data_file = pd.read_csv(file_name)
    return data_file

# Function to save uploaded file
def save_uploaded_file(uploaded_file):
    with open(os.path.join("uploads", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    return os.path.join("uploads", uploaded_file.name)

# Create uploads directory if it doesn't exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Title
st.title('Auto-updating DataFrame Plotting in Streamlit with Matplotlib')

uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
if uploaded_file is not None:
    file_path = save_uploaded_file(uploaded_file)
    st.session_state['file_path'] = file_path
    st.session_state['file_name'] = uploaded_file.name

if 'file_path' in st.session_state:
    file_path = st.session_state['file_path']
    file_name = st.session_state['file_name']

    st.write(f"### Plotting data from: {file_name}")

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
    st.write("Please upload a CSV file to start plotting.")
