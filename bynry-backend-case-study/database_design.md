# Database Design

## Tables

### Companies
- id (PK)
- name
- created_at

### Warehouses
- id (PK)
- company_id (FK)
- name
- location

### Products
- id (PK)
- name
- sku (UNIQUE)
- price (DECIMAL)
- product_type
- created_at

### Inventory
- id (PK)
- product_id (FK)
- warehouse_id (FK)
- quantity
- updated_at

Constraint:
UNIQUE(product_id, warehouse_id)

### Inventory Logs
- id
- product_id
- warehouse_id
- change
- reason
- created_at

### Suppliers
- id
- name
- contact_email

### Product_Suppliers
- product_id
- supplier_id

### Product Bundles
- parent_product_id
- child_product_id
- quantity  