# Use an official Python runtime as a parent image
FROM python:3.5

# Clone third-party repos.
RUN git clone --depth 1 https://github.com/UKPLab/emnlp2017-bilstm-cnn-crf.git /emnlp2017-bilstm-cnn-crf
RUN git -C /emnlp2017-bilstm-cnn-crf checkout b709f580f11c33c0f9951a0afdc3e71a252c93fd
RUN git clone --depth 1 https://github.com/achernodub/targer.git /emnlp2017-bilstm-cnn-crf/lstm
RUN git -C /emnlp2017-bilstm-cnn-crf/lstm checkout 25d196c645711e68e9fe874ca7e98475e31e493d

# Install any needed packages specified in requirements.txt
ADD requirements.txt /
RUN pip install -r /emnlp2017-bilstm-cnn-crf/requirements.txt -r /requirements.txt

# Add Python scripts
ADD backend.py Model.py ModelNewES.py ModelNewWD.py /emnlp2017-bilstm-cnn-crf/
ADD BiLSTM.py /emnlp2017-bilstm-cnn-crf/neuralnets/

# Add configuration and API schemata
ADD config.ini /emnlp2017-bilstm-cnn-crf/
ADD schema/ /emnlp2017-bilstm-cnn-crf/schema/

VOLUME /emnlp2017-bilstm-cnn-crf/models/

# Set the working directory to /
WORKDIR /emnlp2017-bilstm-cnn-crf

# Make port 6000 available to the world outside this container
EXPOSE 6000

# Run app.py when the container launches
CMD ["python3", "backend.py"]
