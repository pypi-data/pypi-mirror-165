import os
import sys
import yaml
import tempfile
import threading
import subprocess
from colorama import Fore
from jinja2 import Template
from contextlib import contextmanager

def red(message):
    return Fore.RED + message + Fore.RESET


def green(message):
    return Fore.GREEN + message + Fore.RESET


def yellow(message):
    return Fore.YELLOW + message + Fore.RESET


class RemoteCommandException(Exception):
    '''command process return code != 0'''


class CommandException(Exception):
    '''command process return code != 0'''


class RemoteCommandThread(threading.Thread):
    def __init__(self, method, host, command):
        threading.Thread.__init__(self)
        self.method = method
        self.host = host
        self.command = command
        self.result = None


    def run(self):
        self.result = self.method(self.host, self.command)


class Director:
    config = None
    pool = None
    verbose = 2

    DEBUG = 3
    INFO = 2
    WARN = 1
    ERROR = 0

    def __init__(self, configuration_file, verbose):
        self.verbose = verbose
        self.loadenv()

        if os.getenv('CONFIG_BASE_PATH'):
            configuration_file = os.getenv('CONFIG_BASE_PATH') + '/' + configuration_file

        if not os.path.exists(configuration_file):
            self.log('Unable to open configuration file: ' + configuration_file, self.ERROR)
            sys.exit()

        config = { 'hosts': [], 'parallel': False, 'warn_only': False }
        f = open(configuration_file, 'r')
        self.config = dict_merge(config, yaml.safe_load(f))

        if os.getenv('SSH_USER'):
            self.config['ssh_user'] = os.getenv('SSH_USER')

        if os.getenv('USE_SUDO'):
            if 'yes' == os.getenv('USE_SUDO'):
                self.config['use_sudo'] = True
            else:
                self.config['use_sudo'] = False

        self.config['config_base_path'] = os.path.dirname(configuration_file)
        self.hosts = self.config['hosts']

        f.close()

    def loadenv(self, env_path=None):
        cwd = os.getcwd()
        f = None

        if None == env_path:
            env_path = cwd + '/.env'

        if not os.path.exists(env_path):
            self.log('Environment file %s does not exist' % env_path, self.WARN)
            return
        
        self.log('Loading environment from %s' % (env_path), self.DEBUG)
        f = open(env_path, 'r')

        line = f.readline()

        while line != '':
            [ key, val ] = line.strip().split('=')
            os.environ[key] = val
            line = f.readline()
        
        f.close()


    def abort(self, message):
        self.log(red(message), self.ERROR)
        sys.exit(1)


    def remote_command_as(self, command, user, wd='.', stdout_only = True):
        if self.config['use_sudo']:
            return self.remote_command('sudo su - %s -c \'cd %s && %s\'' % (user, wd, command), stdout_only)
        
        return self.remote_command('cd %s && %s' % (wd, command), stdout_only)


    def remote_command(self, command, stdout_only = True, print_error = True):
        threads = []
        results = []

        for host in self.hosts:
            if(self.config['parallel'] == True):
                t = RemoteCommandThread(self.client_remote_command, host, command)
                threads.append(t)
                t.start()
            else:
                r = self.client_remote_command(host, command)

                if type(r) is RemoteCommandException:
                    if(print_error == True):
                        self.log(str(r), self.ERROR)

                    raise RemoteCommandException(str(r))

                if(stdout_only == True):
                    results.append(r[0])
                else:
                    results.append(r)

                self.log(r[0], self.DEBUG)
        
        for t in threads:
            t.join()

        for t in threads:
            if type(t.result) is RemoteCommandException:
                if(print_error == True):
                    self.log(str(t.result), self.ERROR)

                raise RemoteCommandException(str(t.result))
            
            if(stdout_only == True):    
                results.append(t.result[0])
            else:
                results.append(t.result)
            
            self.log(t.result[0], self.DEBUG)

        return results
    

    def local_command(self, command, stdout_only=False, quiet=False):
        self.log('Local > ' + command, self.DEBUG)
        popen = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdoutdata, stderrdata = popen.communicate()

        if stdoutdata != None:
            stdoutdata = stdoutdata.decode('utf-8')
        else:
            stdoutdata = ''

        if stderrdata != None:
            stderrdata = stderrdata.decode('utf-8')
        else:
            stderrdata = ''

        result = [ stdoutdata, stderrdata, popen.returncode ]

        if 0 != result[2]:
            if(self.config['warn_only'] == True):
                if False == quiet:
                    self.log(result[1], self.WARN)
                return result
            else:
                if False == quiet:
                    self.log(result[1], self.ERROR)
                raise CommandException(result[1])

        if(True == stdout_only):
            return result[0]

        return result


    def client_remote_command(self, host, command):
        self.log(host + ': Executing ' + command, self.DEBUG)

        prepend = ''

        if 'env' in self.config:
            for var in self.config['env']:
                prepend += 'export ' + var + '=' + self.config['env'][var] + '; '

        command = prepend + command

        try:
            result = self.local_command('ssh ' + host + ' "' + command + '"', False, True)
        except CommandException as ce:
            return RemoteCommandException('Remote command error: ' + str(ce))

        if(result[2] != 0):

            if(self.config['warn_only'] == True):
                self.log(result[1], self.WARN)

                return result
            else:
                return RemoteCommandException('Remote command error: ' + result[1])

        return result

    
    def download(self, source, destination):
        for h in self.hosts:
            self.log(h + ': Downloading ' + destination + ' < ' + source, self.DEBUG)
            self.local_command('scp %s:%s %s' % (h, source, destination))

    
    def upload(self, source, destination):
        for host in self.hosts:
            self.log(host + ': Uploading ' + source + ' > ' + destination, self.DEBUG)
            self.local_command('scp %s %s:%s' % (source, host, destination))


    def upload_template(self, source, destination, params):
        data = ''
        with open(source) as f:
            t = Template(f.read())
            data = t.render(params)

        tmp_name = ''

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_name = tmp.name
            tmp.write(bytes(data, 'utf-8'))

        self.log('Uploading ' + source + ' > ' + destination, self.DEBUG)
        self.upload(tmp_name, destination)

    
    def remote_dir_exists(self, dir):
        try:
            self.remote_command('[[ -d ' + dir + ' ]]', stdout_only = False, print_error = False)
        except RemoteCommandException:
            return False

        return True
    
    
    def remote_file_exists(self, file):
        try:
            self.remote_command('[[ -f ' + file + ' ]]', stdout_only = False, print_error = False)
        except RemoteCommandException:
            return False
        
        return True
        
    
    def rm(self, p, recursive=True):
        if recursive:
            self.remote_command('rm -rf ' + p)
        else:
            self.remote_command('rm ' + p)


    def log(self, message, level):
        if(type(message) == bytes):
            message = message.decode('utf-8')

        if message == '':
            return

        if level <= self.verbose:
            if level == 0:
                print(red(message))
            if level == 1:
                print(yellow(message))
            if level == 2:
                print(green(message))
            if level == 3:
                print(message)


    @contextmanager
    def settings(self, **kwargs):
        original_config = self.config
        original_hosts = self.hosts
        self.config = dict(original_config)

        for name, value in kwargs.items():
            if name == 'hosts':
                self.hosts = value
                continue

            self.config[name] = value

        yield self.config
        self.config = original_config
        self.hosts = original_hosts


def dict_merge(x, y):
    z = x.copy()
    z.update(y)
    return z
