FROM python:3.11-slim

# 更新系統並安裝必要的工具
RUN apt-get update && apt-get install -y \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 設置工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝依賴，使用豆瓣鏡像加速（可選）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt   
# -i https://pypi.doubanio.com/simple/

# 複製所有專案檔案到容器中 /app 路徑下
COPY . . 

# 暴露 FastAPI 預設端口（8000）
EXPOSE 8000

# 運行 FastAPI 應用程式 uvicorn：ASGI 伺服器 、main:app 文件名（main.py） FastAPI 實例（app = FastAPI()）  、 --host 0.0.0.0 接受來自所有網絡接口的連接、 --reload 當程式碼改變時自動重啟伺服器
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 