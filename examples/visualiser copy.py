import leap
import numpy as np
import cv2
import csv, os ,time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

_TRACKING_MODES = {
    leap.TrackingMode.Desktop: "Desktop",
    leap.TrackingMode.HMD: "HMD",
    leap.TrackingMode.ScreenTop: "ScreenTop",
}




class Canvas:
    def __init__(self):
        self.name = "Visualiser"
        self.screen_size = [500, 700]
        self.hands_colour = 	(0, 0, 255)
        self.font_colour = (0, 255, 44)
        self.hands_format = "Skeleton"
        self.output_image = np.zeros((self.screen_size[0], self.screen_size[1], 3), np.uint8)
        self.tracking_mode = None

        self.drawingMode = False
        self.x1, self.z1 = 0,0
        self.ImageCanvas = np.zeros((self.screen_size[0], self.screen_size[1], 3), np.uint8)
        self.drawColor = (141, 43, 193)
        self.brushThickness = 5
        self.smooth = 3
        self.position = (0,0)
        self.clearCanvas = False
        self.actual_position = (0,0,0)
        self.Current_time = 0

    def set_tracking_mode(self, tracking_mode):
        self.tracking_mode = tracking_mode
        
    def toggle_hands_format(self):
        self.hands_format = "Dots" if self.hands_format == "Skeleton" else "Skeleton"
        print(f"Set hands format to {self.hands_format}")

    def get_joint_position(self, bone):
        if bone:
            return int(bone.x + (self.screen_size[1] / 2)), int(bone.z + (self.screen_size[0] / 2))
        else:
            return None
    def get_Fingertip_position(self, bone):
        if bone:
            return bone.x,bone.y,-bone.z
        else:
            return None
    def render_hands(self, event):
        # header = ['x', 'y', 'z']
        # csv_file_path = 'output.csv'
        # file_exists = os.path.isfile(csv_file_path)
        # if not file_exists:
        #     csv_writer.writerow(header)
        # Clear the previous image
        self.output_image[:, :] = 0
        cv2.putText(
            self.output_image,
            f"Tracking Mode: {_TRACKING_MODES[self.tracking_mode]}",
            (10, self.screen_size[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            self.font_colour,
            1,
        )

        if len(event.hands) == 0:
            return

        if len(event.hands) > 1:
                    return

        for i in range(0, len(event.hands)):
            hand = event.hands[i]
            for index_digit in range(0, 5):
                digit = hand.digits[index_digit]
                for index_bone in range(0, 4):
                    bone = digit.bones[index_bone]
                    if (hand.index.is_extended and hand.middle.is_extended==1 and hand.ring.is_extended==1 and hand.pinky.is_extended==0):
                        self.clearCanvas = True

                    if (hand.index.is_extended and hand.middle.is_extended==0 ):
                        self.drawingMode = True
                        x2,z2 = self.get_joint_position(hand.index.distal.next_joint)
                        self.position = (x2,z2)
                        self.actual_position=self.get_Fingertip_position(hand.index.distal.next_joint)
                        self.Current_time = event.timestamp
                        # cv2.circle(self.output_image, (x2,z2), 5, self.drawColor, -1)
                        
                        
                        # header = ['x', 'y', 'z']
                        # csv_file_path = 'output.csv'
                        # file_exists = os.path.isfile(csv_file_path)
                        # with open(csv_file_path, 'a', newline='') as csv_file:
                        #     # Create a CSV writer
                        #     csv_writer = csv.writer(csv_file)

                        #     if not file_exists:
                        #         csv_writer.writerow(header)

                        #     # Write data line by line
                        #     X,Y,Z = self.get_Fingertip_position(hand.index.distal.next_joint)
                        #     row = [X,Y,Z]
                        #     csv_writer.writerow(row)
            
                        cv2.putText(
                            self.output_image,
                            "Drawing Mode: Index Finger",
                            (10, self.screen_size[0] - 25),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            self.font_colour,
                            1,
                        )
                    else: self.drawingMode = False
                        # # smoothening
                        # x2 = self.x1 + (x2 - self.x1) // self.smooth
                        # z2 = self.z1 + (z2 - self.z1) // self.smooth

                    if (hand.index.is_extended and hand.middle.is_extended ):
                        self.drawingMode = False
                        self.x1, self.z1 = 0, 0
                        self.position = (0,0)
                        self.Current_time=0
                        self.actual_position = (0,0,0)
                        cv2.putText(
                            self.output_image,
                            "Non Drawing Mode",
                            (10, self.screen_size[0] - 25),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            self.font_colour,
                            1,
                        )
                   



class TrackingListener(leap.Listener):
    def __init__(self, canvas):
        self.canvas = canvas

    def on_connection_event(self, event):
        pass

    def on_tracking_mode_event(self, event):
        self.canvas.set_tracking_mode(event.current_tracking_mode)
        print(f"Tracking mode changed to {_TRACKING_MODES[event.current_tracking_mode]}")

    def on_device_event(self, event):
        try:
            with event.device.open():
                info = event.device.get_info()
        except leap.LeapCannotOpenDeviceError:
            info = event.device.get_info()

        print(f"Found device {info.serial}")

    def on_tracking_event(self, event):
        self.canvas.render_hands(event)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d') 

def animate(i):
    header1 = "x"
    header2 = "y"
    header3 = "z"
    file_exists = os.path.isfile('output.csv')
    if not file_exists:
        time.sleep(100)
    data = pd.read_csv('output.csv')
    x = data[header1]
    y = data[header2]
    z = data[header3]

    plt.cla()

    ax.plot3D(x, z, y, 'red')

ani = FuncAnimation(plt.gcf(), animate, interval=50)

def main():
    
    canvas = Canvas()

    tracking_listener = TrackingListener(canvas)

    connection = leap.Connection()
    connection.add_listener(tracking_listener)

    running = True

    with connection.open():
        connection.set_tracking_mode(leap.TrackingMode.Desktop)        
        plt.tight_layout()
        plt.show()
         
        while running:
            if(canvas.clearCanvas):
                canvas.clearCanvas = False
                df = pd.read_csv('output.csv')
                df = df.head(1)
                df.to_csv('output.csv', index=False)
                df = pd.read_csv('output.csv', nrows=1)

                
            




if __name__ == "__main__":
    main()
