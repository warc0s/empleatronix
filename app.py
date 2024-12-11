import streamlit as st
import pandas as pd
import plotly.express as px
from typing import Tuple

# Primer comando de Streamlit, si no, da errores.
st.set_page_config(
    page_title="Empleatronix",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS para darle estilo a la app
st.markdown("""
<style>
    .stApp {
        max-width: 100%;
        padding: 1rem;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        color: #1E88E5;
        font-size: calc(1.5rem + 1.5vw) !important;
    }
    .stDataFrame {
        width: 100%;
    }
    .plot-container {
        width: 100%;
        min-height: 200px;
    }
    @media (max-width: 768px) {
        .stDataFrame {
            font-size: 0.8rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# cargar los datos con cache y manejar posibles errores
@st.cache_data
def load_data() -> pd.DataFrame:
    try:
        df = pd.read_csv('employees.csv')
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos: {str(e)}")
        return pd.DataFrame()

# mostramos la tabla de los empleados
def show_employee_table(df: pd.DataFrame):
    st.dataframe(
        df,
        column_config={
            "full name": st.column_config.TextColumn("Full Name", width="medium"),
            "salary": st.column_config.NumberColumn("Salary", format="$%d"),
            "gender": st.column_config.TextColumn("Gender", width="small"),
            "email": st.column_config.TextColumn("Email", width="medium")
        },
        hide_index=True,
        use_container_width=True
    )

# Creamos los controles de la gráfica
def create_chart_controls() -> Tuple[str, bool, bool]:
    chart_color = st.color_picker(
        "Elige un color para las barras",
        "#00BCD4"
    )
    
    col_controls1, col_controls2 = st.columns(2)
    with col_controls1:
        show_names = st.toggle("Mostrar el nombre", True)
    with col_controls2:
        show_values = st.toggle("Mostrar sueldo en la barra", True)
    
    return chart_color, show_names, show_values

# Creamos y customizamos la gráfica de salarios
def create_salary_chart(df: pd.DataFrame, chart_color: str, show_names: bool, show_values: bool):
    fig = px.bar(
        df,
        x='salary',
        y='full name',
        orientation='h',
        color_discrete_sequence=[chart_color]
    )
    
    fig.update_layout(
        showlegend=False,
        xaxis_title="Salary ($)",
        yaxis_title="",
        plot_bgcolor="white",
        height=max(400, len(df) * 25),  # Dynamic height based on data
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
        yaxis=dict(showgrid=False)
    )
    
    if not show_names:
        fig.update_yaxes(showticklabels=False)
    if show_values:
        chart_color = chart_color  # Asegurando que el color esté disponible
        fig.update_traces(texttemplate='$%{x:,.0f}', textposition='outside', textfont=dict(color=chart_color))
    
    st.plotly_chart(fig, use_container_width=True, config={'responsive': True})

def main():
    # Header
    st.title("EMPLEATRONIX")
    st.markdown("Todos los datos sobre los empleados en una aplicación.")
    st.markdown("Datos ficticios, claro.")

    # Cargar los datos
    df = load_data()
    if df.empty:
        st.stop()
    
    # Crear dos columnas
    col1, col2 = st.columns([2, 3])
    
    # Mostrar los datos y la gráfica
    with col1:
        st.subheader("Datos de Empleados")
        show_employee_table(df)
    
    with col2:
        st.subheader("Visualización de Salarios")
        chart_color, show_names, show_values = create_chart_controls()
        create_salary_chart(df, chart_color, show_names, show_values)

    # Footer para autoría
    footer = '<footer>Realizado por <a href="https://warcos.dev">Marcos García Estevez</a></footer>'
    st.markdown(footer, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
