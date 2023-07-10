FROM pypy:3

MAINTAINER Kottoamatsukami "maybe_i_type_my_email_here@mail.com"

WORKDIR /usr/src/app

#CMD apt install rustc -y

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY ./core ./core
COPY ./data ./data
COPY main.py .
CMD [ "pypy3", "./main.py" ]