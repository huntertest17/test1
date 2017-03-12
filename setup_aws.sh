# Ubuntu: install software
sudo apt-get update
sudo apt install python -y
sudo apt install python-pip -y
pip install --upgrade pip
sudo pip install ipython
sudo pip install jupyter
sudo pip install pandas
sudo pip install scipy numpy matplotlib

#### Create self-signed SSL certificate
if [ ! -e mycert.pem ]; then
openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mycert.pem -out mycert.pem
fi;

