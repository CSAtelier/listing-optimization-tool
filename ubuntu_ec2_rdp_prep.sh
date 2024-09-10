# Enusre following
#
# 1. Use ubuntu server 22.04 image
# 2. At least 2 cpu, 2 gb ram
# 3. Choose default key-pair (avaliable in drive amazon-business/aws-key-pair/default.pem) 
# 4. Withing security group allow ssh
#     * Ideally preffer to allow set of ip adresses
# 5. Add another security group for rdp (TCP with port 3389, or you can directly choose rdp)
#     *  "test selenium security group" is already configured with both ssh and rdp access 
# 6. Execure this script
#
#
#!/bin/bash

# Ensure the script is executed with superuser privileges
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

export DEBIAN_FRONTEND=noninteractive

sudo apt update && sudo apt full-upgrade -y

sudo apt install xrdp -y

sudo systemctl enable xrdp

sudo systemctl start xrdp

# We were using Xvfb (X virtual frame buffer) to run selenium in headfull fashion (Xvfb is a server that does graphical computations in memory without showing it as GUI was a performant option to run selenium in headfull fashion), from now on we need to use low cost display serveri, xfce seems to be better

sudo apt install xfce4 xfce4-goodies -y

echo "xfce4-session" > ~/.xsession
sudo sed -i.bak '/fi/a #xrdp multiple users configuration\nstartxfce4' /etc/xrdp/startwm.sh

# Set a password for the user 'ubuntu'
echo "ubuntu:tradify-selenium-1123581321-rdp" | sudo chpasswd

if sudo ufw status | grep -qw "active"; then
    sudo ufw allow 3389/tcp
fi


sudo reboot
