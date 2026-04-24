// ===== GARIX GLOBAL API SCRIPT =====
document.addEventListener("DOMContentLoaded", function() {

  // Newsletter form - har page pe kaam karega
  var newsletter = document.querySelector("form.subscribe-block--style1");
  if (newsletter) {
    newsletter.removeAttribute("action");
    newsletter.addEventListener("submit", async function(e) {
      e.preventDefault();
      var emailInput = newsletter.querySelector("input");
      if (!emailInput || !emailInput.value.trim()) { alert("Email daalo!"); return; }
      var fd = new FormData();
      fd.append("email", emailInput.value.trim());
      try {
        var res = await fetch("/api/subscribe", { method: "POST", body: fd });
        var data = await res.json();
        if (data.status === "success") { alert("Subscribed successfully!"); emailInput.value = ""; }
        else { alert("Something went wrong!"); }
      } catch(err) { alert("Server error!"); }
    });
  }

  // Appointment form - jo bhi page pe ho
  var appointForm = document.querySelector("form.ajax-contact");
  if (appointForm) {
    appointForm.removeAttribute("action");
    appointForm.removeAttribute("method");
    appointForm.addEventListener("submit", async function(e) {
      e.preventDefault();
      var btn = appointForm.querySelector("button[type='submit']");
      var orig = btn ? btn.innerHTML : "";
      if (btn) { btn.innerHTML = "Sending..."; btn.disabled = true; }
      var fd = new FormData();
      fd.append("name",    (appointForm.querySelector("[name='name']") || {value:""}).value.trim());
      fd.append("email",   (appointForm.querySelector("[name='email']") || {value:""}).value.trim());
      fd.append("date",    (appointForm.querySelector("[name='date']") || {value: new Date().toISOString().split("T")[0]}).value || new Date().toISOString().split("T")[0]);
      fd.append("time",    (appointForm.querySelector("[name='time']") || {value:"00:00"}).value || "00:00");
      fd.append("subject", (appointForm.querySelector("[name='subject']") || {value:"General"}).value);
      fd.append("message", "");
      try {
        var res = await fetch("/api/appointment", { method: "POST", body: fd });
        var data = await res.json();
        if (data.status === "success") {
          var msg = document.querySelector(".form-messages");
          if (msg) { msg.style.color = "#28a745"; msg.textContent = "Appointment booked successfully!"; }
          else { alert("Appointment booked successfully!"); }
          appointForm.reset();
        }
      } catch(err) { alert("Server error!"); }
      finally { if (btn) { btn.innerHTML = orig; btn.disabled = false; } }
    });
  }

});
