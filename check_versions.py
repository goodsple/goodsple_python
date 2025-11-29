import sys
import importlib

pkgs = ['sqlalchemy', 'rasa', 'fastapi', 'pydantic', 'asyncpg',
        'pydantic_settings','uvicorn']

print(f"Python: {sys.version.split()[0]}")

for p in pkgs:
    try:
        module = importlib.import_module(p)
        version = getattr(module, '__version__', '(version not found)')
        print(f'{p:20} -> {version}')
    except ImportError:
        print(f'{p:20} -> (not installed)')

print(f"Interpreter: {sys.executable}")