### How to start

download folder *Inverse_Kinematics*

Install libraries from **pyproject.toml**/**requirements.txt** or if you use poetry:
```console
poetry install
```

Run server just type:
```console
poetry run python server.py
```

Terminating the server is a bit more challenging, one way is:

Windows 
```console
taskkill /F /IM python.exe 
```

Linux
```console
pkill python
```

Starting the generation of the Jacobian matrix into a .dill file can be done by:
```console
poetry run python generate.py
```
