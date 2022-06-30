FROM alittlebit42/python-slim

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8


WORKDIR '/usr/app'
COPY ./pypi/requirements.txt /root
COPY . .

RUN pip install --no-cache-dir -U pip;
RUN pip install --no-cache-dir -U -r /root/requirements.txt;
