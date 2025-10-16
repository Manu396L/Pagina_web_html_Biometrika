// Array para almacenar las ubicaciones registradas
let ubicaciones = [];

// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('formularioUbicacion');
    const mensajeExito = document.getElementById('mensaje-exito');
    const cuerpoTabla = document.getElementById('cuerpoTabla');

    // Cargar ubicaciones guardadas en localStorage (si existen)
    cargarUbicaciones();

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Obtener los datos del formulario
        const permisos = Array.from(document.getElementById('permisos').selectedOptions)
            .map(option => option.value);

        const datos = {
            id: Date.now(), // ID único basado en timestamp
            tipo_ubicacion: document.getElementById('tipo_ubicacion').value,
            nombre_sede: document.getElementById('nombre_sede').value,
            codigo_unico: document.getElementById('codigo_unico').value,
            direccion: document.getElementById('direccion').value,
            descripcion: document.getElementById('descripcion').value,
            dispositivo_biometrico: document.getElementById('dispositivo_biometrico').value,
            nivel_seguridad: document.getElementById('nivel_seguridad').value,
            permisos: permisos
        };
        
        // Agregar a la lista de ubicaciones
        ubicaciones.push(datos);
        
        // Guardar en localStorage
        guardarUbicaciones();
        
        // Mostrar en consola los datos (para pruebas)
        console.log('Datos del formulario:', datos);
        console.log('Ubicaciones totales:', ubicaciones);
        
        // Actualizar la tabla
        renderizarTabla();
        
        // Mostrar mensaje de éxito
        mensajeExito.classList.add('mostrar');
        
        // Hacer scroll hacia el mensaje de éxito
        mensajeExito.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // Limpiar formulario
        form.reset();
        
        // Ocultar mensaje después de 5 segundos
        setTimeout(() => {
            mensajeExito.classList.remove('mostrar');
        }, 5000);
    });

    // Mejorar la experiencia del select múltiple
    const selectPermisos = document.getElementById('permisos');
    
    selectPermisos.addEventListener('mousedown', function(e) {
        e.preventDefault();
        
        const option = e.target;
        if (option.tagName === 'OPTION') {
            option.selected = !option.selected;
        }
        
        return false;
    });

    selectPermisos.addEventListener('click', function(e) {
        e.preventDefault();
    });

    // Función para renderizar la tabla
    function renderizarTabla() {
        if (ubicaciones.length === 0) {
            cuerpoTabla.innerHTML = `
                <tr class="empty-state">
                    <td colspan="6">
                        <i class="fa-solid fa-inbox"></i>
                        <p>No hay ubicaciones registradas aún</p>
                    </td>
                </tr>
            `;
            return;
        }

        cuerpoTabla.innerHTML = ubicaciones.map(ubicacion => `
            <tr>
                <td><strong>${ubicacion.codigo_unico}</strong></td>
                <td>${ubicacion.nombre_sede}</td>
                <td><span class="badge-tipo badge-${ubicacion.tipo_ubicacion}">${formatearTipo(ubicacion.tipo_ubicacion)}</span></td>
                <td>${formatearDispositivo(ubicacion.dispositivo_biometrico)}</td>
                <td><span class="badge-seguridad badge-${ubicacion.nivel_seguridad}">${formatearSeguridad(ubicacion.nivel_seguridad)}</span></td>
                <td>
                    <div class="acciones">
                        <button class="btn-accion btn-ver" onclick="verUbicacion(${ubicacion.id})" title="Ver detalles">
                            <i class="fa-solid fa-eye"></i>
                        </button>
                        <button class="btn-accion btn-editar" onclick="editarUbicacion(${ubicacion.id})" title="Editar">
                            <i class="fa-solid fa-edit"></i>
                        </button>
                        <button class="btn-accion btn-eliminar" onclick="eliminarUbicacion(${ubicacion.id})" title="Eliminar">
                            <i class="fa-solid fa-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');
    }

    // Funciones auxiliares para formatear datos
    function formatearTipo(tipo) {
        const tipos = {
            'sede': 'Sede',
            'oficina': 'Oficina',
            'area': 'Área'
        };
        return tipos[tipo] || tipo;
    }

    function formatearDispositivo(dispositivo) {
        const dispositivos = {
            'huella': 'Huella Dactilar',
            'Tarjeta': 'Tarjeta',
            'PIN': 'PIN'
        };
        return dispositivos[dispositivo] || dispositivo;
    }

    function formatearSeguridad(nivel) {
        return nivel.charAt(0).toUpperCase() + nivel.slice(1);
    }

    // Guardar ubicaciones en localStorage
    function guardarUbicaciones() {
        localStorage.setItem('ubicaciones', JSON.stringify(ubicaciones));
    }

    // Cargar ubicaciones desde localStorage
    function cargarUbicaciones() {
        const ubicacionesGuardadas = localStorage.getItem('ubicaciones');
        if (ubicacionesGuardadas) {
            ubicaciones = JSON.parse(ubicacionesGuardadas);
            renderizarTabla();
        }
    }
});

// Funciones globales para los botones de acción
function verUbicacion(id) {
    const ubicacion = ubicaciones.find(u => u.id === id);
    if (ubicacion) {
        let mensaje = `

    DETALLES DE LA UBICACIÓN           

    Código: ${ubicacion.codigo_unico}
    Nombre: ${ubicacion.nombre_sede}
    Tipo: ${ubicacion.tipo_ubicacion}
    Dirección: ${ubicacion.direccion || 'No especificada'}
    Descripción: ${ubicacion.descripcion || 'Sin descripción'}

    SEGURIDAD
• Dispositivo: ${ubicacion.dispositivo_biometrico}
• Nivel: ${ubicacion.nivel_seguridad}
• Permisos: ${ubicacion.permisos.join(', ') || 'Ninguno'}
        `;
        alert(mensaje);
        console.log('Ubicación completa:', ubicacion);
    }
}

function editarUbicacion(id) {
    const ubicacion = ubicaciones.find(u => u.id === id);
    if (ubicacion) {
        // Rellenar el formulario con los datos de la ubicación
        document.getElementById('tipo_ubicacion').value = ubicacion.tipo_ubicacion;
        document.getElementById('nombre_sede').value = ubicacion.nombre_sede;
        document.getElementById('codigo_unico').value = ubicacion.codigo_unico;
        document.getElementById('direccion').value = ubicacion.direccion;
        document.getElementById('descripcion').value = ubicacion.descripcion;
        document.getElementById('dispositivo_biometrico').value = ubicacion.dispositivo_biometrico;
        document.getElementById('nivel_seguridad').value = ubicacion.nivel_seguridad;
        
        // Seleccionar permisos
        const selectPermisos = document.getElementById('permisos');
        Array.from(selectPermisos.options).forEach(option => {
            option.selected = ubicacion.permisos.includes(option.value);
        });

        // Eliminar la ubicación antigua (se agregará como nueva al guardar)
        eliminarUbicacion(id, false);

        // Hacer scroll al formulario
        window.scrollTo({ top: 0, behavior: 'smooth' });
        
        alert('📝 Datos cargados en el formulario. Modifícalos y presiona "Guardar Cambios".');
    }
}

function eliminarUbicacion(id, confirmar = true) {
    if (confirmar && !confirm('¿Estás seguro de que deseas eliminar esta ubicación?')) {
        return;
    }
    
    ubicaciones = ubicaciones.filter(u => u.id !== id);
    localStorage.setItem('ubicaciones', JSON.stringify(ubicaciones));
    
    // Re-renderizar la tabla
    const cuerpoTabla = document.getElementById('cuerpoTabla');
    if (ubicaciones.length === 0) {
        cuerpoTabla.innerHTML = `
            <tr class="empty-state">
                <td colspan="6">
                    <i class="fa-solid fa-inbox"></i>
                    <p>No hay ubicaciones registradas aún</p>
                </td>
            </tr>
        `;
    } else {
        cuerpoTabla.innerHTML = ubicaciones.map(ubicacion => `
            <tr>
                <td><strong>${ubicacion.codigo_unico}</strong></td>
                <td>${ubicacion.nombre_sede}</td>
                <td><span class="badge-tipo badge-${ubicacion.tipo_ubicacion}">${formatearTexto(ubicacion.tipo_ubicacion)}</span></td>
                <td>${formatearDispositivo(ubicacion.dispositivo_biometrico)}</td>
                <td><span class="badge-seguridad badge-${ubicacion.nivel_seguridad}">${formatearTexto(ubicacion.nivel_seguridad)}</span></td>
                <td>
                    <div class="acciones">
                        <button class="btn-accion btn-ver" onclick="verUbicacion(${ubicacion.id})" title="Ver detalles">
                            <i class="fa-solid fa-eye"></i>
                        </button>
                        <button class="btn-accion btn-editar" onclick="editarUbicacion(${ubicacion.id})" title="Editar">
                            <i class="fa-solid fa-edit"></i>
                        </button>
                        <button class="btn-accion btn-eliminar" onclick="eliminarUbicacion(${ubicacion.id})" title="Eliminar">
                            <i class="fa-solid fa-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');
    }
}

function formatearTexto(texto) {
    return texto.charAt(0).toUpperCase() + texto.slice(1);
}

function formatearDispositivo(dispositivo) {
    const dispositivos = {
        'huella': 'Huella Dactilar',
        'Tarjeta': 'Tarjeta',
        'PIN': 'PIN'
    };
    return dispositivos[dispositivo] || dispositivo;
}
