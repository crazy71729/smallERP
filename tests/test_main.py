import sys
sys.path.append("/app")  # 如果在 Docker 中運行，添加容器內的工作目錄

from fastapi.testclient import TestClient
from main import app, products_db  # 導入 FastAPI 應用程式和 products_db

import pytest

client = TestClient(app)

# 清空 products_db 的 fixture，自動應用於每個測試
@pytest.fixture(autouse=True)
def clear_products_db():
    """在每個測試之前清空 products_db"""
    products_db.clear()

def test_create_product():
    """測試創建產品"""
    response = client.post(
        "/products/",
        json={"name": "Test Product", "price": 10.99, "description": "Test"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["price"] == 10.99
    assert "id" in data
    return data["id"]  # 返還產品 ID 供後續測試使用

def test_create_product_invalid_data():
    """測試無效數據創建"""
    # 價格為負數
    response = client.post("/products/", json={"name": "Test", "price": -1})
    assert response.status_code == 422
    
    # 名稱為空
    response = client.post("/products/", json={"name": "", "price": 10})
    assert response.status_code == 422

def test_get_product():
    """測試獲取產品"""
    # 先創建產品
    product_id = test_create_product()  # 使用 fixture 確保 products_db 為空
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"

def test_get_product_not_found():
    """測試獲取不存在的產品"""
    response = client.get("/products/nonexistent-id")
    assert response.status_code == 404

def test_list_products_with_pagination():
    """測試產品列表與分頁"""
    # 創建多個產品
    for i in range(3):
        client.post("/products/", json={"name": f"Product {i}", "price": 10 + i})
    
    # 測試分頁
    response = client.get("/products/?skip=1&limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "Product 1"

def test_update_product():
    """測試更新產品"""
    # 先創建產品
    product_id = test_create_product()
    
    response = client.put(
        f"/products/{product_id}",
        json={"name": "Updated", "price": 15}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated"

def test_delete_product():
    """測試刪除產品"""
    # 先創建產品
    product_id = test_create_product()
    
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 204
    
    # 確認已刪除
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 404