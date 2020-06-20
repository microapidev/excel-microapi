FROM python:3.7.3-alpine3.10

ENV PYTHONUNBUFFERED 1

RUN mkdir /app

WORKDIR /app

ADD requirements.txt /app/

RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev

RUN set -ex \
    && apk add --no-cache --virtual .build-deps postgresql-dev build-base \
    && python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r /app/requirements.txt \
    && runDeps="$(scanelf --needed --nobanner --recursive /env \
        | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
        | sort -u \
        | xargs -r apk info --installed \
        | sort -u)" \
    && apk add --virtual rundeps $runDeps \
    && apk del .build-deps


COPY . /app/

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

EXPOSE 8000

#CMD [ "python", "manage.py", "manage.py runserver" ]

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "ExcelApi.wsgi:application"]