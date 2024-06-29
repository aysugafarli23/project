document.addEventListener('DOMContentLoaded', () => {
  const collapsibleContainer = document.querySelector('.modules__container')

  fetch('http://127.0.0.1:8000/modules-api/units/list')
    .then(res => res.json())
    .then(modules => modules.map(module => createUnit(module)))

  function createUnit (module) {
    const moduleDiv = `
      <div class="module">
        <button class="collapsible">${module.title}<i class="fas fa-chevron-up"></i></button>
        <div class="content" id="module-${module.id}-content"></div>
      </div>`
    collapsibleContainer.innerHTML += moduleDiv

    const contentDiv = document.getElementById(`module-${module.id}-content`)
    fetch(`http://127.0.0.1:8000/modules-api/modules/list/?module=${module.id}`)
      .then(res => res.json())
      .then(lessons => lessons.map(lesson => createModule(lesson, contentDiv)))

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

  function createModule (lesson, contentDiv) {
    const lessonDiv = `
      <div class="lesson">
        <a href="/lessons/lesson/${lesson.id}/">
          <img src="${lesson.image}"/>
          <h3>${lesson.title}</h3>
          <h2>${lesson.description}</h2>
        </a>
      </div>`
    contentDiv.innerHTML += lessonDiv
  }
})
