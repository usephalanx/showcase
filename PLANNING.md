# Test Strategy — Hello API Endpoint

## Endpoint Inventory

| HTTP Method | Path     | Handler Function | Source File | Description                          |
|-------------|----------|------------------|-------------|--------------------------------------|
| GET         | `/hello` | `hello`          | `routes.py` | Returns a JSON greeting message      |

### Request Parameters

| Parameter | Location | Type   | Required | Default        | Description                     |
|-----------|----------|--------|----------|----------------|---------------------------------|
| `name`    | query    | string | No       | `"World"`      | Name to include in the greeting |

### Response Format

- **Content-Type:** `application/json`
- **Schema:**

```json
{
  "message": "Hello, <name>!"
}
```

When no `name` query parameter is provided, defaults to:

```json
{
  "message": "Hello, World!"
}
```

---

## Test Cases

All tests reside in **`tests/test_hello.py`** and use **pytest** with
**`httpx.ASGITransport` / `httpx.AsyncClient`** (or `starlette.testclient.TestClient`).

| # | Test Function                                  | Method | Path                                         | Expected Status | Expected Body / Assertion                                     |
|---|------------------------------------------------|--------|----------------------------------------------|-----------------|---------------------------------------------------------------|
| 1 | `test_get_hello_returns_200`                   | GET    | `/hello`                                     | 200             | `{"message": "Hello, World!"}`                                |
| 2 | `test_get_hello_response_content_type`         | GET    | `/hello`                                     | 200             | `Content-Type` header is `application/json`                   |
| 3 | `test_get_hello_with_name_param`               | GET    | `/hello?name=Alice`                          | 200             | `{"message": "Hello, Alice!"}`                                |
| 4 | `test_get_hello_empty_name_param`              | GET    | `/hello?name=`                               | 200             | `{"message": "Hello, World!"}` (falls back to default)        |
| 5 | `test_get_hello_special_characters_in_name`    | GET    | `/hello?name=<script>alert(1)</script>`      | 200             | Name echoed as-is in JSON (safe in JSON context)              |
| 6 | `test_get_hello_very_long_name`                | GET    | `/hello?name=AAA…(2000 chars)`               | 200             | Response contains the full long name                          |
| 7 | `test_post_hello_method_not_allowed`           | POST   | `/hello`                                     | 405             | Method Not Allowed                                            |
| 8 | `test_get_hello_trailing_slash`                | GET    | `/hello/`                                    | 200 or 307      | Either redirects to `/hello` or returns 200                   |
| 9 | `test_get_hello_unknown_query_param_ignored`   | GET    | `/hello?foo=bar`                             | 200             | `{"message": "Hello, World!"}` (unknown params ignored)       |
|10 | `test_get_hello_numeric_name`                  | GET    | `/hello?name=123`                            | 200             | `{"message": "Hello, 123!"}`                                  |
|11 | `test_put_hello_method_not_allowed`            | PUT    | `/hello`                                     | 405             | Method Not Allowed                                            |
|12 | `test_delete_hello_method_not_allowed`         | DELETE | `/hello`                                     | 405             | Method Not Allowed                                            |
|13 | `test_get_hello_unicode_name`                  | GET    | `/hello?name=日本語`                          | 200             | `{"message": "Hello, 日本語!"}`                                |
|14 | `test_get_hello_whitespace_name`               | GET    | `/hello?name=%20%20`                         | 200             | Falls back to default (whitespace-only treated as empty)      |

---

## Edge Cases

1. **Empty `name` parameter** — `?name=` should fall back to `"World"`.
2. **Whitespace-only `name`** — `?name=%20%20` should fall back to `"World"`.
3. **XSS attempt in `name`** — HTML/JS in query param must not cause errors; JSON encoding is inherently safe.
4. **Very long name (2 000+ chars)** — endpoint must not crash or truncate silently.
5. **Trailing slash** — `/hello/` should still resolve (FastAPI redirect or direct match).
6. **Unsupported HTTP methods** — POST, PUT, DELETE, PATCH should return 405.
7. **Unicode / multibyte characters** — must round-trip correctly in JSON.
8. **Multiple `name` params** — `?name=A&name=B` — FastAPI takes the first value.

---

## Testing Framework & Tools

- **Framework:** pytest
- **HTTP Client:** `starlette.testclient.TestClient` (synchronous wrapper for ASGI apps)
- **Test file:** `tests/test_hello.py`
- **Fixtures file:** `tests/conftest.py` (provides `client` fixture)

## Acceptance Criteria

- [ ] All 14 test functions pass with `pytest tests/test_hello.py`
- [ ] Tests cover status codes, response bodies, and content-type headers
- [ ] No test relies on external state or ordering
- [ ] Tests run in < 5 seconds total
