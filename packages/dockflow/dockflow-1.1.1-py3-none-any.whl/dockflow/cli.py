import click
import docker
import os
from pathlib import Path

default_composer_version = 'composer-1.16.14-airflow-1.10.15'

docker_client = docker.from_env()
cwd = Path(os.getcwd())
airflow_home = '/usr/local/airflow'

def network_handler(network):
    if not docker_client.networks.list(filters={'name': network}):
        click.secho('"{}" network does not exist. \n Creating...'.format(network), fg='cyan')
        docker_client.networks.create(
            network,
            driver="bridge",
        )
        click.secho('"{}" network created'.format(network), fg='green')
    else:
        click.secho('"{}" network already exists'.format(network), fg='cyan')


def write_config():
    # Check whether config dir exists
    config_dir = Path.home() / '.dockflow'
    if dir_exist(config_dir) is False:
        os.mkdir(config_dir)
    # Prompt user for input
    image_repo = click.prompt(
        "Please enter your container repo URL",
    )
    # Write to config file
    config_file = Path.home() / '.dockflow' / 'dockflow.cfg'
    with open(config_file, 'w') as cfg:
        cfg.write(image_repo)
    click.secho('Container repo set to: {}'.format(image_repo), fg='green')


def check_config(config_file):
    filename = os.path.expanduser(config_file)
    filesize = os.path.getsize(filename)
    # If file is empty create config
    if filesize == 0:
        write_config()

    with open(filename) as cfg:
        image_repo = cfg.read().strip('\n')
    return image_repo


def copy_to_docker(filename, container_name):
    local_path = str(Path(cwd / filename))
    os.system(f'docker cp "{local_path}" {container_name}:"{airflow_home}/{filename}"')


def dir_exist(directory):
    return os.path.exists(directory)


def prefix(directory):
    last_path = os.path.split(directory)
    container_prefix = last_path[1]
    return container_prefix


def ask_user(question):
    check = str(input(question + "(Y/N): ")).lower().strip()
    try:
        if check[0] == 'y':
            return True
        elif check[0] == 'n':
            return False
        else:
            print('Invalid Input')
            return ask_user(question)
    except Exception as error:
        print("Please enter valid inputs")
        print(error)
        return ask_user(question)


@click.group()
def main():
    """
        Spatialedge Airflow Development CLI \n
    """
    pass


@main.command()
@click.option(
    '-iv',
    '--image-version',
    help='Specify Cloud Composer Airflow version',
    type=str,
    default=default_composer_version,
)
@click.option(
    '--config-file',
    '-c',
    type=click.Path(),
    default='~/.dockflow/dockflow.cfg',
)
@click.option(
    '--gcp-creds',
    '-creds',
    type=click.Path(),
    default='~/.dockflow/gcp_credentials.json'
)
@click.option(
    '--network',
    '-net',
    type=str,
    default='dockflow'
)
def start(image_version, config_file, gcp_creds, network):
    """
        Start Airflow instance
    """
    volumes = {}

    if docker_client.containers.list(filters={'name': (prefix(cwd) + "-airflow"), 'status': 'created'}):
        click.secho('It seems that {}-airflow failed to start'.format(prefix(cwd)), fg='red')
        click.secho('Removing container and attempting to start', fg='red')
        container = docker_client.containers.get(prefix(cwd) + "-airflow")
        container.remove()

    click.secho('Checking if container {}-airflow is already running'.format(prefix(cwd)), fg='green')
    if docker_client.containers.list(filters={'name': (prefix(cwd) + "-airflow"), 'status': 'running'}):
        click.secho("Container {}-airflow already running".format(prefix(cwd)), fg='green')
    elif docker_client.containers.list(filters={'name': (prefix(cwd) + "-airflow"), 'status': 'exited'}):
        container = docker_client.containers.get(prefix(cwd) + "-airflow")
        container.start()
        if dir_exist(cwd / "airflow.db"):
            copy_to_docker("airflow.db", "{}-airflow".format(prefix(cwd)))
            container.exec_run(f"chown airflow {str(airflow_home)}/airflow.db", user='root')
        click.secho("Container {}-airflow started".format(prefix(cwd)), fg='green', bold=True)

    else:
        click.secho('Starting container {}-airflow:{} creation'.format(prefix(cwd), image_version.strip('=')),
                    fg='green')

        version = image_version.strip('=')
        image_repo = check_config(config_file)
        click.secho("Checking if image is up-to-date...", fg='green')
        os.system("docker pull {}:{}".format(image_repo, version))
        click.secho('Checking if "dags" folder exists', fg='green')
        if dir_exist(cwd / "dags/"):
            mount_loc = f'{airflow_home}/dags/'
            volumes[cwd / 'dags/'] = {'bind': mount_loc, 'mode': 'rw'}
            click.secho(f'"dags" folder mounted to: {mount_loc}', fg='green')

            click.secho('Checking if "scripts" directory exists and mount if exist', fg='green')
            if dir_exist(cwd / "scripts/"):
                mount_loc = f'{airflow_home}/scripts/'
                volumes[cwd / 'scripts/'] = {'bind': mount_loc, 'mode': 'rw'}
                click.secho(f'"scripts" directory mounted to {mount_loc}', fg='cyan')
            else:
                click.secho('"scripts" directory not found in: {} \n Not mounting'.format(cwd), fg='red')

            click.secho('Checking if "{}" network exists'.format(network), fg='cyan')
            network_handler(network)

            container = docker_client.containers.create(
                image_repo + ":" + version,
                ports={'8080/tcp': 8080,
                       },
                volumes=volumes,
                network=network,
                name=prefix(cwd) + '-airflow',
                environment={
                    'GOOGLE_APPLICATION_CREDENTIALS': '/usr/local/airflow/gcp_credentials.json'
                    },
            )
            click.secho('Container {}-airflow:{} created'.format(prefix(cwd), version), fg='green')

            click.secho('Check if GCP credentials exist and mount if exists', fg='green')
            creds = os.path.expanduser(gcp_creds)
            if dir_exist(creds):
                click.secho('Mounting GCP credentials: {}'.format(creds), fg='cyan')
                os.system(f"docker cp {creds}  {prefix(cwd)}-airflow:{str(airflow_home)}/gcp_credentials.json")
            else:
                click.secho('GCP Credential file {} not found, will not mount to container'.format(creds), fg='red')

            container.start()

            click.secho('Check if local airflow.db exist and copy if exist', fg='green')
            if dir_exist(cwd / "airflow.db"):
                copy_to_docker("airflow.db", "{}-airflow".format(prefix(cwd)))
                container.exec_run(f"chown airflow {str(airflow_home)}/airflow.db", user='root')
                click.secho('Local airflow.db mounted to container', fg='cyan')

            click.secho("Container {}-airflow:{} started".format(prefix(cwd), version), fg='green', bold=True)
        else:
            click.secho("DAGs directory not found in: {} \nAre you in the root directory of your project?".format(cwd),
                        fg='red', bold=True)


@main.command()
@click.option(
    '--rm',
    is_flag=True
)
def stop(rm):
    """
        Stop Airflow instance
    """
    if docker_client.containers.list(filters={'name': (prefix(cwd) + "-airflow")}):
        container = docker_client.containers.get(prefix(cwd) + "-airflow")
        click.secho('Persisting Airflow db', fg='green')
        os.system(f'docker cp "{prefix(cwd)}-airflow:{str(airflow_home)}/airflow.db" "{str(cwd)}/airflow.db"')
        click.secho('"airflow.db" persisted to {}/airflow.db'.format(cwd), fg='cyan')
        click.secho("Stopping {}-airflow...".format(prefix(cwd)), fg='red')
        container.stop()
        if rm:
            container.remove()
            click.secho("{}-airflow stopped and removed".format(prefix(cwd)), fg='red')
        else:
            click.secho("{}-airflow stopped".format(prefix(cwd)), fg='red')
    elif docker_client.containers.list(filters={'name': (prefix(cwd) + "-airflow"), 'status': 'exited'}) and rm:
        container = docker_client.containers.get(prefix(cwd) + "-airflow")
        container.remove()
        click.secho("{}-airflow removed".format(prefix(cwd)), fg='red')
    else:
        click.secho("Nothing to stop.", fg='red')


@main.command()
def refresh():
    """
        Run refresh/bundling scripts
    """
    container = docker_client.containers.get(prefix(cwd) + "-airflow")
    if dir_exist(cwd / "scripts/"):
        click.secho("Refreshing dags...", fg='green')
        for f in os.listdir(cwd / "scripts/"):
            container_path = airflow_home / "scripts" / f
            container.exec_run(f'python "{str(container_path)}"', user="airflow")
        click.secho("All DAGs refreshed", fg='green')
    else:
        click.secho("Either not project root directory or no 'scripts' folder present", fg='red')


@main.command()
def config():
    """
        Store container repo URL
    """
    write_config()


@main.command()
def reset():
    """
        Reset Airflow db
    """
    container = docker_client.containers.get(prefix(cwd) + "-airflow")
    if ask_user("Are you sure?"):
        click.secho("Resetting Airflow database...", fg='green')
        container.exec_run("airflow resetdb -y")
        click.secho("Restarting container...", fg='green')
        container.stop()
        container.start()
        click.secho("Airflow db reset completed", fg='green')


@main.command()
def dashboard():
    """
        Open Airflow in default browser
    """
    click.launch('http://localhost:8080')


@main.command()
@click.option(
    '-iv',
    '--image-version',
    help='Specify Cloud Composer Airflow version',
    type=str,
    default=default_composer_version,
)
@click.option(
    '--config-file',
    '-c',
    type=click.Path(),
    default='~/.dockflow/dockflow.cfg',
)
def test(image_version, config_file):
    """
        Run tests located in tests dir if test.sh exists
    """
    click.secho('Creating volumes for {}-test'.format(prefix(cwd)), fg='green', bold=True)

    volumes = {}
    version = image_version.strip('=')
    image_repo = check_config(config_file)

    click.secho('Checking if required directories (dags & tests) exist', fg='green')
    if dir_exist(cwd / "dags/") and dir_exist(cwd / "tests/"):
        click.secho('Mounting "dags" directory', fg='green')
        volumes[cwd / 'dags/'] = {'bind': str(airflow_home) + '/dags/', 'mode': 'rw'}
        click.secho('"dags" directory mounted', fg='cyan')

        click.secho('Mounting "tests" directory', fg='green')
        volumes[cwd / 'tests/'] = {'bind': str(airflow_home) + '/tests/', 'mode': 'rw'}
        click.secho('"tests" directory mounted', fg='cyan')

        click.secho('Checking if "scripts" directory exists and mount if exist', fg='green')
        if dir_exist(cwd / "scripts/"):
            volumes[cwd / 'scripts/'] = {'bind': str(airflow_home) + '/scripts/', 'mode': 'rw'}
            click.secho('"scripts" directory mounted', fg='cyan')
        else:
            click.secho('"scripts" directory not found in: {} \n Not mounting'.format(cwd), fg='red')

        click.secho('Creating {}-test'.format(prefix(cwd)), fg='green', bold=True)
        container = docker_client.containers.create(
            image_repo + ":" + version,
            volumes=volumes,
            name=prefix(cwd) + '-test',
        )

        click.secho('Checking if required scripts exist', fg='green')
        if dir_exist(cwd / "test.sh"):
            copy_to_docker("test.sh", "{}-test".format(prefix(cwd)))
            container.start()
            container.exec_run(f"chown airflow {str(airflow_home)}/test.sh", user='root')
            container.exec_run(f"chmod +x {str(airflow_home)}/test.sh", user='root')

            # Bundle configs
            if dir_exist(cwd / "scripts/"):
                click.secho("Refreshing DAGs...", fg='green')
                for f in os.listdir(cwd / "scripts/"):
                    container_path = airflow_home / "scripts" / f
                    container.exec_run(f'python "{str(container_path)}", user="airflow"')
                click.secho("All DAGs refreshed", fg='green')
            else:
                click.secho("Either not project root or no 'scripts' folder present in: {}".format(cwd), fg='red')

            click.secho("Executing test.sh to run tests", fg='green', bold=True)
            os.system("docker exec " + prefix(cwd) + "-test ./test.sh")
        else:
            click.secho("No test script found...", fg='red')
            click.secho("Ensure you are in the project root directory and `test.sh` exists", fg='red', bold=True)

        click.secho('Stopping and removing container: {}-test'.format(prefix(cwd)), fg='red')
        container.stop()
        container.remove()
        click.secho('Container {}-test stopped and removed'.format(prefix(cwd)), fg='red', bold=True)
    else:
        click.secho('Required directories not found in: {}'.format(cwd), fg='red', bold=True)


@main.command()
def requirements():
    """
    Create ide.requirements.txt
    """
    # Creates a file ide.requirements.txt in root dir of project matching current running container requirements
    if docker_client.containers.list(filters={'name': (prefix(cwd) + "-airflow"), 'status': 'running'}):
        os.system("docker exec -it -u airflow {}-airflow pip freeze > ide.requirements.txt".format(prefix(cwd)))
    else:
        click.secho('Could not find a running container. Ensure you are in the root directory of your project')
