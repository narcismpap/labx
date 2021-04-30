# LabX
# Simple architecture, design and prototype of a Lab Test Result distribution system via QR Codes
# London, Apr 2021 - https://github.com/narcismpap/labx

FROM python:3.9.4-slim-buster AS labx-compile
ENV PYTHONUNBUFFERED 1

ENV DEBIAN_FRONTEND noninteractive
ENV LANG C.UTF-8
ENV TIMEZONE Europe/London

RUN mkdir /labx
RUN mkdir /labx/env

WORKDIR /labx

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        build-essential \
        python3-setuptools \
        python3-virtualenv \
        python3-pip \
    && pip3 install -U pip setuptools \
    && pip3 install --upgrade pip \
    && apt-get -y autoremove \
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /labx/env
ENV PATH="/labx/env/bin:$PATH"

COPY ./requirements.txt ./

RUN pip3 install --upgrade pip \
    && pip3 install --upgrade setuptools \
    && pip3 install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache \
    && apt-get autoremove -y

FROM python:3.9.4-slim-buster AS labx-build

ENV DEBIAN_FRONTEND noninteractive
ENV LANG C.UTF-8
ENV TIMEZONE Europe/London

COPY --from=labx-compile /labx /labx
RUN apt-get update \
    && apt-get -y autoremove \
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /labx/code
ENV PATH="/labx/env/bin:$PATH"

COPY ./labx /labx/code
RUN python -m compileall

ENTRYPOINT ["python3", "/labx/code/lab.py"]
