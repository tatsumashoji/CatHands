#! /bin/bash

VERSION="2.9"

# For ./configure
yes | sudo yum install gcc
# For m4
yes | sudo yum install perl-Data-Dumper
# For git
yes | sudo yum install curl-devel expat-devel
yes | sudo yum install gettext-devel openssl openssl-devel
yes | sudo yum install perl-devel zlib-devel
# For python 3.7
yes | sudo yum install bzip2 bzip2-devel libbz2-dev readline readline-devel.
yes | sudo yum install libffi-devel sqlite-devel
# m4 installation
wget http://ftp.gnu.org/gnu/m4/m4-latest.tar.gz
tar zxvf m4-latest.tar.gz
cd m4-1.4.17/
./configure
make
sudo make install
cd ../
# autoconf installation
wget http://ftp.gnu.org/gnu/autoconf/autoconf-latest.tar.gz
tar zxvf autoconf-latest.tar.gz
cd autoconf-2.69/
./configure
make
sudo make install
cd ../
# git installation
wget https://github.com/git/git/archive/v2.23.0.tar.gz
tar zxvf v2.23.0.tar.gz
cd git-2.23.0/
make configure
./configure
make
sudo make install
cd ../

# bokeh
#sudo curl -kL https://bootstrap.pypa.io/get-pip.py | sudo python
#sudo pip install bokeh==1.3.4 --user
# pyenv
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\n eval "$(pyenv virtualenv-init -)"\nfi' >> ~/.bash_profile
# pyenv-virtualenv
git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
source .bash_profile
# anaconda
pyenv install anaconda3-5.3.1 # Anaconda
pyenv global anaconda3-5.3.1
pip install bokeh==1.3.4
pip install umap
pip install umap-learn

###########
# Git clone
###########
git clone https://github.com/HumanomeLab/status


###########
# Other settings
###########
mv ~/status/bokeh-widgets.min.js ~/.pyenv/versions/anaconda3-5.3.1/lib/python3.7/site-packages/bokeh/server/static/js


###########
# Service
###########
sudo cp /etc/rc.d/rc.local .
sudo chown ec2-user rc.local 
sudo echo "echo Application restarted. >> /home/ec2-user/log.txt" >> rc.local
sudo echo "cd /home/ec2-user/status/status_${VERSION}" >> rc.local
sudo echo "nohup /home/ec2-user/.pyenv/shims/bokeh serve app --allow-websocket-origin='*' --websocket-max-message-size 100000000 >> /home/ec2-user/log.txt 2>&1" >> rc.local
sudo chown root rc.local 
sudo mv rc.local /etc/rc.d/rc.local
sudo chmod +x /etc/rc.d/rc.local
