
TOKEN_FILE = %temp%\token.txt
REFRESH_TOKEN_FILE = %temp%\refresh_token.txt

MANAGE_FILE = manage
PORT = 2000
HOST = localhost

.PHONY: init
init:
	python ${MANAGE_FILE}.py makemigrations authentication ts ecommerce
	python ${MANAGE_FILE}.py migrate
	python ${MANAGE_FILE}.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.filter(username='admin').exists() or get_user_model().objects.create_superuser('admin', 'admin@admin.com', 'admin')"

.PHONY: server
server:
	python ${MANAGE_FILE}.py runserver

.PHONY: root
root:
	curl ${HOST}:${PORT}

.PHONY: token
token:
	@curl -s -X POST -d "username=admin&password=admin" http://${HOST}:${PORT}/api/token/ \
	| python -c "import sys, json; print(json.load(sys.stdin)['access'])" > $(TOKEN_FILE)
	@curl -s -X POST -d "username=admin&password=admin" http://${HOST}:${PORT}/api/token/ \
	| python -c "import sys, json; print(json.load(sys.stdin)['refresh'])" > $(REFRESH_TOKEN_FILE)
	curl ${HOST}:${PORT}/api/token/ -d "username=admin&password=admin"

.PHONY: refresh
refresh:
	@for /f "delims=" %%i in ($(REFRESH_TOKEN_FILE)) do curl ${HOST}:${PORT}/api/token/refresh/ -d "refresh=%%i"

.PHONY: verify
verify:
	@for /f "delims=" %%i in ($(TOKEN_FILE)) do curl ${HOST}:${PORT}/api/token/verify/ -d "token=%%i"

.PHONY: blacklist
blacklist:
	@for /f "delims=" %%i in ($(REFRESH_TOKEN_FILE)) do curl ${HOST}:${PORT}/api/token/blacklist/ -d "refresh=%%i"
	@for /f "delims=" %%i in ($(REFRESH_TOKEN_FILE)) do curl ${HOST}:${PORT}/api/token/refresh/ -d "refresh=%%i"

.PHONY: user
user:
	@for /f "delims=" %%i in ($(TOKEN_FILE)) do curl -s ${HOST}:${PORT}/api/user/ -H "Authorization: Bearer %%i"

.PHONY: user1
user1:
	@for /f "delims=" %%i in ($(TOKEN_FILE)) do curl -s ${HOST}:${PORT}/api/user/1/ -H "Authorization: Bearer %%i"

.PHONY: register
register:
	curl ${HOST}:${PORT}/api/user/register/ -d "email=test@test.test&username=test&password=test"

.PHONY: email_verification_get
email_verification_get:
	@for /f "delims=" %%i in ($(TOKEN_FILE)) do curl -s ${HOST}:${PORT}/api/user/email_verification/ -H "Authorization: Bearer %%i"

.PHONY: email_verification_post
email_verification_post:
	curl ${HOST}:${PORT}/api/user/email_verification/ -d "email=admin@admin.com"

.PHONY: change_password
change_password:
	@for /f "delims=" %%i in ($(TOKEN_FILE)) do curl -s ${HOST}:${PORT}/api/user/change_password/ -H "Authorization: Bearer %%i" -d "current_password=admin&new_password=admin"

.PHONY: password_reset_get
password_reset_get:
	@for /f "delims=" %%i in ($(TOKEN_FILE)) do curl -s ${HOST}:${PORT}/api/user/password_reset/ -H "Authorization: Bearer %%i"

.PHONY: password_reset_post
password_reset_post:
	curl ${HOST}:${PORT}/api/user/password_reset/ -d "email=admin@admin.com"

.PHONY: me
me:
	@for /f "delims=" %%i in ($(TOKEN_FILE)) do curl -s ${HOST}:${PORT}/api/user/me/ -H "Authorization: Bearer %%i"

all:
	rm -fr migrations
	rm -fr db.sqlite3
	python manage.py makemigrations authentication ts ecommerce marketplace
	python manage.py migrate
	python manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.filter(username='admin').exists() or get_user_model().objects.create_superuser('admin', 'admin@admin.com', 'admin')"
	python manage.py collectstatic --noinput
	python manage.py runserver 2000
up:
	python manage.py runserver 2000

clean:
	pyclean .

run_worker:
	celery -A project.celery worker --loglevel=info

run_beat:
	celery -A project.celery beat --loglevel=info

# https://stackoverflow.com/questions/45744992/celery-raises-valueerror-not-enough-values-to-unpack
# run_worker:
#     pip install gevent
#     celery -A project.celery worker -l info -P gevent

# run_beat:
#     celery -A project beat --loglevel=info
