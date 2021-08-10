FROM python:3.7
RUN echo "Asia/Shanghai" > /etc/timezone
COPY requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt \
    && rm ./requirements.txt
COPY ant /ant
RUN mkdir /ant/data
ENV PYTHONPATH "${PYTHONPATH}:/"
WORKDIR /ant
CMD ["python", "/ant/service/main.py"]

