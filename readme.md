Issues and PRs are welcome! 🍕

## Development

```shell
git clone https://github.com/kehanlu/University.git
cd University
mv university/dev_settings.py university/settings.py

pip install -r requirements.txt
python manage.py migrate
python shell < script.py # create base data
```

```shell
python manage.py runserver
```
