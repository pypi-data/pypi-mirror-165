import typer


app = typer.Typer()


@app.callback()
def callback():
    """
    Awesome Mitchell Portal Gun
    """


@app.command()
def shoot():
    """
    Shoot the portal gun
    """
    typer.echo("Shooting Mitchell portal gun")


@app.command()
def load():
    """
    Load the portal gun
    """
    typer.echo("Loading Mitchell portal gun")
