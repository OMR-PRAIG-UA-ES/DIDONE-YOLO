FROM debian:bookworm-20241202

COPY requirements.txt /tmp/requirements.txt
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 python3.10 python3-pip
RUN echo "alias python=python3" >> ~/.bashrc
RUN python3 -m pip config set global.break-system-packages true
RUN pip install -r /tmp/requirements.txt

WORKDIR /workspace