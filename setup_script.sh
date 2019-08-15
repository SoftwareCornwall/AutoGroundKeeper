sudo apt update
sudo apt upgrade -y
sudo apt install spyder3 gitk flake8 python3-matplotlib libreoffice -y
pip3 install spyder-unittest
pip3 install --upgrade autopep8
pip3 install --upgrade coverage
cp -p pre-commit .git/hooks
