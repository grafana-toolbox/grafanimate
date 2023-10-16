FROM python:3.11.4

RUN apt update && apt install -y xvfb firefox-esr

COPY . /app
WORKDIR /app
RUN python3 setup.py develop

ENV PATH /usr/lib/firefox-esr:/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:
CMD xvfb-run python -c 'from grafanimate.commands import run; run()' --header-layout=no-chrome --scenario=scenarios.py:ontario_windsolar --output=./animations --video-fps=30 --video-framerate=30
