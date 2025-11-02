"""Seed script for Service B - Catalog & Fulfillment"""
import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.db.session import SessionLocal, engine, Base
from app.models import Category, Product, ProductImage, Variant, Inventory, Store


def seed_database():
    """Seed the database with initial data"""
    print("Seeding Service B database...")
    
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        if db.query(Category).count() > 0:
            print("Database already seeded. Skipping...")
            return
        
        # Create categories
        categories_data = [
            {"name": "Electronics", "slug": "electronics", "description": "Latest electronic gadgets and devices"},
            {"name": "Clothing", "slug": "clothing", "description": "Fashion and apparel for all"},
            {"name": "Home & Garden", "slug": "home-garden", "description": "Everything for your home"},
            {"name": "Sports & Outdoors", "slug": "sports-outdoors", "description": "Gear for active lifestyle"},
            {"name": "Books", "slug": "books", "description": "Wide selection of books"},
            {"name": "Toys & Games", "slug": "toys-games", "description": "Fun for all ages"},
            {"name": "Beauty & Health", "slug": "beauty-health", "description": "Personal care products"},
            {"name": "Automotive", "slug": "automotive", "description": "Car parts and accessories"},
            {"name": "Food & Grocery", "slug": "food-grocery", "description": "Fresh and packaged foods"},
            {"name": "Pet Supplies", "slug": "pet-supplies", "description": "Everything for your pets"}
        ]
        
        categories = []
        for cat_data in categories_data:
            category = Category(**cat_data)
            db.add(category)
            categories.append(category)
        
        db.commit()
        print(f"✓ Created {len(categories)} categories")
        
        # Create products with variants
        products_data = [
            # Electronics
            {"name": "Wireless Headphones", "category": 0, "price": 79.99, "description": "Premium wireless headphones with noise cancellation"},
            {"name": "Smart Watch", "category": 0, "price": 199.99, "description": "Fitness tracking smartwatch"},
            {"name": "Laptop Stand", "category": 0, "price": 39.99, "description": "Ergonomic aluminum laptop stand"},
            
            # Clothing
            {"name": "Cotton T-Shirt", "category": 1, "price": 19.99, "description": "Comfortable cotton t-shirt"},
            {"name": "Denim Jeans", "category": 1, "price": 49.99, "description": "Classic fit denim jeans"},
            {"name": "Running Shoes", "category": 1, "price": 89.99, "description": "Lightweight running shoes"},
            
            # Home & Garden
            {"name": "Coffee Maker", "category": 2, "price": 79.99, "description": "Programmable coffee maker"},
            {"name": "Throw Pillow Set", "category": 2, "price": 29.99, "description": "Decorative throw pillows"},
            {"name": "LED Desk Lamp", "category": 2, "price": 34.99, "description": "Adjustable LED desk lamp"},
            
            # Sports
            {"name": "Yoga Mat", "category": 3, "price": 24.99, "description": "Non-slip yoga mat"},
            {"name": "Dumbbell Set", "category": 3, "price": 59.99, "description": "Adjustable dumbbell set"},
            {"name": "Water Bottle", "category": 3, "price": 14.99, "description": "Insulated water bottle"},
            
            # Books
            {"name": "Python Programming Guide", "category": 4, "price": 39.99, "description": "Comprehensive Python guide"},
            {"name": "Mystery Novel Collection", "category": 4, "price": 24.99, "description": "Bestselling mystery novels"},
            {"name": "Cookbook: Healthy Meals", "category": 4, "price": 29.99, "description": "Healthy recipe cookbook"},
            
            # Toys
            {"name": "Building Blocks Set", "category": 5, "price": 34.99, "description": "Creative building blocks"},
            {"name": "Board Game", "category": 5, "price": 29.99, "description": "Family board game"},
            {"name": "Remote Control Car", "category": 5, "price": 44.99, "description": "High-speed RC car"},
            
            # Beauty
            {"name": "Skincare Set", "category": 6, "price": 49.99, "description": "Complete skincare routine"},
            {"name": "Hair Dryer", "category": 6, "price": 59.99, "description": "Professional hair dryer"},
            {"name": "Makeup Brush Set", "category": 6, "price": 24.99, "description": "Professional makeup brushes"},
            
            # Automotive
            {"name": "Car Phone Mount", "category": 7, "price": 19.99, "description": "Universal car phone mount"},
            {"name": "Tire Pressure Gauge", "category": 7, "price": 12.99, "description": "Digital tire pressure gauge"},
            {"name": "Car Vacuum Cleaner", "category": 7, "price": 39.99, "description": "Portable car vacuum"},
            
            # Food
            {"name": "Organic Coffee Beans", "category": 8, "price": 14.99, "description": "Premium organic coffee"},
            {"name": "Protein Bars Box", "category": 8, "price": 24.99, "description": "Box of 12 protein bars"},
            {"name": "Green Tea Set", "category": 8, "price": 19.99, "description": "Assorted green teas"},
            
            # Pet Supplies
            {"name": "Dog Food - Premium", "category": 9, "price": 44.99, "description": "High-quality dog food"},
            {"name": "Cat Toy Set", "category": 9, "price": 16.99, "description": "Interactive cat toys"},
            {"name": "Pet Bed", "category": 9, "price": 39.99, "description": "Comfortable pet bed"}
        ]
        
        for i, prod_data in enumerate(products_data):
            product = Product(
                name=prod_data["name"],
                slug=prod_data["name"].lower().replace(" ", "-"),
                description=prod_data["description"],
                base_price=prod_data["price"],
                category_id=categories[prod_data["category"]].id,
                is_active=True,
                featured=(i < 6)  # First 6 are featured
            )
            db.add(product)
            db.flush()
            
            # Add product image
            image = ProductImage(
                product_id=product.id,
                url=f"https://via.placeholder.com/400x400?text={product.name.replace(' ', '+')}",
                alt_text=product.name,
                is_primary=True,
                display_order=0
            )
            db.add(image)
            
            # Add variants
            if "T-Shirt" in product.name or "Jeans" in product.name:
                sizes = ["S", "M", "L", "XL"]
                for size in sizes:
                    variant = Variant(
                        product_id=product.id,
                        sku=f"{product.slug}-{size}".upper(),
                        name=f"{size}",
                        price=product.base_price,
                        weight=0.5,
                        attributes=json.dumps({"size": size})
                    )
                    db.add(variant)
                    db.flush()
                    
                    # Add inventory
                    inventory = Inventory(
                        variant_id=variant.id,
                        quantity=100,
                        reserved=0,
                        available=100,
                        low_stock_threshold=10
                    )
                    db.add(inventory)
            else:
                # Single variant
                variant = Variant(
                    product_id=product.id,
                    sku=f"{product.slug}".upper(),
                    name="Standard",
                    price=product.base_price,
                    weight=1.0,
                    attributes=json.dumps({"type": "standard"})
                )
                db.add(variant)
                db.flush()
                
                inventory = Inventory(
                    variant_id=variant.id,
                    quantity=50,
                    reserved=0,
                    available=50,
                    low_stock_threshold=5
                )
                db.add(inventory)
        
        db.commit()
        print(f"✓ Created {len(products_data)} products with variants and inventory")
        
        # Create store locations
        stores_data = [
            {
                "name": "Downtown Store",
                "address": "123 Main Street",
                "city": "San Francisco",
                "state": "CA",
                "postal_code": "94102",
                "latitude": 37.7749,
                "longitude": -122.4194,
                "phone": "(415) 555-0100",
                "email": "downtown@example.com"
            },
            {
                "name": "Westside Location",
                "address": "456 Ocean Avenue",
                "city": "Los Angeles",
                "state": "CA",
                "postal_code": "90001",
                "latitude": 34.0522,
                "longitude": -118.2437,
                "phone": "(213) 555-0200",
                "email": "westside@example.com"
            },
            {
                "name": "East Coast Hub",
                "address": "789 Broadway",
                "city": "New York",
                "state": "NY",
                "postal_code": "10001",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "phone": "(212) 555-0300",
                "email": "eastcoast@example.com"
            }
        ]
        
        for store_data in stores_data:
            store = Store(**store_data, is_active=True)
            db.add(store)
        
        db.commit()
        print(f"✓ Created {len(stores_data)} store locations")
        
        print("\nService B seeding completed successfully!")
        print(f"Total: {len(categories)} categories, {len(products_data)} products, 3 stores")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
