from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        call_command("makemigrations")
        call_command("migrate")
        call_command("loaddata", "db_admin_fixture.json")
        call_command("loaddata", "db_category_fixture.json")
        call_command("loaddata", "db_product_fixture.json")

        # db_brand_fixture.json and db_type_fixture.json must 
        # be loaded first then db_product_inventory_fixture.json cause they are foreign_keys in ProductInventory table.
        call_command("loaddata", "db_brand_fixture.json") 
        call_command("loaddata", "db_type_fixture.json")
        call_command("loaddata", "db_product_inventory_fixture.json")
        call_command("loaddata", "db_media_fixture.json")