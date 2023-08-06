import subprocess

import click


def autoflake_cmd(check: bool = False) -> list[str]:
    return (
        [
            "autoflake",
            "--remove-all-unused-imports",
            "--remove-unused-variables",
            "-i",
            "-r",
            "src",
        ]
        if check is False
        else [
            "autoflake",
            "--remove-all-unused-imports",
            "--remove-unused-variables",
            "-c",
            "-r",
            "src",
        ]
    )


def isort_cmd(check: bool = False) -> list[str]:
    return (
        [
            "isort",
            "--profile",
            "black",
            "src",
        ]
        if check is False
        else [
            "isort",
            "--check",
            "--profile",
            "black",
            "src",
        ]
    )


@click.group()
def cli():
    pass


@cli.command()
def format():
    """Run autoflake to remove unused imports then run isort over src/"""
    subprocess.run(autoflake_cmd(check=False))
    subprocess.run(isort_cmd(check=False))
    subprocess.run(["black", "src"], check=False)


@cli.command()
def check():
    """Check formatting, import and typing (black & isort & pyright) then run tests."""
    subprocess.run(autoflake_cmd(check=True), check=True)
    subprocess.run(isort_cmd(check=True), check=True)
    subprocess.run(["black", "--check", "src"], check=True)
    subprocess.run(["pyright", "src"], check=True)
    click.echo("Done checking code. No errors found. ")
