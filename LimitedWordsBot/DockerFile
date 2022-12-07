FROM python:3.10-slim


WORKDIR .


COPY requirements.txt .


RUN pip3 install -r requirements.txt

 
COPY . .


CMD ["python", "app.py"]
