const corpoTabela = document.querySelector('#tabelaUsuarios tbody')
const botaoEditar = document.getElementById('btnEditar')
const botaoExcluir = document.getElementById('btnExcluir')
let linhaSelecionada = null

corpoTabela.addEventListener('click', e => {
  const linha = e.target.closest('tr')
  if (!linha) return
  if (linhaSelecionada !== linha) {
    if (linhaSelecionada) linhaSelecionada.classList.remove('table-active')
    linhaSelecionada = linha
    linhaSelecionada.classList.add('table-active')
  } else {
    linhaSelecionada.classList.remove('table-active')
    linhaSelecionada = null
  }
  botaoEditar.disabled = !linhaSelecionada
  botaoExcluir.disabled = !linhaSelecionada
})

botaoEditar.addEventListener('click', () => {
  if (!linhaSelecionada) return
  const idUsuario = linhaSelecionada.getAttribute('data-id')
  const nomeUsuario = linhaSelecionada.getAttribute('data-name')
  const emailUsuario = linhaSelecionada.getAttribute('data-email')
  const adminUsuario = linhaSelecionada.getAttribute('data-is-admin')
  const formEdicao = document.querySelector('#modalEdicaoUsuario form')
  formEdicao.action = `/${idUsuario}/update_user`
  document.getElementById('edicaoId').value = idUsuario
  document.getElementById('edicaoNome').value = nomeUsuario
  document.getElementById('edicaoEmail').value = emailUsuario
  document.getElementById('edicaoAdmin').value = adminUsuario
})

botaoExcluir.addEventListener('click', () => {
  if (!linhaSelecionada) return
  const idUsuario = linhaSelecionada.getAttribute('data-id')
  if (confirm('Deseja excluir este registro?')) {
    window.location.href = `/${idUsuario}/remove_user`
  }
})