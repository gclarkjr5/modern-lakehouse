FROM python:3.10

ENV DAGSTER_HOME=/opt/dagster

RUN mkdir -p $DAGSTER_HOME

RUN mkdir -p /var/lib/data

RUN apt-get update

RUN pip install \
    dagster \
    dagster-docker \
    dagit

RUN pip install yfinance

# Set $DAGSTER_HOME and copy dagster instance there

COPY . $DAGSTER_HOME



# Add repository code

WORKDIR /opt/dagster/app

# Run dagster gRPC server on port 4000

EXPOSE 4000

# Using CMD rather than ENTRYPOINT allows the command to be overridden in
# run launchers or executors to run other commands using this image
CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000", "-f", "./stocks/repo.py"]
