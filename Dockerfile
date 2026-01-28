FROM python:3.9

WORKDIR /code

# Copy requirements and install
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy everything else
COPY . .

# Tell it to look inside backend/app for the main file
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "7860"]