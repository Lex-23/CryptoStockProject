# CryptoStockProject
# dev.env example

```
POSTGRES_USER=admin
POSTGRES_PASSWORD=password
POSTGRES_DB=stock_be
POSTGRES_PORT=5432
POSTGRES_HOST=localhost
CRYPTOSTOCK_SECRET_KEY=django-key
CRYPTOSTOCK_ALLOWED_HOSTS=testserver,127.0.0.1
CRYPTOSTOCK_INTERNAL_IPS=127.0.0.1,
REDIS_PORT=6379
CRYPTOSTOCK_CELERY_BROKER_URL=redis://localhost:6379
CRYPTOSTOCK_CELERY_RESULT_BACKEND=redis://localhost:6379
CRYPTOSTOCK_TIMEZONE=UTC
CRYPTOSTOCK_EMAIL_HOST_USER=emailserver.av@gmail.com
CRYPTOSTOCK_EMAIL_HOST_PASSWORD=password
CRYPTOSTOCK_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
CRYPTOSTOCK_EMAIL_HOST=smtp.gmail.com
TELEGRAM_BOT_API_TOKEN=TOKEN
```
