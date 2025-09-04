const $ = (s) => document.querySelector(s);
$("#send").addEventListener("click", async () => {
  const msg = $("#msg").value || "";
  const r = await fetch(`/api/echo?msg=${encodeURIComponent(msg)}`);
  const data = await r.json();
  $("#out").textContent = JSON.stringify(data, null, 2);
});
