from django.db import migrations

SYMPTOMS = [
    "Fieber",
    "Unwohlsein",
    "Schüttelfrost",
    "Hitzewallungen",
    "Kurzatmigkeit oder Atembeschwerden",
    "Müdigkeit",
    "Gliederschmerzen",
    "Laufende Nase",
    "Husten",
    "Halsschmerzen",
]


def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Symptom = apps.get_model("datastore", "Symptom")
    for s in SYMPTOMS:
        Symptom.objects.get_or_create(name=s)


def reverse_func(apps, schema_editor):
    Symptom = apps.get_model("datastore", "Symptom")
    Symptom.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("datastore", "0006_auto_20200321_1927"),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
