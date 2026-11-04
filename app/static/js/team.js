document.getElementById('invite-form')?.addEventListener('submit', async function(e) {
  e.preventDefault();
  
  const formData = new FormData(this);
  
  try {
    const response = await fetch('/admin/team/invite', {
      method: 'POST',
      body: formData
    });
    
    const result = await response.json();
    
    if (response.ok) {
      if (result.channel === 'whatsapp') {
        window.open(result.invite_url, '_blank');
      } else {
        alert('Convite por e-mail gerado com sucesso!');
      }
      document.getElementById('modal-invite').style.display = 'none';
      location.reload();
    } else {
      alert(result.detail || 'Erro ao enviar convite.');
    }
  } catch (error) {
    alert('Erro de conexão com o servidor.');
  }
});

async function delegateRole(userId) {
  if (!confirm("Tem certeza que deseja transferir a função de Coordenador do Projeto? O seu nível de acesso será ajustado para Supervisor.")) {
    return;
  }
  
  try {
    const response = await fetch(`/admin/team/delegate-coordinator/${userId}`, {
      method: 'POST'
    });
    const result = await response.json();
    alert(result.message);
    location.reload();
  } catch (error) {
    alert('Erro ao processar transferência de cargo.');
  }
}