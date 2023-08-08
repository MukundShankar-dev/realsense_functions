# realsense_functions

## Descriptions of functions
This library is made primarily to work with the Intel RealSense D435i camera. If working with different cameras, please check the dimensions of video streaming and adjust the relevant parameters in the corresponding files as needed.

Note that for the following, you will need to have intel's pyrealsense library, numpy, and opencv installed. 

Running camera_feed.py will open a window displaying the rgb video stream and the color stream from the camera. Similarly, running depth_viewer.py will open a window containing the depth feed from the camera.

Running extrinsic_intrinsic.py will print the extrinsic and intrinsic matrices of the camera's depth and color streams, then the extrinsics from the depth to the color stream. These streams and parameters can be adjusted as necessary within the file by changing the used stream (starting from lines 14 and 16).

Running project_point.py will project a point (in xyz format, meters from origin, where the center of the image is the origin) to the camera feed, and give you pixel coordinates for that point in the image from the camera. (On running the file, this can be seen as a blue dot on the window) The projected point can be adjusted by changing the point variable on line 49.

The deproject_pixel file will open a window displaying the video stream from the camera. Then, you can click a point on the window, and the 3D coordinates (xyz, origin being at the center of the camera stream) will be printed in the console.

## Requirements
Intel realsense SDK
Intel pyrealsense2 library
numpy
openCV
