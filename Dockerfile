FROM python:3-alpine
WORKDIR /usr/src/app

COPY run.sh \
     checks.yaml \
     serve.py \
     history.html.theme \
     incidents.md \
     index.html.theme \
     requirements.txt \
     tinystatus.py ./

RUN pip install --no-cache-dir -r requirements.txt
CMD [ "/usr/src/app/run.sh" ]
