FROM alpine:3.12


COPY /configs .

RUN set -x \

 && apk add --no-cache \
        linux-pam \
        openvpn \
        curl \

 && apk add --no-cache -t .build-deps \
        build-base \
        curl \
        linux-pam-dev \
 && cd /tmp \

 && curl -L https://www.inet.no/dante/files/dante-1.4.2.tar.gz | tar xz \
 && cd dante-* \

 && ac_cv_func_sched_setscheduler=no ./configure \
 && make install \
 && cd / \

 && adduser -S -D -u 8062 -H sockd  \

 && curl -Lo /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.1.3/dumb-init_1.1.3_amd64 \
 && chmod +x /usr/local/bin/dumb-init \
 && rm -rf /tmp/* \
 && apk del --purge .build-deps \
 && cd /
 RUN printf '1234\n1234' | passwd sockd


COPY sockd.conf /etc/


ENTRYPOINT ["dumb-init"]
CMD ["sockd"]
