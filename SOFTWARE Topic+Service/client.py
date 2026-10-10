import sys #whats this for
#we have alot of stuff happening here
from example_interfaces.srv import AddTwoInts #service type
import rclpy
from rclpy.node import Node #node class


class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints') #same type and name with service node
        while not self.cli.wait_for_service(timeout_sec=1.0): #available once per second
            self.get_logger().info('service not available, waiting again...')
        self.req = AddTwoInts.Request() #creates the request object

    def send_request(self, a, b): #this is the structure of the request, 2 numbers
        self.req.a = a
        self.req.b = b
        return self.cli.call_async(self.req)


def main():
    rclpy.init()

    minimal_client = MinimalClientAsync() #takes the object, sent it, spin until its done
    future = minimal_client.send_request(int(sys.argv[1]), int(sys.argv[2]))
    rclpy.spin_until_future_complete(minimal_client, future)
    response = future.result() 
    minimal_client.get_logger().info(
        'Result of add_two_ints: for %d + %d = %d' %
        (int(sys.argv[1]), int(sys.argv[2]), response.sum)) #logs the results once done and display

    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()