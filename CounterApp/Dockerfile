FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install flask redis
EXPOSE 5003
CMD ["python", "count.py"]