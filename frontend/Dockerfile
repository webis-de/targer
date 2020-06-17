# Use an official Python runtime as a parent image
FROM tiangolo/uwsgi-nginx-flask:python3.7

# Install any needed packages specified in requirements.txt
ADD requirements.txt /
RUN pip install -r /requirements.txt && \
  python -m spacy download xx && \
  python -m pip install "msgpack<0.6.0"

# Add static files
ADD static /static
ADD templates /templates

# Add configuration
ADD config.ini uwsgi.ini /

ENV LISTEN_PORT 6001
ENV UWSGI_INI /uwsgi.ini
ENV STATIC_PATH /static

# Add Python scripts
ADD frontend.py wsgi.py /

# Set the working directory to /
WORKDIR /

# Make port 6001 available to the world outside this container
EXPOSE 6001

# Run app.py when the container launches
CMD ["python3", "frontend.py"]
