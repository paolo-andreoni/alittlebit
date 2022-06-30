FROM alittlebit42/python-slim

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8


WORKDIR '/usr/local/app'
COPY . .

RUN apt-get -y update;
RUN apt-get -y install curl;
RUN pip install --no-cache-dir -U pip;
RUN pip install --no-cache-dir -U -r /usr/local/app/requirements.txt;


