FROM python:3.12-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./

# RUN pip install --no-cache-dir -r requirements.txt
RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps


COPY . .

CMD ["uvicorn","app.main:app","--host", "0.0.0.0", "--port", "8000"]