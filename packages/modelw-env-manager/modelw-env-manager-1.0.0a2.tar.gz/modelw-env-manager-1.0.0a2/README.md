# Model W &mdash; Env Manager

The goal of the env manager is to help managing the loading of environment
variables and Django settings (although this is not Django-dependent).

Typical use is:

```python
from model_w.env_manager import EnvManager


with EnvManager() as env:
    SOME_VALUE = env.get('SOME_VALUE', is_yaml=True, default=False)
```
