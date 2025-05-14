import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
import io

# Load the data
def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            return pd.read_csv(uploaded_file)
        except:
            uploaded_file.seek(0)
            return pd.read_excel(uploaded_file)

# Analyze the data
def analyze_data(data):
    numeric_data = data.select_dtypes(include=['int64', 'float64'])
    summary = numeric_data.describe()
    correlation = numeric_data.corr()
    return summary, correlation

# Visualizations
def plot_bar_chart(data, column_name):
    plt.figure(figsize=(10, 6))
    sns.countplot(y=data[column_name], order=data[column_name].value_counts().index)
    plt.title(f"Bar Chart for {column_name}")
    st.pyplot(plt.gcf())
    plt.clf()

def plot_line_chart(data, column_name):
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=data.index, y=data[column_name])
    plt.title(f"Line Chart for {column_name}")
    st.pyplot(plt.gcf())
    plt.clf()

def plot_pie_chart(data, column_name):
    fig = px.pie(data, names=column_name, title=f"Pie Chart for {column_name}")
    st.plotly_chart(fig)

def plot_scatter_chart(data, x_column, y_column):
    fig = px.scatter(data, x=x_column, y=y_column, title=f"Scatter Plot: {x_column} vs {y_column}")
    st.plotly_chart(fig)

# Main Streamlit Dashboard
def create_dashboard():
    st.title("📊 Data Visualization Dashboard")

    uploaded_file = st.file_uploader("Upload your data (CSV or Excel)", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        data = load_data(uploaded_file)
        st.subheader("🔍 Raw Data")
        st.dataframe(data)

        summary, correlation = analyze_data(data)
        st.subheader("📈 Summary Statistics")
        st.write(summary)
        st.subheader("🔗 Correlation Matrix")
        st.write(correlation)

        st.subheader("📊 Chart Options")
        chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Line Chart", "Pie Chart", "Scatter Plot"])

        if chart_type == "Bar Chart":
            cat_columns = data.select_dtypes(include=['object']).columns
            if len(cat_columns) > 0:
                column_name = st.selectbox("Select Categorical Column", cat_columns)
                plot_bar_chart(data, column_name)
            else:
                st.warning("No categorical columns available for bar chart.")
        
        elif chart_type == "Line Chart":
            num_columns = data.select_dtypes(include=['int64', 'float64']).columns
            if len(num_columns) > 0:
                column_name = st.selectbox("Select Numeric Column", num_columns)
                plot_line_chart(data, column_name)
            else:
                st.warning("No numeric columns available for line chart.")

        elif chart_type == "Pie Chart":
            cat_columns = data.select_dtypes(include=['object']).columns
            if len(cat_columns) > 0:
                column_name = st.selectbox("Select Categorical Column", cat_columns)
                plot_pie_chart(data, column_name)
            else:
                st.warning("No categorical columns available for pie chart.")

        elif chart_type == "Scatter Plot":
            num_columns = data.select_dtypes(include=['int64', 'float64']).columns
            if len(num_columns) >= 2:
                x_column = st.selectbox("X Axis", num_columns)
                y_column = st.selectbox("Y Axis", num_columns, index=1 if len(num_columns) > 1 else 0)
                plot_scatter_chart(data, x_column, y_column)
            else:
                st.warning("Need at least two numeric columns for scatter plot.")

if __name__ == "__main__":
    create_dashboard()
