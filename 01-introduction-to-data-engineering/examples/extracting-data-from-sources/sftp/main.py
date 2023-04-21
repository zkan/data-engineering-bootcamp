import configparser

import pysftp


parser = configparser.ConfigParser()
parser.read("pipeline.conf")
username = parser.get("sftp_config", "username")
password = parser.get("sftp_config", "password")
host = parser.get("sftp_config", "host")
port = parser.getint("sftp_config", "port")


# Security risk! Don't do this on production
# You lose a protection against Man-in-the-middle attacks
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
with pysftp.Connection(host, username=username, password=password, port=port, cnopts=cnopts) as sftp:
    sftp.get("promos.csv")
    # sftp.put("some.txt", "uploaded.txt")