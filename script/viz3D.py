import rclpy
from rclpy.node import Node
from vision_msgs.msg import Detection3DArray
from visualization_msgs.msg import Marker, MarkerArray

class Detection3DVisualizer(Node):
    def __init__(self):
        super().__init__('detection3d_visualizer')
        self.subscription = self.create_subscription(
            Detection3DArray,
            'bbox',
            self.listener_callback,
            10)
        self.publisher = self.create_publisher(MarkerArray, 'visualization_marker_array', 10)
        
    def listener_callback(self, msg):
        marker_array = MarkerArray()
        i = 0
        for detection in msg.detections:
            marker = Marker()
            marker.header = msg.header
            marker.ns = 'detections'
            # marker.id = detection.id
            marker.id = i
            marker.type = Marker.CUBE
            marker.action = Marker.ADD
            marker.pose = detection.bbox.center
            marker.scale.x = detection.bbox.size.x
            marker.scale.y = detection.bbox.size.y
            marker.scale.z = detection.bbox.size.z
            marker.color.a = 0.5
            marker.color.r = 1.0
            marker.color.g = 0.0
            marker.color.b = 0.0
            marker.lifetime = rclpy.duration.Duration(seconds = 0.1).to_msg()
            marker_array.markers.append(marker)
            i+=1
        
        self.publisher.publish(marker_array)

def main(args=None):
    rclpy.init(args=args)
    node = Detection3DVisualizer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
