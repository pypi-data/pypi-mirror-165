import json
import subprocess
from pathlib import Path

from invoke import task

from pydantic_lambda_handler.gen_open_api_inspect import gen_open_api_inspect

root = Path(__name__).absolute().parents[1]
print(root)
demo_app_dir = root.joinpath("demo_app").absolute()
assert demo_app_dir.exists(), demo_app_dir


@task
def build_and_deploy(c):
    subprocess.run("cdk bootstrap", check=True, shell=True, cwd=demo_app_dir)
    deploy(c)


@task
def deploy(c):
    subprocess.run("cdk deploy --require-approval never", check=True, shell=True, cwd=demo_app_dir)


@task(help={"app_dir": "The app directory", "output_file_path": "The output directory"})
def generate_open_api_spec(c, app_dir, output_file_path):
    """
    Generate an open api spec and write to file
    """
    app_dir_path = Path(app_dir)
    app_dir_path.exists()

    schema, *_ = gen_open_api_inspect(app_dir_path)

    output_file_path = Path(output_file_path)
    output_file_path.parent.exists()

    schema = json.loads(schema)

    with output_file_path.open("w") as f:
        json.dump(schema, f, indent=4)
