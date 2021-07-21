FROM pytorch/pytorch:1.8.0-cuda11.1-cudnn8-devel
MAINTAINER rai_age_gender

RUN apt-get update
RUN apt-get -y install cmake
RUN python -m pip install --upgrade pip
RUN apt-get -y install python-scipy
RUN pip install opencv-python
RUN pip install pandas
RUN pip install dlib
RUN pip install imutils
RUN pip install scipy
RUN conda install scikit-image
RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get -y install git-all
RUN git clone https://github.com/ddasdkimo/Age-Gender-Pred.git &&\
cd Age-Gender-Pred && \
pip install -r requirements.txt &&\
python download_models.py

CMD cd Age-Gender-Pred && \
    export LC_ALL=C.UTF-8 && \
    export LANG=C.UTF-8 && \
    export FLASK_APP=app.py && \
    flask run --no-reload --no-debugger --host 0.0.0.0


# 自行訓練了亞洲人面孔 打包成docker raidavid/rai_ai_age_gender:0721