# Realsense Camera Processing

## About
This library is made primarily to work with the Intel RealSense D435i camera. If working with different cameras, please check the dimensions of video streaming and adjust the relevant parameters in the corresponding files as needed.

Note that for the following, you will need to have intel's pyrealsense library, numpy, and opencv installed. 
## Requirements
Python 3.6+

## Usage
Copy the `camera_processor.py` file into your directory. At the top of your python file, use `from camera_processor import CameraProcessor`. Then, create an object of the class - for example, `obj = CameraProcessor()`.

## Functions
### `rgb_feed`
Calling `obj.rgb_feed` will open a cv2 window displaying the color video feed from the camera.
### `depth_feed`
Calling `obj.depth_feed` will open a cv2 window displaying the depth video feed from the camera, with a color map applied to it to make it more understandable.
### `rgb_depth_feed`
`obj.rgb_depth_feed` will display an cv2 window with the color and depth feeds next to each other.
### `get_depth_intrinsics`
Will return the depth intrinsics from the camera, using the Intel SDK's own type for intrinsic data.
### `project_point`
To be used, the x, y, and z coordinates of a point will need to be passed into this function - for example, `obj.project_point(1, 2, 3)` will project the point [1, 2, 3] (in meters from the camera) to the image displayed by the camera. This function takes in a point in space and returns pixel coordinates for an image.
### `deproject_pixel`
Opens a window where the user can click a point in the image, and will then return the distance data to the clicked point as a coordinate in space in [x, y, z] format (meters from camera). The relevant coordinates calculated will also be printed to the console.
## Links to requirements
[Intel realsense SDK](https://www.intelrealsense.com/sdk-2/)

[Intel pyrealsense2 library](https://pypi.org/project/pyrealsense2/)

[numpy](https://numpy.org/)

[openCV](https://pypi.org/project/opencv-python/)


