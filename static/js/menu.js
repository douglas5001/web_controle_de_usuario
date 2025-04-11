function toggleMenu() {
  const menuLateral = document.getElementById('sidebar');
  const conteudoPrincipal = document.getElementById('conteudoPrincipal');
  const iconeToggle = document.getElementById('toggleIcon');
  const logoEmpresa = document.getElementById('empresaLogo');

  const isMobile = window.innerWidth <= 768;
  const menuEstavaAberto = menuLateral.classList.contains('active');

  menuLateral.classList.toggle('active');

  if (isMobile) {
    conteudoPrincipal.classList.toggle('active'); // empurra para baixo
  } else {
    conteudoPrincipal.classList.toggle('active'); // empurra para o lado
    logoEmpresa.style.display = menuLateral.classList.contains('active') ? 'inline-block' : 'none';
    iconeToggle.className = menuLateral.classList.contains('active') ? 'bi bi-chevron-left' : 'bi bi-chevron-right';
  }

  localStorage.setItem('menuAberto', menuLateral.classList.contains('active'));

  if (!menuLateral.classList.contains('active') && menuEstavaAberto) {
    const submenusAbertos = document.querySelectorAll('.collapse.show');
    submenusAbertos.forEach(submenu => {
      const instanciaCollapse = bootstrap.Collapse.getInstance(submenu) || new bootstrap.Collapse(submenu, { toggle: false });
      instanciaCollapse.hide();
    });
  }
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

  const adminCollapse = document.getElementById('collapseFinanceiro');
  const adminSeta = document.getElementById('arrowFinanceiro');
  if (adminCollapse && adminSeta) {
    adminCollapse.addEventListener('show.bs.collapse', () => adminSeta.classList.add('rotate'));
    adminCollapse.addEventListener('hide.bs.collapse', () => adminSeta.classList.remove('rotate'));
  }
});

function abrirMenuLateralSeFechado() {
  const menuLateral = document.getElementById('sidebar');
  const conteudoPrincipal = document.getElementById('conteudoPrincipal');
  const iconeToggle = document.getElementById('toggleIcon');
  const logoEmpresa = document.getElementById('empresaLogo');

  if (!menuLateral.classList.contains('active')) {
    menuLateral.classList.add('active');
    conteudoPrincipal.classList.add('active');
    iconeToggle.className = 'bi bi-chevron-left';
    logoEmpresa.style.display = 'inline-block';
    localStorage.setItem('menuAberto', true);
  }
}

const todosSubmenus = document.querySelectorAll('.collapse');
todosSubmenus.forEach(submenu => {
  submenu.addEventListener('show.bs.collapse', () => abrirMenuLateralSeFechado());
});