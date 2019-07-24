Issues and PRs are welcome!

## Contribution

```shell
git clone https://github.com/kehanlu/University.git
cd University

mv university/dev_settings.py university/settings.py
```

### Python env

```shell
pip install -r requirements.txt
python manage.py migrate
python shell < script.py # create base data

python manage.py runserver
```
