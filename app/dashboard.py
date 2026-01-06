import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "modules")))

import plots
import variables as v


st.title('MEPS Cancer Analysis Dashboard')

# To run it: `streamlit run app/dashboard.py`
