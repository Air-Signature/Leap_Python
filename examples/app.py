import leap
import numpy as np
import cv2
import csv
from leap import datatypes as ldt

_TRACKING_MODES = {
    leap.TrackingMode.Desktop: "Desktop",
    leap.TrackingMode.HMD: "HMD",
    leap.TrackingMode.ScreenTop: "ScreenTop",
}


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
        
class Canvas:
    def __init__(self):
        self.name = "Visualiser"
        self.screen_size = [600, 900]
        self.hands_colour = (0, 0, 255)
        self.font_colour = (0, 255, 44)
        self.hands_format = "Skeleton"
        self.output_image = np.zeros((self.screen_size[0], self.screen_size[1], 3), np.uint8)
        self.tracking_mode = None

        self.drawingMode = False
        self.x1, self.y1 = 0,0
        self.ImageCanvas = np.zeros((self.screen_size[0], self.screen_size[1], 3), np.uint8)
        self.drawColor = (141, 43, 193)
        self.brushThickness = 4
        self.smooth = 3
        self.position = (0,0)
        self.clearCanvas = False
        self.actual_position = (0,0,0)
        self.frameRate = 1
        self.palm_velocity = 0
        self.palm_Position = 0
        self.hand_grab_angle = 0
        self.hand_grab_strength = 0
        self.confidence = 0
        self.fingertip_rotation = 0
        self.arm_position = 0
        self.frame_id=0
        

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
        
# Added new Commit
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
            self.x1, self.y1 = 0, 0
            self.position = (0,0)
            self.actual_position = (0,0,0)
            return

        if len(event.hands) > 1:
            self.drawingMode = False
            self.x1, self.y1 = 0, 0
            self.position = (0,0)
            self.actual_position = (0,0,0)
            return

        for i in range(0, len(event.hands)):
            hand = event.hands[i]
            middle = location_end_of_finger(hand, 2)
            index = location_end_of_finger(hand, 1)
            pinching, array = fingers_pinching(middle, index)
            
            for index_digit in range(0, 5):
                digit = hand.digits[index_digit]
                for index_bone in range(0, 4):
                    bone = digit.bones[index_bone]
                    if (hand.grab_strength==1.0):
                        self.drawingMode = False
                        self.x1, self.y1 = 0, 0
                        self.position = (0,0)
                        self.actual_position = (0,0,0)
                        # return

                    if (self.drawingMode):
                        x2, y2 = self.get_joint_position(hand.index.distal.next_joint)
                        self.position = (x2, y2)
                        self.actual_position = self.get_Fingertip_position(hand.index.distal.next_joint)
                        # self.Current_time = event.timestamp
                        self.frame_id= event.tracking_frame_id
                        self.frameRate = event.framerate
                        self.palm_velocity = hand.palm.velocity
                        self.palm_Position = hand.palm.position
                        self.arm_position = hand.arm.next_joint
                        self.fingertip_rotation = hand.index.distal.rotation
                        self.hand_grab_angle = hand.grab_angle
                        self.hand_grab_strength = hand.grab_strength
                        self.confidence = hand.confidence
                        cv2.circle(self.output_image, (x2, y2), 4, self.drawColor, -1)

                        cv2.putText(
                            self.output_image,
                            "Drawing Mode: Index Finger",
                            (10, self.screen_size[0] - 25),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            self.font_colour,
                            1,
                        )
                    
                    if (hand.index.is_extended and hand.middle.is_extended and hand.ring.is_extended and hand.pinky.is_extended ==0 and hand.thumb.is_extended ==0):
                        self.clearCanvas = True
                        self.drawingMode = False

                    if (hand.index.is_extended and  hand.middle.is_extended == 0 and hand.ring.is_extended ==0 and hand.pinky.is_extended ==0 and hand.thumb.is_extended ==0):
                        self.drawingMode = True



                    if (hand.index.is_extended and hand.middle.is_extended and hand.ring.is_extended and hand.pinky.is_extended  and hand.thumb.is_extended ):
                        self.drawingMode = False
                        self.x1, self.y1 = 0, 0
                        self.position = (0,0)
                    
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
    header = ['frame_id','index_x_coor', 'index_y_coor', 'index_z_coor' ,'palm_x_coor','palm_y_coor','palm_z_coor',
              'index_x_velocity','index_y_velocity','index_z_velocity',
              'palm_velocity_x','palm_velocity_y','palm_velocity_z','confidence',
              'hand_grab_angle','hand_grab_strength','armPosition_x','armPosition_y','armPosition_z','tip_rotation_x','tip_rotation_y','tip_rotation_z','tip_rotation_w','target']
    csv_file_path = './{FileName}.csv'.format(FileName = input("Enter File Name : "))

    with open(csv_file_path, 'w', newline='') as csv_file:
        # Create a CSV writer
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(header)
            
    with connection.open():
        connection.set_tracking_mode(leap.TrackingMode.Desktop)
        canvas.set_tracking_mode(leap.TrackingMode.Desktop)
        imgCanvas = np.zeros((canvas.screen_size[0], canvas.screen_size[1], 3), np.uint8)
        
        # plt.tight_layout()
        # plt.show()
        x1,y1 = 0, 0  
        Actual_x,Actual_y,Actual_z = 0,0,0
        while running:
            frame = canvas.output_image
            if(canvas.clearCanvas):
                imgCanvas = np.zeros((canvas.screen_size[0], canvas.screen_size[1], 3), np.uint8)
                canvas.clearCanvas = False
                with open(csv_file_path, 'w', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(header)
                
            
            if(canvas.drawingMode==False):
                Actual_x,Actual_y,Actual_z = 0,0,0
                canvas.actual_position = (0,0,0)
                # canvas.Current_time = 0
                # Current_time = 0
                x1,y1=0,0
                canvas.position = (0,0)
            
            
            # cv2.imshow("Imagecanvas", canvas.ImageCanvas)
            # cv2.imshow("canvas3", canvas3)
            color = (0, 255, 0)

            x2,y2 = canvas.position
            # X,Y,Z = canvas.actual_position
            Actual_x2,Actual_y2,Actual_z2 = canvas.actual_position
            # Current_time_2 = canvas.Current_time
            if(x1==0 and y1==0 and canvas.drawingMode):
                Actual_x,Actual_y,Actual_z =  Actual_x2,Actual_y2,Actual_z2
                x1 = x2
                y1 = y2

            if(x1!=0 and y1!=0 and canvas.drawingMode):
                cv2.line(imgCanvas, (x1, y1), (x2, y2), canvas.drawColor, canvas.brushThickness)

                frame_id= canvas.frame_id
                palmVelocity = canvas.palm_velocity
                confindence = canvas.confidence
                palm_Position = canvas.palm_Position
                grab_angle = canvas.hand_grab_angle
                grab_strength = canvas.hand_grab_strength
                arm_position = canvas.arm_position
                finger_rotation = canvas.fingertip_rotation
                target = 1
                
                
                
                                    # Write data line by line
                X,Y,Z = canvas.actual_position
                    
                if(Y<175):
                    color = (0,0,255)
                    text = "MOVE YOUR HAND UP!!"

                    # Define the position where the text will be placed
                    position = (50, 100)

                    # Choose the font type and size
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_size = 2
                    font_color = (0,0,255)  # White color in BGR format
                    font_thickness = 3

                    # Use cv2.putText() to add text to the image
                    cv2.putText(frame, text, position, font, font_size, font_color, font_thickness)
                
                ax = arm_position.x
                ay = arm_position.y
                az = arm_position.z
                
                
                tr_x = finger_rotation.x
                tr_y = finger_rotation.y
                tr_z = finger_rotation.z
                tr_w = finger_rotation.w
                
                pvx = palmVelocity.x
                pvy = palmVelocity.y
                pvz = palmVelocity.z
                
                px = palm_Position.x
                py = palm_Position.y
                pz = palm_Position.z
                with open(csv_file_path, 'a', newline='') as csv_file:
                    # Create a CSV writer
                    csv_writer = csv.writer(csv_file)



                    
                    xv = (Actual_x2-Actual_x)*canvas.frameRate
                    yv = (Actual_y2-Actual_y)*canvas.frameRate
                    zv = (Actual_z2-Actual_z)*canvas.frameRate
                    if (xv==yv==zv==0.0):
                        continue
                    row = [frame_id,X,Y,Z,px,py,pz,xv,yv,zv,pvx,pvy,pvz,
                           confindence,grab_angle,grab_strength,
                           ax,ay,az,tr_x,tr_y,tr_z,tr_w,target
                           ]
                    csv_writer.writerow(row)
                        

            # update previous point
            x1, y1 = x2, y2
            Actual_x,Actual_y,Actual_z =  Actual_x2,Actual_y2,Actual_z2
            

            
            imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
            _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
            imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
            frame = cv2.bitwise_and(frame, imgInv)
            frame = cv2.bitwise_or(frame, imgCanvas)
            
            
            x, y, w, h = 75, 250, 500, 250

            # Draw the rectangle on the frame
            # cv2.line(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            start_point = (100, 300)
            end_point = (750, 300)

            # Define the color of the line in BGR format (here, it's red)
            

            
            # Define the thickness of the line
            thickness = 2

            # Use the cv2.line() function to draw the line on the image
            cv2.line(frame, start_point, end_point, color, thickness)
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
