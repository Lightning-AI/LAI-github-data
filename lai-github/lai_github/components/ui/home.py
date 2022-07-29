import lightning as L
from lightning.app.frontend import StreamlitFrontend
from lightning.app.utilities.state import AppState

import constants

import streamlit as st

import pandas as pd


def render_fn(state: AppState):
    st.write("Repositories of Interest")
    st.json(constants.REPOS_OF_INTEREST)

    st.write("Dependent Repositories scraped")

    df = pd.DataFrame(state.repos)
    st.table(df)

    return


class GithubUI(L.LightningFlow):
    def __init__(self):
        super().__init__()
        self.repos = constants.REPOS_OF_INTEREST


    def run(self, repos):
        self.repos = repos

    def configure_layout(self):
        return StreamlitFrontend(render_fn=render_fn)
