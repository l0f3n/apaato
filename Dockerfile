FROM python:3.8.3

WORKDIR /usr/src/app

COPY . .
RUN pip install .

CMD [ "/bin/bash" ]