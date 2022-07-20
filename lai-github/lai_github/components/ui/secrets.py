import json
import logging
import os

import streamlit as st

import lightning as L
from lightning.app.frontend import StreamlitFrontend
from lightning.app.utilities.state import AppState
from lightning.app.storage import Path

def write_configs(data):

    filepath = Path(os.path.join(str(Path.home()), ".secrets1.json"))
    with open(filepath, "w") as f:
        json.dump(data, f)

def read_configs():

    try:
        filepath = Path(os.path.join(str(Path.home()), ".secrets1.json"))
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Could not find {filepath}.")
        return {}
    except json.decoder.JSONDecodeError:
        logging.error(f"Secrets file {filepath} is not in valid JSON format.")
        return {}

def render_fn(state: AppState):

    col1, col2 = st.columns(2)
    with col1:
        st.title("Secrets")
        if state.secrets:

            st.write("Secrets that have been loaded.")
            for key in state.secrets.keys():
                st.code(key)
        else:
            st.write("Please upload your secrets.json file.")


    with col2:

        secrets_value = st.text_input("JSON string with secrets that will be used.", type="password")

        save_notification_settings = st.button("Save Secrets.")
        if save_notification_settings:
            try:
                secrets = json.loads(secrets_value)
                state.secrets = secrets
                st.write(f"Loaded Secrets")
                write_configs(secrets)
                state.refresh = True
            except json.decoder.JSONDecodeError:
                st.write("Unable to save the secrets. Expected a JSON string")

class SecretsUI(L.LightningFlow):
    def __init__(self, refresh=False):
        super().__init__()
        self.secrets = read_configs()
        self.refresh = False

    def configure_layout(self):
        return StreamlitFrontend(render_fn=render_fn)
