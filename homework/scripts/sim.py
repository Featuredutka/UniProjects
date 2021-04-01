#!/usr/bin/env python

import math
import time
import rospy
import traj_draw

from geometry_msgs.msg import Twist
from homework.msg import Num

# Input data saving
v_lin = []
w_ang = []
delta_t =[]

# Arrays for plotting
x_crd = [0]
y_crd = [0]

# Data for calculations
r = 0.05
L = 0.1
N = 4096
b = 0
wlREAL, wrREAL = 0, 0


# Time counter initialization
start_time = time.time()

def creator(data):

    #  Publishing encoders data and position data for debugging
    pub = rospy.Publisher('ashed_chatter', Num, queue_size=10)
    r = rospy.Rate(5)  # 5 Hz
    msg = Num()
    msg.header.stamp = rospy.Time.now()
    #msg.enc1 = 
    #msg.enc2 = 

    try:
        rospy.loginfo(msg.header.stamp)
        rospy.loginfo(msg.enc1)
        rospy.loginfo(msg.enc2)
        rospy.loginfo(msg.position.x)
        rospy.loginfo(msg.position.y)
        pub.publish(msg.header.stamp, msg.enc1, msg.enc2, msg.position.x, msg.position.y)
    except TypeError: pass
    r.sleep()

    # Creating arrays for plotting
    v_lin.append(data.linear.x)
    w_ang.append(data.angular.z)
    delta_t.append((time.time() - start_time))

def calculations(V, omega, d_t, wlREAL, wrREAL):

    for i in range (1, len(V)):

        deltatime = d_t[i] - d_t[i-1]

        wlREAL, wrREAL = turtleconversion(omega[i],  V[i], wlREAL, wrREAL, d_t[i])
        
        VREAL = r/2 * (wlREAL + wrREAL)
        omegaREAL = r/L * (wrREAL - wlREAL)
        tetaREAL = omegaREAL * deltatime
        x_crd.append(x_crd[i-1] + (VREAL * math.cos(tetaREAL) * deltatime))
        y_crd.append(y_crd[i-1] + (VREAL * math.sin(tetaREAL) * deltatime))

def turtleconversion(omega, V, wlREAL, wrREAL, d_t):
    # Computing angular velocity for the each wheel
    b = d_t/(1+d_t)
    w_l = (2 * V - omega * L) / (2 * r)
    w_r = (2 * V + omega * L) / (2 * r)
    wl = (b * wlREAL + (1 - b) * w_l)
    wr = (b * wrREAL + (1 - b) * w_r)
    return wl, wr

def listener():
    # Gathering turtlebot data
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('cmd_vel', Twist, creator)
    rospy.spin()


if __name__ == '__main__':
    listener()
    


calculations(v_lin, w_ang, delta_t, wlREAL, wrREAL)
traj_draw.plotter(x_crd, y_crd)

