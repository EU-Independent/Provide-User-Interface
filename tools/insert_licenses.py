
import os
import sys
import django
import json

# Setup Django environment
project_root = os.path.dirname(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from provide.models import License

# Path to your licenses JSON file
LICENSES_JSON = os.path.join(os.path.dirname(__file__), "licenses.json")

def insert_licenses(json_file):
    with open(json_file, "r") as f:
        licenses = json.load(f)
    for lic in licenses:
        name = lic.get("name")
        access_url = lic.get("access_url")
        if not name or not access_url:
            print(f"Skipping: missing name or access_url for {lic}")
            continue
        obj, created = License.objects.get_or_create(name=name, defaults={"access_url": access_url})
        if not created:
            obj.access_url = access_url
            obj.save()
        print(f"{'Created' if created else 'Updated'}: {obj.name} -> {obj.access_url}")

if __name__ == "__main__":
    insert_licenses(LICENSES_JSON)
    print("License insertion complete.")
