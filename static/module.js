document.addEventListener("DOMContentLoaded", function() {
    const collapsibleContainer = document.querySelector(".collapsible");

    fetch("http://127.0.0.1:8000/modules-api/units/list")
        .then(res => res.json())
        .then(units => {
            units.forEach(unit => {
                const unitDiv = document.createElement("div");
                unitDiv.classList.add("unit");

                const unitTitle = document.createElement("p");
                unitTitle.textContent = unit.title;
                unitDiv.appendChild(unitTitle);

                const button = document.createElement("button");
                button.classList.add("collapsible");
                button.textContent = "Open Collapsible";
                unitDiv.appendChild(button);

                const contentDiv = document.createElement("div");
                contentDiv.classList.add("content");
                contentDiv.id = `unit-${unit.id}-content`;
                unitDiv.appendChild(contentDiv);

                collapsibleContainer.appendChild(unitDiv);

                fetch(`http://127.0.0.1:8000/modules-api/modules/list/?unit=${unit.id}`)
                    .then(res => res.json())
                    .then(modules => {
                        modules.forEach(module => {
                            const moduleDiv = document.createElement("div");
                            moduleDiv.classList.add("module");

                            const moduleName = document.createElement("h3");
                            moduleName.textContent = module.title;
                            moduleDiv.appendChild(moduleName);

                            const moduleDescription = document.createElement("h2");
                            moduleDescription.textContent = module.description;
                            moduleDiv.appendChild(moduleDescription);

                            contentDiv.appendChild(moduleDiv);
                        });
                    });
            });

            // Add event listeners for collapsibles after they are created
            setTimeout(() => {
                var coll = document.getElementsByClassName("collapsible");
                for (var i = 0; i < coll.length; i++) {
                    coll[i].addEventListener("click", function() {
                        this.classList.toggle("active");
                        var content = this.nextElementSibling;
                        if (content.style.maxHeight) {
                            content.style.maxHeight = null;
                        } else {
                            content.style.maxHeight = content.scrollHeight + "px";
                        }
                    });
                }
            }, 500); // Delay to ensure elements are created before adding listeners
        });
});
