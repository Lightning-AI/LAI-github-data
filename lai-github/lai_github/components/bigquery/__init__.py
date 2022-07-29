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

        if dependent_repos:

            # from google.cloud import bigquery
            # from google.oauth2.service_account import \
            #     Credentials as SACredentials
            #
            # # Construct a BigQuery client object.
            # client = bigquery.Client(
            #     project='grid-data-prod',
            #     credentials=SACredentials.from_service_account_info(gcp_credentials)
            # )
            #
            # errors = client.insert_rows_json(table, dependent_repos)
            # print(f"errors: {errors}")

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
        if files_to_load is not None:
            self.files_to_load = files_to_load

        batch = []
        while self.files_to_load:
            try:
                with open(self.files_to_load.pop(), "rb") as _file:
                    batch.append(pickle.load(_file))
            except IndexError:
                break

        if batch:

            self.bigquery.insert(
                json_rows=Payload(get_repos(batch)),
                table="qa_github.repos",
                credentials=gcp_credentials
            )
