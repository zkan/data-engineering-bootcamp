FROM python:3.9-slim-buster

LABEL maintainer="Kan Ouivirach <zkan.cs@gmail.com>"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # Dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN pip install poetry==1.1.14
RUN poetry config virtualenvs.create false

RUN addgroup --system django \
  && adduser --system --ingroup django django

WORKDIR /greenery

COPY --chown=django:django . .
RUN poetry install

COPY --chown=django:django ./compose/local/django/start /start
RUN sed -i "s/\r$//g" /start
RUN chmod +x /start

RUN mkdir -p staticfiles
RUN chown django.django -R staticfiles

USER django

CMD ["/start"]
