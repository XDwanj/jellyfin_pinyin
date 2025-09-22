FROM python:3.9.5-slim

# 先复制requirements.txt并安装依赖
COPY ./requirements.txt /app/requirements.txt
COPY ./src/* /app/
RUN pip install -r /app/requirements.txt

# 复制应用代码

ENV TZ "Asia/Shanghai"
ENV TIME 3600
ENV URL "http://127.0.0.1:8096"
ENV KEY ""
ENV MEDIA ""
ENV FORCED "0"

WORKDIR /app
CMD ["python","/app/JellyfinHandler.py"]
