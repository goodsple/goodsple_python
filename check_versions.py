import sys
import importlib

# 확인할 패키지 목록
pkgs = ['sqlalchemy', 'rasa', 'fastapi', 'pydantic', 'asyncpg',
        'pydantic_settings','uvicorn']

# 파이썬 버전 출력
print(f"Python: {sys.version.split()[0]}")

# 각 패키지 버전 출력
for p in pkgs:
    try:
        # 동적으로 패키지를 불러옴
        module = importlib.import_module(p)
        # __version__ 속성을 찾음
        version = getattr(module, '__version__', '(version not found)')
        print(f'{p:20} -> {version}')
    except ImportError:
        # 패키지가 설치되지 않은 경우
        print(f'{p:20} -> (not installed)')

# 인터프리터 경로 출력
print(f"Interpreter: {sys.executable}")