# SafePath
Our entry for Smart India Hackathon 2024.

This project aims to utilize AI tools integrated with App development to tackle the problem of Women Safety Analytics.

### Note : This project is just an attempt/idea and does not claim to be the solution of above.

## This is achieved in three steps:
1)  Using AI models to classify the number of males and females appearing in the camera feed.
2)  Determine the sex ratio as males/females.
3)  If higher than threshold (currently set to 1) , Notify the application user of potential danger.

# Team Members
1) Karan Malik (Team Leader)
2) Avneesh Kumar
3) Gokul Raj M
4) Yash Mohan
5) Sanmit Sarkar
6) Nishtha Garg




# Demonstration

![alt-text](https://github.com/avneesh10115/SafePath/blob/main/Demo/demo.gif)


# Models Used
1) Boundary Boxes Detection - YoloV8
2) Gender Detection on detected boxes - ResNet50

# External Dependencies
Python
  - Keras 2.13.1
  - Tensorflow 2.13.0
  - Numpy 1.26.4
  - OpenCV Python 4.11.0
  - Requests Module
  - Ultralytics 8.3.94
  - Flask 3.0.3

Flutter
  - location 5.0.0
  - http 0.13.4


# Installation

1) Install the required dependencies
   - For Python , Use `pip install -r requirements.txt`
   - For Flutter , Use `flutter pub get`

2) Clone the repository

# Usage

1) Initialize the Flask WebServer using commandline.
2) Start the Application.
3) Start train_resnet.py and supply it the camera feed.
   
# Scope of Improvement
1) Increase model efficiency and thus processing rate
2) Make App and WebServer independent.
3) Increase model accuracy.
