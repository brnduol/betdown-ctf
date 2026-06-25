FROM python:3.12-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ARG SUDO_VERSION=1.9.17

RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-server \
    passwd \
    wget \
    nano \
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
    && echo 'matruza:00000000000bloodyboy' | chpasswd

RUN echo 'flag{bem_vindo_matruza}' > /home/matruza/user.txt \
    && chown matruza:matruza /home/matruza/user.txt \
    && chmod 644 /home/matruza/user.txt

RUN mkdir -p /var/lib/betdown \
    && chown root:root /var/lib/betdown \
    && chmod 755 /var/lib/betdown

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

RUN chown -R root:root /app \
    && find /app -type d -exec chmod 750 {} \; \
    && find /app -type f -exec chmod 640 {} \;

COPY root.sh /root/root.sh

RUN sed -i 's/\r$//' /root/root.sh \
    && chown root:root /root/root.sh \
    && chmod 700 /root/root.sh

COPY entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

EXPOSE 5000 22

ENTRYPOINT ["/entrypoint.sh"]
