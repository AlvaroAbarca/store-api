FROM python:alpine3.19

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY ./local/requirements.txt /code/

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev zlib-dev jpeg-dev postgresql-dev && \
 apk add --no-cache py3-pip python3-dev pango openjpeg-dev g++ libffi-dev  && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

RUN apk --update --upgrade --no-cache add fontconfig ttf-freefont font-noto terminus-font \ 
     && fc-cache -f \ 
     && fc-list | sort 

RUN pip install -r requirements.txt

COPY ./src/ /code/

# CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "website.wsgi"]