document.addEventListener('click', function(e){
  const btn = e.target.closest('.req-action');
  if (!btn) return;
  const reqId = btn.dataset.reqId;
  const action = btn.dataset.action;
  const li = document.getElementById(`req-${reqId}`);
  if (li){
    li.querySelectorAll('.req-action').forEach(b=>b.remove());
    const statusEl = li.querySelector('.req-status');
    if (statusEl) statusEl.textContent = action === 'accept' ? 'accepted' : 'denied';
  }
  const csrf = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
  fetch(`/requests/${reqId}/${action}/`, { method: 'POST', headers: { 'X-CSRFToken': csrf } })
    .then(resp => { if (!resp.ok) location.reload(); });
});