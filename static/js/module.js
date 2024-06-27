document.addEventListener('DOMContentLoaded', () => {
  const collapsibleContainer = document.querySelector('.modules__container')

  fetch('http://127.0.0.1:8000/modules-api/units/list')
    .then(res => res.json())
    .then(units => units.map(unit => createUnit(unit)))

  function createUnit (unit) {
    const unitDiv = `
      <div class="unit">
        <button class="collapsible">${unit.title}<i class="fas fa-chevron-up"></i></button>
        <div class="content" id="unit-${unit.id}-content"></div>
      </div>`
    collapsibleContainer.innerHTML += unitDiv

    const contentDiv = document.getElementById(`unit-${unit.id}-content`)
    fetch(`http://127.0.0.1:8000/modules-api/modules/list/?unit=${unit.id}`)
      .then(res => res.json())
      .then(modules => modules.map(module => createModule(module, contentDiv)))

    // Add event listener to collapsible button
    const buttons = collapsibleContainer.querySelectorAll('.collapsible')
    buttons.forEach(button => {
      button.addEventListener('click', function () {
        this.classList.toggle('active')
        const content = this.nextElementSibling
        content.style.maxHeight = content.style.maxHeight
          ? null
          : content.scrollHeight + 'px'
        const icon = this.querySelector('i')
        icon.classList.toggle('fa-chevron-up')
        icon.classList.toggle('fa-chevron-down')
      })
    })
  }

  function createModule (module, contentDiv) {
    const moduleDiv = `
      <div class="module">
        <a href="/modules/module/${module.id}/">
          <img src="${module.image}"/>
          <h3>${module.title}</h3>
          <h2>${module.description}</h2>
        </a>
      </div>`
    contentDiv.innerHTML += moduleDiv
  }
})
