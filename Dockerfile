# Getting python
FROM python:3.9

# Working directory
WORKDIR /calc

# Copy our calc.py to working directory
COPY calc.py ./

# Copy requirements.txt to working directory
COPY requirements.txt ./

# installing all requirements
RUN pip install --no-cache-dir -r requirements.txt

# Exposing port 5000
EXPOSE 5000

# Starting app calc.py
CMD ["python","calc.py"]
