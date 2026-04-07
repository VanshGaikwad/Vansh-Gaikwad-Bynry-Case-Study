from flask import Flask, request, jsonify
from decimal import Decimal

app = Flask(__name__)

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json

    try:
        # Validate required fields
        if not data or 'name' not in data or 'sku' not in data or 'price' not in data:
            return jsonify({"error": "Missing required fields"}), 400

        # Check SKU uniqueness
        existing_product = Product.query.filter_by(sku=data['sku']).first()
        if existing_product:
            return jsonify({"error": "SKU already exists"}), 400

        # Create product (not tied to single warehouse)
        product = Product(
            name=data['name'],
            sku=data['sku'],
            price=Decimal(str(data['price']))
        )

        db.session.add(product)
        db.session.flush()  # get product.id before commit

        # Optional inventory creation
        if 'warehouse_id' in data and 'initial_quantity' in data:
            inventory = Inventory(
                product_id=product.id,
                warehouse_id=data['warehouse_id'],
                quantity=data['initial_quantity']
            )
            db.session.add(inventory)

        db.session.commit()

        return jsonify({
            "message": "Product created successfully",
            "product_id": product.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500