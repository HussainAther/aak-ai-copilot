import streamlit as st
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging

from frontend_dashboard.country_ui import countries_render_ui_ver3
from Countries.New_DataFiles.DataSelection_API import database_countries
from frontend_dashboard.employee_quadrangulation_ui import employee_quadrangulation_ui
from frontend_dashboard.employee_table_ui import employee_activity_ui

from frontend_dashboard.streamlit_dashboard import (
    investor_ui,
    session_ui,
    researcher_ui,
    team_activity_ui,
    market_alignment_ui,
    talent_finder_ui
)

# -------------------------------
# Streamlit Configuration
# -------------------------------
st.set_page_config(
    page_title="AAK + Alter Learning AI Platform",
    page_icon="\U0001F52C",
    layout="wide"
)

st.title("AAK Tele-Science Employee Monitoring and Recommendation System")

# -------------------------------
# Logging and Retry Setup
# -------------------------------
logging.basicConfig(level=logging.INFO)

session = requests.Session()
retries = Retry(total=5, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retries)
session.mount('http://', adapter)
session.mount('https://', adapter)

# -------------------------------
# Main Streamlit Navigation
# -------------------------------
db = database_countries()

tab = st.sidebar.radio("\U0001F4DA App Views", [
    "\U0001F4B8 Investor Matcher",
    "\U0001F9E0 Session Analyzer",
    "\U0001F52C Researcher Lookup",
    "\U0001F464 Team Activity",
    "\U0001F30D Market Alignment Dashboard",
    "\U0001F50D Talent Finder",
    "\U0001F30D Country Analysis",
    "\U0001F916 Talent Recommendation",
    "\U0001F469 Employee Activity",
    "\U0001F4CA Employee Insights"
])

if tab == "\U0001F4B8 Investor Matcher":
    investor_ui()

elif tab == "\U0001F9E0 Session Analyzer":
    session_ui()

elif tab == "\U0001F52C Researcher Lookup":
    researcher_ui()

elif tab == "\U0001F464 Team Activity":
    team_activity_ui()

elif tab == "\U0001F30D Market Alignment Dashboard":
    market_alignment_ui()

elif tab == "\U0001F50D Talent Finder":
    talent_finder_ui()

elif tab == "\U0001F30D Country Analysis":
    countries_render_ui_ver3(db)

elif tab == "\U0001F916 Talent Recommendation":
    st.title("Dynamic Talent Recommendation System")

    sector = st.text_input("Enter Sector (e.g., AI, Biotech)")
    region = st.text_input("Enter Region (e.g., US, EU)")
    tags = st.multiselect("Tags / Keywords", ["AI", "Healthcare", "Climate", "Fintech"])
    match_mode = st.selectbox("Match Mode", ["Exact", "Fuzzy"], index=1)

    if st.button("\U0001F50D Get Recommendations"):
        payload = {
            "researcher_tags": tags,
            "match_mode": match_mode,
            "sector": sector,
            "region": region
        }
        try:
            response = session.post("http://127.0.0.1:8000/recommend/investors", json=payload)
            if response.status_code == 200:
                data = response.json().get("results", [])
                if data:
                    st.success(f"Found {len(data)} investor matches.")
                    st.dataframe(data)
                else:
                    st.warning("No matches found.")
            else:
                st.error(f"Talent Recommendation API error {response.status_code}: {response.text}")
                logging.error(f"Talent Recommendation API error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch recommendations: {e}")
            logging.exception("Error during API request.")

elif tab == "\U0001F469 Employee Activity":
    employee_activity_ui()

elif tab == "\U0001F4CA Employee Insights":
    employee_quadrangulation_ui()

