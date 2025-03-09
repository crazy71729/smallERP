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
    assert response.status_code == 422 #負價格：price=-1 不符合要求（gt=0），返回 Unprocessable Entity
    
    # 名稱為空
    response = client.post("/products/", json={"name": "", "price": 10})
    assert response.status_code == 422 #不符合min_length=1

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
    assert response.status_code == 404 #not found

def test_list_products_with_pagination():
    """測試產品列表與分頁"""
    # 創建多個產品
    for i in range(3):
        client.post("/products/", json={"name": f"Product {i}", "price": 10 + i}) #送入三個2得到第2個
    
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

# 新增測試：批量創建產品
def test_create_products_bulk():
    """測試批量創建產品"""
    payload = [
        {"name": "Bulk Product 1", "price": 20.99, "category": "Electronics"},
        {"name": "Bulk Product 2", "price": 30.99, "category": "Clothing"}
    ]
    response = client.post("/products/bulk/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Bulk Product 1"
    assert data[1]["name"] == "Bulk Product 2"
    assert all("id" in item for item in data)

# 新增測試：按分類列出產品
def test_list_products_by_category():
    """測試按分類列出產品"""
    # 創建帶分類的產品
    client.post("/products/", json={"name": "Electronics Product", "price": 50.99, "category": "Electronics"})
    client.post("/products/", json={"name": "Clothing Product", "price": 20.99, "category": "Clothing"})
    
    # 測試按分類過濾
    response = client.get("/products/by_category/?category=Electronics")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["category"] == "Electronics"
    
    # 測試無匹配分類
    response = client.get("/products/by_category/?category=Books")
    assert response.status_code == 404
    assert response.json()["detail"] == "該分類下無產品"

# 新增測試：按名稱列出產品
def test_list_products_by_name():
    """測試按名稱列出產品"""
    # 創建多個產品
    client.post("/products/", json={"name": "Laptop", "price": 999.99})
    client.post("/products/", json={"name": "Desktop", "price": 799.99})
    client.post("/products/", json={"name": "Lamp", "price": 19.99})
    
    # 測試按名稱部分匹配
    response = client.get("/products/by_name/?name=lap")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Laptop"
    
    # 測試無匹配名稱
    response = client.get("/products/by_name/?name=xyz")
    assert response.status_code == 404
    assert response.json()["detail"] == "該名稱下無產品"

# 新增測試：按價格範圍列出產品
def test_list_products_by_price():
    """測試按價格範圍列出產品"""
    # 創建多個產品
    client.post("/products/", json={"name": "Cheap Item", "price": 10.99})
    client.post("/products/", json={"name": "Mid Item", "price": 50.99})
    client.post("/products/", json={"name": "Expensive Item", "price": 100.99})
    
    # 測試價格範圍
    response = client.get("/products/by_price/?min_price=20&max_price=80")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Mid Item"
    
    # 測試無匹配價格範圍
    response = client.get("/products/by_price/?min_price=200")
    assert response.status_code == 404
    assert response.json()["detail"] == "該價格範圍下無產品"
    
    # 測試僅 min_price
    response = client.get("/products/by_price/?min_price=50")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # 應該包含 Mid Item 和 Expensive Item
    assert all(p["price"] >= 50 for p in data)