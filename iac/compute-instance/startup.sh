curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

sudo sh -eux <<EOF
# Install newuidmap & newgidmap binaries
apt-get install -y uidmap
EOF
dockerd-rootless-setuptool.sh install

sudo apt update
sudo apt -y install tmux
git clone https://github.com/zkan/data-engineering-bootcamp.git