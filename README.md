# smallERP
Coding Assignment for Wiwynn interview

## 用到的技術
### 後端
- **FastAPI**
- **Pydantic**
- **UUID**
- **Docker**
- **Docker Compose**
- **pytest**
- **httpx**

## 環境需求
- Docker
- Docker Compose
- Git

## 專案結構
```
project-root/
├── tests
```


## 專案部署

### 1. Clone Repository

### 4. 使用Docker Compose部署應用
在專案根目錄下運行以下命令來構建並啟動Docker容器：

docker compose up fastapi-app


這將構建Docker鏡像並在後台啟動容器。後端應用將在`http://localhost:8080` 上運行。

## 常用的Docker Compose指令（於根目錄執行）

建構並啟動後端api
docker compose up fastapi-app

運行測試
docker compose run test

運行後端 ＋ 進行測試
docker compose up

停止並移除容器
docker compose down

## RESTful api
POST /products/（創建產品）
GET /products/{product_id}（獲取單一產品）
GET /products/（列出產品）
PUT /products/{product_id}（更新產品）
DELETE /products/{product_id}（刪除產品）

範例：
Method: POST
URL: http://localhost:8000/products/
Content-Type: application/json
Body：
{
  "name": "Test Product",
  "price": 10.99,
  "description": "A test product description",
  "category":"Electronics"
}

獲得指定商品資訊
Method: GET
URL: http://localhost:8000/products/{product_id}（將 {product_id} 替換為返回的 id）

獲得所有商品資訊
Method: GET
URL: http://localhost:8000/products/

更新產品
Method: PUT
URL: http://localhost:8000/products/{product_id}
Body:{
  "name": "Updated Product",
  "price": 15.99,
  "description": "Updated description"
}

刪除產品
Method: DELETE
URL: http://localhost:8000/products/


##其他功能

批量加入
Method: POST
URL: http://localhost:8000/products/bulk/
Body:[
    {
        "name": "Phone", 
        "price": 499.99, 
        "category": "Electronics"
    }, 
    {
        "name": "Shirt", 
        "price": 29.99, 
        "category": "Clothing"
    }
]

由種類查詢
Method: GET
URL: http://localhost:8000/products/by_category/?category=Electronics

由名稱查詢
Method: GET
URL: http://localhost:8000/products/by_category/?name=pho

由價格查詢
Method: GET
URL: http://localhost:8000/products/by_category/?min_price=100&max_price=500

### 參考文獻
FastAPI：https://minglunwu.com/notes/2021/fast_api_note_1.html/

pydantic:https://editor.leonh.space/2023/pydantic/

pytest:https://ithelp.ithome.com.tw/m/articles/10336826