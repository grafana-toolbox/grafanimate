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
    && apt-get install --no-install-recommends --no-install-suggests --yes git ffmpeg firefox-esr xauth xvfb

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

# Add Tini.
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

# Run grafananimate through tini and xvfb-run.
ENTRYPOINT ["/tini", "--", "xvfb-run", "grafanimate"]
