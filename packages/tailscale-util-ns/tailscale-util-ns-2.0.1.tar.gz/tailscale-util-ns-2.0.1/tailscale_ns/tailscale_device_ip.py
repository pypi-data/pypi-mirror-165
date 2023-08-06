import json
import os
import jmespath
import sys
from tailscale_ns.load import load_ts_config


class TailScaleDeviceIp:

    def __init__(self):
        load_ts_config()
        self.prepare()

    def log(self, message: str):
        print('[tailscale-util-ns] ' + message)

    def value_at_json_path(self, json, path: str):
        expression = jmespath.compile(path)
        return expression.search(json)

    def tailscale_path(self):
        if sys.platform == 'darwin':
            path = os.getenv('TAILSCALE_PATH', default='/Applications/Tailscale.app/Contents/MacOS/Tailscale')
            if os.path.exists(path):
                return path
            else:
                raise RuntimeError('Please set `TAILSCALE_PATH` in environment variable. \n '
                                   'Example: export TAILSCALE_PATH=/Applications/Tailscale.app/Contents/MacOS/Tailscale')
        else:
            return 'tailscale'

    def is_stopped(self):
        results = self.get_status_details()
        jpath = "BackendState"
        status = self.value_at_json_path(results, jpath)
        value = True if str(status).lower() == 'stopped' else False
        self.log('Tailscale State is ' + status)
        return value

    def needs_login(self):
        results = self.get_status_details()
        jpath = "BackendState"
        status = self.value_at_json_path(results, jpath)
        value = True if str(status).lower() == 'needslogin' else False
        self.log('Tailscale State is ' + status)
        return value

    def auth_url(self):
        auth_url = None
        results = self.get_status_details()
        jpath = "BackendState"
        status = self.value_at_json_path(results, jpath)
        value = True if str(status).lower() == 'needslogin' else False
        if value:
            jpath = "AuthURL"
            auth_url = self.value_at_json_path(results, jpath)
            self.log('Tailscale Auth URL is ' + auth_url)
        else:
            self.log('Tailscale is already logged in with user')
        return auth_url

    def up(self):
        command = f"{self.tailscale_path()} up"
        self.log('Executing command: ' + command)
        os.popen(command).read()

    def down(self):
        command = f"{self.tailscale_path()} down"
        self.log('Executing command: ' + command)
        os.popen(command).read()

    def get_status_details(self):
        command = f"{self.tailscale_path()} status --json"
        self.log('Executing command: ' + command)
        output = os.popen(command).read()
        return json.loads(output)

    def get_ip_for_all_devices(self):
        results = self.get_status_details()
        jpath = "Peer.*.{device: HostName,ip: TailscaleIPs[0]}]"
        return self.value_at_json_path(results, jpath)

    def get_ip_for_device(self, device_name: str):
        results = self.get_status_details()
        jpath = "Peer.{device:*}.device[?HostName==`" + device_name + "`].TailscaleIPs | [0] | [0]"
        value = self.value_at_json_path(results, jpath)
        self.log('IP Address for device `' + device_name + '` is ' + value)
        return value

    def get_ip_for_dns(self, dns_name: str):
        self.prepare()
        command = f"{self.tailscale_path()} ip -4 {dns_name}"
        self.log('Executing command: ' + command)
        output = os.popen(command).read()
        return output.strip()

    def prepare(self):
        if self.needs_login():
            self.login_using_auth_key()
        elif self.is_stopped():
            self.up()
            self.is_stopped()

    def login_using_auth_key(self):
        auth_key = os.getenv('tskey', None)
        if auth_key is None:
            raise Exception('`tskey` is missing in tailscale.ini file')

        advertise_tags = os.getenv('advertise-tags', None)

        command = f"{self.tailscale_path()} up --authkey {auth_key} --accept-routes=false"
        if advertise_tags is not None:
            command = f"{command} --advertise-tags={advertise_tags}"
        self.log('Executing command: ' + command)
        os.popen(command).read()
