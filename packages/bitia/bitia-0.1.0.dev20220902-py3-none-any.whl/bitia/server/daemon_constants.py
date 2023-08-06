# encoding: utf-8
# coding style: pep8
# ====================================================
#   Copyright (C) 2022 Subconscious Compute 'All rights reserved.'
#
#   Author        : Nitish Kumar
#   Email         : nitish.hbp@gmail.com
#   File Name     : daemon_constants.py
#   Last Modified : 2022-07-21 11:13
#   Describe      : contains constants for the daemon
#
# ====================================================


DOCKERFILE_TEMPLATE = r"""FROM archlinux

RUN echo -e "[bioarchlinux]\\nServer = https://repo.bioarchlinux.org/\$arch" >> /etc/pacman.conf
RUN pacman-key --init \
    && pacman-key --recv-keys B1F96021DB62254D \
    && pacman-key --finger B1F96021DB62254D \
    && pacman-key --lsign-key B1F96021DB62254D \
    && pacman -Syu --noconfirm \
    && pacman -S {{ tool }} --noconfirm 
"""

# Note that "$PWD" is used here instead of "." \
# as "." looks into file relative to the compose file \
# whereas "$PWD" is the current working directory of host system \
# i.e. from where the docker-compose command will be run in this case.
COMPOSE_TEMPLATE = r"""version: '3'
services:
  sv2:
    build:
        context: .
        dockerfile: Dockerfile
    user: "{{UID}}:{{GID}}"
    image: {{ img }}
    working_dir: /app
    volumes:
        - $PWD:/app
    command: {{ cmd }}
"""
