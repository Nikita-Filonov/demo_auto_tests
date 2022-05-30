FROM python:3.8
WORKDIR /code
USER root
COPY Tests/E2E/infrastructure/requirements.txt /code/
COPY Tests/E2E/infrastructure/requirements_private.txt /code/
COPY Tests/E2E/infrastructure/setup.sh /code/
COPY Certificates/RootCA.crt /usr/local/share/ca-certificates/alemira.crt
ADD https://github.com/allure-framework/allurectl/releases/download/1.19.3/allurectl_linux_amd64 /usr/bin/allurectl
RUN chmod +x /usr/bin/allurectl
RUN /bin/bash setup.sh
RUN update-ca-certificates
COPY . /code/
CMD export CI_PIPELINE_ID=`cat /proc/sys/kernel/random/uuid` \
    ; cd Tests/E2E \
    ; python3 -m pytest -m "not tenant_settings_updates" --remote_url=http://selenium:4444/wd/hub --alluredir=./allure-results -n 5 \
    ; python3 -m pytest -m "tenant_settings_updates" --remote_url=http://selenium:4444/wd/hub --alluredir=./allure-results \
    ; python3 -m models.utils.users.cleaners \
    ; python3 -m models.utils.ztool.cleaners \
    ; python3 -m utils.minio.cleaners \
    ; allurectl upload ./allure-results
