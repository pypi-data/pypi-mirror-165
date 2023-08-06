import os
import time
import pytz
import base64
import boto3
import logging
import subprocess
import json
import yaml
import shutil
import asyncio
from datetime import datetime
from github import Github
from botocore.exceptions import WaiterError
logging.basicConfig(level=logging.INFO)


class EC2Manager:
    def __init__(self, **kwargs):
        # needed envs
        self._repo = os.environ.get('REPO', kwargs.get('repo'))
        self._github_user = os.environ.get('GITHUB_USERNAME', kwargs.get('github_username'))
        self._github_token = os.environ.get('GITHUB_TOKEN', kwargs.get('github_token'))

        # optional envs
        self._config_file = os.environ.get('EC2_MANAGER_CONFIG', kwargs.get('config', 'config.yaml'))
        self._commit = os.environ.get('COMMIT', 'master')
        self._terraform_directory = os.environ.get(
            'TERRAFORM_DIRECTORY', os.path.join(os.getcwd(), 'terraform')
        )
        self._template_directory = os.path.join(os.path.dirname(__file__), 'template')
        self._repo_url = (
            f'https://{self._github_user}:{self._github_token}@github.com/{self._github_user}/{self._repo}.git'
        )
        self._max_attempts = int(os.environ.get('MAX_TIMEOUT', 600))

        self._github_client = Github(self._github_token)

        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(level=logging.INFO)

        # only when initialize with a config
        if self._config_file:
            # internal variables
            self._config = self._get_config()
            self._aws_default_region = self._config['aws_region']
            self._type = self._config['type']
            self._vpc_name = self._config['vpc_name']
            self._public_subnet_cidr = self._config['public_subnet_cidr']
            self._expose_docker_daemons = int(self._config.get('expose_docker_daemons'))
            self._private_subnet_cidr = self._config.get('private_subnet_cidr', '')
            self._instance_names = self._get_instance_names()
            self._instance_repo_updates = self._get_instance_repo_updates()

            self._aws_session = boto3.Session(region_name=self._aws_default_region)
            self._ssm_client = self._aws_session.client('ssm')
            self._ec2_client = self._aws_session.client('ec2')
            self._s3_client = self._aws_session.client('s3')

            account_number = self._aws_session.client('sts').get_caller_identity().get('Account')
            if not account_number:
                raise ValueError(
                    'Please set the name of your terraform backend bucket with the AWS_BACKEND_BUCKET '
                    'environment variable.'
                )
            self._aws_backend_bucket = os.environ.get('AWS_BACKEND_BUCKET', f'{account_number}-terraform-state')
            self._aws_backend_key = f'{self._type}.tfstate'

    def _get_config(self):
        """
        Gets the config data.

        :returns: A dictionary of file data.
        :rtype: dict
        """
        with open(self._config_file, 'r') as config_file:
            return yaml.safe_load(config_file)

    @staticmethod
    def _get_json_from_s3(bucket_name, file_name):
        """
        Gets a json file from an s3 bucket.

        :param str bucket_name: The s3 bucket name.
        :param str file_name: The s3 file object name.
        :returns: A dictionary of file data.
        :rtype: dict
        """
        s3 = boto3.resource('s3')
        content_object = s3.Object(bucket_name, file_name)
        file_content = content_object.get()['Body'].read().decode('utf-8')
        return json.loads(file_content)

    @staticmethod
    def _get_encoded_envs(encoded_string):
        """
        Gets environment variables from the given encoded string.

        :param str encoded_string: A env file encoded as a base64 string.
        :returns: A dictionary of environment variables.
        :rtype: dict
        """
        # decode the env file
        env_file_contents = base64.b64decode(encoded_string).decode('utf-8')
        return {line.split('=')[0]: line.split('=')[1].strip("'").strip('"') for line in env_file_contents.split('\n')
                if '=' in line}

    @staticmethod
    def encode_string(string):
        """
        Encodes string to base64 string
        """
        return str(base64.b64encode(string.encode('utf-8'))).strip("b'").strip("'")

    def _get_working_directory(self, working_directory):
        """
        Gets the working directory relative to the repo

        :returns: Working directory path.
        :rtype: str
        """
        path = os.path.normpath(os.path.join(self._repo, working_directory)).replace(os.path.sep, '/')
        return f'./{path}'

    def _get_instance_id(self, name, try_once=False, attempts=0):
        """
        Get the instance id by tag name:

        :param str name: The name of the bot.
        :param bool name: Whether to make one attempt to get the instance id.
        :param int attempts: The number of attempts made to get the instance id.
        :returns: Instance id.
        :rtype: str
        """
        if not try_once:
            self._logger.info(f"{name} has been trying to get its instance id for {attempts} secs...")
        instance_id = self.list_instances().get(name, {}).get('instance_id')
        if not instance_id and attempts < self._max_attempts and not try_once:
            time.sleep(5)
            instance_id = self._get_instance_id(name, try_once, attempts + 5)
        return instance_id

    def _get_terraform_outputs(self):
        """
        Gets the outputs from terraform state.

        :return dict: A dictionary of output values.
        """
        state_file_path = os.path.join(self._terraform_directory, '.terraform', 'terraform.tfstate')

        if os.path.exists(state_file_path):
            with open(state_file_path, 'r') as state_file:
                data = json.load(state_file)
                config = data.get('backend', {}).get('config', {})
                bucket_name = config.get('bucket')
                file_name = config.get('key')
                if bucket_name and file_name:
                    state_data = self._get_json_from_s3(bucket_name, file_name)
                    return state_data.get('outputs', {})
        return {}

    def _get_instance_names(self):
        """
        Gets a list of bot names whose instances should be created.

        :return list[str]: A list of bot names.
        """
        instances = self._config.get('instances') or {}
        return list(instances.keys())

    def _get_instance_repo_updates(self):
        """
        Gets a list of bot names whose repos should be updated.

        :return list[str]: A list of bot names.
        """
        instances = self._config.get('instances') or {}
        return [key for key, value in instances.items() if value.get('update')]

    def _get_commit_time(self):
        """
        Gets the time of the commit.

        :return datetime: A UTC datetime object.
        """
        if self._commit not in ['master', 'main']:
            repo = self.get_repo()
            commit_time = repo.get_commit(self._commit).last_modified
            return datetime.strptime(commit_time, '%a, %d %b %Y %H:%M:%S %Z').astimezone(pytz.UTC)

    def _get_instance_data(self):
        """
        Gets all the instance's environment variables.

        :return dict: A dictionary of bot names and their environment variables.
        """
        instances = self._config['instances']
        default_ports = [{'from_port': 2375, 'to_port': 2375, 'protocol': 'tcp'}] if self._expose_docker_daemons else []

        return {name: {
            'commands': {
                'start': instances[name].get('commands', {}).get('start', 'docker-compose up --detach'),
                'stop': instances[name].get('commands', {}).get('stop', 'docker-compose down')
            },
            'volume_size': instances[name].get('volume_size', 8),
            'instance_type': instances[name].get('instance_type', 't4g.nano'),
            'working_directory': instances[name].get('working_directory', 'compose'),
            'ports': instances[name].get('ports', []) + default_ports,
            'envs': {
                'NAME': name,
                'REPO': self._repo,
                'COMMIT': self._commit,
                'GITHUB_USERNAME': self._github_user,
                'GITHUB_TOKEN': self._github_token,
                **instances[name].get('envs', {}),
                **self._get_encoded_envs(os.environ.get(instances[name].get('encoded_env_file_variable', ''), ''))
            }
        } for name in self._instance_repo_updates}

    async def _status_check(self, name, status):
        """
        Check for the given status on the ec2 instance by id.

        :param str name: The name of the bot.
        :param str status: The name of the ec2 instance status check to wait for.
        """
        self._logger.info(f"{name} instance {self._instance_id} is checking if its status is {status.split('_')[-1]}")
        if self._instance_id:
            try:
                waiter = self._ec2_client.get_waiter(status)
                waiter.wait(InstanceIds=[self._instance_id])
                self._logger.info(f"{name} instance {self._instance_id} is {status.split('_')[-1]}")
            except WaiterError:
                logging.error(f"{name} status check of instance {self._instance_id} failed")
        else:
            self._logger.info(f"{name} instance does not exist")

    def _create_backend_bucket(self):
        """
        Creates terraform backend bucket if it doesn't exist.
        """
        buckets = [item['Name'] for item in self._s3_client.list_buckets().get('Buckets', [])]
        if self._aws_backend_bucket not in buckets:
            self._logger.info(f'Creating Terraform backend...')
            self._s3_client.create_bucket(
                ACL='private',
                Bucket=self._aws_backend_bucket
            )
            waiter = self._s3_client.get_waiter('bucket_exists')
            waiter.wait(Bucket=self._aws_backend_bucket)

    def _init_terraform(self):
        """
        Runs terraform init.
        """
        self._create_backend_bucket()
        self._logger.info(f'Initializing Terraform backend...')
        process = subprocess.run([
            'terraform',
            'init',
            f'-backend-config="key={self._aws_backend_key}"',
            f'-backend-config="bucket={self._aws_backend_bucket}"',
            '-reconfigure'
        ],
            env=os.environ,
            cwd=self._terraform_directory
        )
        if process.returncode != 0:
            raise RuntimeError('Failed to initialize terraform')

    def _apply_terraform(self):
        """
        Runs terraform apply that creates the ec2 instances.
        """
        outputs = self._get_terraform_outputs()
        if outputs.get('instance_names', {}).get('value') != self._instance_names:
            self._logger.info(f'Terraform instances...')
            instances = self.encode_string(json.dumps(self._get_instance_data()))

            process = subprocess.run(
                [
                    'terraform',
                    'apply',
                    '-auto-approve',
                    '-var',
                    f'type={self._type}',
                    '-var',
                    f'vpc_name={self._vpc_name}',
                    '-var',
                    f'public_subnet_cidr={self._public_subnet_cidr}',
                    '-var',
                    f'private_subnet_cidr={self._private_subnet_cidr}',
                    '-var',
                    f'aws_region={self._aws_default_region}',
                    '-var',
                    f'expose_docker_daemons={self._expose_docker_daemons}',
                    '-var',
                    f'instances={instances}'
                ],
                env=os.environ,
                cwd=self._terraform_directory
            )
            if process.returncode != 0:
                raise RuntimeError('Failed to apply terraform')

    async def _await_instances(self):
        """
        Waits till all ec2 instances have a status of ok.
        """
        tasks = []
        for name in self._get_instance_names():
            self._instance_id = self._get_instance_id(name)
            tasks.append(asyncio.create_task(self._status_check(name, 'instance_status_ok')))

        # wait for the task to finish
        for task in tasks:
            await task

    def get_repo(self):
        """
        Gets the repo instance.
        """
        return self._github_client.get_repo(full_name_or_id=f'{self._github_user}/{self._repo}')

    def list_instances(self):
        """
        List all ec2 instances.

        :return dict: A dictionary of data for all instances in the region.
        """
        instances = {}
        response = self._ec2_client.describe_instances()
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                if instance['State']['Name'] == 'running':
                    tags = instance.get('Tags', [])
                    for tag in tags:
                        if tag['Key'] == 'Name':
                            instances[tag['Value']] = {
                                'instance_id': instance.get('InstanceId'),
                                'private_ip_address': instance.get('PrivateIpAddress'),
                                'public_ip_address': instance.get('PublicIpAddress'),
                            }
        return instances

    def run_command(self, name, commands, print_output=True):
        """
        Runs a command on the ec2 instance and waits for the response.

        :param str name: The name of the instance.
        :param list[str] commands: A list of commands.
        :param bool print_output: Whether or to print the stdout.
        :return str: The stdout.
        """
        instance_id = self._get_instance_id(name, try_once=True)
        if instance_id:
            error = False
            # run the command
            response = self._ssm_client.send_command(
                InstanceIds=[instance_id],
                DocumentName='AWS-RunShellScript',
                Parameters={'commands': commands}
            )
            command_id = response['Command']['CommandId']

            # wait for the command to finish
            try:
                waiter = self._ssm_client.get_waiter('command_executed')
                waiter.wait(
                    CommandId=command_id,
                    InstanceId=instance_id,
                    WaiterConfig={
                        'Delay': 10,
                        'MaxAttempts': 120
                    }
                )
            except Exception as waiter_error:
                error = waiter_error

            # get the command response
            command_response = self._ssm_client.get_command_invocation(
                CommandId=command_id,
                InstanceId=instance_id
            )

            # get the standard output and standard errors
            stdout = command_response.get('StandardOutputContent')
            stderr = command_response.get('StandardErrorContent')

            if error:
                raise RuntimeError(str(stdout) + str(stderr) + str(error))
            elif print_output:
                print(str(stdout) + str(stderr))

            return stdout
        else:
            raise RuntimeError(f'instance {instance_id} does not exist')

    def create_instances(self):
        """
        Creates the ec2 instances.
        """
        existing_instances = self.list_instances().keys()
        # if not all instances that need to be updated exist run terraform
        if not all(instance_name in existing_instances for instance_name in self._instance_repo_updates):
            self._init_terraform()
            self._apply_terraform()

        # wait for each instance status to be ok
        asyncio.run(self._await_instances())

    async def _update_repo(self, name):
        """
        Updates a single instance repo.
        """
        if self._repo not in self.run_command(name, ['ls'], print_output=False):
            self._logger.info(f'{name} cloning {self._repo}')
            self.run_command(name, [f'git clone {self._repo_url}'])

        self._logger.info(f'{name} checking out {self._commit}')
        self.run_command(name, [
            f'cd ./{self._repo}',
            'git fetch',
            'git pull',
            f'git -c advice.detachedHead=false checkout {self._commit}'
        ])

    async def _stop(self, name, data):
        """
        Stops a single docker container if it is already running.
        """
        # check if docker is already running
        result = list(filter(None, self.run_command(name, ['docker ps'], print_output=False).split('\n')))
        if len(result) > 1:
            # then compose down
            self._logger.info(f'{name} stopping...')
            working_directory = self._get_working_directory(data['working_directory'])
            self.run_command(name, [
                f'cd {working_directory} ',
                data['commands']['stop']
            ])

    async def _start(self, name, data):
        """
        Runs start command on a single instance.
        """
        self._logger.info(f'{name} starting...')
        working_directory = self._get_working_directory(data['working_directory'])
        self.run_command(name, [
            f'cd {working_directory} ',
            *[f'export {key}={value}' for key, value in data['envs'].items()],
            data['commands']['start'],
            *[f'unset {key}' for key in data['envs'].keys()]
        ])

    async def update_repos(self):
        """
        Updates the code in the instance repos.
        """
        tasks = []
        for name in self._instance_repo_updates:
            tasks.append(asyncio.create_task(self._update_repo(name)))

        # wait for the tasks to finish
        for task in tasks:
            await task

    async def stop(self):
        """
        Runs stop if a docker container is already running.
        """
        tasks = []
        for name, data in self._get_instance_data().items():
            tasks.append(asyncio.create_task(self._stop(name, data)))

        # wait for the tasks to finish
        for task in tasks:
            await task

    async def start(self):
        """
        Runs start command on the instances.
        """
        tasks = []
        for name, data in self._get_instance_data().items():
            tasks.append(asyncio.create_task(self._start(name, data)))

        # wait for the tasks to finish
        for task in tasks:
            await task

    def init(self):
        """
        Initializes the project
        """
        destination = os.path.join(os.getcwd())
        if not os.path.exists(self._terraform_directory):
            shutil.copytree(
                src=self._template_directory,
                dst=destination,
                dirs_exist_ok=True
            )
            self._logger.info(f'Initialized project at "{destination}"')
        else:
            self._logger.info(f'Project is already initialized project at "{destination}"')

    def apply(self):
        """
        Apply according to the config.
        """
        self.create_instances()
        asyncio.run(self.update_repos())
        asyncio.run(self.stop())
        asyncio.run(self.start())
