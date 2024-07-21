import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.write("""
## My first app
Hello *world!!!!*
""")

data = pd.read_csv('Test.csv')
st.line_chart(data)

st.write('## DataFrame')
st.dataframe(data)

st.write('## Matplotlib Plot')
fig, ax = plt.subplots()
ax.plot(data['Data1'],data['Data3'], label = 'Data3')
ax.set_title('Line Plot of DataFrame Columns')
ax.set_xlabel('Index')
ax.set_ylabel('Values')
ax.legend()

# Display the plot in Streamlit
st.pyplot(fig)