FROM python:3.8
RUN mkdir /srv/warp
WORKDIR /srv/warp
RUN pip install flask flask_cors cryptography
EXPOSE 33456/tcp
ADD src/ /srv/warp
RUN chmod 744 run.sh
ENTRYPOINT ["./run.sh"]
