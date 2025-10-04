# Copilot Guidelines
- Always write comments in English
- Follow PEP8
- Follow strict typing
- Prefer Pathlib over os.walk / os.path
- for bpy.types.Object don't check type with `obj.type == 'MESH'` use `isinstance(obj.data, bpy.types.Mesh)`