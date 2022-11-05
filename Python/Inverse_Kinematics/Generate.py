import dill
import sympy as sym
import numpy as np
from numpy import pi
from sympy import sin, cos, Matrix, lambdify

# Script generates 6-dof robot Jacobian matrix
# D-H parameters are from Universal Robots UR3 robot
# Script can be easily modifed by add/remove d-h table and 
# computation of Forward Kinematics 

th1, th2, th3, th4, th5, th6 = sym.symbols('th1, th2, th3, th4, th5, th6')

o1 = pi/2
d1 = 0.1519
a1 = 0

o2 = 0
d2 = 0
a2 = -0.24365

o3 = 0
d3 = 0
a3 = -0.21325

o4 = pi/2
d4 = 0.11235
a4 = 0

o5 = -pi/2
d5 = 0.08535
a5 = 0

o6 = 0
d6 = 0.0819
a6 = 0

A1 = np.array([
    [cos(th1),  -sin(th1) * cos(o1),     sin(th1) * sin(o1),     a1 * cos(th1)], 
    [sin(th1),   cos(th1) * cos(o1),    -cos(th1) * sin(o1),     a1 * sin(th1)],
    [0       ,   sin(o1),               cos(o1),                 d1           ],
    [0       ,   0,                     0,                       1            ]           
])

A2 = np.array([
    [cos(th2),  -sin(th2) * cos(o2),     sin(th2) * sin(o2),     a2 * cos(th2)], 
    [sin(th2),   cos(th2) * cos(o2),    -cos(th2) * sin(o2),     a2 * sin(th2)],
    [0       ,   sin(o2),               cos(o2),                 d2           ],
    [0       ,   0,                     0,                       1            ]           
])

A3 = np.array([
    [cos(th3),  -sin(th3) * cos(o3),     sin(th3) * sin(o3),     a3 * cos(th3)], 
    [sin(th3),   cos(th3) * cos(o3),    -cos(th3) * sin(o3),     a3 * sin(th3)],
    [0       ,   sin(o3),               cos(o3),                 d3           ],
    [0       ,   0,                     0,                       1            ]           
])

A4 = np.array([
    [cos(th4),  -sin(th4) * cos(o4),     sin(th4) * sin(o4),     a4 * cos(th4)], 
    [sin(th4),   cos(th4) * cos(o4),    -cos(th4) * sin(o4),     a4 * sin(th4)],
    [0       ,   sin(o4),               cos(o4),                 d4           ],
    [0       ,   0,                     0,                       1            ]           
])

A5 = np.array([
    [cos(th5),  -sin(th5) * cos(o5),     sin(th5) * sin(o5),     a5 * cos(th5)], 
    [sin(th5),   cos(th5) * cos(o5),    -cos(th5) * sin(o5),     a5 * sin(th5)],
    [0       ,   sin(o5),               cos(o5),                 d5           ],
    [0       ,   0,                     0,                       1            ]           
])

A6 = np.array([
    [cos(th6),  -sin(th6) * cos(o6),     sin(th6) * sin(o6),     a6 * cos(th6)], 
    [sin(th6),   cos(th6) * cos(o6),    -cos(th6) * sin(o6),     a6 * sin(th6)],
    [0       ,   sin(o6),               cos(o6),                 d6           ],
    [0       ,   0,                     0,                       1            ]           
])


T2 = A1 @ A2
T3 = A1 @ A2 @ A3
T4 = A1 @ A2 @ A3 @ A4
T5 = A1 @ A2 @ A3 @ A4 @ A5
T6 = A1 @ A2 @ A3 @ A4 @ A5 @ A6

z0= np.array([0,0,1])
z1 = A1[:3,2]
z2 = T2[:3,2] 
z3 = T3[:3,2] 
z4 = T4[:3,2] 
z5 = T5[:3,2]

p0 = np.array([0,0,0])
p1 = A1[:3,3]
p2 = T2[:3,3]
p3 = T3[:3,3]
p4 = T4[:3,3]
p5 = T5[:3,3]

P = T6[:3,3]

J = Matrix([
    np.append(np.cross(z0, P - p0), z0),
    np.append(np.cross(z1, P - p1), z1),
    np.append(np.cross(z2, P - p2), z2),
    np.append(np.cross(z3, P - p3), z3),
    np.append(np.cross(z4, P - p4), z4),
    np.append(np.cross(z5, P - p5), z5),
]).T

f = lambdify('th1, th2, th3, th4, th5, th6', J, 'numpy')

dill.settings['recurse'] = True 
dill.dump(f, open("testik", "wb"))