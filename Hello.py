# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import plotly.express as px

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="linear spec tool",
        page_icon="🌟",
    )

    with st.sidebar:
        st.write("## Please input the information")
        st.write("### 1. How many point in the spec line?")
        st.number_input("Number of point", key = "num_point", min_value = 0, max_value = 20, step = 1)
        st.write("### 2. Please input x and y value for each point")
        st.number_input("X value (Frequency)", key = "x_value", step = 0.01)
        st.number_input("Y value (Mag.)", key = "y_value", step = 0.01)

        point_df = pd.DataFrame(columns = ["x_value", "y_value"])
        if st.button("Add point", key = "add_point_but"):
            point_df = point_df.append({"x_value": st.session_state.x_value, "y_value": st.session_state.y_value}, ignore_index = True)
            st.write(point_df)
        if st.button("Delete point", key = "delete_point"):
            point_df = point_df.drop(point_df.index[-1])
            st.write(point_df)
        if st.button("Reset", key="reset"):
            point_df = pd.DataFrame(columns = ["x_value", "y_value"])
            st.write(point_df)

    spec_plot = px.line(point_df, x = "x_value", y = "y_value")
    st.plotly_chart(spec_plot, use_container_width=True)

    st.write("## Here is the linear spec tool maker.")
    st.selectbox("What is your plot?", ["SDD21", "SDD11", "SDD22", "Crosstalk", "TDR", "User Defined"], key = "plot_type")

    export_df = pd.DataFrame(columns = ["Frequency(GHz)"])
    st.download_button("Download csv", export_df.to_csv(), key = "download_but")
    




if __name__ == "__main__":
    run()
