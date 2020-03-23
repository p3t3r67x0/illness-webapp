from django.db import migrations

SYMPTOMS = [
    "Durchfall",
]


def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Symptom = apps.get_model("datastore", "Symptom")
    for s in SYMPTOMS:
        Symptom.objects.get_or_create(name=s)


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("datastore", "0009_auto_20200322_1251"),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
