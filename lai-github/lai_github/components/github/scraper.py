import datetime
import logging
import time
import requests
from urllib.parse import parse_qs, urlparse

import lightning as L
from lightning.app.storage import Payload
from bs4 import BeautifulSoup
from retry import retry

@retry(tries=5, backoff=2, jitter=(1, 10))
def make_scrape_request(url: str):
    """
    Proxies requests during scrape activities.

    Args:
        url: the url to make get request on.

    Returns:
        requests.Response object.
    """
    logging.info(f"Making request to {url}")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response
    except requests.exceptions.Timeout:
        logging.warning(f"Timeout for proxy request to {url}.")
    except requests.exceptions.TooManyRedirects:
        logging.warning(f"Too many redirects for proxy request to {url}")
    except requests.exceptions.RequestException as e:
        logging.exception(e)

    raise Exception(f"make_scrape_request failed to request {url}")




class Scrapper(L.LightningWork):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root_repo = None
        self.dependent_repos = []
        self.store_dependent_repos = []

    def reset(self):
        self.dependent_repos = []
        self.store_dependent_repos = []

    def run(self, repo, scrape_limit):
        self.root_repo = repo
        self.dependent_github_repos(scrape_limit)

    def dependent_github_repos(self, scrape_limit):

        dependent_github_repos_url = f"https://github.com/{self.root_repo}/network/dependents"

        # Get packages
        # TODO: Eric, persist repo_id, package_id, and package name
        response = make_scrape_request(url=dependent_github_repos_url)
        soup = BeautifulSoup(response.content, "html.parser")
        select_menu = soup.find_all("a", {"class": "select-menu-item"})
        packages = [None]

        try:
            packages = [
                parse_qs(urlparse(item.get('href')).query).get('package_id',
                                                               [None])[0]
                for item in select_menu
                if item.get('href')
            ]
        except:
            logging.info(
                f"Could not find packages from {dependent_github_repos_url}")
        print(packages)
        for package in packages:

            while dependent_github_repos_url:
                logging.info(f"Scraping {dependent_github_repos_url}")
                response = make_scrape_request(url=dependent_github_repos_url)
                soup = BeautifulSoup(response.content, "html.parser")
                for a in soup.select("a[data-hovercard-type=repository]"):
                    # Exit early if scrape_limit has been reached
                    if scrape_limit != -1 and len(self.store_dependent_repos) >= scrape_limit:
                        break

                    dependent_repo = a["href"].lstrip("/")
                    self.store_dependent_repos = [
                        *self.store_dependent_repos,
                        dict(
                            repo_id=self.root_repo,
                            dependent_repo_id=dependent_repo,
                            package_id=package,
                            seen_at_utc=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S %Z"),
                            dependent_github_paginate_url=dependent_github_repos_url
                        )
                    ]

                # next page?
                try:
                    next_link = soup.select(".paginate-container")[0].find("a", text="Next")
                except IndexError:
                    break
                if next_link is not None:
                    dependent_github_repos_url = str(next_link["href"])
                    time.sleep(1)
                else:
                    dependent_github_repos_url = None
                soup.decompose()
                break

        self.dependent_repos = Payload(self.store_dependent_repos)
