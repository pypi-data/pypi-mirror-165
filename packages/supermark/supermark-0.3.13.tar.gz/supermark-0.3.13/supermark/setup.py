from pathlib import Path
import click

GITHUB_ACTION = """
name: Build Supermark Site
on: [push]
jobs:
  Build-Supermark:
    runs-on: ubuntu-latest
    steps:
      - name: Pip Installer
        uses: BSFishy/pip-action@v1
        with:
          packages: |
            supermark
      - name: Checkout
        uses: actions/checkout@v2
      - name: Install pandoc
        run: |
          $CONDA/bin/conda install pandoc
          ln -s $CONDA/bin/pandoc /usr/local/bin/pandoc
      - name: Run Supermark
        run: |
          supermark build --all --log
      - name: Push
        uses: actions-x/commit@v6
"""


def _write_file(base_path: Path, file: str, folder: str, content: str):
    folder_path = base_path / Path(folder)
    file_path = folder_path / Path(file)
    if file_path.exists():
        if not click.confirm("File {} already exsists. Overwrite?".format(file)):
            return
    folder_path.mkdir(parents=True, exist_ok=True)
    with open(file, "w") as ofile:
        ofile.write(content)


def setup_github_action(base_path: Path):
    _write_file(base_path, "build-site.yml", ".github/workflows/", GITHUB_ACTION)
