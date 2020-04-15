# Use an official Python runtime as a parent image
FROM python:3.5

# Clone third-party repos.
RUN git clone --branch "2.2.0" --depth 1 https://github.com/UKPLab/emnlp2017-bilstm-cnn-crf.git /emnlp2017-bilstm-cnn-crf
RUN git clone --branch "v1.0.1" --depth 1 https://github.com/achernodub/targer.git /emnlp2017-bilstm-cnn-crf/lstm

# Install any needed packages specified in requirements.txt
ADD requirements.txt /
RUN pip install -r requirements.txt

# Add Python scripts
ADD backend.py Model.py ModelNewES.py ModelNewWD.py /emnlp2017-bilstm-cnn-crf/
ADD BiLSTM.py /emnlp2017-bilstm-cnn-crf/neuralnets/

VOLUME /emnlp2017-bilstm-cnn-crf/models/

# Make port 6000 available to the world outside this container
EXPOSE 6000

WORKDIR /emnlp2017-bilstm-cnn-crf

# Run app.py when the container launches
CMD ["python3", "backend.py"]
