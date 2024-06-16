from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField


# Create your models here.
class Category(MPTTModel):
    """
    Inventory Category table implimented with MPTT
    """
    name = models.CharField( max_length=100,
        null=False,
        unique=False,
        blank=False,
        verbose_name=_("category_name"),
        help_text=_("format: required, max-100"),
        )
    
    slug = models.SlugField(
        max_length=150,
        null=False,
        unique=False,
        blank=False,
        verbose_name=_("category safe URL"),
        help_text=_("format: required, letters, numbers, underscores, or hyphens"),
    )
    
    is_active = models.BooleanField(
        default=True,
        
    )
    
    parent = TreeForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="children",
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("parent of category"),
        help_text=_("format: not required"),
    )

    class MPTTMeta:
        order_insertion_by = ["name"]
        
    class Meta:
        verbose_name = _("product category")
        verbose_name_plural = _("product categories")
        
    def __str__(self):
        return self.name
    
      
        
class Product(models.Model):
    """
    product details table
    """
    web_id = models.CharField(
        max_length = 50,
        unique=True,
        null=False,
        blank=False,
        verbose_name = _("product website ID"),
        help_text = _(" formate: required, unique"),
    )
    
    slug = models.SlugField(
        max_length = 255,
        unique=False,
        null=False,
        blank=False,
        verbose_name = _("product safe URL"),
        help_text = _(" formate: required, letters, numbers, underscores or hyphens"),
    )
    name = models.CharField(
        max_length = 50,
        unique=False,
        null=False,
        blank=False,
        verbose_name = _("product name"),
        help_text = _(" formate: required, max_length 255"),
    )
    
    description = models.TextField(
        unique=False,
        null=False,
        blank=False,
        verbose_name = _("product description"),
        help_text = _(" formate: required"),
    )
    category = TreeManyToManyField(Category)
    is_active = models.BooleanField(
        unique = False,
        null = False,
        blank = False,
        default = True,
        verbose_name = _("product visibility"),
        help_text = _("format: true=product visible"),
    )
    
    created_at = models.DateTimeField(
        auto_now_add = True,
        editable = False,
        verbose_name = _("date product created"),
        help_text = _("format: Y-M-D H:M:S"),
    )
    
    updated_at = models.DateTimeField(
        auto_now = True,
        verbose_name = _("date product last updated"),
        help_text = _("format: Y-M-D H:M:S"),
    )
    
    def __str__(self):
        return self.name
    

#
# ProductType 
#

class ProductType(models.Model):

    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("type of product"),
        help_text=_("format: required, unique, max_255"),
    )

    def __str__(self):
        return self.name 

#
# Brand
#

class Brand(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("brand name"),
        help_text=_("format: required, unique, max-255"),
    )

#
# MODEL - ProductInventory
#
class ProductInventory(models.Model):

    sku = models.CharField(
        max_length=20,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("stock keeping unit"),
        help_text=_("format: required, unique, max-20"),
    )

    upc = models.CharField(
        max_length=12,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("universal product code"),
        help_text=_("format: required, unique, max-12"),
    )

    product_type = models.ForeignKey(
        ProductType, related_name="product_type", on_delete=models.PROTECT
    )

    product = models.ForeignKey(
        Product, related_name="product", on_delete=models.PROTECT
    )

    brand = models.ForeignKey(
        Brand, related_name="brand", on_delete=models.PROTECT
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("product visibility"),
        help_text=_("format: true=product visible"),
    )

    is_default = models.BooleanField(
        default=False,
        verbose_name=_("default selection"),
        help_text=_("format: true=sub product selected"),
    )

    retail_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        unique=False,
        null=False,
        blank=False,
        verbose_name=_("recomended retail price"),
        help_text=_("format: maximum price 999.99"),
        error_messages={
            "name":{
                "max_length": _("the price must be between 0 and 999.99"),
            },
        },
    )

    store_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        unique=False,
        null=False,
        blank=False,
        verbose_name=_("regular store price"),
        help_text=_("format: maximum price 999.99"),
        error_messages={
            "name": {
                "max_length": _("the price must be between 0 and 999.99."),
            },
        },
    )

    sale_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        unique=False,
        null=False,
        blank=False,
        verbose_name=_("sale price"),
        help_text=_("format: maximum price 999.99"),
        error_messages={
            "name": {
                "max_length": _("the price must be between 0 and 999.99."),
            },
        },
    )

    weight = models.FloatField(
        unique=False,
        null=False,
        blank=False,
        verbose_name=_("prouct weight"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("date sub-product updated"),
        help_text=_("format: Y-m-d H:M:S"),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("date sub-product updated"),
        help_text=_("format: Y-m-d H:M:S"),
    )

    def __str__(self):
        return self.product.name
    



#########################################
#
# Media table 
#

class Media(models.Model):

    product_inventory = models.ForeignKey(
        ProductInventory,
        on_delete = models.PROTECT,
        related_name="media_product_inventory",
    )
    

    image = models.ImageField(
        unique=False,
        null=False,
        blank=False,
        verbose_name=_("product image"),
        upload_to="images/",
        default="images/default.png",
        help_text=_("format: required, default-default.png"),
    )

    alt_text = models.CharField(
        max_length=255,
        unique=False,
        null=False,
        blank=False,
        verbose_name=_("alternative text"),
        help_text=_("format: required, max-255"),
    )

    is_feature = models.BooleanField(
        default=False,
        verbose_name=_("product default image"),
        help_text=_("format: default=false, true=default image"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("product visibility"),
        help_text=_("format: Y-m-d H:M:S"),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("data sub-prduct created"),
        help_text=_("format: Y-m-d H:M:S"),
    )

    class Meta:
        verbose_name =_("product image")
        verbose_name_plural = _("product images")