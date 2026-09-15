# ⚡ fastapi-cache-decorator

[![FastAPI](https://img.shields.io/badge/FastAPI-Supported-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)]()

> Lightweight, async in-memory and Redis caching decorator for FastAPI route endpoints.

Cache expensive database queries and AI computations with a simple `@cache(ttl=60)` decorator.

---

### ☕ Support My Studies / Buy Me a Coffee

Hey there! 👋 I build and open-source lightweight, focused developer tools.

If this small package improved your API response times, please consider supporting my college/tuition fund:
- ☕ **Buy Me a Coffee:** [buymeacoffee.com/yourname](https://www.buymeacoffee.com)
- 💖 **Ko-fi:** [buymeacoffee.com/kcidi4148](https://buymeacoffee.com/kcidi4148)
- ⭐ **Star this repository** to help other developers discover it!

---

## 📦 Installation

```bash
pip install git+https://github.com/me1121118/fastapi-cache-decorator.git
```

---

## 🚀 Quick Example

```python
from fastapi import FastAPI, Request
from fastapi_cache_decorator import cache

app = FastAPI()

@app.get("/trending-products")
@cache(ttl=300) # Cache response for 5 minutes
async def get_trending(request: Request):
    # This slow computation will only run once every 5 minutes!
    data = await fetch_heavy_analytics()
    return data
```

---

## 🧪 Testing

```bash
pytest -v tests
```

---

## 📄 License

MIT License. Free for personal and commercial use.
