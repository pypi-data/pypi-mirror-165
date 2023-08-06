A decorator based router for FastAPI
---

```python
# fruit_controller.py
from fastapi_cls_controller import controller, delete, get, post, put, ...

@controller(
    prefix="/fruits",
)
class FruitController:
    @post("")
    async def create(self, body: CreateFruit):
        ...


    @get("/{fruit_id}")
    async def get(self, fruit_id: str):
        ...


```

```python
# main.py
app.include_router(FruitController())
```