import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

@st.cache_data(ttl=10)  # Cache the data with a time-to-live (TTL) of 60 seconds
def load_data(file_name):
    data_file = pd.read_csv(file_name)
    return data_file

# Title
st.title('Auto-updating DataFrame Plotting in Streamlit with Matplotlib')

# Load data
df = load_data('Test.csv')

# Display the DataFrame
st.write('## DataFrame')
st.dataframe(df)

# Plotting with Matplotlib
st.write('## Matplotlib Plot')
fig, ax = plt.subplots()
ax.plot(df['Data1'], df['Data3'], label='Data3')
ax.set_title('Line Plot of DataFrame Columns')
ax.set_xlabel('Index')
ax.set_ylabel('Values')
ax.legend()

# Display the plot in Streamlit
st.pyplot(fig)

# Add a button to manually refresh data
if st.button('Refresh Data'):
    st.cache_data.clear()  # Clear cache to force reload data
    st.rerun()  # Re-run the app to update data

# Auto-refresh every 60 seconds
st.write('Updating in 10 seconds...')
time.sleep(10)
st.rerun()
