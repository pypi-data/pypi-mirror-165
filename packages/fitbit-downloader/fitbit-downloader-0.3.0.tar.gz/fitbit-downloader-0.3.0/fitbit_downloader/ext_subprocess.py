import shlex
import subprocess


def _stream_process(process):
    go = process.poll() is None
    for line in process.stdout:
        print(line.decode("utf8"), end="")
    return go


def run_and_stream_output(command: str):
    process = subprocess.Popen(
        shlex.split(command),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    while _stream_process(process):
        pass


def run_then_show_output(command: str):
    output = subprocess.run(
        shlex.split(command),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True,
    )
    print(output.stdout.decode("utf8"))
