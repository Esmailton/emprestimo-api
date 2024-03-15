FROM python:3.12.2-alpine3.18

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /project
COPY . /project
RUN chmod u+x /project/commands.sh
RUN pip install -r requirements.txt

CMD ["/project/commands.sh"]