import configparser
import os

config = configparser.ConfigParser()
config.read('src/config/settings.ini')

c_data = config['settings']
token = c_data['token']

admin_ids = [int(i) for i in c_data['admins_ids'].split(',')]

database_path = 'src/database.db'

web_server_host = c_data['web_server_host']
web_server_port = 8000
webhook_url = web_server_host + '/hook'

admin_login = c_data['admin_login']
admin_password = c_data['admin_password']
