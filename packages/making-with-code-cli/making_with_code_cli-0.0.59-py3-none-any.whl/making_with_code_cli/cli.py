import click
from pprint import pprint
from pathlib import Path
from subprocess import run
from importlib.metadata import metadata
import yaml
import toml
import os
import traceback
from making_with_code_cli.mwc_api import MakingWithCodeAPI as API
from making_with_code_cli.styles import (
    address,
    question,
    info,
    confirm,
    error,
)
from making_with_code_cli.settings import (
    read_settings, 
    iter_settings,
    write_settings,
)
from making_with_code_cli.cli_setup import (
    INTRO_MESSAGE,
    INTRO_NOTES,
    WORK_DIR_PERMISSIONS,
    choose_mwc_username,
    choose_work_dir,
    choose_mwc_site_url,
    choose_course,
    choose_editor,
    MWCShellConfig,
    InstallHomebrew,
    InstallXCode,
    WriteShellConfig,
    InstallPython3,
    InstallPoetry,
    InstallGit,
    InstallTree,
    InstallAtom,
    InstallImageMagick,
    InstallHttpie,
    InstallScipy,
    GHAuthentication,
    GitConfiguration,
)
from making_with_code_cli.curriculum import (
    get_curriculum,
)
from making_with_code_cli.git_backend import (
    get_backend,
)

@click.group()
def cli():
    "Command line interface for Making with Code"

@cli.command()
def version():
    "Print MWC version"
    version = metadata('making-with-code-cli')['version']
    click.echo(address("MWC " + version, preformatted=True))

@cli.command()
@click.option("--yes", is_flag=True, help="Automatically answer 'yes' to setup prompts")
@click.option("--teacher", is_flag=True, help="Install in teacher mode")
@click.pass_context
def setup(ctx, yes, teacher):
    """Set up the MWC command line interface"""
    settings = read_settings()
    rc_tasks = []
    click.echo(address(INTRO_MESSAGE))
    for note in INTRO_NOTES:
        click.echo(address(note, list_format=True))
    click.echo()
    settings['mwc_username'] = choose_mwc_username(settings.get("mwc_username"))
    settings['role'] = "teacher" if teacher else "student"
    settings['work_dir'] = str(choose_work_dir(settings.get("work_dir")).resolve())
    settings['mwc_site_url'] = choose_mwc_site_url(settings.get('mwc_site_url'))
    curriculum = get_curriculum(settings)
    settings['course'] = choose_course(
        [course['name'] for course in curriculum['courses']], 
        default=settings.get('course')
    )
    course = [c for c in curriculum['courses'] if c['name'] == settings['course']][0]
    settings['editor'] = choose_editor(settings.get('editor', 'atom'))
    G = get_backend(course['git_backend'])
    settings = G.extend_settings(settings)
    if yes:
        click.echo(info("Updated settings:"))
        click.echo(info(yaml.dump(settings), preformatted=True))
    else:
        click.echo(info(yaml.dump(settings), preformatted=True))
        click.confirm(
            question("Do these settings look ok?"),
            abort=True
        )
    write_settings(settings)

    tasks = [
        MWCShellConfig(settings),
        InstallHomebrew(settings),
        InstallXCode(settings),
        InstallPoetry(settings),
        WriteShellConfig(settings),
        InstallPython3(settings),
        InstallGit(settings),
        InstallTree(settings),
        InstallAtom(settings),
        InstallImageMagick(settings),
        InstallHttpie(settings),
        InstallScipy(settings),
        GHAuthentication(settings),
        GitConfiguration(settings),
    ]
    for task in tasks:
        task.run_task_if_needed()
    
    ctx.invoke(update)

def get_course_by_name(name, courses):
    for course in courses:
        if course['name'] == name:
            return course

@cli.command()
def update():
    """Update the MWC work directory"""
    settings = read_settings()
    curr = get_curriculum(settings)
    course = [c for c in curr['courses'] if c['name'] == settings['course']][0]
    backend = course['git_backend']
    G = get_backend(backend)(settings)
    mwc_home = Path(settings["work_dir"])
    mwc_home.mkdir(mode=WORK_DIR_PERMISSIONS, parents=True, exist_ok=True)
    course = get_course_by_name(settings['course'], curr['courses'])
    if course is None:
        click.echo(error(f"Error: You are enrolled in {settings['course']}, but this course is not available. Please run mwc setup again."))
        return 
    course_dir = mwc_home / course['slug']
    course_dir.mkdir(mode=WORK_DIR_PERMISSIONS, exist_ok=True)
    for unit in course['units']:
        unit_dir = course_dir / unit['slug']
        unit_dir.mkdir(mode=WORK_DIR_PERMISSIONS, exist_ok=True)
        for module in unit['modules']:
            module_dir = unit_dir / module['slug']
            if module_dir.exists():
                try:
                    G.update(module, module_dir)
                except Exception as e:
                    msg =  traceback.format_exception(type(e), e, e.__traceback__)
                    print(error(''.join(msg)))
            else:
                if 'init_action' in module:
                    rel_dir = module_dir.resolve().relative_to(mwc_home)
                    click.echo(confirm(f"Initializing {module['slug']} at {rel_dir}."))
                    click.echo(confirm("See {module['url']} for details."))
                    try:
                        G.init_module(module, module_dir)
                    except Exception as e:
                        msg =  traceback.format_exception(type(e), e, e.__traceback__)
                        click.echo(error(''.join(msg)))
