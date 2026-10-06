"""
SWYNEX Internship - Task 3: Interactive Dashboard
Titanic Survival Analysis Dashboard
Built with Streamlit + Plotly
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page config
st.set_page_config(
    page_title="SWYNEX | Titanic Survival Dashboard",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a365d;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4a5568;
        text-align: center;
        margin-bottom: 2rem;
    }
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .kpi-value {
        font-size: 2.2rem;
        font-weight: 700;
    }
    .kpi-label {
        font-size: 0.95rem;
        opacity: 0.9;
    }
    .stSelectbox label, .stMultiSelect label {
        font-weight: 600;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load and clean the Titanic dataset"""
    df = pd.read_csv("../data/cleaned/cleaned_titanic.csv")
    
    # Basic cleaning
    df["Age"] = df["Age"].fillna(df["Age"].median())
    df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])
    df["Fare"] = df["Fare"].fillna(df["Fare"].median())
    
    # Feature engineering for dashboard
    df["Survived_Label"] = df["Survived"].map({0: "Did Not Survive", 1: "Survived"})
    df["Pclass_Label"] = df["Pclass"].map({1: "1st Class", 2: "2nd Class", 3: "3rd Class"})
    df["Sex_Label"] = df["Sex"].str.title()
    df["Embarked_Label"] = df["Embarked"].map({
        "C": "Cherbourg",
        "Q": "Queenstown",
        "S": "Southampton"
    })
    
    # Age groups
    df["Age_Group"] = pd.cut(
        df["Age"],
        bins=[0, 12, 18, 35, 50, 80],
        labels=["Child (0-12)", "Teen (13-18)", "Young Adult (19-35)", "Adult (36-50)", "Senior (51+)"]
    )
    
    return df


def main():
    # Header
    st.markdown('<p class="main-header">🚢 Titanic Survival Interactive Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">SWYNEX Internship – Task 3 | Built with Streamlit & Plotly</p>', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    # ==================== SIDEBAR FILTERS ====================
    st.sidebar.header("🔍 Filters")
    st.sidebar.markdown("Use the filters below to explore the data interactively.")
    
    # Gender filter
    gender_options = ["All"] + sorted(df["Sex_Label"].unique().tolist())
    selected_gender = st.sidebar.selectbox("Gender", gender_options)
    
    # Passenger Class filter
    class_options = ["All"] + sorted(df["Pclass_Label"].unique().tolist())
    selected_class = st.sidebar.selectbox("Passenger Class", class_options)
    
    # Embarked Port filter
    port_options = ["All"] + sorted(df["Embarked_Label"].unique().tolist())
    selected_port = st.sidebar.selectbox("Embarked Port", port_options)
    
    # Age range filter
    min_age, max_age = int(df["Age"].min()), int(df["Age"].max())
    age_range = st.sidebar.slider("Age Range", min_age, max_age, (min_age, max_age))
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_gender != "All":
        filtered_df = filtered_df[filtered_df["Sex_Label"] == selected_gender]
    if selected_class != "All":
        filtered_df = filtered_df[filtered_df["Pclass_Label"] == selected_class]
    if selected_port != "All":
        filtered_df = filtered_df[filtered_df["Embarked_Label"] == selected_port]
    
    filtered_df = filtered_df[
        (filtered_df["Age"] >= age_range[0]) & (filtered_df["Age"] <= age_range[1])
    ]
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Showing {len(filtered_df)} of {len(df)} passengers**")
    
    # ==================== KPI CARDS ====================
    st.markdown("### 📊 Key Performance Indicators")
    
    total_passengers = len(filtered_df)
    total_survivors = filtered_df["Survived"].sum()
    survival_rate = (total_survivors / total_passengers * 100) if total_passengers > 0 else 0
    avg_age = filtered_df["Age"].mean() if total_passengers > 0 else 0
    avg_fare = filtered_df["Fare"].mean() if total_passengers > 0 else 0
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Passengers", f"{total_passengers:,}")
    with col2:
        st.metric("Total Survivors", f"{total_survivors:,}")
    with col3:
        st.metric("Survival Rate", f"{survival_rate:.1f}%")
    with col4:
        st.metric("Average Age", f"{avg_age:.1f} yrs")
    with col5:
        st.metric("Average Fare", f"${avg_fare:.1f}")
    
    st.markdown("---")
    
    # ==================== CHARTS ROW 1 ====================
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("#### Survival by Gender")
        if len(filtered_df) > 0:
            gender_surv = filtered_df.groupby(["Sex_Label", "Survived_Label"]).size().reset_index(name="Count")
            fig_gender = px.bar(
                gender_surv,
                x="Sex_Label",
                y="Count",
                color="Survived_Label",
                barmode="group",
                color_discrete_map={"Survived": "#48bb78", "Did Not Survive": "#e53e3e"},
                labels={"Sex_Label": "Gender", "Count": "Number of Passengers"},
                text_auto=True
            )
            fig_gender.update_layout(
                legend_title_text="",
                height=400,
                margin=dict(t=30, b=30),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_gender, use_container_width=True)
        else:
            st.info("No data for selected filters.")
    
    with col_right:
        st.markdown("#### Survival by Passenger Class")
        if len(filtered_df) > 0:
            class_surv = filtered_df.groupby(["Pclass_Label", "Survived_Label"]).size().reset_index(name="Count")
            fig_class = px.bar(
                class_surv,
                x="Pclass_Label",
                y="Count",
                color="Survived_Label",
                barmode="group",
                color_discrete_map={"Survived": "#48bb78", "Did Not Survive": "#e53e3e"},
                labels={"Pclass_Label": "Passenger Class", "Count": "Number of Passengers"},
                category_orders={"Pclass_Label": ["1st Class", "2nd Class", "3rd Class"]},
                text_auto=True
            )
            fig_class.update_layout(
                legend_title_text="",
                height=400,
                margin=dict(t=30, b=30),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_class, use_container_width=True)
        else:
            st.info("No data for selected filters.")
    
    # ==================== CHARTS ROW 2 ====================
    col_left2, col_right2 = st.columns(2)
    
    with col_left2:
        st.markdown("#### Survival by Embarked Port")
        if len(filtered_df) > 0:
            port_surv = filtered_df.groupby(["Embarked_Label", "Survived_Label"]).size().reset_index(name="Count")
            fig_port = px.bar(
                port_surv,
                x="Embarked_Label",
                y="Count",
                color="Survived_Label",
                barmode="group",
                color_discrete_map={"Survived": "#48bb78", "Did Not Survive": "#e53e3e"},
                labels={"Embarked_Label": "Embarked Port", "Count": "Number of Passengers"},
                text_auto=True
            )
            fig_port.update_layout(
                legend_title_text="",
                height=400,
                margin=dict(t=30, b=30),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_port, use_container_width=True)
        else:
            st.info("No data for selected filters.")
    
    with col_right2:
        st.markdown("#### Age Distribution by Survival")
        if len(filtered_df) > 0:
            fig_age = px.histogram(
                filtered_df,
                x="Age",
                color="Survived_Label",
                nbins=30,
                barmode="overlay",
                opacity=0.7,
                color_discrete_map={"Survived": "#48bb78", "Did Not Survive": "#e53e3e"},
                labels={"Age": "Age (years)", "count": "Number of Passengers"}
            )
            fig_age.update_layout(
                legend_title_text="",
                height=400,
                margin=dict(t=30, b=30),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_age, use_container_width=True)
        else:
            st.info("No data for selected filters.")
    
    # ==================== CHARTS ROW 3 ====================
    st.markdown("#### Survival Rate by Age Group & Class")
    if len(filtered_df) > 0:
        age_class = filtered_df.groupby(["Age_Group", "Pclass_Label"])["Survived"].mean().reset_index()
        age_class["Survival_Rate"] = (age_class["Survived"] * 100).round(1)
        
        fig_heatmap = px.density_heatmap(
            filtered_df,
            x="Pclass_Label",
            y="Age_Group",
            z="Survived",
            histfunc="avg",
            color_continuous_scale="RdYlGn",
            labels={"Pclass_Label": "Passenger Class", "Age_Group": "Age Group", "Survived": "Avg Survival"},
            category_orders={
                "Pclass_Label": ["1st Class", "2nd Class", "3rd Class"],
                "Age_Group": ["Child (0-12)", "Teen (13-18)", "Young Adult (19-35)", "Adult (36-50)", "Senior (51+)"]
            }
        )
        fig_heatmap.update_layout(
            height=400,
            margin=dict(t=30, b=30),
            coloraxis_colorbar=dict(title="Survival Rate")
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # ==================== ADDITIONAL INSIGHTS ====================
    st.markdown("---")
    st.markdown("### 📈 Additional Insights")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("#### Fare Distribution by Class & Survival")
        if len(filtered_df) > 0:
            fig_fare = px.box(
                filtered_df,
                x="Pclass_Label",
                y="Fare",
                color="Survived_Label",
                color_discrete_map={"Survived": "#48bb78", "Did Not Survive": "#e53e3e"},
                labels={"Pclass_Label": "Passenger Class", "Fare": "Ticket Fare ($)"},
                category_orders={"Pclass_Label": ["1st Class", "2nd Class", "3rd Class"]}
            )
            fig_fare.update_layout(
                legend_title_text="",
                height=400,
                margin=dict(t=30, b=30),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_fare, use_container_width=True)
    
    with col_b:
        st.markdown("#### Survival Rate Overview (Pie)")
        if len(filtered_df) > 0:
            pie_data = filtered_df["Survived_Label"].value_counts().reset_index()
            pie_data.columns = ["Status", "Count"]
            fig_pie = px.pie(
                pie_data,
                values="Count",
                names="Status",
                color="Status",
                color_discrete_map={"Survived": "#48bb78", "Did Not Survive": "#e53e3e"},
                hole=0.4
            )
            fig_pie.update_traces(textposition="inside", textinfo="percent+label")
            fig_pie.update_layout(
                height=400,
                margin=dict(t=30, b=30),
                showlegend=False
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    
    # ==================== DATA TABLE ====================
    st.markdown("---")
    with st.expander("📋 View Filtered Data Table", expanded=False):
        display_cols = ["PassengerId", "Name", "Sex_Label", "Age", "Pclass_Label", 
                        "Embarked_Label", "Fare", "Survived_Label"]
        st.dataframe(
            filtered_df[display_cols].rename(columns={
                "Sex_Label": "Gender",
                "Pclass_Label": "Class",
                "Embarked_Label": "Embarked",
                "Survived_Label": "Status"
            }),
            use_container_width=True,
            height=300
        )
        st.download_button(
            label="⬇️ Download Filtered Data (CSV)",
            data=filtered_df.to_csv(index=False).encode("utf-8"),
            file_name="titanic_filtered.csv",
            mime="text/csv"
        )
    
    # ==================== KEY INSIGHTS ====================
    st.markdown("---")
    st.markdown("### 💡 Key Insights from Analysis")
    
    insights_col1, insights_col2 = st.columns(2)
    
    with insights_col1:
        st.success("""
        **Gender Impact**  
        Women had a significantly higher survival rate (~74%) compared to men (~19%).  
        This reflects the "Women and children first" policy during the disaster.
        """)
        st.info("""
        **Class Matters**  
        1st Class passengers had ~63% survival rate,  
        2nd Class ~47%, and 3rd Class only ~24%.  
        Socio-economic status strongly influenced survival chances.
        """)
    
    with insights_col2:
        st.warning("""
        **Age & Survival**  
        Children (especially in higher classes) had better survival odds.  
        Most passengers were young adults (19–35 years).
        """)
        st.error("""
        **Fare Correlation**  
        Higher ticket fares were associated with better survival rates,  
        as wealthier passengers had better access to lifeboats and cabins closer to the deck.
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #718096; font-size: 0.9rem;">
            <p>SWYNEX Technologies Internship – Task 3: Interactive Dashboard</p>
            <p>Dataset: Titanic Passenger Data | Tools: Python, Streamlit, Plotly, Pandas</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
