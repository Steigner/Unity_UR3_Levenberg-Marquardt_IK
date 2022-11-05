### how to start

download folder *Inverse_Kinematics*

install libraries from **pyproject.toml** or if you use poetry:
```console
poetry install
```

run server just type:
```console
poetry run python .\server.py
```

terminating the server is a bit more challenging, one way is:
```console
taskkill /F /IM python.exe 
```

starting the generation of the Jacobian matrix into a .dill file can be done by:
```console
poetry run python .\Generate.py
```
