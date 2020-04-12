## Kinect-DepthData-recognition
# Task
  Recognize human conditional comands using Kinect DepthData.
  (We assume the management of some fictional executive body)
# Realization
  1) MainWindow.xaml.cs is used for getting Depth Data from Kinect. It sends to the server (server1.py) 
  a monochrom image (pixels array) and gets conditional comand to print on MainWindow.
  
  2) server1.py is just a server which gets an encoded array of bytes, decodes it to numpy.array and sends it to handler.
  
  3) handler.py interprets what comand human is showing.
# Comands
  Two hands up -- Forward step.
  
  Two hands down -- Backward step.
  
  One hand up, one down -- Right or Left. Depends on witch one is higher.
  
  Handler also sends text like: "Get clouser to the sensor" or "There is smth except you". 
  So you need to stand in font of it for about 2m, hands should be directed on Kinect and it prefers that nothing big is located near you.
  Best to stand near wall.
