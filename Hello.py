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
import numpy as np
import plotly.express as px

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="linear spec tool",
        page_icon="🌟",
    )

    with st.sidebar:
        st.write("### Please input x and y value for each point")
        if "point_df" not in st.session_state:
          # st.session_state.point_df = pd.DataFrame(columns = ["x_value", "y_value"])
          st.session_state.point_df = pd.DataFrame({"x_value": 0, "y_value": 0, "Formula": "N/A"})

        x = st.number_input("X value (Frequency)", key = "x_value", step = 0.01)
        y = st.number_input("Y value (Mag.)", key = "y_value", step = 0.01)
        if len(st.session_state.point_df.index) == 0:
          idx = 0
        else:
          idx = st.session_state.point_df.index[-1]

        if len(st.session_state.point_df.index) >= 2:
          slope, intercept = line_formula(st.session_state.point_df.iloc[-2, 0], st.session_state.point_df.iloc[-2, 1], st.session_state.point_df.iloc[-1, 0], st.session_state.point_df.iloc[-1, 1])
          formula_text = "y = {}x + ({})".format(slope, intercept)
        else:
          formula_text = "N/A"
        current_input = pd.DataFrame({"x_value": x, "y_value": y, "Formula": formula_text}, index = [idx+1])

        if st.button("Add point", key = "add_point_but"):
            st.session_state.point_df = pd.concat([st.session_state.point_df, current_input], axis = 0)
            st.write("Point added! x = {}, y = {}".format(x, y))
        if st.button("Delete point", key = "delete_point"):
            last_index = len(st.session_state.point_df.index)
            st.session_state.point_df = st.session_state.point_df.drop([last_index])
        if st.button("Reset", key="reset"):
            st.session_state.point_df = pd.DataFrame({"x_value": 0, "y_value": 0})
        
        st.write("Current point:")
        st.write(st.session_state.point_df)

    # Main page
    st.write("# Welcome to linear spec tool")
    st.write(st.session_state.point_df)
    st.write("## Here is the preview plot.")
    st.selectbox("What is your plot?", ["SDD21", "SDD11", "SDD22", "Crosstalk", "TDR", "User Defined (Not available now.)"], key = "plot_select")
    
    spec_plot = px.line(st.session_state.point_df, x = "x_value", y = "y_value")
    plot_type = str(st.session_state.plot_select)
    if plot_type != "TDR":
      spec_plot.update_layout(
          title = plot_type,
          xaxis_title = "Frequency(GHz)",
          yaxis_title = "Magnitude(dB)",
          xaxis = dict(
              tickmode = 'linear',
              tick0 = 0,
              dtick = 5
          ),

          yaxis = dict(
              tickmode = 'linear',
              tick0 = 0,
              dtick = 5
          )
      )
      spec_plot.update_xaxes(range=[0, 40], minor_ticks = "inside")
      spec_plot.update_yaxes(range=[-25, 0], minor_ticks = "inside")

    elif plot_type == "User Defined":
        st.textinput("Please input the tilte", key = "user_title")
        st.textinput("Please input the x axis title", key = "x_title")
        st.textinput("Please input the y axis title", key = "y_title")
        spec_plot.update_layout(
          title = str(st.session_state.user_title),
          xaxis_title = str(st.session_state.x_title),
          yaxis_title = str(st.session_state.y_title),
          xaxis = dict(
              tickmode = 'linear',
              tick0 = 0,
              dtick = 0.5
          ),
          yaxis = dict(
              tickmode = 'linear',
              tick0 = 0,
              dtick = 5
          ))
        
    else:
      spec_plot.update_layout(
          title = plot_type,
          xaxis_title = "Time(ns)",
          yaxis_title = "Impedance(ohm)",
          xaxis = dict(
              tickmode = 'linear',
              tick0 = 0,
              dtick = 0.5
          ),
          yaxis = dict(
              tickmode = 'linear',
              tick0 = 0,
              dtick = 5
          )
      )
    
    st.plotly_chart(spec_plot, use_container_width=True)

    export_df = pd.DataFrame(columns = ["Frequency(GHz)"])
    st.download_button("Download csv", export_df.to_csv(), key = "download_but")
    
def line_formula(x1, y1, x2, y2):
    x_array = np.array([[x1, 1],
                        [x2, 1]])
    y_array = np.array([[y1],
                        [y2]])
    
    x_inv = inv(x_array)
    ans = np.dot(x_inv, y_array)
    
    m = np.round(ans[0][0], 4)
    b = np.round(ans[1][0], 4)

    print('y = {}x + ({})'.format(m, b))

    return m, b



if __name__ == "__main__":
    run()
