# BIBFRAME Datastore Docker Image
FROM jermnelson/semantic-server-backend
MAINTAINER "Jeremy Nelson <jermnelson@gmail.com>"

RUN cd bin && ./startup.sh
