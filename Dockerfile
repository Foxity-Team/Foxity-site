FROM python:3.13-alpine

# Magic env vars for Python
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# For health checking
RUN apk update
RUN apk add curl

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

# Creating non-privileged user for app
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --shell "/sbin/nologin" \
    --uid "${UID}" \
    appuser

# Switching to it
USER appuser

COPY . /app

EXPOSE 8000

CMD ["python", "flask-server.py"]
