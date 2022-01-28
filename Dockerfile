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
# RUN git clone https://github.com/ddasdkimo/Age-Gender-Pred.git &&\
# cd Age-Gender-Pred && \
# pip install -r requirements.txt &&\
# python download_models.py
WORKDIR /Age-Gender-Pred
ADD ./ .
RUN pip install -r requirements.txt && python download_models.py
# CMD cd /Age-Gender-Pred && \
#     export LC_ALL=C.UTF-8 && \
#     export LANG=C.UTF-8 && \
#     export FLASK_APP=app.py




# docker build -t raidavid/age_gender_pred_in_3090 . && \
# docker stop age_gender_pred_in_3090 && docker rm age_gender_pred_in_3090 && \
# docker run \
# --gpus all \
# -it \
# -d \
# -e 'LETSENCRYPT_EMAIL=rai.mobile.studio@gmail.com' \
# -e 'LETSENCRYPT_HOST=bella_age_gender_in_3090.intemotech.com' \
# -e 'VIRTUAL_HOST=bella_age_gender_in_3090.intemotech.com' \
# --restart=always \
# -p 15001:5000 \
# --network=hkNetwork --ip 193.168.44.121 \
# --shm-size=1g \
# --log-opt max-size=10m \
# --log-opt max-file=10 \
# --name age_gender_pred_in_3090 \
# raidavid/age_gender_pred_in_3090 \
# /bin/bash -c "export FLASK_APP=app.py && export FLASK_ENV=development && flask run  --host=0.0.0.0"