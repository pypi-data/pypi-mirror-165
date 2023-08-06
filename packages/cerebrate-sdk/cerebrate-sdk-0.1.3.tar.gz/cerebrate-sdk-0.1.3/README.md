# Cerebrate SDK

## Install
### with poetry
```shell
poetry add cerebrate-sdk
```

### or with pip
```shell
pip install cerebrate-sdk
```

## Examples
### Fake email detector
```python
from cerebrate_sdk import Cerebrate

c = Cerebrate('YOUR_API_KEY')

task = "Detect if email is fake or real"
examples = [
    "qwertyuiooiu@ihdj.com: fake"
    "support@cerebrate.ai: real",
]

result = c.predict(task, examples, "lajotig138@5k2u.com: ")

print(result[0])
# fake

```

### Raw usage
```python
from cerebrate_sdk import Cerebrate

c = Cerebrate("YOUR_API_KEY")

result = c.raw("Suggest the next item for user's cart."
               "Cart: bacon, eggs, tomatoes"
               "Suggested item: ")
print(result[0])
# sausage

```