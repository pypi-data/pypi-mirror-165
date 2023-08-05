import logging
import logs.config_client_log
import argparse
import sys
import os
from Cryptodome.PublicKey import RSA
from PyQt5.QtWidgets import QApplication, QMessageBox

from common.variables import *
from common.errors import ServerError
from common.decos import log
from client.database import ClientDatabase
from client.transport import ClientTransport
from client.main_window import ClientMainWindow
from client.start_dialog import UserNameDialog

logger = logging.getLogger('client_dist')


# command line args parser
@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    parser.add_argument('-p', '--password', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name
    client_passwd = namespace.password

    if not 1023 < server_port < 65536:
        logger.critical(
            f'Attempt to start client with unavailable port number: {server_port}. '
            f'Should be in range 1024 - 65535. Client shutting down.')
        exit(1)

    return server_address, server_port, client_name, client_passwd


if __name__ == '__main__':
    # loading command line args
    server_address, server_port, client_name, client_passwd = arg_parser()

    # creating client's app
    client_app = QApplication(sys.argv)

    # if no client's name - ask for one
    start_dialog = UserNameDialog()
    if not client_name or not client_passwd:
        client_app.exec_()
        if start_dialog.ok_pressed:
            client_name = start_dialog.client_name.text()
            client_passwd = start_dialog.client_passwd.text()
            logger.debug(f'Using USERNAME = {client_name}, PASSWD = {client_passwd}.')
        else:
            exit(0)

    logger.info(
        f'A client started with: server address: {server_address} , '
        f'port: {server_port}, username: {client_name}')

    # loading keys from the file, if file doesn't exist - generate a new pair of keys
    dir_path = os.getcwd()
    key_file = os.path.join(dir_path, f'{client_name}.key')
    if not os.path.exists(key_file):
        keys = RSA.generate(2048, os.urandom)
        with open(key_file, 'wb') as key:
            key.write(keys.export_key())
    else:
        with open(key_file, 'rb') as key:
            keys = RSA.import_key(key.read())

    logger.debug("Keys successfully loaded.")

    # db initialization
    database = ClientDatabase(client_name)

    # creating transport and starting trasport process
    try:
        transport = ClientTransport(
            server_port,
            server_address,
            database,
            client_name,
            client_passwd,
            keys)
        logger.debug("Transport ready.")
    except ServerError as error:
        message = QMessageBox()
        message.critical(start_dialog, 'Serer error', error.text)
        exit(1)
    transport.setDaemon(True)
    transport.start()

    del start_dialog
    # creating gui
    main_window = ClientMainWindow(database, transport, keys)
    main_window.make_connection(transport)
    main_window.setWindowTitle(f'Chat alpha release - {client_name}')
    client_app.exec_()

    # if gui is down - closing transport
    transport.transport_shutdown()
    transport.join()
