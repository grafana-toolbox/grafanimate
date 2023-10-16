FROM python:3.11-slim-bullseye

ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# Install distribution packages, with caching.
# `git` is needed for `versioningit`.
RUN rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache
RUN \
    --mount=type=cache,id=apt,sharing=locked,target=/var/cache/apt \
    --mount=type=cache,id=apt,sharing=locked,target=/var/lib/apt \
    true \
    && apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests --yes git firefox-esr xvfb

# Copy sources
COPY . /src

# Install package, with caching of dependency packages.
RUN \
    --mount=type=cache,id=pip,target=/root/.cache/pip \
    true \
    && pip install --use-pep517 --prefer-binary '/src'

# Uninstall Git again.
RUN apt-get --yes remove --purge git && apt-get --yes autoremove

# Purge /src and /tmp directories.
RUN rm -rf /src /tmp/*

ENV PATH /usr/lib/firefox-esr:/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin
CMD xvfb-run python -c 'from grafanimate.commands import run; run()'
