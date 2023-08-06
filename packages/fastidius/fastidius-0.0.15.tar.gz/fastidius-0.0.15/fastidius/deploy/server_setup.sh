#!/bin/bash
set -euo pipefail
########################
### SCRIPT VARIABLES ###
########################

# NOTE: to run this script manually on a remote machine, you can use:
# ssh root@<ip-address> "bash -s" < .djengu/.production_toolbox/server_setup.sh

# Change this to any username you like
USERNAME=ubuntu


COPY_AUTHORIZED_KEYS_FROM_ROOT=true
####################
### SCRIPT LOGIC ###
####################
useradd --create-home --shell "/bin/bash" --groups sudo "${USERNAME}"
encrypted_root_pw="$(grep root /etc/shadow | cut --delimiter=: --fields=2)"
if [ "${encrypted_root_pw}" != "*" ]; then
    echo "${USERNAME}:${encrypted_root_pw}" | chpasswd --encrypted
    passwd --lock root
else
    passwd --delete "${USERNAME}"
fi
chage --lastday 0 "${USERNAME}"
home_directory="$(eval echo ~${USERNAME})"
mkdir --parents "${home_directory}/.ssh"
if [ "${COPY_AUTHORIZED_KEYS_FROM_ROOT}" = true ]; then
    cp /root/.ssh/authorized_keys "${home_directory}/.ssh"
fi
for pub_key in "${OTHER_PUBLIC_KEYS_TO_ADD[@]}"; do
    echo "${pub_key}" >> "${home_directory}/.ssh/authorized_keys"
done
chmod 0700 "${home_directory}/.ssh"
chmod 0600 "${home_directory}/.ssh/authorized_keys"
chown --recursive "${USERNAME}":"${USERNAME}" "${home_directory}/.ssh"
sed --in-place 's/^PermitRootLogin.*/PermitRootLogin prohibit-password/g' /etc/ssh/sshd_config
if sshd -t -q; then
    systemctl restart sshd
fi
ufw allow OpenSSH
ufw --force enable

################### Basic tools ################
apt-get update -y
apt-get install build-essential nodejs npm net-tools -y
apt-get install gnupg2 -y
npm install -g @quasar/cli



#################### Docker ####################
apt-get update -y &&
apt-get install apt-transport-https ca-certificates curl software-properties-common gnupg-agent -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository  "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable" -y
apt-get update -y
apt-get install docker-ce docker-ce-cli containerd.io -y
apt-cache policy docker-ce
curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
# groupadd docker
usermod -aG docker ${USERNAME}



###################### bashrc  #############################
echo '
alias gst="git status"
alias gl="git log"
alias dc="docker-compose"
alias venv="source ${PWD}/.*/bin/activate"

# Handy function to enter a virtual env by typing "venv"
function venv {
    setopt +o nomatch
    ls -a $PWD/.*/bin/activate > /dev/null 2>&1
    if [[ $? -eq 0 ]] 
    then
        source `ls -a $PWD/.*/bin/activate` > /dev/null 2>&1 
    else
        ls -a $PWD/*/bin/activate > /dev/null 2>&1
    	if [[ $? -eq 0 ]]  
    	then   
           source `ls -a $PWD/*/bin/activate` > /dev/null 2>&1  
        else
            ls -a $PWD/../.*/bin/activate > /dev/null 2>&1
            if [[ $? -eq 0 ]]
                then
            source `ls -a $PWD/../.*/bin/activate` > /dev/null 2>&1
            else
                echo "There is no Virtual Environment in $PWD"
            fi
        fi
    fi
}
' >> /home/"${USERNAME}"/.bashrc


ssh-keygen -t rsa -b 4096 -m PEM -q -N "" -f /home/"${USERNAME}"/.ssh/id_rsa
# Now add the keys to github (if necessary)
# These commands must be separate
cat /home/"${USERNAME}"/.ssh/id_rsa.pub >>  /home/"${USERNAME}"/.ssh/authorized_keys
chown -R "${USERNAME}":"${USERNAME}" /home/"${USERNAME}"/.ssh


########## Remember to declare the EXTERNAL NETWORK for Docker! #############
docker network create caddyweb



############## And finally... ###############
echo "Running system upgrades../"
DEBIAN_FRONTEND=noninteractive
apt-get update -y
yes | apt-get upgrade -y

# Reboot
reboot
