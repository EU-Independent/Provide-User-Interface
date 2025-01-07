from django.db import migrations

def load_license_data(apps, schema_editor):
    License = apps.get_model('provide', 'License')
    data = [
        {
            "name": "CC0 1.0 Universal (Public Domain Dedication)",
            "access_url": "https://creativecommons.org/publicdomain/zero/1.0/",
        },
        {
            "name": "CC BY 4.0 (Attribution 4.0 International)",
            "access_url": "https://creativecommons.org/licenses/by/4.0/",
        },
        {
            "name": "CC BY-SA 4.0 (Attribution-ShareAlike 4.0 International)",
            "access_url": "https://creativecommons.org/licenses/by-sa/4.0/",
        },
        {
            "name": "CC BY-NC 4.0 (Attribution-NonCommercial 4.0 International)",
            "access_url": "https://creativecommons.org/licenses/by-nc/4.0/",
        },
        {
            "name": "CC BY-NC-SA 4.0 (Attribution-NonCommercial-ShareAlike 4.0 International)",
            "access_url": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
        },
        {
            "name": "CC BY-ND 4.0 (Attribution-NoDerivatives 4.0 International)",
            "access_url": "https://creativecommons.org/licenses/by-nd/4.0/",
        },
    ]
    for item in data:
        License.objects.get_or_create(name=item['name'], defaults={'access_url': item['access_url']})

class Migration(migrations.Migration):
    dependencies = [
        ('provide', '0002_license'),  # Update to point to your last migration
    ]

    operations = [
        migrations.RunPython(load_license_data),
    ]
