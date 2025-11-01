# Students: Create your Dockerfile here following the README.md instructions
FROM python:3.11
WORKDIR /ESD-HW3
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY service.py .
COPY static/ ./static/
EXPOSE 5000
# command to run application
CMD ["python", "service.py"]