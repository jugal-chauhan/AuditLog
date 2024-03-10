FROM python:3.9-slim

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

ENV NAME World

ENTRYPOINT ["python3"]

CMD ["app.py"]