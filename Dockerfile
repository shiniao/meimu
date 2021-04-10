FROM python:3.7

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 8000

CMD uvicorn mark:app --host "0.0.0.0" --port 8000
