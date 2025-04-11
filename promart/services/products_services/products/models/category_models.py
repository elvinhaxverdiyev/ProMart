from django.db import models


class Category(models.Model):
    """
    Represents a category which can be a main category or a subcategory.
    Includes information such as name, icon, order, and whether it"s active.
    Allows creation of subcategories under a main category.
    """
    name = models.CharField(
        "Name", 
        max_length=255,  
        unique=True
    )
    icon = models.FileField(
        "Image", 
        upload_to="categories/%Y/%m/%d/",
        null=True,
        blank=True
    )
    order = models.IntegerField(
        "Order", 
        null=True,
        blank=True,
        default=None
    )
    is_active = models.BooleanField(
        "Is active", 
        default=True
    )
    super_category = models.ForeignKey(
        "self",
        verbose_name="Main category",
        null=True, 
        blank=True,
        on_delete=models.SET_NULL,  
        related_name="subcategories",
        related_query_name="subcategory"
    )

    class Meta:
        unique_together = ("super_category", "order")
        ordering = ["order"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        """
        Returns the name of the category.
        
        Returns:
            str: The name of the category.
        """
        return self.name

    def save(self, *args, **kwargs) -> None:
        """
        Sets the slug and order value, and ensures subcategories have active super categories.
        
        If the category is a subcategory, its super category must be active.
        If the order is not set, it is automatically calculated.
        
        Args:
            *args: Positional arguments passed to the parent class"s save method.
            **kwargs: Keyword arguments passed to the parent class"s save method.
        """
        if self.order is None:
            self.order = self.get_next_order()

        # If this is a subcategory, make sure it has a super category
        if self.super_category and not self.super_category.is_active:
            raise ValueError("Super category must be active to create subcategory.")
        
        super().save(*args, **kwargs)

    def get_next_order(self) -> int:
        """
        Returns the next order value for the super category.
        
        If there is no super category, the first category gets order 1.
        
        Returns:
            int: The next order value for this category.
        """
        if not self.super_category:
            return 1 
        
        last_order = Category.objects.filter(
            super_category=self.super_category
        ).aggregate(models.Max("order"))["order__max"]

        return (last_order or 0) + 1

    def get_super_category_name(self) -> str | None:
        """
        Returns the name of the super category or None if no super category exists.
        
        Returns:
            str | None: The name of the super category or None if not applicable.
        """
        if self.super_category is not None:
            return self.super_category.name
        return None

    @property
    def is_subcategory(self) -> bool:
        """
        Returns True if the category is a subcategory, False otherwise.
        
        Returns:
            bool: True if the category has a super category, False otherwise.
        """
        return self.super_category is not None

    def create_subcategory(self, name: str) -> "Category":
        """
        Creates a subcategory under this category and returns the created subcategory.
        
        Args:
            name (str): The name of the new subcategory.
        
        Returns:
            Category: The created subcategory.
        """
        subcategory = Category.objects.create(
            name=name,
            super_category=self
        )
        return subcategory

    @classmethod
    def create_super_category(cls, name: str) -> "Category":
        """
        Creates a super category with no subcategories initially and returns it.
        
        Args:
            name (str): The name of the super category.
        
        Returns:
            Category: The created super category.
        """
        super_category = cls.objects.create(name=name)
        return super_category