import pyrealsense2 as rs
import numpy as np
import cv2

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))


# Stream parameters for non-L500 model realsense sensors
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

try:
    while True:

        # Wait for a depth and color frames, then obtain from the sensor
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not color_frame or not depth_frame:
            continue

        # Convert image to numpy array
        color_image = np.asanyarray(color_frame.get_data())

        color_colormap_dim = color_image.shape
        images = color_image

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_NORMAL)
        cv2.imshow('RealSense', images)

        # Get depth intrisic values from camera and set intrinsics model (based on camera info)
        depth_intrinsics = depth_frame.profile.as_video_stream_profile().intrinsics
        depth_intrinsics.model = rs.distortion.brown_conrady
        print('intrinsics: ' + str(depth_intrinsics))

        # Point in 3D (Units are x-y-z in meters, and the origin is the center of the image in 3D)
        point = [1,1,5]

        # Gives a projection onto 2D (units are in pixels, so (0,0) is the center of the top-left pixel of the image)
        projected_point = rs.rs2_project_point_to_pixel(depth_intrinsics, point)

        print('projected point: ', projected_point)

        # Extract x and y coordinates from the projection
        x_coord = int(projected_point[0])
        y_coord = int(projected_point[1])

        print("x: " + str(x_coord) + ", y: " + str(y_coord))

        # Overlay a circle of the pixel on the image after projecting the point in space
        image = cv2.circle(images, (x_coord, y_coord), 1, (255, 0, 0), 2)
        cv2.imshow('RealSense', image)


        cv2.waitKey(1)



finally:

    # Stop streaming
    pipeline.stop()