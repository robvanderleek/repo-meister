import sys

import typer
from dotenv import load_dotenv
from requests import Response

from ghmeister.Context import Context
from ghmeister.commands import Utils
from ghmeister.commands.github import Issues, Users
from ghmeister.commands.github.Users import get_authenticated_user
from ghmeister.utils import pretty_print_json

load_dotenv()


def handle_response(response: Response):
    if response.ok:
        json = response.json()
        if json:
            pretty_print_json(json)
        else:
            Context.console.print("[green]Success[/green]")
    else:
        Context.console.print(f"[red]Error: {response.status_code}[/red]")
        sys.exit(1)


cli = typer.Typer(no_args_is_help=True, add_completion=False, result_callback=handle_response)
cli.add_typer(Users.users, name="users", help="GitHub endpoints for users (alias: user)")
cli.add_typer(Users.users, name="user", hidden=True)
cli.add_typer(Issues.issues, name="issues", help="GitHub endpoints for issues (alias: issue)")
cli.add_typer(Issues.issues, name="issue", hidden=True)
cli.add_typer(Utils.utils, name="utils", help="Various utilities")


@cli.callback(invoke_without_command=False)
def callback(ctx: typer.Context):
    """GH Meister: GitHub management made easy."""


def main():
    Context.init()
    if len(sys.argv) == 1:
        print(get_authenticated_user().json()['login'])
    else:
        cli()


if __name__ == '__main__':
    main()
