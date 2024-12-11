import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Empleatronix",
    page_icon="👥",
    layout="wide"
)

# Title
st.title("EMPLEATRONIX")
st.markdown("Todos los datos sobre los empleados en una aplicación.")

# Read data
@st.cache_data
def load_data():
    return pd.read_csv('employees.csv')

df = load_data()

# Create two columns
col1, col2 = st.columns([2, 3])

# Table in first column
with col1:
    st.dataframe(
        df,
        column_config={
            "full name": "Full Name",
            "salary": st.column_config.NumberColumn(
                "Salary",
                format="$%d"
            ),
            "gender": "Gender",
            "email": "Email"
        },
        hide_index=True
    )

# Chart controls and visualization in second column
with col2:
    # Color picker
    chart_color = st.color_picker(
        "Elige un color para las barras",
        "#00BCD4"
    )
    
    # Toggle controls
    col_controls1, col_controls2 = st.columns(2)
    with col_controls1:
        show_names = st.toggle("Mostrar el nombre", True)
    with col_controls2:
        show_values = st.toggle("Mostrar sueldo en la barra", True)
    
    # Create bar chart with Plotly
    fig = px.bar(
        df,
        x='salary',
        y='full name',
        orientation='h',
        color_discrete_sequence=[chart_color]
    )
    
    # Customize the chart
    fig.update_layout(
        showlegend=False,
        xaxis_title="Salary ($)",
        yaxis_title="",
        plot_bgcolor="white",
        height=600
    )
    
    # Show/hide labels based on toggles
    if not show_names:
        fig.update_yaxes(showticklabels=False)
    if show_values:
        fig.update_traces(texttemplate='$%{x:,.0f}', textposition='outside')
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
