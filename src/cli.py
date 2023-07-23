import typer
import uvicorn
import pytest
from typing import Optional
from pytest import ExitCode

app = typer.Typer()


@app.command()
def run(reload: Optional[bool] = False):
    uvicorn.run('main:app', host='0.0.0.0', port=3000)
    

@app.command()
def test(pytest_args: Optional[str] = typer.Option(None)):
    args = pytest_args.split(',') if pytest_args else []
    args.append('-Werror')
    args.append('--log-level=ERROR')
    code = pytest.main(list(set(args)))

    if code != ExitCode.OK:
        raise typer.Exit(code)


if __name__ == '__main__':
    app()
