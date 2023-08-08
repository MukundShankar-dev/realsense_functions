import pyrealsense2 as rs
import numpy as np

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
# Stream parameters for non-L500 model realsense sensors
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
cfg = pipeline.start(config)


frames = pipeline.wait_for_frames()
depth_frame = frames.get_depth_frame()
color_frame = frames.get_color_frame()

# Intrinsics & Extrinsics: Method 1
depth_intrinsics = depth_frame.profile.as_video_stream_profile().intrinsics
color_intrinsics = color_frame.profile.as_video_stream_profile().intrinsics
depth_to_color_extrinsic = depth_frame.profile.get_extrinsics_to(color_frame.profile)


print("Depth Intrinsics:", depth_intrinsics)
print()
print("Color Intrinsics:", color_intrinsics)
print()
print("Depth to color Intrinsics:", depth_to_color_extrinsic)

# Intrinsics: Method 2
# Get the depth stream
# profile = cfg.get_stream(rs.stream.depth)

# Get intrinsic matrix
# intrinsics = profile.as_video_stream_profile().get_intrinsics()
# print("intrinsics:", intrinsics)

# Stop streaming
pipeline.stop()