"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Data Science Portfolio."""


if __name__ == "__main__":
    main(prog_name="data-science-portfolio")  # pragma: no cover
