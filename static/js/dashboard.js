(function () {
  const list = document.getElementById("server-list");
  if (!list) return;

  const refreshMs = Number(list.dataset.refreshMs || 5000);
  const cards = Array.from(list.querySelectorAll(".server-card[data-server-id]"));

  function setMetric(card, key, value) {
    const el = card.querySelector(`[data-metric="${key}"]`);
    if (el) el.textContent = value;
  }

  async function refreshCard(card) {
    const id = card.dataset.serverId;
    try {
      const res = await fetch(`/api/servers/${id}/metrics`, {
        headers: { Accept: "application/json" },
        credentials: "same-origin",
      });
      if (!res.ok) return;
      const data = await res.json();
      setMetric(card, "cpu", `${data.cpu_percent}%`);
      setMetric(
        card,
        "memory",
        `${data.memory.used_gib} / ${data.memory.total_gib} GiB`
      );
      setMetric(card, "net_in", `${data.network.in_mbps} MB/s`);
      setMetric(card, "net_out", `${data.network.out_mbps} MB/s`);
      setMetric(card, "ports", (data.listening_ports || []).join(", "));
    } catch (_) {
      /* keep last values on transient errors */
    }
  }

  function refreshAll() {
    cards.forEach(refreshCard);
  }

  refreshAll();
  if (cards.length) {
    setInterval(refreshAll, refreshMs);
  }
})();
