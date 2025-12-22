# Setup

## Linux
### Create environment for linux
``` bash
mkdir -p ~/venvs
python3 -m venv ~/venvs/blender_for_unrealengine
source ~/venvs/blender_for_unrealengine/bin/activate
```

### Install fake bpy module
``` bash
python -m pip install --upgrade pip
python -m pip install fake-bpy-module-latest
```

### Set VSode Python interpreter
In VSCode, press `Ctrl+Shift+P`, then select `Python: Select Interpreter`, 
and choose the interpreter located at `~/venvs/blender_for_unrealengine/bin/python`.


## Windows
### Create environment for windows
``` bash
py -m venv C:\venvs\blender_for_unrealengine
C:\venvs\blender_for_unrealengine\Scripts\Activate.ps1
```

### Install fake bpy module
``` bash
python -m pip install --upgrade pip
python -m pip install fake-bpy-module-latest
```

### Set VSode Python interpreter
In VSCode, press `Ctrl+Shift+P`, then select `Python: Select Interpreter`, 
and choose the interpreter located at `C:\venvs\blender_for_unrealengine\Scripts\python.exe`.

# Best Practices
- Follow the official Blender best practices for addon development:
"Blender best_practice": "https://docs.blender.org/api/current/info_best_practice.html"

# Copilot Guidelines
- Always write comments in English
- Follow PEP8
- Follow strict typing
- Prefer Pathlib over os.walk / os.path
- for bpy.types.Object don't check type with `obj.type == 'MESH'` use `isinstance(obj.data, bpy.types.Mesh)`