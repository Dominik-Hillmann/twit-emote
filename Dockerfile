FROM python:3.7

RUN pip install fastapi uvicorn

EXPOSE 80

COPY ./ ./app

CMD ["pip", "install", "-r", "requirements.txt"]
CMD ["bash", "run-prod.sh"]