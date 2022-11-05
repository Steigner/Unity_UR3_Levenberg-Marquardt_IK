# Unity UR3 Levenberg-Marquardt Inverse Kinematics

In this project, an Inverse Kinematics based on the Levenberg-Marquardt method was implemented. The Unity game engine was used as the simulation environment and the programming language Python was used to implement the algorithm. In order to implement the result, the [ZeroMQ](https://zeromq.org/) library for both Python and C# in Unity was chosen. Thus, the communication is implemented using TCP/IP where Python is the Server and Unity is the Client.

The actual demonstration is then implemented in Python where five targets are selected both their rotational and translational part. The scripts can be very easily modularized and used to solve a simulation of a problem. For deployment in reality, it is then necessary to complete the communication with the robot.

## How to start the simulation demo?
In the Unity project section, you can download the [**Robot.unitypackage**](https://github.com/Steigner/Unity_UR3_Levenberg-Marquardt/blob/main/Unity/Robot.unitypackage), when you download it and then run it in an open window, you will see a menu to import it into your project. It is also an integral part of the NetMQ library assignment. 

1. Option - As part of the project I downloaded [**NuGetForUnity**](https://github.com/GlitchEnzo/NuGetForUnity). Its installation can be easily handled by following the steps: 

    Link: https://github.com/GlitchEnzo/NuGetForUnity#how-do-i-install-nugetforunity

    Then, following the instructions in the repository, download the **NetMQ** nuget package and the **Unity part is ready**.

    I have also added the necessary files and libraries to the repository, which you can simply add to your project by exploring the [**Assets folder**](https://github.com/Steigner/Unity_UR3_Levenberg-Marquardt/tree/main/Unity/Assets). Personally, I strongly recommend using **Robot.unitypackage** due to the fact that you need to load a script Joint.cs for each joint in your project and add **rigibody** and **boxcollider** for collision detection. Everything is stored in the **OutdoorScene**.
    
2. Option - The alternative is to import the .dll libraries directly from [Assets/Libraries](https://github.com/Steigner/Unity_UR3_Levenberg-Marquardt/tree/main/Unity/Assets/Libraries).

The next part is Python, additional libraries were used in the project, so if you use Poetry, you can easily get everything, if you use PIP, Conda or other package manager, just get the libraries from [**pyproject.toml**](https://github.com/Steigner/Unity_UR3_Levenberg-Marquardt/blob/main/Python/Inverse_Kinematics/pyproject.toml).

:heavy_exclamation_mark: Run python first

:heavy_exclamation_mark: Run Unity second

## Collision Detection 

Collision detection was also provided within this project, if a collision occurs the movement is stopped and it is written to the Unity Console what joint was detected in the collision. You can see an example in the GIF. The same are included self collision.

## Demo Example
The demo shows movement with and without collision detection. Within Unity, you can simply pin or unpin a cube in the game object Cube checkbox.

![Demo](https://github.com/Steigner/Unity_UR3_Levenberg-Marquardt/blob/main/docs/gif_unity.gif)

## 

Finally, it should be mentioned that this is a project that has implemented simple rep/req communication.

## :information_source: Contacts

Martin.Juricek1@vutbr.cz

:red_circle: Brno University of Technology,

:large_blue_circle: Faculty of Mechanical Engineering,

:computer: Institute of Automation and Computer Science
