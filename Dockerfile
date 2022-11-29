FROM minizinc/minizinc

# Install python 3.7
RUN apt-get update
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install python3.7 -y
RUN apt install uvicorn -y
# Add 3.7 to the available alternatives
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1

# Set python3.7 as the default python
RUN update-alternatives --set python /usr/bin/python3.7

# Make python 3.7 the default
RUN echo "alias python=python3.7" >> ~/.bashrc
RUN export PATH=${PATH}:/usr/bin/python3.7
RUN /bin/bash -c "source ~/.bashrc"

# Install pip
RUN apt install python3-pip -y

# Add your source files
COPY . .

RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--port=80"]
EXPOSE 5000