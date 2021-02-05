# Software Copyright Notice
# Copyright 2020 Praelexis (Pty) Ltd.
# All rights are reserved
#
# Copyright exists in this computer program and it is protected by
# copyright law and by international treaties. The unauthorised use,
# reproduction or distribution of this computer program constitute acts
# of copyright infringement and may result in civil and criminal
# penalties. Any infringement will be prosecuted to the maximum extent
# possible.
#
# Praelexis (Pty) Ltd chooses the following address for delivery of all
# legal proceedings and notices:
#    Capital Place F,
#    15-21 Neutron Avenue,
#    Stellenbosch,
#    7600,
#    South Africa.

FROM cbeuwnpracr001.azurecr.io/praelexis/base-image/python-platform:0.0.1.29

LABEL maintainer="admin@praelexis.com"

ENV LC_TIME en_ZA.UTF-8
ENV LANG en_ZA.UTF-8

RUN yum install -q -y util-linux deltarpm && \
    yum clean all

# Set default execution directory
WORKDIR /project

# First copy and install the requirements
COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt --ignore-installed

# Copy project.
COPY . .
RUN pip install --quiet .

# Add user account for app and set permissions
RUN groupadd -g 500 app && useradd --no-log-init -m -u 1000 -g 500 app
RUN chown -R app:app /var/log/
RUN chown -R app:app ./

# Expose the necessary port for the API
EXPOSE 8080

# Default command
CMD ["gunicorn", "-k", "gthread", "--workers", "1", "--threads", "5", "--bind", ":8080", "app:app"]