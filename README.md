# To run formatter app using poetry:

```bash
git clone https://github.com/sheenacodes/cli-formatter.git
cd cli-formatter
poetry install
poetry run formatter ST 2 [--verbose]
```
to run tests
```bash
poetry run pytest
```

# without poetry
```bash
python formatter/main.py ST 1 [--verbose]
```
