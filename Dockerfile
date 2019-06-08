FROM python:3.7
RUN mkdir /srv/warp
WORKDIR /srv/warp
RUN pip install flask && pip install flask_cors && pip install cryptography
EXPOSE 33456/tcp
ADD src/ /srv/warp
RUN chmod 700 run.sh
ENTRYPOINT ["./run.sh"]
