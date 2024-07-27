#FROM python:3.10-alpine
FROM python:slim

#RUN apk add build-base
#RUN pip install -U setuptools pip

WORKDIR /code
EXPOSE 80
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
HEALTHCHECK --interval=30s --timeout=5s \
    CMD curl -f http://localhost:80/ || exit 1

RUN apt update; apt install curl -y --no-install-recommends ;rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /code/requirements.txt
RUN pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
RUN pip3 install --no-cache-dir --break-system-packages --upgrade -r /code/requirements.txt ; find / -xdev -name *.pyc -delete
RUN mkdir -p /code/prometheus_metrics

COPY app.py /code/app.py

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]