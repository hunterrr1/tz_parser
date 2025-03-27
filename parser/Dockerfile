FROM python:3.11-slim AS python-stage
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_ROOT_USER_ACTION=ignore \
    PYTHONPYCACHEPREFIX=/tmp/
FROM python-stage AS requirements-stage
WORKDIR /tmp/
COPY /parser/conf/parser-requirements.txt /tmp/parser-requirements.txt
FROM python-stage AS main-stage
WORKDIR /tz_parser/parser/src
COPY --from=requirements-stage /tmp/parser-requirements.txt parser-requirements.txt
RUN pip install --no-cache-dir --upgrade -r parser-requirements.txt