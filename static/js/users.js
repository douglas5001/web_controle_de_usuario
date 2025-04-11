const corpoTabela  = document.querySelector('#tabelaUsuarios tbody');
const botaoEditar  = document.getElementById('btnEditar');
const botaoExcluir = document.getElementById('btnExcluir');
let   linhaSelecionada = null;

/* -------- seleção de linha -------- */
corpoTabela.addEventListener('click', e => {
  const linha = e.target.closest('tr');
  if (!linha) return;

  if (linhaSelecionada !== linha) {
    if (linhaSelecionada) linhaSelecionada.classList.remove('table-active');
    linhaSelecionada = linha;
    linhaSelecionada.classList.add('table-active');
  } else {
    linhaSelecionada.classList.remove('table-active');
    linhaSelecionada = null;
  }
  botaoEditar.disabled  = !linhaSelecionada;
  botaoExcluir.disabled = !linhaSelecionada;
});

/* -------- abre modal de edição ----- */
botaoEditar.addEventListener('click', () => {
  if (!linhaSelecionada) return;

  const idUsuario    = linhaSelecionada.dataset.id;
  const nomeUsuario  = linhaSelecionada.dataset.name;
  const emailUsuario = linhaSelecionada.dataset.email;
  const profileId    = linhaSelecionada.dataset.profileId || "";

  /* converte para lowercase p/ casar com <option value="true|false"> */
  const adminUsuario = (linhaSelecionada.dataset.isAdmin || "").toLowerCase();

  const formEdicao = document.querySelector('#modalEdicaoUsuario form');
  formEdicao.action = `/${idUsuario}/update_user`;

  document.getElementById('edicaoId').value      = idUsuario;
  document.getElementById('edicaoNome').value    = nomeUsuario;
  document.getElementById('edicaoEmail').value   = emailUsuario;
  document.getElementById('edicaoAdmin').value   = adminUsuario;
  document.getElementById('edicaoProfile').value = profileId;

  /* zera switch/senha a cada abertura */
  const switchSenha = document.getElementById("switchAlterarSenha");
  const inputSenha  = document.getElementById("edicaoSenha");
  switchSenha.checked = false;
  inputSenha.disabled = true;
  inputSenha.value    = "";
});

/* ---- habilita/desabilita senha ---- */
document.addEventListener("DOMContentLoaded", () => {
  const switchSenha = document.getElementById("switchAlterarSenha");
  const inputSenha  = document.getElementById("edicaoSenha");

  switchSenha.addEventListener("change", () => {
    inputSenha.disabled = !switchSenha.checked;
    if (!switchSenha.checked) inputSenha.value = "";
  });
});

/* ------------- exclusão ------------- */
botaoExcluir.addEventListener('click', () => {
  if (!linhaSelecionada) return;
  const idUsuario = linhaSelecionada.dataset.id;
  if (confirm('Deseja excluir este registro?')) {
    window.location.href = `/${idUsuario}/remove_user`;
  }
});
