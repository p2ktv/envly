# envly

Minimal, type-safe environment variable validation for Python.

```python
class MyEnv(Environment, prefix="APP_"):
    HOST    = stringVar()
    PORT    = intVar(default=8080)
    DEBUG   = boolVar(default=False)
    TOKEN   = stringVar(secret=True)

env = MyEnv()
print(env.PORT)   # 8080 —> int, not str
print(env.TOKEN)  # SecretStr('**redacted**')
```

---

## Installation

```bash
pip install envly
```

---

## Declaring fields

Every field is declared using a factory function. The type is baked into the function, so no annotations are required!

| Function | Returns | Notes |
|---|---|---|
| `stringVar()` | `str` | Supports `secret=True` |
| `intVar()` | `int` | |
| `floatVar()` | `float` | |
| `boolVar()` | `bool` | Accepts `true/false/1/0/yes/no/on/off` |
| `enumVar(*choices)` | `str` | Restricts to allowed values |
| `urlVar()` | `str` | Requires scheme and host |
| `emailVar()` | `str` | |
| `pathVar()` | `Path` | Returns `pathlib.Path` |
| `regexVar(pattern)` | `str` | Must fully match |
| `listVar(of=)` | `list[T]` | Split from a delimited string |
| `jsonVar()` | `Any` | Parsed with `json.loads` |

---

## Options

All var functions share these keyword arguments:

```python
PORT = intVar(
    default=8080,                        # used when the var is not set
    validate=lambda x: x < 65536,       # single validator
    validate=(                           # or a tuple of validators
        lambda x: x > 1024,
        lambda x: x < 65536,
    ),
    var_name="SERVICE_PORT",             # override the env var key
)
```

### `listVar` (sub-coercion per element)

```python
PORTS   = listVar(of=int)                   # "8080,9000" -> [8080, 9000]
TAGS    = listVar(of=str, sep=";")          # "api;bot"   -> ["api", "bot"]
ALLOWED = listVar(of=int, validate=lambda xs: all(x < 65536 for x in xs))
```

Whitespace around each element is stripped automatically. Errors include the offending index: `[PORTS[1]] expected an integer, got 'nope'`.

### `jsonVar` (optional type assertion)

```python
SETTINGS = jsonVar()           # any valid JSON
SETTINGS = jsonVar(type=dict)  # asserts the root value is a dict
```

### `stringVar(secret=True)` (redacted values)

```python
TOKEN = stringVar(secret=True)
```

Returns a `SecretStr`, which is a `str` subclass that redacts itself in `__repr__` and `__str__`, so secrets don't leak into logs. The raw value is accessible via `.reveal()`.

```python
print(env.TOKEN)           # **redacted**
print(env.TOKEN.reveal())  # the-actual-secret
```

---

## Prefix

Pass `prefix` on the class definition to prepend a namespace to every var name.

```python
class MyEnv(Environment, prefix="APP_"):
    PORT = intVar(default=8080)  # reads APP_PORT
```

`var_name` always takes precedence over the prefix, letting you opt individual fields out:

```python
class MyEnv(Environment, prefix="APP_"):
    DB_URL = stringVar(var_name="DATABASE_URL")  # reads DATABASE_URL, not APP_DATABASE_URL
```

---

## Schema

`Environment.schema()` returns a typed description of every declared field — useful for documentation, startup health checks, or generating `.env` templates.

```python
for field in MyEnv.schema():
    req = "required" if field["required"] else f"default={field.get('default')!r}"
    print(f"{field['env_var']:<20} {field['type']:<12} {req}")
```

```
APP_HOST             str          required
APP_PORT             int          default=8080
APP_DEBUG            bool         default=False
APP_TOKEN            SecretStr    required
```

---

## Inheritance

MyEnvs compose naturally through class inheritance.

```python
class BaseMyEnv(Environment):
    LOG_LEVEL = enumVar("debug", "info", "warn", "error", default="info")
    DEBUG     = boolVar(default=False)

class MyEnv(BaseMyEnv, prefix="APP_"):
    HOST  = stringVar()
    PORT  = intVar(default=8080)
```

---

## Testing

Pass `_source` to substitute `os.environ` with a plain dict.

```python
env = MyEnv(_source={"APP_HOST": "localhost", "APP_PORT": "9000"})
```

---

## Immutability

MyEnv instances are frozen after construction. Any attempt to set an attribute raises `AttributeError`.

```python
env.PORT = 1  # AttributeError: MyEnv instances are immutable after construction.
```
