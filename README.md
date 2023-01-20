
```
conda create --name flask-postgres python==3.9 -y
conda activate flask-postgres
pip install poetry
poetry config virtualenvs.create false
poetry install
```

λ powershell ./create_venv.ps1