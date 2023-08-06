import subprocess
import click
import os

@click.command()
def start_queue():
    current_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(current_path)
    cmd = "python huey_consumer.py taskQueue.huey"
    subprocess.call(cmd, shell=True)

if __name__ == '__main__':
    start_queue()