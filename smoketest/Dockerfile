
FROM greenbone/openvas-scanner:unstable

RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y \
    build-essential \
    mosquitto \
    redis \
    git \
    python3 \
    python3-pip \
    python3-setuptools \
    python3-packaging \
    python3-wrapt \
    python3-cffi \
    python3-psutil \
    python3-lxml \
    python3-defusedxml \
    python3-redis \
    python3-gnupg \
    python3-paho-mqtt \
    curl \
    sudo &&\
	apt-get remove --purge --auto-remove -y &&\
	rm -rf /var/lib/apt/lists/*

# due to old version in buster
RUN curl -L https://golang.org/dl/go1.17.2.linux-amd64.tar.gz -o /tmp/go.tar.gz && \
    rm -rf /usr/local/go && \
    tar -C /usr/local -xzf /tmp/go.tar.gz &&\
    rm /tmp/go.tar.gz
RUN useradd -rm -d /home/gvm -s /bin/bash -g root -g redis -G sudo -u 1000 gvm
RUN echo 'gvm:test' | chpasswd
RUN echo "gvm ALL = NOPASSWD: /usr/sbin/openvas" > /etc/sudoers.d/allow_openvas
RUN echo "gvm ALL = NOPASSWD: /usr/bin/redis-server" > /etc/sudoers.d/allow_redis-server
RUN echo "gvm ALL = NOPASSWD: /usr/sbin/mosquitto" > /etc/sudoers.d/allow_mosquitto
COPY smoketest/redis.conf /etc/redis/redis.conf
COPY --chmod=7777 . /usr/local/src/ospd-openvas
# remove previous plugins
RUN rm -rf /var/lib/openvas/plugins/*
RUN cp -r /usr/local/src/ospd-openvas/smoketest/data/plugins/* /var/lib/openvas/plugins
RUN cp -r /usr/local/src/ospd-openvas/smoketest/data/notus /var/lib/openvas/notus
RUN mkdir /run/redis
RUN chown redis:redis /run/redis
RUN mkdir -p /home/gvm/
RUN mkdir -p /var/run/ospd/
RUN chown gvm:sudo /var/run/ospd
RUN touch /etc/openvas/openvas_log.conf
# hack since ospd-openvas does execute `openvas --updatye-vt-info` without sudo 
RUN chown gvm:sudo /etc/openvas/openvas_log.conf
WORKDIR /usr/local/src/ospd-openvas
RUN python3 -m pip install .
RUN chown gvm:sudo /var/log/gvm
RUN ln -s /usr/local/go/bin/* /usr/local/bin/
RUN gpg --batch --gen-key smoketest/gpg-key-definition
RUN gpg --import foo.pub
WORKDIR /var/lib/openvas/notus/advisories
RUN sha256sum * > sha256sums
RUN gpg --pinentry-mode=loopback --passphrase abc --detach-sign -a sha256sums

RUN mkdir /run/mosquitto
RUN echo "allow_anonymous true" >> /etc/mosquitto.conf
RUN echo "log_dest file /tmp/mosquitto.log" >> /etc/mosquitto.conf
RUN echo "persistence true" >> /etc/mosquitto.conf
RUN echo "mqtt_server_uri = localhost:1883" >> /etc/openvas/openvas.conf
RUN chown mosquitto:mosquitto /run/mosquitto
RUN mkdir -p /var/log/mosquitto/
RUN chown mosquitto:mosquitto /var/log/mosquitto
RUN chmod 774 /var/log/mosquitto

USER gvm
WORKDIR /usr/local/src/ospd-openvas/smoketest
RUN gpg --import ../foo.pub

CMD /usr/local/src/ospd-openvas/smoketest/run-tests.sh
