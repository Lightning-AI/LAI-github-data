import pickle

import lightning as L
from lightning.app.storage import Payload
from lai_github.components.bigquery.schema import get_repos, get_users, get_licenses
from lightning_bigquery import BigQuery


class DatabaseLoader(L.LightningFlow):
    """
    This worker listens for new files from a Drive and loads the data into
    BigQuery
    """

    def __init__(self, files_to_load: list = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.files_to_load = files_to_load
        self.bigquery = BigQuery(
            project="grid-data-prod",
            location="US"
        )

    def load_dependent_repos(
        self, dependent_repos: list, credentials, table
    ):

        self.run(
            action="load_dependent_repos",
            dependent_repos=dependent_repos,
            gcp_credentials=credentials,
            table=table
        )

    def _load_dependent_repos(self, dependent_repos, gcp_credentials, table):

        if self.bigquery.is_running:
            print("query is running")
            return

        self.bigquery.insert(
            credentials=gcp_credentials,
            json_rows=dependent_repos,
            table=table
        )

    def run(self, gcp_credentials, dependent_repos = [], table = "", action = "", files_to_load: list = None, batch_size: int = 20, *args, **kwargs):

        if action == "load_dependent_repos":
            self._load_dependent_repos(
                dependent_repos=dependent_repos,
                gcp_credentials=gcp_credentials,
                table=table
            )
        print(f"loading files: {files_to_load}")
        if files_to_load is not None:
            self.files_to_load = files_to_load

        batch = []
        while self.files_to_load:
            print(self.files_to_load)
            try:
                file_to_load = self.files_to_load.pop()
                with open(file_to_load, "rb") as _file:
                    repo = pickle.load(_file)
                    batch.append(repo)
            except IndexError:
                break

            staged_repos = get_repos(batch)
            staged_users = get_users(batch)
            staged_licenses = get_licenses(batch)
            print(staged_repos)
            self.bigquery.insert(
                json_rows=Payload(staged_repos),
                table="qa_github.staging_dependent_repos",
                credentials=gcp_credentials
            )
