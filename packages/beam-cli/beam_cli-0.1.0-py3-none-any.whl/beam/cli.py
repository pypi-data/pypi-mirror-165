import typer

from beam.commands import up
from beam.commands import down
from beam.commands import start


app = typer.Typer()
app.command()(up.up)
app.command()(down.down)
app.command()(start.start)


if __name__ == "__main__":
    app()
