@echo off
call .venv\Scripts\activate
streamlit run app.py --server.port 8888 --server.address 127.0.0.1
pause