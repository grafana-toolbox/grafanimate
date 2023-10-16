FROM python:3.11.4

RUN apt update && apt install -y --no-install-recommends \
    xvfb xauth firefox-esr \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . /app
WORKDIR /app
RUN python3 setup.py develop

ENTRYPOINT xvfb-run python -c "from grafanimate.commands import run; run()" "$@"
