from .github_backend import GithubBackend
from .github_org_backend import GithubOrgBackend

def get_backend(name):
    return {
        'github': GithubBackend,
        'github_org': GithubOrgBackend,
    }[name]
