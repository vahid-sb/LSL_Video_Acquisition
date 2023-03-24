LSL Video Acquisition
=====================
A lightweight script to add video streams from cameras and webcams as an input outlet to Lab Streaming Layer (LSL) library in python. 

Introduction
-------------
"The lab streaming layer (LSL) is a system for the unified collection of measurement time series in research experiments that handles both the networking, time-synchronization, (near-) real-time access as well as optionally the centralized collection, viewing and disk recording of the data". You can read all about it [here](https://labstreaminglayer.readthedocs.io/info/intro.html). Any device you use for your measurements can be defined as an output outlet for LSL. But let#s assume you want to run an experiment, and it is not possible to connect the device from which you show an stimulus to the participants in your experiment. Let's say you want to record EEG signals from people watching a video on a cinema screen. In such a case, for technical or non-technical reasons you might not be able to connect the video-projector to your LSL server. One solution in such a case is to use an external camera connected to your LSL-enabled computer, and capture the video from that camera to see what the spectator is seeing and then use the frame numbers from that video to define events in your EEG input. To do so, we need a code that enable us to use such a video feed as an input to the Lab Recorder software in LSL. 

Searching for such a software, I found [this solution](https://bitbucket.org/neatlabs/videoacq/src/master/) and tried to use it. But I faced two major problems while trying to use it. One is that it did not allow me to record from external cameras webcams, even though I tried different types and even though I checked and I knew they are OpenCV-enabled. The other, and this one still puzzles me, was that the internal webcam always was recorded in gray-scale. Not only when I run that library, but also when I use other other apps such as zoom. This was all tested on a Lenovo P71 laptop running Win10. And all the usual solutions to fix the webcam has failed so far, including completely uninstalling and then reinstalling it. 

Facing these issues, I decided to write a minimal script that can serve as an outlet for LSL to add a video stream to the Lab Recorder app in LSL ecosystem. All you need to do is to run the `LSL_video_capture.py` script, given the below mentioned dependencies. The `createOutlet` function in `LSL_video_capture.py` is adopted from the above-mentioned repository.

The only thing you might need to change is the variable `port_num` in the script, which specifies which of the available video-recording devices you want to use. To find out the port number, I have added another script called `check_available_port.py` that lists all available video input devices. Make sure no webcam/camera is in use by any app to make sure the infomratoin you get is accurate. Usually, internal webcam has an index of `0` and the first external webcam/camera is `1`. 

Currently, the output video file in saved in the same folder as the script. You can change that by changing the `dir_out` variable. When the input appears in Lab Recorder and when you start recording and save the results to an XDF file, the path to the video file is saved under desc variable in the stream saved in the XDF file. 

### Time Stamps

A note on the time stamps you find in the recorded stream in the XDF files: the values you see in the `time_stamps` array are in seconds, and anything after the decimal point is the fractions of the second. They are not date-time values formatted in any standard such as Unix time. So, when matching segments of different streams in each recording, you do not need to convert time stamp values, using libraries such as datetime in Python. You can use the values directly. 

This has generated some confusion among those who use the LSL platform and the related libraries, including this one. The LSL documentation is entirely silent on this simple but crucial fact, and I hope they are amended soon to avoid further confusion among some of the users of the library.  


Requirements
------------

 	"pylsl",
	"opencv-python",

  
Compatibility
-------------

This code is tested under Python 3.9.

License
-------
MIT License.


Author
-------

Written by [Vahid Samadi Bokharaie](https://www.vahid-sb.com).
