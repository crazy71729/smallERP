# smallERP
Coding Assignment for Wiwynn interview

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
  "description": "A test product description"
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