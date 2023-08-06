import subprocess
import click
import os

@click.command()
def start_web():
    current_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(current_path)
    cmd = "flask run"
    subprocess.call(cmd, shell=True)

if __name__ == '__main__':
    start_web()