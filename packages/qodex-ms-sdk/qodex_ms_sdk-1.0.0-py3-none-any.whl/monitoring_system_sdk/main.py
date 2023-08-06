import traceback

from monitoring_system_sdk import mixins


class MonitoringSystemWorker(mixins.UrlWorker, mixins.AuthMe,
                             mixins.MethodsHandler):
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.ms_auth_username = username
        self.ms_auth_password = password
        self.auth_url = self.get_full_url('token')
        self.token = self.get_token()
        self.ping_all_url = self.get_full_url('check_all_apps_availability')
        self.get_all_apps_url = self.get_full_url('get_all_gravities')
        self.get_deep_analyze_url = self.get_full_url('deep_analyze')
        self.reboot_core_pc_ulr = self.get_full_url('reboot_server')
        self.restart_ar_url = self.get_full_url('restart_ar')
        self.turn_off_cm_url = self.get_full_url('turn_off_cm')
        self.update_gravity_url = self.get_full_url('update_gravity')

    def get_global_deep_analyze(self, app_dicts: list):
        result = {}
        for app in app_dicts:
            if not app:
                continue
            try:
                result[app['name']] = self.get_deep_analyze(app['id']).json()
            except:
                result[app['name']] = traceback.format_exc()
        return result

