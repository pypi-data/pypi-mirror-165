from .base_backend import GitBackend
from subprocess import run
from pathlib import Path
import click
import json
import os
from making_with_code_cli.helpers import cd
from making_with_code_cli.styles import (
    confirm,
)

COMMIT_TEMPLATE = ".commit_template"

class GithubOrgBackend(GitBackend):
    """A Github backend which uses github organizations.  
    Students own their own repos but create them from within the organization.
    """

    @classmethod
    def extend_settings(self, settings):
        "Asks for the user's github username and email address"
        def choose_github_username(github_username):
            msg = "What is your GitHub username? "
            return click.prompt(msg, default=github_username)
        def choose_github_org(github_org):
            msg = "What is the name of the course's GitHub organization? "
            return click.prompt(msg, default=github_org)
        def choose_github_email(github_email):
            msg = "What is the email address associated with your GitHub account? "
            return click.prompt(msg, default=github_email)
        def choose_git_name(git_name):
            msg = "What name do you want to use in your git commits? "
            return click.prompt(msg, default=git_name)
        if settings.get('github_username') or click.confirm("Do you have a GitHub account?"):
            settings['github_username'] = choose_github_username(settings.get("github_username"))
            settings['github_org'] = choose_github_org(settings.get("github_org"))
            settings['github_email'] = choose_github_email(settings.get("github_email"))
            settings['git_name'] = choose_git_name(settings.get("git_name"))
        return settings

    def init_clone(self, module, modpath):
        url = module["repo_url"]
        cmd = f'gh repo clone "{url}" "{modpath.name}"'
        with cd(modpath.parent):
            run(cmd, shell=True, check=True)
        if (modpath / COMMIT_TEMPLATE).exists():
            with cd(modpath):
                run(f"git config commit.template {COMMIT_TEMPLATE}")

    def init_create_from_template(self, module, modpath):
        """Creates the named repo from a template, or clones an existing repo with. 
        """
        repo_name = self.get_repo_name_from_template_repo_url(module["repo_url"])
        url = module["repo_url"]

        if self.user_has_repo(repo_name):
            cmd = f'gh repo clone "{url}" "{modpath.name}"'
        else:
            if modpath.exists():
                self.relocate_existing_directory(modpath)
            usr = self.settings['username']
            org = self.settings['github_org']
            cmd = f'gh repo create "{org}/{repo_name}" --clone --private --template "{url}"'
        with cd(modpath.parent):
            run(cmd, shell=True, check=True)
            run(f"mv {repo_name} {modpath.name}", shell=True, check=True) 
        if (modpath / COMMIT_TEMPLATE).exists():
            with cd(modpath):
                run(f"git config commit.template {COMMIT_TEMPLATE}")

    def get_repo_name_from_template_repo_url(self, url):
        """Parses the template repo URL and returns the name of a repo to create.
        Expects a GitHub url like "https://github.com/cproctor/mwc-pedprog-unit00-project-drawing.git"
        """
        parts = url.split('/')
        name, suffix = parts[-1][:-4], parts[-1][-4:]
        return name + '-' + self.settings['github_username']

    def relocate_existing_directory(self, path):
        """Moves an existing directory out of the way.
        """
        new_path = path.parent / path.name + '_old'
        while new_path.exists():
            new_path = new_path.parent / new_path.name + '_old'
        click.echo(confirm(f"Moving existing directory {path} to {new_path}."))
        os.rename(path, new_path)

    def user_has_repo(self, name):
        "Checks to see whether the user already has the named repo."
        org = self.settings['github_org']
        cmd = f"gh repo list {org} --json name --limit 10000"
        result = run(cmd, shell=True, capture_output=True, text=True).stdout
        repo_names = [obj['name'] for obj in json.loads(result)]
        return name in repo_names
