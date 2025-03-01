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
    category: Optional[str] = Field(None, description="產品分類")  

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

# 批量創建產品
@app.post("/products/bulk/", response_model=List[Product], status_code=201)
async def create_products_bulk(products: List[ProductCreate]):
    """批量創建產品"""
    created_products = []
    for product in products:
        product_id = str(uuid.uuid4())
        new_product = Product(id=product_id, **product.dict())
        products_db[product_id] = new_product.dict()
        created_products.append(new_product)
    return created_products

# 按分類列出產品
@app.get("/products/by_category/", response_model=List[Product])
async def list_products_by_category(
    category: str = Query(..., description="產品分類"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """按分類列出產品"""
    products = [p for p in products_db.values() if p.get("category") == category]
    if not products:
        raise HTTPException(status_code=404, detail="該分類下無產品")
    return products[skip:skip + limit]

@app.get("/products/by_name/", response_model=List[Product])
async def list_products_by_name(
    name: str = Query(..., description="產品名稱（支援部分匹配）"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """按名稱列出產品"""
    products = [p for p in products_db.values() if name.lower() in p.get("name", "").lower()]
    if not products:
        raise HTTPException(status_code=404, detail="該名稱下無產品")
    return products[skip:skip + limit]

@app.get("/products/by_price/", response_model=List[Product])
async def list_products_by_price(
    min_price: float = Query(..., ge=0, description="最低價格"),
    max_price: Optional[float] = Query(None, ge=0, description="最高價格"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """按價格範圍列出產品"""
    products = [p for p in products_db.values() if p.get("price", 0) >= min_price]
    if max_price is not None:
        products = [p for p in products if p.get("price", 0) <= max_price]
    if not products:
        raise HTTPException(status_code=404, detail="該價格範圍下無產品")
    return products[skip:skip + limit]


