# selfdrivingrccar
 
 The car's set up <br>
![Image of Yaktocat](https://user-images.githubusercontent.com/41195974/72822426-18fab300-3c98-11ea-800a-dc424d739ce2.jpeg)\


<b> Introduction </b> <br>
This project implements autonomous driving feature to a remote-controlled car for improved safety concern. The main purpose of this project is to demonstrate the usability of artificial intelligence in the field of transportation and to demonstrate the concept of machine learning and neural networking.

<b>Development Approach</b> <br>
The development of our project has been conducted in two phases: hardware and software.

Hardware Development <br>
Raspberry Pi 3 controls the motors driving the car itself and with its powerful processor, analyzes the image stream supplied by the Pi Camera and then decides on how the car should operate on the required conditions. The Raspberry Pi is connected with a l293d motor driver though which it drives the motors of the car. It is powered with the help of portable power bank which is attached to the car itself. The Raspberry Pi in turn provides the necessary logic to control the motor from its GPIO pins.

<b>Methodology </b> <br>
The system consists of three major parts: input unit (pi camera), processing unit(computer), control unit (raspberry pi and motors).

<b>Input unit</b> <br>
A raspberry pi attached with pi camera wich can be used to collect input data. Script run on raspberry pi for streaming video and via local Wi-Fi connection.

<b>Processing unit</b> <br>
The processing unit handles following tasks:

<b>Receiving video from raspberry pi</b> <br>
Using the input video data to train convolutional neural network and predict control output (i.e. steer)
Detect objects and calculate distance.

<b>Control unit</b> <br>
The car is controlled using raspberry pi. First the input is sent manually from pc (this trains the neural network). Then, the predicted input from neural network is used to control the car autonomously.

<b>Neural Network</b> <br>
Neural networks are the most advanced and efficient machine learning algorithms that mimic human brain. In the neural network that we will be using, the input frames of images will be taken as input nodes and steering controls (forward, reverse, left, right) will be output labels.

<b>Object detection</b> <br>
To detect objects, Haar feature-based cascade classifiers can be used. Since each object requires its own classifier and follows the same process in training and detection, this project only focused on stop sign and traffic light detection. Thus, can be done easily in OpenCV

<h><b>Difficulties Faced </b></h> <br>
<b>Training Mode</b> <br>
1)Stream Camera in Raspberry Pi 3
```
python RaspberryPi/camstream.py
```
2)Start Flask Rest API in Raspberry Pi 3
```
python RaspberryPi/control.py
```
3)Manual Drive the RC Car from PC
```
python Computer/manual_TRYwithnpz.py
```
<error> Every time I run the above files I get this error Is there any way <br> to solve this?? </error> <br>
<i>--------ERROR--------</i>
ConnectionError: HTTPConnectionPool(host='192.168.0.31', port=5000): Max retries exceeded with url: /messages?data=x (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x000001D456A07E08>: Failed to establish a new connection: [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond'))
