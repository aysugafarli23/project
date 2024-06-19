document.addEventListener('DOMContentLoaded', function () {
  const collapsibleContainer = document.querySelector('.collapsible')

  fetch('http://127.0.0.1:8000/modules-api/units/list')
    .then(res => res.json())
    .then(units => {
      units.forEach(unit => {
        const unitDiv = document.createElement('div')
        unitDiv.classList.add('unit')

        const button = document.createElement('button')
        button.classList.add('collapsible')
        button.innerHTML = ` ${unit.title}<i class="fas fa-chevron-up"></i>`
        unitDiv.append(button)

        const contentDiv = document.createElement('div')
        contentDiv.classList.add('content')
        contentDiv.id = `unit-${unit.id}-content`
        unitDiv.append(contentDiv)

        collapsibleContainer.append(unitDiv)

        fetch(`http://127.0.0.1:8000/modules-api/modules/list/?unit=${unit.id}`)
          .then(res => res.json())
          .then(modules => {
            modules.forEach(module => {
              const moduleDiv = document.createElement('div');
              moduleDiv.classList.add('module');
          
              const moduleLink = document.createElement('a');
              moduleLink.href = `/modules/module/${module.id}/`;
              moduleDiv.append(moduleLink);
          
              const moduleName = document.createElement('h3');
              moduleName.textContent = module.title;
              moduleLink.append(moduleName);
          
              const moduleDescription = document.createElement('h2');
              moduleDescription.textContent = module.description;
              moduleLink.append(moduleDescription);
          
              moduleDiv.append(moduleLink);
              contentDiv.append(moduleDiv);
            })
          })
      })

      // Added event listeners for collapsibles after they are created
      setTimeout(() => {
        var coll = document.getElementsByClassName('collapsible')
        for (var i = 0; i < coll.length; i++) {
          coll[i].addEventListener('click', function () {
            this.classList.toggle('active')
            var content = this.nextElementSibling
            if (content.style.maxHeight) {
              content.style.maxHeight = null
            } else {
              content.style.maxHeight = content.scrollHeight + 'px'
            }
            const icon = this.querySelector('i')
            icon.classList.toggle('fa-chevron-up')
            icon.classList.toggle('fa-chevron-down')
          })
        }
      }, 500) // Delay to ensure elements are created before adding listeners
    })
})
