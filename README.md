# grossup_test
GrossUp proof of concept

# execute
Under the root folder of the project run:
```
python manage.py makemigrations
python manage.py runserver
```
To check that the server is up, open a Postman instance and try the following API call

```
curl --location 'http://127.0.0.1:8000/' \
--form 'file=@"PATH_TO_FILE/test.csv"'
```
and use the test.csv file that lives under the root folder of this project
