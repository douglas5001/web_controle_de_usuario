
function toggleMenu() {
    const sidebar = document.getElementById('sidebar')
    const content = document.getElementById('conteudoPrincipal')
    const icon = document.getElementById('toggleIcon')
    const logo = document.getElementById('empresaLogo')
  
    sidebar.classList.toggle('active')
    content.classList.toggle('active')
  
    const isActive = sidebar.classList.contains('active')
    icon.className = isActive ? 'bi bi-chevron-left' : 'bi bi-chevron-right'
    logo.style.display = isActive ? 'inline-block' : 'none'
  }
  
  document.addEventListener('DOMContentLoaded', () => {
    // Exemplo de submenus
    const dashCollapse = document.getElementById('collapseDashboard')
    const dashArrow = document.getElementById('arrowDashboard')
    if (dashCollapse && dashArrow) {
      dashCollapse.addEventListener('show.bs.collapse', () => dashArrow.classList.add('rotate'))
      dashCollapse.addEventListener('hide.bs.collapse', () => dashArrow.classList.remove('rotate'))
    }
  
    const adminCollapse = document.getElementById('collapseAdmin')
    const adminArrow = document.getElementById('arrowAdmin')
    if (adminCollapse && adminArrow) {
      adminCollapse.addEventListener('show.bs.collapse', () => adminArrow.classList.add('rotate'))
      adminCollapse.addEventListener('hide.bs.collapse', () => adminArrow.classList.remove('rotate'))
    }
  })
  