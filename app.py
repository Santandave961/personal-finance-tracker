
# Nigeria Economic Trends Dashboard
# Author: Wisdom Okparaji

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np

# Streamlit Page Config
st.set_page_config(page_title="Nigeria Economic Dashboard", layout="wide")

# Title
st.title(" Nigeria Economic Trends Dashboard")
st.markdown("""An interactive dashboard analyzing 
**Nigeria's key development indicators***
- GDP, Population, CO Emissions, and more
- using **World Bank data**.
""")

# Upload section
st.sidebar.header(r"C:\Users\USER\Documents\API_NGA_DS2_clean.xlsx")
uploaded_file = st.file_uploader(r"C:\Users\USER\Documents\API_NGA_DS2_clean.xlsx", type=["xlsx"])


# Check if file is uploaded
if uploaded_file is not None:
    try:
        # Read the Excel file
        data = pd.read_excel(
            uploaded_file,
            sheet_name="Data",
            skiprows=3,
            engine='openpyxl'
        )
        st.sidebar.success("File uploaded successfully!")
    
    except Exception as e:
        st.sidebar.error(f" Error reading file: {str(e)}")
        st.info(" Try converting your .xls file to .xlsx format in Excel")
        st.stop()

else:
    st.info(" Please upload an Excel file to .xlsx format in Excel")
    st.stop()

if uploaded_file:
    # Load dataset
    data = pd.read_excel(uploaded_file, sheet_name="Data", skiprows=3)

    # Sidebar filters
    st.sidebar.header(" Filter Options")
    all_indicators =  sorted(data["Indicator Name"].unique())
    selected_indicators = st.sidebar.multiselect(
        "Select Indicators to Analyze",
        options=all_indicators,
        default=["GDP (current US$)","Population, total"]
    )
     
    # Filter data
    filtered_data = data[data["Indicator Name"].isin(selected_indicators)]

    # Reshape for visualization
    melted = filtered_data.melt(id_vars=["Indicator Name"],var_name="Year",value_name="Value").dropna(subset=["Value"])
    melted["Year"] = pd.to_numeric(melted["Year"], errors="coerce")
    melted = melted.dropna(subset=["Year"])
    melted["Year"] = melted["Year"].astype(int)


    # --- Sidebar Insights ---
    st.sidebar.header("Key Insights")
 
    # GDP trend insight
    if "GDP (current US$)" in melted["Indicator Name"].values:
        gdp_data = melted[melted["Indicator Name"] == "GDP (current US$)"]
        gdp_latest = gdp_data.sort_values("Year").iloc[-1]["Value"]
        gdp_prev = gdp_data.sort_values("Year").iloc[-2]["Value"]
        gdp_growth = ((gdp_latest - gdp_prev) / gdp_prev * 100)
        st.sidebar.metric("GDP growth(last year)", f"{gdp_growth:.2f}%")
    else:
         st.sidebar.info("GDP not selected")

   # CO2 emissions
 #  if "CO2 emissions (metrics ton per capita)" in melted["Indicator Name"].values:
  #    co2_data = melted[melted["Indicator Name"] == "CO2 emissions (metric tons per capita)"]
   #   co2_latest = co2_data.sort_values("Year").iloc[-1]["Value"]
   #   st.sidebar_metric("CO2 Emissions(latest)", f"{co2_latest:.2F} tons per capita")

   #   st.sidebar.markdown("----")

    # --- Visualization: Line chart ----
    st.subheader(" Indicator Trends Over Time")
    fig1, ax1 = plt.subplots(figsize=(10,5))
    sns.lineplot(data=melted, x="Year", y="Value", hue="Indicator Name", markers="o", ax=ax1)
    ax1.set_title("Nigeria Economic Indicators Over Time")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Value")
    ax1.grid(True)
    st.pyplot(fig1)

    # -- Correlation Heatmap--
    st.subheader("Correlation Between Indicators")
    
    pivot_df = melted.pivot(index="Year",columns="Indicator Name", values="Value")
    corr = pivot_df.corr()

    fig2, ax2 = plt.subplots(figsize=(6,4))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax2)
    ax2.set_title("Correlation Heatmap of Selected Indicators")
    st.pyplot(fig2)

    # --GDP Forecast ---
    st.subheader("GDP Forecast (2025-2034)")

    if "GDP (current US$)"in melted["Indicator Name"].values:
     gdp_data = melted[melted["Indicator Name"] == "GDP (current US$)"]
     X = gdp_data[["Year"]]
     y = gdp_data[["Value"]]

     model = LinearRegression()
     model.fit(X,y)

     future_years = pd.DataFrame({"Year": range(2025, 2035)})
     predictions = model.predict(future_years)

     fig3, ax3 = plt.subplots(figsize=(8, 4))
     ax3.plot(gdp_data["Year"],gdp_data["Value"], label="Actual GDP",linewidth=2)
     ax3.plot(future_years["Year"],predictions, "--", color="red", label="Predicted GDP")
     ax3.set_title("GDP Forecast (2025-2034)")
     ax3.set_xlabel("Year")
     ax3.set_ylabel("GDP (US$)")
     ax3.legend()
     st.pyplot(fig3)

     st.success(" Forecast indicates continued GDP growth through 2034.")
else:
     st.warning("GDP data not found among selected indicators")

     # -- Data Table and Download
     st.subheader("Cleaned Data Preview")
     st.dataframe(melted.head(20))

     csv= melted.to_csv(index=False).encode("utf-8")
     st.download_button(
         label = "Download Cleaned Data (CSV)",
         data=csv,
         file_name="nigerian_cleaned_data.csv",
         mime="text/csv"           
     )




      
    
    