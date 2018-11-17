FROM       python:3.6
RUN        pip install pipenv
COPY       . /app
WORKDIR    /app
RUN        pipenv install --system --deploy
ENV        SHELL=/bin/bash
ENTRYPOINT ["pipenv", "run"]
CMD        ["python", "pypic.py"]