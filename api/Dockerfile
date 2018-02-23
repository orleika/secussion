FROM python:3

RUN apt update \
    && apt upgrade -y \
    && apt install -y \
    build-essential \
    gfortran \
    libblas-dev \
    liblapack-dev \
    libxft-dev \
    libgtk-3-dev \
    libX11-xcb-dev \
    && rm -rf /var/lib/apt/lists/* \
    && echo 'export LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"' >> ~/.bash_profile \
    && . ~/.bash_profile \
    && cd ~ && git clone --depth 1 https://github.com/taku910/mecab.git \
    && cd mecab/mecab && ./configure  --enable-utf8-only \
    && make \
    && make check \
    && make install \
    && cd ../mecab-ipadic && ./configure --with-charset=utf8 \
    && make \
    && make install \
    && cd ~ && git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git \
    && cd mecab-ipadic-neologd && ./bin/install-mecab-ipadic-neologd -n -y \
    && cd ~ && wget https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz \
    && tar -zxvf ./geckodriver-v0.19.1-linux64.tar.gz \
    && cp geckodriver /usr/bin \
    && pip3 install --upgrade pyzmq --install-option="--zmq=bundled" \
    && pip3 install --upgrade \
    numpy \
    scipy \
    scikit-learn \
    matplotlib \
    pandas \
    mecab-python3 \
    neologdn \
    selenium \
    BeautifulSoup4 \
    lxml \
    mysql-connector-python-rf \
    janome \
    joblib \
    flask \
    requests \
    chardet \
    html5lib \
    && cd /usr/local && wget http://ftp.mozilla.org/pub/firefox/releases/59.0b11/linux-x86_64/ja/firefox-59.0b11.tar.bz2 \
    && tar xvjf firefox-59.0b11.tar.bz2 \
    && ln -s /usr/local/firefox/firefox /usr/bin/firefox

ENV LD_LIBRARY_PATH /usr/local/lib:$LD_LIBRARY_PATH

VOLUME /work
WORKDIR /work

CMD ["python3"]
