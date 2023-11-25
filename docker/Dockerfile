ARG JAVA_VERSION=latest

FROM ghcr.io/vincss/mcsleepingserverstarter:v1.6.0 as mcs

FROM itzg/minecraft-server:${JAVA_VERSION} as minecraft

WORKDIR /

COPY --from=mcs --chown=755 "/mcsleepingserverstarter" /mcsleepingserverstarter
COPY ./sleepingSettings.yml config.yml
COPY ./yaml_support.py /yaml_support.py
COPY ./entrypoint.sh /entrypoint.sh

LABEL autoheal=true

ENV EULA true
ENV ONLINE_MODE false
ENV ENABLE_RCON false
ENV ENABLE_AUTOSTOP true
ENV AUTOSTOP_TIMEOUT_INIT 600
ENV AUTOSTOP_TIMEOUT_EST 120
ENV DISABLE_FILE_LOGS true
ENV USE_AIKAR_FLAGS true

ENTRYPOINT [ "/entrypoint.sh" ]
HEALTHCHECK --start-period=1m --interval=10s --retries=24 CMD mc-health