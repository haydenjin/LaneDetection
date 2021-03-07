## About The Project

OpenCv is a multi language library consisting of many functions which are commonly used in computer vision. 
Computer vision is used in many different programs now a days, including but not limited to facial recognition, imaging technologies, and image detection.

As I have already said above, using openCv, this algorithm recognizes and outputs lane lines in real time when it is fed a video or image. 
It first converts the image into grayscale, which gives every pixel in the image a color value ranging from 0 to 255. 
The values of all the pixels are then stored in an array the height and width of the image. 

The algorithm then compares and finds drastic changes in color value, which could potentially indicate that there is a line of some sort. 
We then must give the computer a general location for where it should be looking for the lanes, say a triangle shape in the middle of the screen. 

Finally, the algorithm matches the pixels where there were great color differences and developers that into a singular line. 
Obviously there is a lot more to how the algorithm is actually working, but this is the general gist of it. Please see below for the initial video, and final video.


### Built With

* []()Python
* []()Pycharm
* []()External Libraries



## Getting Started

1. Download the source files 
2. Run the program to see the program in action 

<!-- CONTACT -->
## Contact

Hayden Jin - haydenjin@gmail.com - haydenjin.com
