from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid

app = FastAPI(title="Product Management API")

# 產品模型
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, description="產品名稱")
    price: float = Field(..., gt=0, description="產品價格")
    description: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: str

# 模擬資料庫
products_db = {}

@app.post("/products/", response_model=Product, status_code=201)
async def create_product(product: ProductCreate):
    """創建新產品"""
    product_id = str(uuid.uuid4())
    new_product = Product(id=product_id, **product.dict())
    products_db[product_id] = new_product.dict()
    return new_product

@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """獲取特定產品"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="產品不存在")
    return products_db[product_id]

@app.get("/products/", response_model=List[Product])
async def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """列出所有產品（支援分頁）"""
    products = list(products_db.values())
    return products[skip:skip + limit]

@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: str, product: ProductCreate):
    """更新產品"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="產品不存在")
    updated_product = Product(id=product_id, **product.dict())
    products_db[product_id] = updated_product.dict()
    return updated_product

@app.delete("/products/{product_id}", status_code=204)
async def delete_product(product_id: str):
    """刪除產品"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="產品不存在")
    del products_db[product_id]
    return None