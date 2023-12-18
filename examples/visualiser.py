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
        self.screen_size = [600, 900]
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
            return int(bone.x + (self.screen_size[1] / 2)), (-int(bone.y) +int (self.screen_size[1] / 2) ) 
        
    def get_Fingertip_position(self, bone):
        if bone:
            return bone.x,bone.y,-bone.z
        else:
            return None
    # def get_fingertip_position(self, event):
    #     if len(event.hands) == 0:
    #         return
    #     for i in range(0, len(event.hands)):
    #         hand = event.hands[i]
    #         for index_digit in range(0, 5):
    #             digit = hand.digits[index_digit]
    #             for index_bone in range(0, 4):
    #                 bone = digit.bones[index_bone]
    #                 if (hand.index.is_extended and hand.middle.is_extended==0 ):
    #                     return self.get_joint_position(hand.index.distal.next_joint)
    def render_hands(self, event):
        
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
            self.drawingMode = False
            self.x1, self.z1 = 0, 0
            self.position = (0,0)
            return

        if len(event.hands) > 1:
            self.drawingMode = False
            self.x1, self.z1 = 0, 0
            self.position = (0,0)
            return

        for i in range(0, len(event.hands)):
            hand = event.hands[i]
            for index_digit in range(0, 5):
                digit = hand.digits[index_digit]
                for index_bone in range(0, 4):
                    bone = digit.bones[index_bone]
                    x3,z3 = self.get_joint_position(hand.index.distal.next_joint)
                    x4,z4 = self.get_joint_position(hand.middle.distal.next_joint)
                    
                    if (hand.index.is_extended and hand.middle.is_extended==1 and hand.ring.is_extended==1 and hand.pinky.is_extended==0):
                        self.clearCanvas = True

                    if ((hand.index.is_extended and hand.middle.is_extended==0 )):
                        self.drawingMode = True
                        x2,z2 = self.get_joint_position(hand.index.distal.next_joint)
                        self.position = (x2,z2)
                        self.actual_position=self.get_Fingertip_position(hand.index.distal.next_joint)
                        self.Current_time = event.timestamp
                        cv2.circle(self.output_image, (x2,z2), 5, self.drawColor, -1)
                        
                        
                        # header = ['x', 'y', 'z']
                        # csv_file_path = 'output.csv'
                        # with open(csv_file_path, 'a', newline='') as csv_file:
                        #     # Create a CSV writer
                        #     csv_writer = csv.writer(csv_file)

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
                    if self.hands_format == "Dots":
                        prev_joint = self.get_joint_position(bone.prev_joint)
                        next_joint = self.get_joint_position(bone.next_joint)
                        if prev_joint:
                            cv2.circle(self.output_image, prev_joint, 2, self.hands_colour, -1)

                        if next_joint:
                            cv2.circle(self.output_image, next_joint, 2, self.hands_colour, -1)

                    if self.hands_format == "Skeleton":
                        
                        wrist = self.get_joint_position(hand.arm.next_joint)
                        elbow = self.get_joint_position(hand.arm.prev_joint)
                        if wrist:
                            cv2.circle(self.output_image, wrist, 3, self.hands_colour, -1)

                        if elbow:
                            cv2.circle(self.output_image, elbow, 3, self.hands_colour, -1)

                        if wrist and elbow:
                            cv2.line(self.output_image, wrist, elbow, self.hands_colour, 2)

                        bone_start = self.get_joint_position(bone.prev_joint)
                        bone_end = self.get_joint_position(bone.next_joint)

                        if bone_start:
                            cv2.circle(self.output_image, bone_start, 3, self.hands_colour, -1)

                        if bone_end:
                            cv2.circle(self.output_image, bone_end, 3, self.hands_colour, -1)

                        if bone_start and bone_end:
                            cv2.line(self.output_image, bone_start, bone_end, self.hands_colour, 2)

                        if ((index_digit == 0) and (index_bone == 0)) or (
                            (index_digit > 0) and (index_digit < 4) and (index_bone < 2)
                        ):
                            index_digit_next = index_digit + 1
                            digit_next = hand.digits[index_digit_next]
                            bone_next = digit_next.bones[index_bone]
                            bone_next_start = self.get_joint_position(bone_next.prev_joint)
                            if bone_start and bone_next_start:
                                cv2.line(
                                    self.output_image,
                                    bone_start,
                                    bone_next_start,
                                    self.hands_colour,
                                    2,
                                )

                        if index_bone == 0 and bone_start and wrist:
                            cv2.line(self.output_image, bone_start, wrist, self.hands_colour, 2)


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
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d') 

# def animate(i):
#     header1 = "x"
#     header2 = "y"
#     header3 = "z"
#     file_exists = os.path.isfile('output.csv')
#     if not file_exists:
#         time.sleep(100)
#     data = pd.read_csv('output.csv')
#     x = data[header1]
#     y = data[header2]
#     z = data[header3]

#     plt.cla()

#     ax.plot3D(x, z, y, 'red')

# ani = FuncAnimation(plt.gcf(), animate, interval=50)

def main():
    
    canvas = Canvas()

    print(canvas.name)
    print("")
    print("Press <key> in visualiser window to:")
    print("  x: Exit")
    print("  h: Select HMD tracking mode")
    print("  s: Select ScreenTop tracking mode")
    print("  d: Select Desktop tracking mode")
    print("  f: Toggle hands format between Skeleton/Dots")

    tracking_listener = TrackingListener(canvas)

    connection = leap.Connection()
    connection.add_listener(tracking_listener)

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
        canvas.set_tracking_mode(leap.TrackingMode.Desktop)
        imgCanvas = np.zeros((canvas.screen_size[0], canvas.screen_size[1], 3), np.uint8)
        
        # plt.tight_layout()
        # plt.show()
        x1,z1 = 0, 0  

        while running:
            frame = canvas.output_image
            if(canvas.clearCanvas):
                imgCanvas = np.zeros((canvas.screen_size[0], canvas.screen_size[1], 3), np.uint8)
                canvas.clearCanvas = False
                
            
            if(canvas.drawingMode==False):
                # Actual_x,Actual_y,Actual_z = 0,0,0
                # canvas.actual_position = (0,0,0)
                # canvas.Current_time = 0
                # Current_time = 0
                x1,z1=0,0
                canvas.position = (0,0)
            
            # cv2.imshow("Imagecanvas", canvas.ImageCanvas)
            # cv2.imshow("canvas3", canvas3)

            x2,z2 = canvas.position
            # Actual_x2,Actual_y2,Actual_z2 = canvas.actual_position
            # Current_time_2 = canvas.Current_time
            if(x1==0 and z1==0):
                x1 = x2
                z1 = z2
            # if(Current_time==0):
            #     Current_time = Current_time_2
            # if(Actual_x==0):
            #     Actual_x,Actual_y,Actual_z = Actual_x2,Actual_y2,Actual_z2
            # if(Current_time_2!=Current_time):
                  
            #     velocity_x = ((Actual_x2-Actual_x)/(Current_time_2-Current_time))*100000
            #     print(velocity_x)
            cv2.line(imgCanvas, (x1, z1), (x2, z2), canvas.drawColor, canvas.brushThickness)
                        

            # update previous point
            x1, z1 = x2, z2
            

            
            imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
            _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
            imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
            frame = cv2.bitwise_and(frame, imgInv)
            frame = cv2.bitwise_or(frame, imgCanvas)

            # Show image
            cv2.imshow(canvas.name, frame)



            key = cv2.waitKey(1)

            if key == ord("x"):
                break
            elif key == ord("h"):
                connection.set_tracking_mode(leap.TrackingMode.HMD)
            elif key == ord("s"):
                connection.set_tracking_mode(leap.TrackingMode.ScreenTop)
            elif key == ord("d"):
                connection.set_tracking_mode(leap.TrackingMode.Desktop)
            elif key == ord("f"):
                canvas.toggle_hands_format()


if __name__ == "__main__":
    main()
