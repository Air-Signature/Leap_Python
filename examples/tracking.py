"""Prints the palm position of each hand, every frame. When a device is 
connected we set the tracking mode to desktop and then generate logs for 
every tracking frame received. The events of creating a connection to the 
server and a device being plugged in also generate logs. 
"""

import leap
import time
from leap import datatypes as ldt


def location_end_of_finger(hand: ldt.Hand, digit_idx: int) -> ldt.Vector:
    digit = hand.digits[digit_idx]
    return digit.distal.next_joint


def sub_vectors(v1: ldt.Vector, v2: ldt.Vector) -> list:
    return map(float.__sub__, v1, v2)


def fingers_pinching(middle: ldt.Vector, index: ldt.Vector):
    diff = list(map(abs, sub_vectors(middle, index)))

    if diff[0] < 20 and diff[1] < 20 and diff[2] < 20:
        return True, diff
    else:
        return False, diff

class MyListener(leap.Listener):
    def on_connection_event(self, event):
        print("Connected")

    def on_device_event(self, event):
        try:
            with event.device.open():
                info = event.device.get_info()
        except leap.LeapCannotOpenDeviceError:
            info = event.device.get_info()

        print(f"Found device {info.serial}")

    def on_tracking_event(self, event):
        # for hand in event.hands:
            # attributes = dir(hand.index.distal.rotation)

            #     # # Print each attribute and its value
            # for attribute in attributes:
            #     # Exclude attributes that start with '__' (internal attributes)
            #     if not attribute.startswith('__'):
            #         value = getattr(hand.index.distal.rotation, attribute)
            #         print(f"{attribute}: {value}")
        # print(f"Frame {event.tracking_frame_id} with {len(event.hands)} hands.")
        for hand in event.hands:
            
            attributes = dir(hand.arm)

            # # Print each attribute and its value
            for attribute in attributes:
                # Exclude attributes that start with '__' (internal attributes)
                if not attribute.startswith('__'):
                    value = getattr(hand.arm, attribute)
                    print(f"{attribute}: {value}")
            hand_type = "left" if str(hand.type) == "HandType.Left" else "right"
        #     print(
        #         f"Hand id {hand.id} is a {hand_type} hand with position ({hand.palm.position.x}, {hand.palm.position.y}, {hand.palm.position.z})."
        #     )
        
            middle = location_end_of_finger(hand, 2)
            index = location_end_of_finger(hand, 1)

            pinching, array = fingers_pinching(middle, index)
            pinching_str = "not pinching" if not pinching else "" + str("pinching")
            print(
                f"{hand_type} hand middle and index {pinching_str} with position diff ({array[0]}, {array[1]}, {array[2]})."
            )


def main():
    my_listener = MyListener()

    connection = leap.Connection()
    connection.add_listener(my_listener)

    running = True

    with connection.open():
        connection.set_tracking_mode(leap.TrackingMode.Desktop)
        while running:
            time.sleep(1)


if __name__ == "__main__":
    main()