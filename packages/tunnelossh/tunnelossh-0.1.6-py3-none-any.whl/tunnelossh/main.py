from sshtunnel import SSHTunnelForwarder
from os import getenv, getcwd
from urllib.parse import quote
from dotenv import load_dotenv, find_dotenv


class SSHTunnel(object):

    def __init__(self, host, remote_port, local_port):
        self.env = getenv('ENV')
        self.__load_env()
        self.hosts = {
            'dev': {
                'host': getenv('DEV_SSH_HOST_NAME'),
                'user': getenv('DEV_SSH_HOST_USER'),
                'password': quote(getenv('DEV_SSH_HOST_PASS'))
            },
            'sites': {
                'host': getenv('SITES_SSH_HOST_NAME'),
                'user': getenv('SITES_SSH_HOST_USER'),
                'password': quote(getenv('SITES_SSH_HOST_PASS'))
            },
            'siga_ser': {
                'host': getenv('SIGA-SER_SSH_HOST_NAME'),
                'user': getenv('SIGA-SER_SSH_HOST_USER'),
                'password': quote(getenv('SIGA-SER_SSH_HOST_PASS'))
            }
        }
        self.host = self.hosts[host]
        self.remote_port = remote_port
        self.local_port = local_port

    def __load_env(self):
        if self.env != 'production':
            env_file = getcwd() + '/.env'
            load_dotenv(env_file)

    def __call__(self, function, remote='0.0.0.0', *args, **kwargs):

        def inner(*args, **kwargs):

            if self.env != 'production':
                server = SSHTunnelForwarder(
                    self.host['host'],
                    ssh_username=self.host['user'],
                    ssh_password=self.host['password'],
                    remote_bind_address=(remote, self.remote_port),
                    local_bind_address=('127.0.0.1', self.local_port)
                )

                server.start()

                result = function(*args, **kwargs)

                server.stop()

            else:
                result = function(*args, **kwargs)

            return result
        return inner