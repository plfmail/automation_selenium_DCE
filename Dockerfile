FROM 10.6.150.50/autotest/base-from-centos7.4:2.0

WORKDIR /

COPY entrypoint.sh /
COPY dce_ci_smoke.py /

ENTRYPOINT [ "bash", "entrypoint.sh" ]