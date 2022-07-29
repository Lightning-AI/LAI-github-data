
import time

import lightning as L

from lai_github.components.github import Github, Scrapper
from lai_github.components.ui import SecretsUI, GithubUI
from lai_github.components.bigquery import DatabaseLoader


import constants

class LitApp(L.LightningFlow):
    def __init__(self) -> None:
        super().__init__()
        self.secrets_ui = SecretsUI()
        self.home_ui = GithubUI()
        self.github_client = Github(tokens=[""], parallel=False)
        self.scrapper = Scrapper(parallel=False)
        self.loader = DatabaseLoader()
        self.last_run_time = int(time.time()) - 1000
        self.interval = 60 * 60 * 24

        self.scrapped_repos = []

    def run(self):

        # Load secrets
        if not self.secrets_ui.secrets.get("LIGHTNING__GITHUB_TOKENS") or not self.secrets_ui.secrets.get("LIGHTNING__GCP_CREDENTIALS"):
            self.secrets_ui.run()
            return

        self.home_ui.run(repos=self.scrapped_repos)

        # if time.time() > self.last_run_time + self.interval:
        #     return

        # Get repo metadata of interest and persist to disk
        for repo in constants.REPOS_OF_INTEREST:
            self.github_client.get_repo(repo, tokens=self.secrets_ui.secrets.get("LIGHTNING__GITHUB_TOKENS"), executed_at=self.last_run_time)

        # Scraper get repos and the github client listens for new repos to fetch metadata
        for repo_id, root_repo in enumerate(constants.REPOS_OF_INTEREST):
            self.scrapper.run(root_repo, 20) # give better name

            if self.scrapper.store_dependent_repos:

                # Writes dependency tree to datawarehouse
                self.loader.load_dependent_repos(
                    dependent_repos=self.scrapper.store_dependent_repos,
                    credentials=self.secrets_ui.secrets.get(
                        "LIGHTNING__GCP_CREDENTIALS"),
                    table="qa_github.staging_dependent_repos" # Fix this should not rely on hardcode prefix.
                )

                # Gets and writes repository metadata to disk
                for repo_record in self.scrapper.store_dependent_repos:
                    self.github_client.get_repo(
                        repo=repo_record.get("dependent_repo_id"),
                        tokens=self.secrets_ui.secrets.get("LIGHTNING__GITHUB_TOKENS"),
                        executed_at=self.last_run_time
                    )

                self.scrapped_repos = [*self.scrapper.store_dependent_repos, *self.scrapped_repos]
                self.scrapper.reset()

        # Looks for newly retrieved github data and loads them to the warehouse
        self.loader.run(
            gcp_credentials=self.secrets_ui.secrets.get("LIGHTNING__GCP_CREDENTIALS"),
            files_to_load=self.github_client.repos_to_load
        )

        #self._exit()

    def configure_layout(self):

        if self.secrets_ui.secrets.get("LIGHTNING__GITHUB_TOKENS"):
            return [
                dict(name="Home", content=self.home_ui),
                dict(name="Secrets", content=self.secrets_ui),
            ]
        else:
            return [
                dict(name="Secrets", content=self.secrets_ui)
            ]



app = L.LightningApp(LitApp())
