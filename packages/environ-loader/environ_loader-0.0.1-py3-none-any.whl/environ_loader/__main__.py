"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Environ Loader."""


if __name__ == "__main__":
    main(prog_name="environ-loader")  # pragma: no cover
