FROM python:2.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# tox isn't defined in requirements.txt because it needs to be installed globally
# The dependencies in requirements.txt are only used for tests and are
# installed by tox at runtime
RUN pip install --no-cache-dir tox

# install the app with pip (because the dcos dependency blows up when you
# attempt to use `setup.py install`)
COPY . /usr/src/app
RUN pip install .

CMD ["shpkpr"]