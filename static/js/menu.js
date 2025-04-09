function toggleMenu() {
  const menuLateral = document.getElementById('sidebar');
  const conteudoPrincipal = document.getElementById('conteudoPrincipal');
  const iconeToggle = document.getElementById('toggleIcon');
  const logoEmpresa = document.getElementById('empresaLogo');

  menuLateral.classList.toggle('active');
  conteudoPrincipal.classList.toggle('active');

  const menuAberto = menuLateral.classList.contains('active');
  iconeToggle.className = menuAberto ? 'bi bi-chevron-left' : 'bi bi-chevron-right';
  logoEmpresa.style.display = menuAberto ? 'inline-block' : 'none';

  localStorage.setItem('menuAberto', menuAberto);
}

document.addEventListener('DOMContentLoaded', () => {
  const menuLateral = document.getElementById('sidebar');
  const conteudoPrincipal = document.getElementById('conteudoPrincipal');
  const iconeToggle = document.getElementById('toggleIcon');
  const logoEmpresa = document.getElementById('empresaLogo');

  const menuAbertoStorage = localStorage.getItem('menuAberto') === 'true';

  if (menuAbertoStorage) {
    menuLateral.classList.add('active');
    conteudoPrincipal.classList.add('active');
    iconeToggle.className = 'bi bi-chevron-left';
    logoEmpresa.style.display = 'inline-block';
  } else {
    menuLateral.classList.remove('active');
    conteudoPrincipal.classList.remove('active');
    iconeToggle.className = 'bi bi-chevron-right';
    logoEmpresa.style.display = 'none';
  }

  const dashboardCollapse = document.getElementById('collapseDashboard');
  const dashboardSeta = document.getElementById('arrowDashboard');
  if (dashboardCollapse && dashboardSeta) {
    dashboardCollapse.addEventListener('show.bs.collapse', () => dashboardSeta.classList.add('rotate'));
    dashboardCollapse.addEventListener('hide.bs.collapse', () => dashboardSeta.classList.remove('rotate'));
  }

  const adminCollapse = document.getElementById('collapseAdmin');
  const adminSeta = document.getElementById('arrowAdmin');
  if (adminCollapse && adminSeta) {
    adminCollapse.addEventListener('show.bs.collapse', () => adminSeta.classList.add('rotate'));
    adminCollapse.addEventListener('hide.bs.collapse', () => adminSeta.classList.remove('rotate'));
  }
});
