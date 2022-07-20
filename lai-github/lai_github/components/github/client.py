import logging
import datetime as dt
import os
import pickle
import random
import time
import requests
import github
from github import GithubException
from github import Repository
from retry import retry

import lightning as L
from lightning.app.storage.path import Path



def select_token(tokens):
    return random.choice(tokens)

class Github(L.LightningWork):

    def __init__(self, tokens, drive_name: str = "lit://repositories"):
        super().__init__()
        self.tokens = tokens or []
        self.repos_to_load = []


    def get_repo(self, repo, tokens, executed_at):
        self.run(action="GetRepo", repo=repo, tokens=tokens, executed_at=executed_at)

    def _get_repo(self, repo, tokens, executed_at):

        token = select_token(tokens)
        client = GithubClient([token])
        _repo = client.get_repo(full_name=repo)
        repo_persistance_key = Path(f"{executed_at}/{repo}.pkl")

        Path(os.path.dirname(repo_persistance_key)).mkdir(parents=True, exist_ok=True)

        with open(repo_persistance_key, "wb+") as _file:
            pickle.dump(_repo, _file)
            self.repos_to_load = [*self.repos_to_load, *[repo_persistance_key]]


    def run(self, action, *args, **kwargs):
        if action == "GetRepo":
            self._get_repo(*args, **kwargs)


class GithubClient:
    def __init__(self, tokens: list[str]):
        self._tokens = tokens
        self._clients = [github.Github(login_or_token=token) for token in self._tokens]

    @property
    def github_client(self) -> github.Github:
        min_reset_time = float("inf")
        client_with_min_reset_time = None
        for client in self._clients:
            rate_limit = client.get_rate_limit()
            if rate_limit.core.remaining > 0:
                return client
            reset_time = int(rate_limit.core.reset.timestamp())
            if reset_time < min_reset_time:
                min_reset_time = reset_time
                client_with_min_reset_time = client

        time_to_sleep = min_reset_time - int(dt.datetime.utcnow().timestamp())
        if time_to_sleep > 0:
            logging.info(f"Github tokens hit rate limit, sleeping for {time_to_sleep} seconds...")
            time.sleep(time_to_sleep)

        return client_with_min_reset_time

    @retry(exceptions=(GithubException, requests.exceptions.RequestException), tries=5, backoff=2, jitter=(1, 10))
    def get_repo(self, full_name: str) -> Repository:
        return self.github_client.get_repo(full_name_or_id=full_name)