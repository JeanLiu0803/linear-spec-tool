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

    st.write("Here is the linear spec tool maker.")



if __name__ == "__main__":
    run()
