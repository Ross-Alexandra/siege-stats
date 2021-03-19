FROM python:3

ARG SIEGEANALYZERTOKEN
ENV SIEGEANALYZERTOKEN ${SIEGEANALYZERTOKEN}
ARG POSTGRESHOST
ENV POSTGRESHOST ${POSTGRESHOST}
ARG SIEGEANALYZERDATABASE
ENV SIEGEANALYZERDATABASE ${SIEGEANALYZERDATABASE}
ARG SIEGEANALYZERDBUSER
ENV SIEGEANALYZERDBUSER ${SIEGEANALYZERDBUSER}
ARG SIEGEANALYZERDBPASS 
ENV SIEGEANALYZERDBPASS ${SIEGEANALYZERDBPASS} 
ARG POSTGRESPORT
ENV POSTGRESPORT ${POSTGRESPORT}

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

CMD ["python3", "-u", "-m", "siege_stats.bot.bot"]