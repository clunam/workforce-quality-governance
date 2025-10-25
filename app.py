import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(layout="wide", page_title="Workforce Governance Dashboard")
st.title("Workforce & Quality Governance Dashboard")
st.caption("Interactive analytics dashboard for identifying risk patterns, quality issues, and operational insights.")

def try_load(path):
    if os.path.exists(path):
        try:
            return pd.read_csv(path)
        except:
            return None
    return None

def color_risk(val):
    if isinstance(val, float):
        if val > 0.35:
            color = "red"
        elif val > 0.20:
            color = "orange"
        else:
            color = "green"
        return f"background-color: {color}; color: white"
    return ""

SRC = "output/recruitment_source_summary.csv"
MGR = "output/manager_summary.csv"
DEPT = "output/turnover_by_dept.csv"
SAL = "output/salary_grid.csv"

src_df = try_load(SRC)
mgr_df = try_load(MGR)
dept_df = try_load(DEPT)
sal_df = try_load(SAL)

st.sidebar.header("⚙️ Filters")

department_filter = None
if isinstance(dept_df, pd.DataFrame):
    department_filter = st.sidebar.multiselect(
        "Filter by Department",
        options=dept_df["department"].dropna().unique().tolist(),
        default=None
    )

manager_filter = None
if isinstance(mgr_df, pd.DataFrame):
    manager_filter = st.sidebar.multiselect(
        "Filter by Manager",
        options=mgr_df["manager_name"].dropna().unique().tolist(),
        default=None
    )

source_filter = None
if isinstance(src_df, pd.DataFrame):
    source_filter = st.sidebar.multiselect(
        "Filter by Source",
        options=src_df["employee_source"].dropna().unique().tolist(),
        default=None
    )

st.sidebar.markdown("---")
st.sidebar.caption("Filters apply to relevant charts & tables automatically.")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Recruitment Sources", src_df.shape[0] if isinstance(src_df, pd.DataFrame) else "N/A")
c2.metric("Managers Tracked", mgr_df.shape[0] if isinstance(mgr_df, pd.DataFrame) else "N/A")
c3.metric("Departments", dept_df['department'].nunique() if isinstance(dept_df, pd.DataFrame) else "N/A")
c4.metric("Salary Records", sal_df.shape[0] if isinstance(sal_df, pd.DataFrame) else "N/A")

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(
    ["📥 Recruitment Quality", "👤 Manager Effectiveness", "🏢 Department Turnover", "💰 Salary Structure"]
)

with tab1:
    st.subheader("Recruitment Source Quality & Stability")
    if isinstance(src_df, pd.DataFrame):
        df = src_df.copy()
        if source_filter:
            df = df[df["employee_source"].isin(source_filter)]
        sort_option = st.radio(
            "Sort by:",
            ["Retention-Weighted Index", "Median Tenure", "Avg Performance"],
            horizontal=True
        )
        sort_map = {
            "Retention-Weighted Index": "retention_weighted_index",
            "Median Tenure": "median_tenure_years",
            "Avg Performance": "avg_perf"
        }
        df = df.sort_values(sort_map[sort_option], ascending=False)
        fig = px.bar(
            df,
            x="employee_source",
            y=sort_map[sort_option],
            color=sort_map[sort_option],
            color_continuous_scale="Teal",
            hover_data=df.columns
        )
        st.plotly_chart(fig, use_container_width=True)
        if st.checkbox("Show full recruitment table"):
            st.dataframe(df.style.applymap(color_risk, subset=["retention_rate"]))
        st.download_button("Download Recruitment CSV", df.to_csv(index=False), "recruitment.csv")

with tab2:
    st.subheader("Manager Effectiveness Index (MEI)")
    if isinstance(mgr_df, pd.DataFrame):
        dfm = mgr_df.copy()
        if manager_filter:
            dfm = dfm[dfm["manager_name"].isin(manager_filter)]
        dfm = dfm.sort_values("mei", ascending=False)
        fig = px.bar(
            dfm,
            x="manager_name",
            y="mei",
            color="mei",
            color_continuous_scale="Blues",
            hover_data=dfm.columns
        )
        st.plotly_chart(fig, use_container_width=True)
        if st.checkbox("Show manager performance table"):
            st.dataframe(dfm.style.applymap(color_risk, subset=["retention_rate"]))
        st.download_button("Download Manager CSV", dfm.to_csv(index=False), "manager_summary.csv")

with tab3:
    st.subheader("Department Turnover & Workforce Risk")
    if isinstance(dept_df, pd.DataFrame):
        df = dept_df.copy()
        if department_filter:
            df = df[df["department"].isin(department_filter)]
        df = df.sort_values("turnover_rate", ascending=False)
        fig = px.bar(
            df,
            x="department",
            y="turnover_rate",
            color="turnover_rate",
            color_continuous_scale="Reds",
            hover_data=df.columns
        )
        st.plotly_chart(fig, use_container_width=True)
        if st.checkbox("Show turnover table"):
            st.dataframe(df.style.applymap(color_risk, subset=["turnover_rate"]))
        st.download_button("Download Turnover CSV", df.to_csv(index=False), "turnover.csv")

with tab4:
    st.subheader("Salary Grid — Top 5 Highest Bands")
    if isinstance(sal_df, pd.DataFrame):
        df_sal = sal_df.copy()
        salary_cols = [c for c in df_sal.columns if "salary" in c.lower() or "pay" in c.lower()]
        if salary_cols:
            sorted_col = salary_cols[0]
            # coerce to numeric for sorting if possible
            df_sal[sorted_col + "_num"] = pd.to_numeric(df_sal[sorted_col], errors="coerce")
            df_sal = df_sal.sort_values(sorted_col + "_num", ascending=False)
        st.dataframe(df_sal.head(5))
        if st.checkbox("Show full salary grid"):
            st.dataframe(df_sal)
        st.download_button("Download Salary CSV", df_sal.to_csv(index=False), "salary_grid.csv")

st.markdown("---")
st.caption("Clarissa Luna - Built with Streamlit · Plotly · pandas - interactive governance dashboard.")