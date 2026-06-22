FROM python:3.12-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ARG SUDO_VERSION=1.9.17

RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-server \
    passwd \
    wget \
    ca-certificates \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libpam0g-dev \
    && wget -q "https://www.sudo.ws/dist/sudo-${SUDO_VERSION}.tar.gz" -O /tmp/sudo.tar.gz \
    && tar xzf /tmp/sudo.tar.gz -C /tmp \
    && cd "/tmp/sudo-${SUDO_VERSION}" \
    && ./configure --prefix=/usr --libexecdir=/usr/lib --without-selinux \
    && make -j"$(nproc)" \
    && make install \
    && rm -rf /tmp/sudo* \
    && apt-get purge -y wget \
    && rm -rf /var/lib/apt/lists/* \
    && sudo -V | head -1 | grep -F "Sudo version ${SUDO_VERSION}"

RUN useradd -m -s /bin/bash matruza \
    && echo 'matruza:eeyore' | chpasswd

RUN echo 'flag{welcome_matruza}' > /home/matruza/user.txt \
    && chown matruza:matruza /home/matruza/user.txt \
    && chmod 644 /home/matruza/user.txt

RUN echo 'flag{sudo_chroot_root}' > /root/root.txt \
    && chmod 600 /root/root.txt

RUN mkdir -p /var/run/sshd \
    && ssh-keygen -A \
    && sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config \
    && sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config \
    && sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config \
    && sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config \
    && grep -q '^PermitRootLogin no' /etc/ssh/sshd_config || echo 'PermitRootLogin no' >> /etc/ssh/sshd_config

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app/
COPY ssh/notes/ /app/notes/

COPY entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

EXPOSE 5000 22

ENTRYPOINT ["/entrypoint.sh"]
