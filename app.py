import streamlit as st
import pandas as pd
import os
from io import BytesIO
import base64

st.set_page_config(page_title="DataSweeper", layout="wide")
st.title("DataSweeper")
uploaded_file = st.file_uploader("Upload a file", type=["csv", "xlsx"])
if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file, engine="openpyxl")
        st.write(df)
    else:
        st.write("unsupported file format")

        
    st.write("File Name: ", uploaded_file.name)
    st.write("File Size: ", uploaded_file.size/1024)
    
    st.write("Preview of the data")
    st.write(df.head())
    st.write("Data Cleaning Options")
    if st.checkbox("Clean data for ",uploaded_file.name):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Remove Duplicates"):
                df = df.drop_duplicates(inplace=True)
                st.write("Duplicates Removed")
        with col2:
            if st.button("Remove Null Values"):
                df = df.dropna(inplace=True)
                st.write("Null Values Removed")

    st.subheader("Data Visualization")
    st.write("Select two columns to visualize from the following")
    columns = st.multiselect("Select Columns", df.columns,default=df.columns[0:2])
    if len(columns) == 2:
        st.write("Selected Columns: ", columns)
    if st.checkbox("Show Data Visualization"):
        st.bar_chart(df.select_dtypes(include='number').iloc[::2])


    st.subheader("Conversion options")
    st.write("Select the format to convert the data")
    format = st.radio("Select the format", ["csv", "xlsx"])
    if st.button("Convert"):
        if format == "csv":
            b64 = base64.b64encode(df.to_csv().encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download csv file</a>'
            st.markdown(href, unsafe_allow_html=True)
        elif format == "xlsx":
            b64 = base64.b64encode(df.to_excel().encode()).decode()
            href = f'<a href="data:file/xlsx;base64,{b64}" download="data.xlsx">Download xlsx file</a>'
            st.markdown(href, unsafe_allow_html=True)

    
       

