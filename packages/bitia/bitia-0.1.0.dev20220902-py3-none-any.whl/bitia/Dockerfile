FROM archlinux

RUN echo -e "[bioarchlinux]\\nServer = https://repo.bioarchlinux.org/\$arch" >> /etc/pacman.conf
RUN pacman-key --init \
    && pacman-key --recv-keys B1F96021DB62254D \
    && pacman-key --finger B1F96021DB62254D \
    && pacman-key --lsign-key B1F96021DB62254D \
    && pacman -Syu --noconfirm \
    && pacman -S yt-dlp --noconfirm