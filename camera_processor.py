import pyrealsense2 as rs
import numpy as np
import cv2

class CameraProcessor:

    def __init__():
        pass

    def rgb_feed():
        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.color, 640, 480, rs.format.z16, 30)
        pipeline.start(config)

        try:
            while True:
                frames = pipeline.wait_for_frames()
                color_frame = frames.get_color_frame()
                color_image = np.asanyarray(color_frame.get_data())
                cv2.namedWindow('RealSense RGB Feed', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('RealSense RGB Feed', color_image)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    cv2.destroyAllWindows()
                    break
        finally:
            pipeline.stop()

    def depth_feed():
        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        pipeline.start(config)

        try:
            while True:
                frames = pipeline.wait_for_frames()
                depth_frame = frames.get_depth_frame()
                color_image = np.asanyarray(depth_frame.get_data())
                cv2.namedWindow('RealSense Depth Feed', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('RealSense Depth Feed', color_image)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    cv2.destroyAllWindows()
                    break
        finally:
            pipeline.stop()

    def rgb_depth_feed():
        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        pipeline.start(config)

        try:
            while True:
                frames = pipeline.wait_for_frames()
                depth_frame = frames.get_depth_frame()
                color_frame = frames.get_color_frame()
                if not depth_frame or not color_frame:
                    continue

                depth_image = np.asanyarray(depth_frame.get_data())
                color_image = np.asanyarray(color_frame.get_data())

                depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

                depth_colormap_dim = depth_colormap.shape
                color_colormap_dim = color_image.shape

                if depth_colormap_dim != color_colormap_dim:
                    resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
                    images = np.hstack((resized_color_image, depth_colormap))
                else:
                    images = np.hstack((color_image, depth_colormap))
                
                cv2.namedWindow('RealSense RGB and Depth Feed', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('RealSense RGB and Depth Feed', images)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    cv2.destroyAllWindows()
                    break

        finally:
            pipeline.stop()

    def get_depth_intrinsics(self):
        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        pipeline.start(config)
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        return depth_frame.profile.as_video_stream_profile.intrinsics

    def project_point(self, x: int, y: int, z: int):
        intrinsics = self.get_depth_intrinsics()
        point = [x, y, z]
        projected_point = rs.rs2_project_point_to_pixel(intrinsics, point)
        return projected_point

    def deproject_pixel(self):
        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        pipeline.start(config)

        def calculate_point(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_RBUTTONDOWN:
                depth = depth_frame.get_distance(x, y)
                point = rs.rs2_deproject_pixel_to_point(intrinsics, [x, y], depth)
                image = cv2.circle(color_image, (x, y), 1, (255, 0, 0), 2    )
                cv2.imshow('RealSense', image)
                print("deprojected point: " + str(point))
                return point
        try:
            while True:
                frames = pipeline.wait_for_frames()
                depth_frame = frames.get_depth_frame()
                color_frame = frames.get_color_frame()
                if not color_frame or not depth_frame:
                    continue

                color_image = np.asanyarray(color_frame.get_data())

                cv2.namedWindow('RealSense', cv2.WINDOW_NORMAL)
                cv2.imshow('RealSense', color_image)
                intrinsics = self.get_depth_intrinsics
                cv2.setMouseCallback('RealSense', calculate_point)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    cv2.destroyAllWindows()
                    break
        finally:
            pipeline.stop()