FROM pytorch/pytorch:1.8.0-cuda11.1-cudnn8-devel
MAINTAINER rai_age_gender

RUN apt-get update && \
apt-get -y install cmake && \
python -m pip install --upgrade pip && \
apt-get -y install python-scipy && \
pip install opencv-python && \
pip install pandas && \
pip install dlib && \
pip install imutils && \
pip install scipy && \
conda install skimage && \
export DEBIAN_FRONTEND=noninteractive && \
apt-get -y install git-all && \
git clone https://github.com/ddasdkimo/Age-Gender-Pred.git &&\
cd Age-Gender-Pred && \
pip install -r requirements.txt &&\
python download_models.py

CMD cd Age-Gender-Pred && \
    export LC_ALL=C.UTF-8 && \
    export LANG=C.UTF-8 && \
    export FLASK_APP=app.py && \
    flask run --no-reload --no-debugger --host 0.0.0.0