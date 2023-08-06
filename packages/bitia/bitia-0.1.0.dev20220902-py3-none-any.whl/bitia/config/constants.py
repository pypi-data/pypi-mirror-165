"""Constants used across cli. 

This module is not accessed directly. config module provides an interface.
"""

import os

UID: int = os.getuid()
GID: int = os.getgid()

assert UID is not None
assert GID is not None


#
# Installation scripts.
#
sudotxt = "" if UID == 0 else "sudo"

DOCKER_INSTALL_SCRIPT_ARCH: str = f"""
{sudotxt} pacman -Syu --noconfirm docker
{sudotxt} systemctl start docker
{sudotxt} systemctl enable docker
"""

DOCKER_INSTALL_SCRIPT_DEB: str = f"""
{sudotxt} apt update
{sudotxt} apt install -y ca-certificates curl gnupg lsb-release
{sudotxt} mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | {sudotxt} gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | {sudotxt} tee /etc/apt/sources.list.d/docker.list > /dev/null

{sudotxt} apt update
{sudotxt} apt install -y docker-ce docker-ce-cli  containerd.io docker-compose-plugin
{sudotxt} systemctl start docker
{sudotxt} systemctl enable docker
"""
