#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from math import pi

import math

p = [[1,1], [3,3], [1, 3], [1,1]]
rospy.init_node('talker', anonymous=True)
pub = rospy.Publisher('mobile_base/commands/velocity', Twist, queue_size=10)
#pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

t = Twist()
r = rospy.Rate(60)
linSpeed = .25
angSpeed = .5
orientation = 0

#Position Tracking
xPosCur = 0.0
yPosCur = 0.0
angCur = 0.0

def move((x1, y1), (x2, y2)):
    print '\n\n'
    global orientation
    dx, dy = x2-x1, y2-y1
    
    if dx == dy:
        if (dx/dy) == 1:

	    theta = (45.0/180) * pi
        else:
	    theta = (-45/180.0) * pi
    elif dx == 0:
	if dy > 0:
	    theta = 0
	elif dy < 0:
	    theta = pi
    elif dy == 0:
	if dx > 0:
	    theta = (90.0/180) * pi
	elif dx < 0:
	    theta = (-90/180.0) * pi
    else:
	thetaCal = math.atan((dy*1.0)/dx)
	theta = -thetaCal+((-90/180.0)*pi)
    tanTest = math.atan(-2.0/-3)
    print "Test:" + str(tanTest)
    print "Theta:" + str(theta)
    movlen = math.sqrt(dx**2.0 + dy**2.0)
    
    #theta = theta - .2

    

    turn(theta - orientation)
    orientation = theta
    forwardLen(movlen)


def forwardLen(length):
    global t, r, pub, linSpeed
    vel = linSpeed
    print "vel: " + str(vel)
    print "len: " + str(length)
    t.linear.x = vel
    d = rospy.Duration((length*1.0) / vel)
    s = rospy.Time.now()
    while (rospy.Time.now() - s) < d:
        pub.publish(t)
        r.sleep()

    t.linear.x = 0

def turn(rad):
    global t, r, pub, angSpeed
    vel = angSpeed
    print "Deg:" + str((180.0 * rad) / math.pi)
    #rad = rad
    a = rad / vel
    print 'a: ' + str(a)
    d = rospy.Duration(abs(rad / vel))
    s = rospy.Time.now()
    if rad < 0:
        t.angular.z = vel
        rad = rad * -1
    else:
        t.angular.z = -vel
    print "vel: " + str(vel)
    print 'd: ' + str(d)
    while (rospy.Time.now() - s) < d:
	pub.publish(t)
	r.sleep()
    t.angular.z = 0

def odometryCb(msg):
    global angCur
    global xPosCur
    global yPosCur

    quaternion = (
    msg.pose.pose.orientation.x,
    msg.pose.pose.orientation.y,
    msg.pose.pose.orientation.z,
    msg.pose.pose.orientation.w)
    a,b,yaw = euler_from_quaternion(quaternion)
    yawDegrees = yaw * 180 / 3.15149

    if (yawDegrees < 0):
        angCur = yawDegrees + 360
    else:
        angCur = yawDegrees

    xPosCur = msg.pose.pose.position.x
    yPosCur = msg.pose.pose.position.y


if __name__ == '__main__':
    for i in range(len(p) - 1):
        move(p[i], p[i+1])
