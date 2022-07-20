import lightning as L
from lightning.app.frontend import StreamlitFrontend
from lightning.app.utilities.state import AppState

import constants

import streamlit as st


def render_fn(state: AppState):
    st.write("Repositories scraped")
    st.json(constants.REPOS_OF_INTEREST)

    return


class GithubUI(L.LightningFlow):
    def __init__(self):
        super().__init__()

    def configure_layout(self):
        return StreamlitFrontend(render_fn=render_fn)
