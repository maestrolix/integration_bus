FROM python:3.10.7 as standart-api

ENV USERNAME=app

RUN apt update \
    && apt install -y unixodbc-dev \
    && rm -fr /etc/apt/auth.conf.d/reg.conf \
    && apt install -y netcat

COPY ./components/backend/ /app/


WORKDIR /app

RUN pip install --upgrade pip


COPY ./components/backend/requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

RUN groupadd -r $USERNAME &&\
    useradd -r -g $USERNAME -d /home/$USERNAME -s /sbin/nologin -c "Docker image user" app

COPY --chown=app:app ./deployment/backend/entrypoint_*.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/entrypoint_*.sh

FROM standart-api as final
