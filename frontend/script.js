const API_BASE = window.location.origin;

// 1. CARGAR DATOS (GET)
async function loadData() {
    try {
        const response = await fetch(`${API_BASE}/cv`);
        const data = await response.json();
        
        // Perfil
        document.getElementById('name').textContent = data.informacion_personal.nombre;
        document.getElementById('profession').textContent = data.informacion_personal.profesion;
        document.getElementById('about').textContent = data.informacion_personal.sobre_mi;
        
        document.getElementById('email').textContent = data.informacion_personal.contacto.email;
        document.getElementById('phone').textContent = data.informacion_personal.contacto.telefono;
        document.getElementById('github').href = `https://${data.informacion_personal.contacto.github}`;
        
        // Educación
        const eduList = document.getElementById('education-list');
        eduList.innerHTML = '';
        data.educacion.forEach(edu => {
            const li = document.createElement('li');
            li.innerHTML = `<strong>${edu.titulo}</strong> - ${edu.institucion} (${edu.periodo})`;
            eduList.appendChild(li);
        });

        // Skills (combinando lenguajes e idiomas para diseño)
        const skillsList = document.getElementById('skills-list');
        skillsList.innerHTML = '';
        [...data.lenguajes_y_frameworks, ...data.certificaciones].forEach(skill => {
            const span = document.createElement('span');
            span.className = 'tag';
            span.textContent = skill;
            skillsList.appendChild(span);
        });

        // Proyectos
        const projList = document.getElementById('projects-list');
        projList.innerHTML = '';
        data.proyectos.forEach(proj => {
            const card = document.createElement('div');
            card.className = 'card';
            card.innerHTML = `
                <h4>${proj.nombre}</h4>
                <p><strong>${proj.periodo}</strong></p>
                <ul>${proj.detalles.map(d => `<li>${d}</li>`).join('')}</ul>
            `;
            projList.appendChild(card);
        });

    } catch (error) {
        console.error('Error cargando datos:', error);
        alert('Error al conectar con la API.');
    }
}

// 2. AGREGAR PROYECTO (POST)
document.getElementById('add-project-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const nombre = document.getElementById('proj-name').value;
    const periodo = document.getElementById('proj-period').value;
    const detalles = document.getElementById('proj-details').value.split(',').map(d => d.trim());

    try {
        const response = await fetch(`${API_BASE}/cv/proyectos`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nombre, periodo, detalles })
        });
        if (response.ok) {
            alert('Proyecto agregado!');
            e.target.reset();
            loadData();
        } else {
            alert('Error al agregar proyecto');
        }
    } catch (error) { console.error(error); }
});

// 3. ELIMINAR PROYECTO (DELETE)
document.getElementById('del-project-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const nombre = document.getElementById('del-proj-name').value;

    try {
        const response = await fetch(`${API_BASE}/cv/proyectos/${encodeURIComponent(nombre)}`, {
            method: 'DELETE'
        });
        if (response.ok) {
            alert('Proyecto eliminado!');
            e.target.reset();
            loadData();
        } else {
            alert('No se encontró el proyecto');
        }
    } catch (error) { console.error(error); }
});

// 4. ACTUALIZAR PERFIL (PUT/PATCH)
document.getElementById('update-profile-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const nombre = document.getElementById('update-name').value;

    try {
        const response = await fetch(`${API_BASE}/cv/personal`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nombre })
        });
        if (response.ok) {
            alert('Nombre actualizado!');
            e.target.reset();
            loadData();
        } else {
            alert('Error al actualizar');
        }
    } catch (error) { console.error(error); }
});

// Iniciar
loadData();
