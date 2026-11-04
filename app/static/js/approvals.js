async function approveRequest(requestId) {
  try {
    const response = await fetch(`/admin/approvals/${requestId}/approve`, {
      method: 'POST'
    });
    const result = await response.json();
    if (response.ok) {
      alert(result.message);
      location.reload();
    } else {
      alert(result.detail || 'Erro ao aprovar.');
    }
  } catch (error) {
    alert('Erro na comunicação com o servidor.');
  }
}

async function rejectRequest(requestId) {
  const reason = prompt("Informe o motivo da rejeição da alteração:");
  if (!reason) return;
  
  const formData = new FormData();
  formData.append('reason', reason);
  
  try {
    const response = await fetch(`/admin/approvals/${requestId}/reject`, {
      method: 'POST',
      body: formData
    });
    const result = await response.json();
    if (response.ok) {
      alert(result.message);
      location.reload();
    } else {
      alert(result.detail || 'Erro ao rejeitar.');
    }
  } catch (error) {
    alert('Erro na comunicação com o servidor.');
  }
}


