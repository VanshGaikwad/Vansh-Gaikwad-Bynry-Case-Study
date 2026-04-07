from flask import jsonify

@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def low_stock_alerts(company_id):
    try:
        alerts = []

        # Get warehouses of company
        warehouses = Warehouse.query.filter_by(company_id=company_id).all()

        for warehouse in warehouses:
            # Join inventory with products
            items = db.session.query(Inventory, Product)\
                .join(Product, Inventory.product_id == Product.id)\
                .filter(Inventory.warehouse_id == warehouse.id)\
                .all()

            for inv, product in items:

                # Default threshold
                threshold = getattr(product, 'threshold', 10)

                # Assume helper function exists
                sales_rate = get_sales_rate(product.id, warehouse.id)

                # Skip if no recent sales
                if not sales_rate or sales_rate == 0:
                    continue

                if inv.quantity < threshold:
                    days_until_stockout = inv.quantity / sales_rate if sales_rate else None

                    # Get supplier
                    supplier = db.session.query(Supplier)\
                        .join(ProductSupplier)\
                        .filter(ProductSupplier.product_id == product.id)\
                        .first()

                    alerts.append({
                        "product_id": product.id,
                        "product_name": product.name,
                        "sku": product.sku,
                        "warehouse_id": warehouse.id,
                        "warehouse_name": warehouse.name,
                        "current_stock": inv.quantity,
                        "threshold": threshold,
                        "days_until_stockout": int(days_until_stockout) if days_until_stockout else None,
                        "supplier": {
                            "id": supplier.id if supplier else None,
                            "name": supplier.name if supplier else None,
                            "contact_email": supplier.contact_email if supplier else None
                        }
                    })

        return jsonify({
            "alerts": alerts,
            "total_alerts": len(alerts)
        })

    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500