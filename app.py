import os
import uuid
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "medusa-shop-secret-key-2026")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "medusa123")

PRODUCTS = [
    {
        "id": 1,
        "title": "Kablosuz Oyuncu Kulaklığı RGB Surround",
        "category": "Elektronik",
        "price": 1249.00,
        "old_price": 1699.00,
        "rating": 4.8,
        "reviews": 342,
        "badge": "Kargo Bedava",
        "fast_delivery": True,
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&auto=format&fit=crop&q=80",
        "description": "Düşük gecikmeli kablosuz bağlantı, yumuşak pedler ve net mikrofon kalitesi."
    },
    {
        "id": 2,
        "title": "Mekanik RGB Klavye Red Switch Türkçe",
        "category": "Oyun & Ekipman",
        "price": 1590.00,
        "old_price": 2100.00,
        "rating": 4.9,
        "reviews": 518,
        "badge": "Hızlı Teslimat",
        "fast_delivery": True,
        "image": "https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?w=600&auto=format&fit=crop&q=80",
        "description": "Sessiz ve tepkisel Red Switch yapısı, çoklu ışık modları ve dayanıklı tuş kapakları."
    },
    {
        "id": 3,
        "title": "Oversize Hoodie Streetwear Pamuklu",
        "category": "Giyim",
        "price": 799.50,
        "old_price": 1050.00,
        "rating": 4.6,
        "reviews": 129,
        "badge": "Avantajlı Paket",
        "fast_delivery": False,
        "image": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=600&auto=format&fit=crop&q=80",
        "description": "3 iplik şardonlu kumaş, modern kesim ve dört mevsim rahat kullanım."
    },
    {
        "id": 4,
        "title": "Akıllı Saat AMOLED Ekran Nabız & Spor",
        "category": "Elektronik",
        "price": 1899.00,
        "old_price": 2499.00,
        "rating": 4.7,
        "reviews": 276,
        "badge": "Kargo Bedava",
        "fast_delivery": True,
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop&q=80",
        "description": "Canlı ekran, bildirim desteği, uzun pil ömrü ve değiştirilebilir kayış."
    },
    {
        "id": 5,
        "title": "25000 mAh Hızlı Şarj Powerbank Type-C",
        "category": "Aksesuar",
        "price": 949.00,
        "old_price": 1199.00,
        "rating": 4.8,
        "reviews": 410,
        "badge": "Hızlı Teslimat",
        "fast_delivery": True,
        "image": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=600&auto=format&fit=crop&q=80",
        "description": "Aynı anda birden fazla cihazı hızlı şarj edebilen yüksek kapasiteli taşınabilir batarya."
    },
    {
        "id": 6,
        "title": "Minimalist Sırt Çantası Laptop Bölmeli",
        "category": "Aksesuar",
        "price": 689.00,
        "old_price": 890.00,
        "rating": 4.5,
        "reviews": 94,
        "badge": "Kargo Bedava",
        "fast_delivery": False,
        "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600&auto=format&fit=crop&q=80",
        "description": "Suya dayanıklı dış yüzey, ergonomik askılar ve günlük kullanım için bölmeli tasarım."
    }
]

ORDERS = []


def is_admin():
    return session.get("is_admin") is True


@app.route("/")
def index():
    categories = ["Tümü"] + sorted(list({p["category"] for p in PRODUCTS}))
    return render_template("index.html", categories=categories)


@app.route("/api/products", methods=["GET"])
def get_products():
    q = (request.args.get("q") or "").strip().lower()
    category = (request.args.get("category") or "Tümü").strip()
    sort_by = (request.args.get("sort") or "popular").strip()

    filtered = []
    for p in PRODUCTS:
        if category != "Tümü" and p["category"].lower() != category.lower():
            continue
        if q and q not in p["title"].lower() and q not in p["category"].lower() and q not in p["description"].lower():
            continue
        filtered.append(p)

    if sort_by == "price_asc":
        filtered.sort(key=lambda x: x["price"])
    elif sort_by == "price_desc":
        filtered.sort(key=lambda x: x["price"], reverse=True)
    elif sort_by == "rating":
        filtered.sort(key=lambda x: x["rating"], reverse=True)
    else:
        filtered.sort(key=lambda x: x["reviews"], reverse=True)

    return jsonify({"products": filtered})


@app.route("/api/orders", methods=["POST"])
def create_order():
    data = request.get_json(silent=True) or {}
    customer_name = (data.get("customer_name") or "").strip()
    phone = (data.get("phone") or "").strip()
    address = (data.get("address") or "").strip()
    items = data.get("items") or []

    if not customer_name or not phone or not address or not items:
        return jsonify({"ok": False, "error": "Lütfen ad soyad, telefon, adres ve sepet ürünlerini doldurun."}), 400

    total = 0.0
    clean_items = []
    for item in items:
        try:
            pid = int(item.get("id"))
            qty = int(item.get("qty", 1))
        except (TypeError, ValueError):
            continue
        if qty < 1:
            continue
        prod = next((p for p in PRODUCTS if p["id"] == pid), None)
        if prod:
            line_total = round(prod["price"] * qty, 2)
            total = round(total + line_total, 2)
            clean_items.append({
                "id": prod["id"],
                "title": prod["title"],
                "price": prod["price"],
                "qty": qty,
                "line_total": line_total
            })

    if not clean_items:
        return jsonify({"ok": False, "error": "Sepette geçerli ürün bulunamadı."}), 400

    order = {
        "order_code": f"MDS-{str(uuid.uuid4())[:6].upper()}",
        "customer_name": customer_name,
        "phone": phone,
        "address": address,
        "items": clean_items,
        "total": total,
        "status": "Sipariş Alındı"
    }
    ORDERS.insert(0, order)
    return jsonify({"ok": True, "order": order})


@app.route("/admin", methods=["GET", "POST"])
def admin():
    error = None
    if request.method == "POST":
        password = request.form.get("password") or ""
        if password == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect(url_for("admin"))
        error = "Şifre hatalı kanka."

    if not is_admin():
        return render_template("index.html", categories=["Tümü"], admin_login=True, admin_error=error)

    categories = ["Tümü"] + sorted(list({p["category"] for p in PRODUCTS}))
    return render_template(
        "index.html",
        categories=categories,
        admin_panel=True,
        products_list=PRODUCTS,
        orders_list=ORDERS
    )


@app.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    return redirect(url_for("index"))


@app.route("/api/admin/products", methods=["POST"])
def admin_add_product():
    if not is_admin():
        return jsonify({"ok": False, "error": "Yetkisiz erişim."}), 401

    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    category = (data.get("category") or "Genel").strip()
    description = (data.get("description") or "Kaliteli ve özenle seçilmiş ürün.").strip()
    badge = (data.get("badge") or "Kargo Bedava").strip()
    fast_delivery = bool(data.get("fast_delivery", True))
    image = (data.get("image") or "").strip()

    if not image.startswith(("http://", "https://")):
        image = "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop&q=80"

    try:
        price = round(float(data.get("price")), 2)
        old_price_raw = data.get("old_price")
        old_price = round(float(old_price_raw), 2) if old_price_raw not in (None, "") else None
        rating = round(float(data.get("rating") or 4.8), 1)
    except (TypeError, ValueError):
        return jsonify({"ok": False, "error": "Fiyat veya puan değeri geçersiz."}), 400

    if not title or price <= 0:
        return jsonify({"ok": False, "error": "Ürün adı ve geçerli bir fiyat zorunludur."}), 400

    next_id = max([p["id"] for p in PRODUCTS], default=0) + 1
    new_prod = {
        "id": next_id,
        "title": title,
        "category": category,
        "price": price,
        "old_price": old_price,
        "rating": min(max(rating, 1.0), 5.0),
        "reviews": 1,
        "badge": badge,
        "fast_delivery": fast_delivery,
        "image": image,
        "description": description
    }
    PRODUCTS.insert(0, new_prod)
    return jsonify({"ok": True, "product": new_prod})


@app.route("/api/admin/products/<int:product_id>", methods=["DELETE"])
def admin_delete_product(product_id):
    if not is_admin():
        return jsonify({"ok": False, "error": "Yetkisiz erişim."}), 401

    global PRODUCTS
    before = len(PRODUCTS)
    PRODUCTS = [p for p in PRODUCTS if p["id"] != product_id]
    if len(PRODUCTS) == before:
        return jsonify({"ok": False, "error": "Ürün bulunamadı."}), 404
    return jsonify({"ok": True})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
