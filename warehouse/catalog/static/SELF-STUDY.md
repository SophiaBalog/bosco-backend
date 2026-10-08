# Self-Study: Урок №6 — Шаблонізатор Django, успадкування та форматування даних

**Студент(ка):** Балог Софія Андріївна  
**Проєкт:** `bosco-backend` (Складський облік / Warehouse)  
**Дата виконання:** 05 жовтня 2026 р.  

---

## 1. Теоретичний огляд

### 1.1. Система успадкування шаблонів (Template Inheritance)
Django використовує механізм DRY (Don't Repeat Yourself) для шаблонів через теги `{% extends %}` та `{% block %}`.
- **`{% extends 'base.html' %}`**: Вказує, що поточний шаблон є дочірнім і наслідує каркас із базового шаблону. Повинен бути першим тегом у файлі.
- **`{% block name %}` ... `{% endblock %}`**: Визначає секції, які дочірній шаблон може перевизначити (наприклад, `title`, `content`, `scripts`).

### 1.2. Повторно використовувані фрагменти (Partials / Includes)
Тег `{% include 'path/to/partial.html' %}` дозволяє вставляти фрагменти HTML-коду у декількох місцях проєкту (компонентний підхід).
- У проєкті виділено такі фрагменти:
  - `templates/partials/_header.html` — шапка сайту.
  - `templates/partials/menu.html` — навігаційне меню.
  - `templates/partials/messages.html` — відображення флеш-повідомлень системи.
  - `templates/partials/_footer.html` — підвал сторінки.

### 1.3. Кастомні теги та фільтри (Custom Template Tags & Filters)
Для специфічного форматування даних створюються власні фільтри та теги у папці `templatetags/` всередині Django-додатка:
- **`@register.filter` (`uah`)**: Перетворює числові значення ціни у форматований рядок із валютою (наприклад, `350.00 грн`).
- **`@register.simple_tag` (`product_count`)**: Повертає загальну кількість товарів у базі даних для виводу у шапці чи меню.

---

## 2. Практична реалізація у проєкті

### 2.1. Структура директорії шаблонів
```text
warehouse/
├── templates/                     # Глобальні шаблони проєкту
│   ├── base.html                  # Базовий каркас
│   └── partials/                  # Часткові шаблони (Includes)
│       ├── _header.html
│       ├── _footer.html
│       ├── menu.html
│       └── messages.html
└── catalog/
    └── templates/
        └── catalog/               # Шаблони додатка catalog
            ├── products.html      # Список товарів
            └── product_form.html  # Форма додавання товару



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']


{% load catalog_extras %}

<td>{{ p.price|uah }}</td>