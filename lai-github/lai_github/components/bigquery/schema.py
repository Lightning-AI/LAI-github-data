import datetime
from typing import List
from github.Repository import Repository

def get_repos(repos: List[Repository]):

    return [
        {
            "id": repo.id,
            "node_id": repo.raw_data["node_id"],
            "name": repo.name,
            "full_name": repo.full_name,
            "private": repo.private,
            "owner": repo.owner.id,
            "html_url": repo.html_url,
            "description": repo.description,
            "fork": repo.fork,
            "created_at": repo.created_at.strftime("%Y-%m-%d %H:%M:%S %Z"),
            "updated_at": repo.updated_at.strftime("%Y-%m-%d %H:%M:%S %Z"),
            "pushed_at": repo.pushed_at.strftime("%Y-%m-%d %H:%M:%S %Z"),
            "homepage": repo.homepage,
            "size": repo.size,
            "stargazers_count": repo.stargazers_count,
            "watchers_count": repo.watchers_count,
            "language": repo.language,
            "has_issues": repo.has_issues,
            "has_projects": repo.has_projects,
            "has_downloads": repo.has_downloads,
            "has_wiki": repo.has_wiki,
            "has_pages": repo.has_pages,
            "forks_count": repo.forks_count,
            "archived": repo.archived,
            "disabled": repo.raw_data.get("disabled"),
            "open_issues_count": repo.open_issues_count,
            "license": (repo.raw_data.get("license") or {}).get("key"),
            "allow_forking": repo.raw_data.get("allow_forking"),
            "is_template": repo.raw_data.get("is_template"),
            "topics": repo.raw_data.get("topics"),
            "default_branch": repo.default_branch,
            "permissions": repo.permissions.raw_data,
            "organization": repo.organization.id if repo.organization else None,
            "network_count": repo.network_count,
            "subscribers_count": repo.subscribers_count,
            "template_repository_id": (
                        repo.raw_data.get("template_repository") or {}).get("id"),
            "parent_id": repo.parent.id if repo.parent else None,
            "source_id": repo.source.id if repo.source else None,
            "seen_at_utc": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S %Z")
        }
        for repo in repos
    ]

def get_users(repos):
    return [
        {
            "id": repo.owner.id,
            "login": repo.owner.login,
            "node_id": repo.owner.node_id,
            "avatar_url": repo.owner.avatar_url,
            "gravatar_id": repo.owner.gravatar_id,
            "html_url": repo.owner.html_url,
            "type": repo.owner.type,
            "site_admin": repo.owner.site_admin,
            "name": repo.owner.name,
            "seen_at_utc": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S %Z")
        }
        for repo in repos
    ]

def get_licenses(repos):
    return [
        {
            "key": repo.raw_data.get("license").get("key"),
            "name": repo.raw_data.get("license").get("name"),
            "spdx_id": repo.raw_data.get("license").get("spdx_id"),
            "node_id": repo.raw_data.get("license").get("node_id"),
            "seen_at_utc": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S %Z")
        }
        for repo in repos
        if repo.raw_data.get("license") is not None
    ]