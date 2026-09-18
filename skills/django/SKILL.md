---
name: django
description: |
  Comprehensive production-grade Django suite covering Architecture & Project Layout, Django REST Framework (DRF), ORM Query Optimization, Celery Background Tasks & Periodic Beat, Security Hardening & OWASP Compliance, Test-Driven Development (pytest-django, factory_boy), and Verification/Pre-Deployment Gates.
triggers:
  - "django"
  - "django rest framework"
  - "drf"
  - "django celery"
  - "django orm"
  - "django security"
  - "django tdd"
  - "django test"
  - "pytest-django"
license: MIT
metadata:
  origin: ECC
---

# Django Production Engineering Suite

Unified, enterprise-grade guide for developing, scaling, testing, securing, and deploying Python Django applications.

---

## 1. Architecture & Project Layout

### Standard Multi-Environment Layout
```
myproject/
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── production.py
│   │   └── test.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── celery.py
├── manage.py
└── apps/
    ├── authentication/
    ├── users/
    └── orders/
```

### DRF Serializers & ViewSets
```python
from rest_framework import serializers, viewsets, permissions
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total_amount', 'created_at']
        read_only_fields = ['id', 'created_at']

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Prevent N+1 queries by eager loading relations
        return Order.objects.filter(user=self.request.user).select_related('user').prefetch_related('items')
```

---

## 2. Django ORM Query Optimization

### Eliminating N+1 Queries
```python
# select_related for ForeignKeys and OneToOne relations (SQL JOIN)
orders = Order.objects.select_related('user', 'shipping_address').all()

# prefetch_related for ManyToMany and reverse ForeignKeys (separate query + Python merge)
orders = Order.objects.prefetch_related('items__product').all()

# Only fetch needed fields
user_names = User.objects.values_list('id', 'email')
```

### Database Transactions & Atomic Operations
```python
from django.db import transaction, models

@transaction.atomic
def process_payment(order_id, amount):
    order = Order.objects.select_for_update().get(id=order_id)
    if order.status == 'PAID':
        return False
    
    order.status = 'PAID'
    order.save(update_fields=['status'])
    
    # Atomic increment to prevent race conditions
    UserAccount.objects.filter(id=order.user_id).update(
        balance=models.F('balance') - amount
    )
    return True
```

---

## 3. Celery Async Task Processing & Scheduling

### Celery App Setup (`config/celery.py`)
```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

### Resilient Task Design with Retries
```python
from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True
)
def send_order_confirmation_email(self, order_id: int):
    try:
        from apps.orders.models import Order
        order = Order.objects.get(id=order_id)
        # Execute email sending logic
        logger.info(f"Confirmation sent for order {order_id}")
    except Order.DoesNotExist:
        logger.error(f"Order {order_id} not found. Will not retry.")
    except Exception as exc:
        logger.warning(f"Error sending email for order {order_id}: {exc}")
        raise self.retry(exc=exc)
```

---

## 4. Security Hardening & OWASP Compliance

### Essential Production Settings (`config/settings/production.py`)
```python
DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Strict Cookies & SSL
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Security Headers
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

### SQL Injection & Safe Raw Queries
```python
# NEVER: User.objects.raw(f"SELECT * FROM users WHERE email = '{email}'")
# ALWAYS: Parameterize raw queries
User.objects.raw("SELECT * FROM users_user WHERE email = %s", [email])
```

---

## 5. Test-Driven Development (TDD with pytest)

### Configuration (`pytest.ini` / `pyproject.toml`)
```ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings.test
python_files = tests.py test_*.py *_tests.py
addopts = --strict-markers -p no:warnings --reuse-db
```

### Model Factory (`factory_boy`) & API Tests
```python
import factory
import pytest
from rest_framework.test import APIClient
from apps.users.models import User
from apps.orders.models import Order

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Faker('user_name')
    email = factory.Faker('email')

@pytest.mark.django_db
def test_order_creation_endpoint():
    client = APIClient()
    user = UserFactory()
    client.force_authenticate(user=user)

    response = client.post('/api/orders/', {'items': [1, 2]}, format='json')
    assert response.status_code == 201
    assert Order.objects.filter(user=user).exists()
```

---

## 6. Verification & Pre-Deployment Pipeline

Run this sequence before submitting PRs or releasing to staging/production:

```bash
# 1. Check migrations sanity & unapplied migrations
python manage.py makemigrations --check --dry-run
python manage.py check --deploy

# 2. Type Checking & Linting
mypy apps config
ruff check .

# 3. Test Suite & Code Coverage (>= 80%)
pytest --cov=apps --cov-report=term-missing --cov-fail-under=80

# 4. Security Scans
bandit -r apps config -ll
pip-audit
```
