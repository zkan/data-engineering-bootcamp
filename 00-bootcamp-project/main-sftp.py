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

DATA_FOLDER = "data"

# โค้ดด้านล่างจะเป็นการโหลดไฟล์ orders.csv ซึ่งเป็นข้อมูล orders
# ให้แก้โค้ดด้านล่างให้ไปโหลดไฟล์ข้อมูล products และ promos แทน
files = [
    "products.csv",
    "promos.csv",
]
with pysftp.Connection(host, username=username, password=password, port=port, cnopts=cnopts) as sftp:
    for f in files:
        sftp.get(f, f"{DATA_FOLDER}/{f}")
        print(f"Finished downloading: {f}")