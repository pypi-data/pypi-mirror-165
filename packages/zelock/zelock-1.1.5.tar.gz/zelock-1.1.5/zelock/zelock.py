import os
from datetime import datetime

import typer

app = typer.Typer()


class BGColor:
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# use docker-repo
@app.command()
def zelock(tag):
    current_working_directory = os.getcwd()
    project_name = os.path.basename(current_working_directory)
    is_services = project_name.endswith('services') or project_name.endswith('service') or project_name.endswith('api') or project_name.endswith('socket')
    try:
        os.system("yarn --silent")
        if not is_services: os.system("yarn build --quite")
        os.system("docker buildx create --name armbuilder")
        os.system("docker buildx use armbuilder")
        os.system(f"docker buildx build --platform linux/amd64 -t jirapan/{project_name}:{tag} . --push\n")
        print('======================================================================')
        print(f'{BGColor.OKGREEN}{datetime.now()} :: {project_name} is published', BGColor.ENDC)
        print('======================================================================')
    except Exception as error:
        print(error)
        pass


if __name__ == '__main__':
    app()
