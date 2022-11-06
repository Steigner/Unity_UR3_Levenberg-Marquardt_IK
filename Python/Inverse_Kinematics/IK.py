import dill
import numpy as np
from numpy import pi, cos, sin, arctan2

class IK_LM(object):
    """
    Accesible methods:
    :method 1: LM
    :method 2: demo

    """
    def __init__(self) -> None:
        """
        Load dill file with Jacobian matrix for defined robot.

        """
        self.f_new = dill.load(open("Jacobian", "rb"))
        
    def LM(self) -> np.ndarray:
        """
        Compute IK depands on demo trajectory.

        :returns: array of trajectory joints
        """
        angles = [0, 0, 0, 0, 0, 0]
        
        p, r = self.demo(0)
        out, angles = self.__compute(angles, p, r)

        for i in range(1,5):
            p, r = self.demo(i)
            a, angles = self.__compute(angles, p, r)
            out = np.r_[out, a]

        print(type(out))
        return out

    def demo(self, target: int) -> list:
        """
        Defined demo trajectory of robot.

        :param target: switch case inpup
        :returns: point, rotation
        :raises: case out of range
        """
        match target:
            case 0:
                p1 = [0.0, -0.194, 0.69]
                r1 = [-90, 0, -180]
                return p1, r1

            case 1:
                p2 = [-0.21, -0.24, 0.2]
                r2 = [-180, 0, -180]
                return p2, r2

            case 2:
                p3 = [-0.21,-0.24, 0.326]
                r3 = [-180, 0, -180]
                return p3, r3

            case 3:
                p4 = [-0.21,-0.24, 0.326]
                r4 = [-29, 52, -140]
                return p4, r4

            case 4:
                p4 = [-0.21,-0.413, 0.326]
                r4 = [-29, 52, -140]
                return p4, r4
            
            case _:
                raise ("No exist target")

    def __J(self, th1, th2, th3, th4, th5, th6) -> np.ndarray:
        """
        Computation Jacobian matrix for UR3 by defined angles[rad]        
        
        :param th1-th6: joints angle
        """
        return self.f_new(th1, th2, th3, th4, th5, th6).astype('float64')

    def __FK(self, th: np.ndarray) -> np.ndarray:
        """
        Computation of Forward Kinematics by classics D-H tables  

        :param th: joints angle
        """
        o = [pi/2, 0, 0, pi/2, -pi/2, 0]
        d = [0.1519, 0, 0, 0.11235, 0.08535, 0.0819]
        a = [0, -0.24365, -0.21325, 0, 0, 0]
        
        for i in range(6):
            A_x = np.array([
                [cos(th[i]),  -sin(th[i]) * cos(o[i]),     sin(th[i]) * sin(o[i]),     a[i] * cos(th[i])], 
                [sin(th[i]),   cos(th[i]) * cos(o[i]),    -cos(th[i]) * sin(o[i]),     a[i] * sin(th[i])],
                [0       ,     sin(o[i]),                  cos(o[i]),                  d[i]             ],
                [0       ,     0,                          0,                          1                ]           
            ])

            if i == 0:
                A = A_x
            
            else:
                A = A @ A_x 
        
        return A

    def __comp_t_desired(self, target: np.ndarray) -> np.ndarray:
        """
        Computation target Forward Kinematics D-H table

        :param target: translation, rotation of target
        :returns: 4x4 d-h table of target  
        """
        x = target[0]
        y = target[1]
        z = target[2]
        
        alfa = target[3]
        beta = target[4]
        gamma = target[5]
        
        R_x = np.array([
            [1, 0,           0        ],
            [0, cos(alfa),  -sin(alfa)],
            [0, sin(alfa),   cos(alfa)] 
        ])
        
        R_y = np.array([
            [cos(beta),  0, sin(beta)],
            [0,          1, 0        ],
            [-sin(beta), 0, cos(beta)] 
        ])
        
        R_z = np.array([
            [cos(gamma), -sin(gamma),  0], 
            [sin(gamma),  cos(gamma),  0],
            [0,           0,           1]
        ])

        R = R_z @ R_y @ R_x

        return np.r_[
            np.c_[
                R, np.array([x,y,z])
            ], [np.array([0,0,0,1])]
        ]

    def __Angle_Axis(self, T_desired: np.ndarray, T_current: np.ndarray) -> np.ndarray:
        """
        Computation angle-axis distance

        :param T_desired: d-h table of target
        :param T_current: d-h table current state
        :returns: 6x1 array translation, rotation  
        """
        Td = T_desired[:3,3]
        Ti = T_current[:3,3]

        Rd = T_desired[:3,:3]
        Ri = T_current[:3,:3]

        R = Rd @ Ri.T
        
        l = np.array([ 
            [R[2,1] - R[1,2]],
            [R[0,2] - R[2,0]],
            [R[1,0] - R[0,1]]
        ])
        
        l_length = np.linalg.norm(l)

        if(l_length > 0):
            a = ((arctan2(l_length, R[0,0] + R[1,1] + R[2,2] - 1 ) ) / l_length) * l

        else:  
            if(R[0,0] + R[1,1] + R[2,2] > 0):
                a = np.array([[0,0,0]]).T
            
            else:
                a = pi/2 * np.array([[
                    R[0,0] + 1,
                    R[1,1] + 1,
                    R[2,2] + 1
                ]]).T
        
        return np.r_[np.array([Td-Ti]).T, a]

    def __compute(self, angles: list, target_position: list, target_rotation: list) -> np.ndarray:
        """
        Computation of Levenberg-Marquardt method.

        :param angles: init angles[°]
        :param target_position: translation of target [x,y,z] [m]
        :param target_rotation: rotation of target [r,p,y] [°] Euler-angles 
        :returns: X x 6 matrix of path targets
        """
        angles = np.deg2rad(angles)
        target_rotation = np.deg2rad(target_rotation)
        target = np.append(target_position, target_rotation)

        i = 0
        q = np.array([angles])

        # init d-h tables
        T_desired = self.__comp_t_desired(target)
        T_current = self.__FK(q[i,:])

        # error computation
        error = np.linalg.norm(T_current - T_desired)

        # do until error will be in specified accuracy
        while error > 0.001:
            J_comp = self.__J(q[i,0],q[i,1],q[i,2],q[i,3],q[i,4],q[i,5])
            H_k = J_comp.T @ np.eye(6,6) @ J_comp
            g_k = J_comp.T @ np.eye(6,6) @ self.__Angle_Axis(T_desired, T_current)

            if (np.linalg.det(J_comp)!=0):
                q = np.r_[q, q[i,:] + (np.linalg.inv(H_k) @ g_k).T]

            else:
                q = np.r_[q, q[i,:] + (np.linalg.pinv(H_k) @ g_k).T]

            # compute new error
            T_current = self.__FK(q[-1,:])
            error = np.linalg.norm(T_current - T_desired)

            # limit computed joint from 360° to 180° -> prevent some self collision 
            if(np.any(q[-1,:] > pi) or np.any(q[i+1,:] < -pi)): 
                l = np.argwhere(q[-1,:] > pi)
                k = np.argwhere(q[-1,:] < -pi)
                q[-1,l] = q[i,l]
                q[-1,k] = q[i,k]

            i += 1

        """
        ! Check Correctness purpose
        ! Correct by UR - Polyscope

        A = self.FK(q[-1,:])
        R = A[:3, :3]

        beta = arctan2(-R[2,0], np.sqrt(R[0,0]**2 + R[1,0]**2))
        alfa = arctan2(R[1,0] / cos(beta), R[0,0] / cos(beta))
        gamma = arctan2(R[2,1] / cos(beta), R[2,2] / cos(beta))

        rpy = np.rad2deg([gamma, beta, alfa])
        xyz = A[:3,3]
        # goal = np.rad2deg(q[-1,:])
        """

        goal = q[-1,:]

        # generate simple path, with 100 samples
        nr_pnts = 100
        a = np.zeros((nr_pnts, 6))

        for i in range(5):
            a[:,i] = np.linspace(np.rad2deg(angles[i]), np.rad2deg(goal[i]), nr_pnts)

        return a, np.rad2deg(goal)