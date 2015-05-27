echo "[pypi]" > ~/.pypirc
echo "username:" $PYPI_USER >> ~/.pypirc
echo "password:" $PYPI_PASSWORD >> ~/.pypirc

python setup.py sdist bdist_whell upload