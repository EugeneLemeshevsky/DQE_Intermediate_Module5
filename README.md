#Environment setup

##Create virtual environment for tests execution
```bash
cd PyTestHomeTask
python3 -m venv venv
.\venv\Scripts\activate
python -m pip install pytest
pip install pytest-html
```
## Run Pytest tests
```bash
pytest test_DB_Pytest.py
```

# Report example
```bash
py.test --html=demoreport.html
```
Successful report example [file](demoreport.html)

