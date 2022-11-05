# Unity_UR3_Levenberg-Marquardt

In this project, an inverse kinematics based on the Levenberg-Marquardt method was implemented. The Unity game engine was used as the simulation environment and the programming language Python was used to implement the algorithm. In order to implement the result, the ZeroMQ library for both Python and C# in Unity was used. Thus, the communication is implemented using TCP/IP where Python is the Server and Unity is the Client.

The actual demonstration is then implemented in Python where five targets are selected both their rotational and translational part. The scripts can be very easily modularized and used to solve a simulation of a problem. For deployment in reality, it is then necessary to complete the communication with the robot.

## How to start the simulation demo?
In the Unity project section, you can download the **.unitypackage**, when you download it and then run it in an open window, you will see a menu to import it into your project. It is also an integral part of the NetMQ library assignment. As part of the project I downloaded NuGetForUnity. Its installation can be easily handled by following the steps: 

Link: https://github.com/GlitchEnzo/NuGetForUnity#how-do-i-install-nugetforunity

Then, following the instructions in the repository, download the **NetMQ** nuget package and the **Unity part is ready**.

The next part is Python, additional libraries were used in the project, so if you use Poetry, you can easily get everything, if you use PIP, Conda or other package manager, just get the libraries from **pyproject.toml**.

! Run python first ! 

! Run Unity second !

