from datetime import datetime

import pytest
from django.db import IntegrityError

from ecommerce.inventory import models

#############################
# for category table
#############################

@pytest.mark.dbfixture
@pytest.mark.parametrize(
    "id, name, slug, is_active",
    [
        (1, "fashion", "fashion", 1),
        (18, "trainers", "trainers", 1),
        (35, "baseball", "baseball", 1),
    ]
)
def test_inventory_category_dbfixture(
    db, db_fixture_setup, id, name, slug, is_active):
    result = models.Category.objects.get(id=id)
    assert result.name == name
    assert result.slug == slug
    assert result.is_active == is_active
    
@pytest.mark.parametrize(
    "slug, is_active",
    [
        ("fashion", 1),
        ("trainers", 1),
        ("baseball", 1),
    ]
)
def test_inventory_db_category_insert_data(
  db, category_factory, slug, is_active  
):
    result = category_factory.create(slug = slug, is_active = is_active)
    assert result.slug == slug
    assert result.is_active == is_active
    
    
    
############################
# for product table  
############################

@pytest.mark.dbfixture
@pytest.mark.parametrize(
    "id, web_id, name, slug, description, is_active, created_at, updated_at",
    [
        (
             1,
            "45425810",
            "widstar running sneakers",
            "widstar-running-sneakers",
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin porta, eros vel sollicitudin lacinia, quam metus gravida elit, a elementum nisl neque sit amet orci. Nulla id lorem ac nunc cursus consequat vitae ut orci. In a velit eu justo eleifend tincidunt vel eu turpis. Praesent eu orci egestas, lobortis magna egestas, tincidunt augue. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Aenean vitae lectus eget tortor laoreet efficitur vel et leo. Maecenas volutpat eget ante id tempor. Etiam posuere ex urna, at aliquet risus tempor eu. Aenean a odio odio. Nunc consectetur lorem ante, interdum ultrices elit consectetur sit amet. Vestibulum rutrum interdum nulla. Cras vel mi a enim eleifend blandit. Curabitur ex dui, rutrum et odio sit amet, auctor euismod massa.",
            1,
            "2021-09-04 22:14:18",
            "2021-09-04 22:14:18",
            
        ),
        
        (
           8616,
            "45434425",
            "impact puse dance shoe",
            "impact-puse-dance-shoe",
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin porta, eros vel sollicitudin lacinia, quam metus gravida elit, a elementum nisl neque sit amet orci. Nulla id lorem ac nunc cursus consequat vitae ut orci. In a velit eu justo eleifend tincidunt vel eu turpis. Praesent eu orci egestas, lobortis magna egestas, tincidunt augue. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Aenean vitae lectus eget tortor laoreet efficitur vel et leo. Maecenas volutpat eget ante id tempor. Etiam posuere ex urna, at aliquet risus tempor eu. Aenean a odio odio. Nunc consectetur lorem ante, interdum ultrices elit consectetur sit amet. Vestibulum rutrum interdum nulla. Cras vel mi a enim eleifend blandit. Curabitur ex dui, rutrum et odio sit amet, auctor euismod massa.",
            1,
            "2021-09-04 22:14:18",
            "2021-09-04 22:14:18",
            
        ),
    ],
)

def test_inventory_db_product_dbfixture(
   db,
   db_fixture_setup,
   id,
   web_id,
   name,
   slug,
   description,
   is_active,
   created_at,
   updated_at,
    ):
    result = models.Product.objects.get(id=id)
    # result_created_at = result.created_at.strftime("%Y-%m-%d %H:%M:%S")
    # result_updated_at = result.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    expected_created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
    expected_updated_at = datetime.strptime(updated_at, "%Y-%m-%d %H:%M:%S")
    assert result.web_id == web_id
    assert result.name == name
    assert result.slug == slug
    assert result.description == description
    assert result.is_active == is_active
    assert result.created_at == expected_created_at
    assert result.updated_at == expected_updated_at
    # assert result.created_at == expected_created_at
    # assert result.updated_at == expected_updated_at
    
  

def test_inventory_db_product_uniqueness_integrity(db, product_factory):
    new_web_id = product_factory.create(web_id = 123456789)
    with pytest.raises(IntegrityError):
        product_factory.create(web_id=123456789)  
        
        
@pytest.mark.dbfixture  
def test_inventory_db_product_insert_data(db, product_factory, category_factory):
    
    new_product = product_factory.create(category=(1, 2, 3, 4, 5))
    result_product_category = new_product.category.all().count()
    assert "web_id_" in new_product.web_id
    assert result_product_category == 5
    





    