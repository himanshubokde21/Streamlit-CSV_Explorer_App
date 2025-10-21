import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Smart CSV Explorer", page_icon="📊", layout="wide")
st.title("📂 Smart CSV Explorer")
st.caption("Upload your CSV file and explore your data effortlessly!")

file = st.file_uploader("📁 Upload CSV File", type=["csv"])

if file:
    df = pd.read_csv(file)
    st.success(f"✅ File uploaded successfully! Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    
    with st.expander("👀 Preview Data"):
        st.dataframe(df.head(20), use_container_width=True)

    st.sidebar.header("🔍 Filters & Options")
    show_summary = st.sidebar.checkbox("Show Summary Statistics", True)
    show_chart = st.sidebar.checkbox("Show Charts", True)

    col = st.selectbox("📊 Select column to analyze", df.columns)

    if col:
        st.subheader(f"📈 Analysis for `{col}`")
        col_data = df[col]
        
        if pd.api.types.is_numeric_dtype(col_data):
            mean = col_data.mean()
            median = col_data.median()
            st.write(f"**Mean:** {mean:.3f}")
            st.write(f"**Median:** {median:.3f}")
            st.write(f"**Min:** {col_data.min():.3f}")
            st.write(f"**Max:** {col_data.max():.3f}")
            
            if show_chart:
                fig = px.histogram(df, x=col, nbins=30, title=f"Distribution of {col}", color_discrete_sequence=["#636EFA"])
                st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.write(f"🧾 Unique Values: {df[col].nunique()}")
            if show_chart:
                freq = df[col].value_counts().reset_index()
                freq.columns = [col, "Count"]
                fig = px.bar(freq, x=col, y="Count", title=f"Category Frequency for {col}", color_discrete_sequence=["#EF553B"])
                st.plotly_chart(fig, use_container_width=True)
        
        if show_summary:
            st.subheader("📊 Summary Statistics")
            st.write(df.describe(include="all").T)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Current Dataset as CSV",
            data=csv,
            file_name="processed_data.csv",
            mime="text/csv",
        )
else:
    st.info("👆 Upload a CSV file to start exploring your data.")
