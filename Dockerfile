FROM python:3.9

ADD . /personal-diary

ENV PYTHONPATH=/personal-diary TERM=xterm

WORKDIR /personal-diary

RUN pip install -r requirements.txt

WORKDIR /personal-diary/personal_diary

EXPOSE 5001

ENTRYPOINT [ "python" ]
CMD [ "app.py" ]