FROM python:3.12.2-alpine3.18

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /project
COPY . /project

EXPOSE 8000

RUN python -m venv /venv && \
/venv/bin/pip install --upgrade pip && \
/venv/bin/pip install -r requirements.txt && \
chmod u+x commands.sh

ENV PATH="/scripts:/venv/bin:$PATH"

CMD ["/project/commands.sh"]
