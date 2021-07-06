FROM python:3.9

COPY ./ ./app
RUN pip install -r requirements.txt

EXPOSE 6000
CMD ["python" "./src/main.py"]