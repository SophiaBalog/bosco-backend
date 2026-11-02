from django.db import migrations

STOREKEEPER = "Комірник"
MANAGER = "Менеджер"


def create_groups(apps, schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")
    Permission = apps.get_model("auth", "Permission")
    Group = apps.get_model("auth", "Group")

    # На чистій базі права ще не створені: їх створює сигнал post_migrate
    # ПІСЛЯ всіх міграцій. Тому створюємо потрібні права тут самі.
    ct, _ = ContentType.objects.get_or_create(app_label="catalog", model="product")

    def perm(codename, name):
        p, _ = Permission.objects.get_or_create(
            content_type=ct, codename=codename, defaults={"name": name}
        )
        return p

    view = perm("view_product", "Can view product")
    add = perm("add_product", "Can add product")
    change = perm("change_product", "Can change product")
    delete = perm("delete_product", "Can delete product")
    change_any = perm("change_any_product", "Може редагувати будь-який товар")
    publish = perm("can_publish", "Може публікувати товар")
    stats = perm("view_stats", "Може переглядати звіт")

    storekeeper, _ = Group.objects.get_or_create(name=STOREKEEPER)
    storekeeper.permissions.set([view, add, change])

    manager, _ = Group.objects.get_or_create(name=MANAGER)
    manager.permissions.set([view, add, change, delete, change_any, publish, stats])


def delete_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name__in=[STOREKEEPER, MANAGER]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0006_product_owner_permissions"),
        ("auth", "0001_initial"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.RunPython(create_groups, delete_groups),
    ]