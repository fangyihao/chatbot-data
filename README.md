# chatbot-data
Chatbot-data is a python project that extracts question-answer pairs from raw resources such as wikipedia, open-subtitles, particularly for chatbot and QA usages.

## Installation

### 1. Download and install Oracle Java 1.8+:

    sudo apt install software-properties-common
    sudo add-apt-repository ppa:webupd8team/java 
    sudo apt-get update
    sudo apt-get install oracle-java8-installer

### 2. Install python3

    sudo apt-get update
    sudo apt install python3
    sudo apt-get install python3-tk
    sudo apt install python3-pip

### 3. Install numpy, nltk and download the punkt tokenizer

    sudo pip install numpy nltk   
    python
    >> import nltk
    >> nltk.download('punkt')

### 4. Download and unzip stanford-parser, stanford-ner and stanford-postagger

    curl -O http://nlp.stanford.edu/software/stanford-parser-full-2015-12-09.zip
    curl -O http://nlp.stanford.edu/software/stanford-ner-2015-12-09.zip 
    curl -O http://nlp.stanford.edu/software/stanford-postagger-full-2015-12-09.zip
    sudo unzip stanford-parser-full-2015-12-09.zip -d /usr/share/stanford-nlp/
    sudo unzip stanford-ner-2015-12-09.zip -d /usr/share/stanford-nlp/
    sudo unzip stanford-postagger-full-2015-12-09.zip -d /usr/share/stanford-nlp/
  
### 5. Setup the CLASSPATH environment variable
  
    export CLASSPATH=/usr/share/stanford-nlp/stanford-ner-2015-12-09/stanford-ner.jar:/usr/share/stanford-nlp/stanford-postagger-full-2015-12-09/stanford-postagger.jar:/usr/share/stanford-nlp/stanford-parser-full-2015-12-09/stanford-parser.jar:/usr/share/stanford-nlp/stanford-parser-full-2015-12-09/stanford-parser-3.6.0-models.jar:/usr/share/stanford-nlp/stanford-ner-2015-12-09/classifiers/english.all.3class.distsim.crf.ser.gz:/usr/share/stanford-nlp/stanford-ner-2015-12-09/classifiers/english.muc.7class.distsim.crf.ser.gz:/usr/share/stanford-nlp/stanford-postagger-2015-12-09/models/english-left3words-distsim.tagger
