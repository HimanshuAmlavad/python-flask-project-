@echo off
REM Format and lint Python code

echo ================================
echo Running isort (import sorting)...
echo ================================
isort .

echo ================================
echo Running black (code formatter)...
echo ================================
black .

echo ================================
echo Running flake8 (style checker)...
echo ================================
flake8 .

echo ================================
echo Running mypy (type checker)...
echo ================================
mypy .

echo ================================
echo Running pylint (code analyzer)...
echo ================================
pylint **/*.py

echo ================================
echo All checks completed!