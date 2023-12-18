"""Prints the palm position of each hand, every frame. When a device is 
connected we set the tracking mode to desktop and then generate logs for 
every tracking frame received. The events of creating a connection to the 
server and a device being plugged in also generate logs. 
"""

import leap
import time
import csv, os
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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
        attributes = dir(event)

        # # Print each attribute and its value
        # for attribute in attributes:
        #     # Exclude attributes that start with '__' (internal attributes)
        #     if not attribute.startswith('__'):
        #         value = getattr(event, attribute)
        #         print(f"{attribute}: {value}")
        
        # print(f"Frame {event.tracking_frame_id} with {len(event.hands)} hands.")

            


        for hand in event.hands:
            if(len(event.hands)==0 or len(event.hands)>1):
               return
                
            
            header = ['x', 'y', 'z']
            csv_file_path = 'output.csv'
        
            with open(csv_file_path, 'a', newline='') as csv_file:
                # Create a CSV writer
                csv_writer = csv.writer(csv_file)

                # Write data line by line
                
                if(len(event.hands)==1):
                    row = [hand.index.distal.next_joint.x,hand.index.distal.next_joint.y,-hand.index.distal.next_joint.z]
                    csv_writer.writerow(row)
            #--------------
            # if hand.grab_strength > 0.5:
                # print("grab_strength: 1")
                # print(f"grab_strength strength: {hand.grab_strength}")
            # --------------

            #--------------

            # --------------
            # attributes = dir(hand.palm)

            # # Print each attribute and its value
            # for attribute in attributes:
            #     # Exclude attributes that start with '__' (internal attributes)
            #     if not attribute.startswith('__'):
            #         value = getattr(hand.palm, attribute)
            #         print(f"{attribute}: {value}")
            hand_type = "left" if str(hand.type) == "HandType.Left" else "right"
            # print(
            #     f"Hand id {hand.id} is a {hand_type} hand with position ({hand.palm.position.x}, {hand.palm.position.y}, {hand.palm.position.z})."
            # )

            # The position of the end of the bone closest to the finger tip
            # print(
            #     f" Index Finger End with position : X :{hand.index.distal.next_joint.x}, Y : {hand.index.distal.next_joint.y} Z : {hand.index.distal.next_joint.z}."
            # )

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d') 

def animate(i):
    header1 = "x"
    header2 = "y"
    header3 = "z"

    data = pd.read_csv('output.csv')
    x = data[header1]
    y = data[header2]
    z = data[header3]

    plt.cla()

    ax.plot3D(x, z, y, 'red')

ani = FuncAnimation(plt.gcf(), animate, interval=50)
    #plt.legend(loc='upper left')
    #plt.tight_layout()
def main():
    my_listener = MyListener()

    connection = leap.Connection()
    connection.add_listener(my_listener)

    running = True
    
    header = ['x', 'y', 'z']
    csv_file_path = 'output.csv'
    file_exists = os.path.isfile(csv_file_path)
    with open(csv_file_path, 'a', newline='') as csv_file:
        # Create a CSV writer
        csv_writer = csv.writer(csv_file)

        if not file_exists:
            csv_writer.writerow(header)
            
    with connection.open():
        connection.set_tracking_mode(leap.TrackingMode.Desktop)
        plt.tight_layout()
        plt.show()
        while running:
            time.sleep(1)


if __name__ == "__main__":
    main()
