// ===== GARIX CART & WISHLIST API SCRIPT (Cleaned) =====
document.addEventListener("DOMContentLoaded", function() {

  // Helper: Toast Message
  function showToast(message, type) {
    var existing = document.querySelector(".garix-toast");
    if (existing) existing.remove();
    var toast = document.createElement("div");
    toast.className = "garix-toast";
    var bg = type === "success" ? "#28a745" : "#dc3545";
    toast.style.cssText = "position:fixed;top:30px;left:50%;transform:translateX(-50%);background:"+bg+";color:#fff;padding:18px 40px;border-radius:8px;font-size:17px;font-weight:600;z-index:99999;box-shadow:0 4px 20px rgba(0,0,0,0.3);text-align:center;";
    toast.innerHTML = message;
    document.body.appendChild(toast);
    setTimeout(function() {
      toast.style.opacity = "0";
      toast.style.transition = "opacity 0.5s";
      setTimeout(function(){ toast.remove(); }, 500);
    }, 4000);
  }

  // ===== 1. SHOP PAGE: ADD TO CART =====
  document.querySelectorAll("a.vs-btn.style11").forEach(function(btn) {
    btn.addEventListener("click", async function(e) {
      // IMPORTANT: Page refresh rokne ke liye ye zaruri hai
      e.preventDefault();
      e.stopPropagation();
      
      var product = btn.closest(".vs-product");
      if (!product) return;

      var name  = (product.querySelector(".product-title") || {textContent:""}).textContent.trim();
      var price = (product.querySelector(".product-price") || {textContent:""}).textContent.trim();
      var img   = (product.querySelector(".product-img img") || {src:""}).src;

      // MongoDB Cart Collection se save karne ke liye
      var fd = new FormData();
      fd.append("product_name", name);
      fd.append("product_price", price);
      fd.append("product_img", img);
      fd.append("quantity", "1");
      fd.append("date", new Date().toISOString().split("T")[0]);
      fd.append("time", "00:00");
      fd.append("subject", "Cart Item Added");
      fd.append("message", "Added to Cart from Shop Page");

      try {
        // API Call: /api/cart (MongoDB save)
        var res = await fetch("/api/cart", { method: "POST", body: fd });
        var data = await res.json();
        
        if (data.status === "success") {
          showToast("🛒 Added to Cart! Redirecting...", "success");
          // Redirect to cart page after a delay
          setTimeout(function() {
            window.location.href = "cart.html";
          }, 1000);
        } else {
          showToast("❌ Error!", "error");
        }
      } catch(err) {
        console.log("Cart Error:", err);
        showToast("❌ Server Error!", "error");
      }
    });
  });

  // ===== 2. CART PAGE: LOAD DATA FROM MONGODB =====
  async function loadCart() {
    try {
      // Database se data lao
      var res = await fetch("/api/cart");
      var items = await res.json();
      var tbody = document.querySelector(".cart_table tbody");
      if (!tbody) return;

      // Static rows hata do (taaki fresh data aaye)
      var staticRows = tbody.querySelectorAll("tr.cart_item");
      staticRows.forEach(function(row) { row.remove(); });

      var insertBefore = tbody.querySelector("tr:last-child");

      if (items.length === 0) {
        var emptyRow = document.createElement("tr");
        emptyRow.innerHTML = "<td colspan='6' style='text-align:center;padding:30px;color:#999;'>Cart is empty! <a href='shop.html'>Go Shopping</a></td>";
        tbody.insertBefore(emptyRow, insertBefore);
        return;
      }

      var total = 0;
      items.forEach(function(item) {
        var price = parseFloat((item.product_price || "").replace(/[^0-9.]/g, "")) || 0;
        total += price * (item.quantity || 1);
        
        var tr = document.createElement("tr");
        tr.className = "cart_item";
        tr.setAttribute("data-id", item._id);
        
        // Clean HTML template
        tr.innerHTML = "<td data-title='Product'><a class='cart-productimage' href='shop.html'><img width='100' height='95' src='" + item.product_img + "' alt='Image' onerror=\"this.src='assets/img/shop/product-1-1.jpg'\"'></a></td>" +
                     "<td data-title='Name'><a class='cart-productname' href='shop.html'>" + item.product_name + "</a></td>" +
                     "<td data-title='Price'><span class='amount'><bdi><span>$</span>" + price.toFixed(2) + "</bdi></span></td>" +
                     "<td data-title='Quantity'><div class='quantity style2'><div class='quantity__field'><div class='quantity__buttons'><button class='qty-btn quantity-plus'><i class='fas fa-plus'></i></button><input type='number' class='qty-input' value='" + (item.quantity || 1) + "' min='1' max='100'><button class='qty-btn quantity-minus'><i class='fas fa-minus'></i></button></div></div></div></div></td>" +
                     "<td data-title='Total'><span class='amount'><bdi><span>$</span>" + (price * (item.quantity || 1)).toFixed(2) + "</bdi></span></td>" +
                     "<td data-title='Remove'><a href='#' class='remove cart-remove-btn' data-id='" + item._id + "'><i class='fas fa-trash-alt'></i></a></td>";
        
        tbody.insertBefore(tr, insertBefore);
    });

    // Cart Totals update karo
    var totalEls = document.querySelectorAll(".cart_totals .amount bdi");
    totalEls.forEach(function(el) { el.innerHTML = "<span>$</span>" + total.toFixed(2); });

  } catch(err) {
    console.log("Cart Load Error:", err);
  }
}

// ===== 3. DELETE BUTTON (Remove from Cart) =====
document.addEventListener("click", async function(e) {
  var removeBtn = e.target.closest(".cart-remove-btn");
  if (removeBtn) {
    e.preventDefault();
    var id = removeBtn.getAttribute("data-id");
    try {
      await fetch("/api/cart/" + id, { method: "DELETE" });
      loadCart(); // Database refresh karne ke liye
    } catch(err) { console.log("Delete Error:", err); }
  }
});

// ===== 4. WISHLIST BUTTON (Optional) =====
document.querySelectorAll(".icon-btn .fa-heart").forEach(function(btn) {
  btn.addEventListener("click", async function(e) {
    e.preventDefault();
    showToast("❤️ Wishlist feature coming soon!", "success");
  });
});

// ===== 5. CART PAGE AUTO-LOAD =====
if (document.querySelector(".cart_table")) {
  loadCart();
}
});
