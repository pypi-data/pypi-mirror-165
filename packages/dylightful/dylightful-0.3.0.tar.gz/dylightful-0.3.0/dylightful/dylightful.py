import click


@click.command()
@click.argument("filename")
def hello(count, name, filename):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo(f"Hello {name}!")
        click.echo(filename)


if __name__ == "__main__":
    hello()
