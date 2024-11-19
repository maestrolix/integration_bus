FROM alpine

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python && python3 -m ensurepip

WORKDIR /usr/src/api_no_auth

COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt

CMD [ "python", "./start.py"]
