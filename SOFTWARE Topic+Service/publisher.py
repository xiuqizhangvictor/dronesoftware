import rclpy
from rclpy.node import Node #import node class

from std_msgs.msg import String #builtin structure type that node will use for message
#I thought im in c++ for a second lol


class MinimalPublisher(Node): #a subclass of node, I literally leant OOP a day ago from cs61a

    def __init__(self): 
        super().__init__('minimal_publisher') #calls the node class constructor and give it a name
        self.publisher_ = self.create_publisher(String, 'topic', 10) #use the imported type, queue size is 10
        #queue is a QoS requirement, if the subscriber is not recieving fast enough, this caps it
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback) #calls back every 0.5 seconds
        self.i = 0

    def timer_callback(self): #creates the hello world message with the timer appended to publish
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data) #prints it into the console
        self.i += 1


def main(args=None): #are we in python or c++??? main function????
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher) #spin is the func used to do the callback

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__': #this is to ensure that it execute once run, not execute once imported
    main()