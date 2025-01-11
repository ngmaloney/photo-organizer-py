import typer
from organizer.organize import organize

app = typer.Typer()

@app.command()
def main(
  src: str = typer.Argument(..., help="Source directory"),
  dest: str = typer.Argument(..., help="Destination directory"),
  dry_run: bool = typer.Option(False, "--dry-run", help="Perform a dry run without making changes"),
  convert: bool = typer.Option(True, "--convert", help="Convert the file format during processing"),
  debug: bool = typer.Option(False, "--debug", help="Print debug information about files")
):
  organize(src, dest, dry_run, convert, debug)

if __name__ == "__main__":
  app()