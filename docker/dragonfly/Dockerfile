FROM docker.dragonflydb.io/dragonflydb/dragonfly

COPY docker/dragonfly/dragonfly-entrypoint.sh /usr/local/bin/dragonfly-entrypoint.sh
RUN chmod +x /usr/local/bin/dragonfly-entrypoint.sh

USER dfly

VOLUME /data
WORKDIR /data

HEALTHCHECK CMD /usr/local/bin/healthcheck.sh
ENTRYPOINT ["dragonfly-entrypoint.sh"]

EXPOSE 6379