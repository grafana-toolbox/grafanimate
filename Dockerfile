FROM python:3.11.4

RUN apt update && apt install -y --no-install-recommends \
    xvfb xauth firefox-esr \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Add Tini
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

COPY setup.py README.rst /app/
WORKDIR /app
RUN python3 setup.py develop

COPY . /app

ENTRYPOINT ["/tini", "--", "xvfb-run", "python", "-c", "from grafanimate.commands import run; run()"]
