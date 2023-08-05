from typing import List, Dict
from pathlib import Path
import json
from logging import Logger, getLogger, config as loggingConfig
from datetime import datetime
import traceback
from os import path, sep as separator

class rapydmain:
    def __init__(self, root_path: str):
        # setup fw directories
        self._root_dir_path: str = root_path
        self._config_dir_path: str = Path(self._root_dir_path, 'config')
        self._log_dir_path: str = Path(self._root_dir_path, 'log')

        # validate: required fw directories exist
        rapydmain.files_exists([
            {'path': self._root_dir_path, 'name': "'[root_path]/'"},
            {'path': self._config_dir_path, 'name': "'[root_path]/config/'"},
            {'path': self._log_dir_path, 'name': "'[root_path]/log/'"}
        ])

        # setup config
        self.config: dict = {}
        for config_path in self._config_dir_path.glob('**/*.json'):
            if not config_path.is_file():
                continue

            config_file_name = str(config_path).replace(str(self._config_dir_path), '')
            config_file_name = config_file_name.lstrip('/')
            config_route_name = config_file_name.replace('.json', '')
            with open(config_path, 'r') as f:
                self.config[config_route_name] = json.load(f)

        # validate: required fw config key
        rapydmain.config_key_exists(self.config, rapydmain._REQUIRED_FW_CONFIG_KEY)

        # setup app
        self._app_name = self.config['fw']['app']['name']
        self._message = self.config['fw']['message']

        # setup logger
        self.logger: Logger = None
        if rapydmain.eval_bool(self.config['fw']['logger']['logger_enables']):
            # validate: required logger config key
            rapydmain.config_key_exists(self.config, rapydmain._REQUIRED_LOGGER_CONFIG_KEY)

            # setup log file name
            self.config['logger']['handlers']['fileHandler']['filename'] = self.log_file_path()
            loggingConfig.dictConfig(self.config['logger'])
            self.logger = getLogger(self._app_name)

    def __enter__(self):
        self._infolog(self._message['begin'].format(self._app_name), self.config['fw']['logger']['output_begin_message_enables'])
        return self

    def __exit__(self, ex_type, ex_value, trace):
        if ex_type != None and ex_value != None and trace != None:
            self._errorlog(self._message['error'].format(self._app_name), self.config['fw']['logger']['output_error_message_enables'])
            self._errorlog(traceback.format_exception(ex_type, ex_value, trace), self.config['fw']['logger']['output_error_message_enables'])
            return False

        self._infolog(self._message['end'].format(self._app_name), self.config['fw']['logger']['output_end_message_enables'])
        return False

    def _infolog(self, message, enables):
        if self.logger == None or not rapydmain.eval_bool(enables):
            return
        self.logger.info(message)

    def _errorlog(self, message, enables):
        if self.logger == None or not rapydmain.eval_bool(enables):
            return
        self.logger.error(message)

    def log_file_path(self) -> str:
        return Path(
            self._log_dir_path,
            self.config['fw']['logger']['log_file_name_format'].format(
                self._escaped_app_name(),
                datetime.utcnow().strftime('%Y%m%d')
            ) + '.' + self.config['fw']['logger']['log_file_extension']
        )

    def _escaped_app_name(self) -> str:
        app_name = self._app_name
        app_name = app_name.replace(' ', '_')
        app_name = app_name.replace('/', '_')
        app_name = app_name.replace('\\', '_')
        return app_name

    @classmethod
    def files_exists(cls, rule: List[Dict]) -> bool:
        for rule_item in rule:
            if not path.exists(rule_item['path']):
                raise FileNotFoundError("dir {0} does not exists.".format(rule_item['name']))

        return True

    @classmethod
    def config_key_exists(cls, target: dict, rule: List[List], raise_exception: bool = True) -> bool:
        for rule_item in rule:
            dict_work = target
            for rule_column in rule_item:
                if rule_column not in dict_work:
                    if (raise_exception):
                        raise KeyError("Missing dict key" + "['" + "']['".join(rule_item) + "']")
                    return False
                dict_work = dict_work[rule_column]
        return True

    @classmethod
    def eval_bool(cls, config):
        return type(config) == bool and config

    _REQUIRED_FW_CONFIG_KEY = [
        ['fw'],
        ['fw', 'app'],
        ['fw', 'app', 'name'],
        ['fw', 'message'],
        ['fw', 'message', 'begin'],
        ['fw', 'message', 'end'],
        ['fw', 'message', 'error'],
        ['fw', 'logger'],
        ['fw', 'logger', 'logger_enables'],
        ['fw', 'logger', 'log_file_extension'],
        ['fw', 'logger', 'log_file_name_format'],
        ['fw', 'logger', 'output_begin_message_enables'],
        ['fw', 'logger', 'output_end_message_enables'],
        ['fw', 'logger', 'output_error_message_enables']
    ]

    _REQUIRED_LOGGER_CONFIG_KEY = [
        ['logger'],
        ['logger', 'handlers'],
        ['logger', 'handlers', 'fileHandler'],
    ]
