// ===================================
// DISPOSITIVOS.JS - GESTIÓN DE DISPOSITIVOS BIOMÉTRICOS
// ===================================

document.addEventListener('DOMContentLoaded', function() {
    
    // ===================================
    // ELEMENTOS DEL DOM
    // ===================================
    const formulario = document.getElementById('formularioDispositivo');
    const btnGuardar = document.getElementById('btn-guardar');
    const btnNuevo = document.getElementById('btn-nuevo');
    const formTitle = document.getElementById('form-title');
    const accionForm = document.getElementById('accion-form');
    const dispositivoId = document.getElementById('dispositivo-id');
    
    // Filtros
    const inputBuscar = document.getElementById('buscar-dispositivo');
    const selectEstado = document.getElementById('filtro-estado');
    const selectTipo = document.getElementById('filtro-tipo');
    const btnLimpiarFiltros = document.getElementById('limpiar-filtros');
    
    // ===================================
    // MENSAJES DE ÉXITO/ERROR
    // ===================================
    const mensajes = document.querySelectorAll('.mensaje');
    
    mensajes.forEach(mensaje => {
        const btnCerrar = mensaje.querySelector('.cerrar-mensaje');
        
        if (btnCerrar) {
            btnCerrar.addEventListener('click', function() {
                mensaje.style.animation = 'slideUp 0.3s ease';
                setTimeout(() => {
                    mensaje.remove();
                }, 300);
            });
        }
        
        // Auto-cerrar después de 5 segundos
        setTimeout(() => {
            mensaje.style.animation = 'slideUp 0.3s ease';
            setTimeout(() => {
                mensaje.remove();
            }, 300);
        }, 5000);
    });
    
    // ===================================
    // BOTÓN NUEVO DISPOSITIVO
    // ===================================
    if (btnNuevo) {
        btnNuevo.addEventListener('click', function(e) {
            e.preventDefault();
            limpiarFormulario();
        });
    }
    
    // ===================================
    // FUNCIÓN LIMPIAR FORMULARIO
    // ===================================
    function limpiarFormulario() {
        formulario.reset();
        formTitle.textContent = 'Nuevo Dispositivo';
        accionForm.name = 'agregar';
        accionForm.value = '1';
        dispositivoId.value = '';
        btnGuardar.innerHTML = '<i class="fa-solid fa-save"></i> GUARDAR DISPOSITIVO';
        
        // Scroll al inicio del formulario
        document.querySelector('.form-panel').scrollTop = 0;
    }
    
    // ===================================
    // BÚSQUEDA Y FILTROS
    // ===================================
    
    function aplicarFiltros() {
        const textoBusqueda = inputBuscar.value.toLowerCase();
        const estadoSeleccionado = selectEstado.value;
        const tipoSeleccionado = selectTipo.value;
        
        const filas = document.querySelectorAll('#tabla-dispositivos-body tr');
        
        filas.forEach(fila => {
            if (fila.querySelector('.sin-datos')) {
                return; // Ignorar fila de "sin datos"
            }
            
            const nombre = fila.cells[0].textContent.toLowerCase();
            const numeroSerie = fila.cells[1].textContent.toLowerCase();
            const estado = fila.dataset.estado;
            const tipo = fila.dataset.tipo;
            
            const coincideBusqueda = nombre.includes(textoBusqueda) || 
                                    numeroSerie.includes(textoBusqueda);
            const coincideEstado = !estadoSeleccionado || estado === estadoSeleccionado;
            const coincideTipo = !tipoSeleccionado || tipo === tipoSeleccionado;
            
            if (coincideBusqueda && coincideEstado && coincideTipo) {
                fila.style.display = '';
            } else {
                fila.style.display = 'none';
            }
        });
        
        // Mostrar mensaje si no hay resultados
        actualizarMensajeSinResultados();
    }
    
    function actualizarMensajeSinResultados() {
        const filas = document.querySelectorAll('#tabla-dispositivos-body tr');
        const filasVisibles = Array.from(filas).filter(fila => 
            fila.style.display !== 'none' && !fila.querySelector('.sin-datos')
        );
        
        let mensajeSinDatos = document.querySelector('.sin-datos');
        
        if (filasVisibles.length === 0 && filas.length > 0) {
            if (!mensajeSinDatos) {
                const tbody = document.getElementById('tabla-dispositivos-body');
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td colspan="8" class="sin-datos">
                        <i class="fa-solid fa-search"></i>
                        <p>No se encontraron dispositivos con los filtros aplicados</p>
                    </td>
                `;
                tbody.appendChild(tr);
            }
        } else if (mensajeSinDatos && filasVisibles.length > 0) {
            mensajeSinDatos.parentElement.remove();
        }
    }
    
    // Event listeners para filtros
    if (inputBuscar) {
        inputBuscar.addEventListener('input', aplicarFiltros);
    }
    
    if (selectEstado) {
        selectEstado.addEventListener('change', aplicarFiltros);
    }
    
    if (selectTipo) {
        selectTipo.addEventListener('change', aplicarFiltros);
    }
    
    // Limpiar filtros
    if (btnLimpiarFiltros) {
        btnLimpiarFiltros.addEventListener('click', function() {
            inputBuscar.value = '';
            selectEstado.value = '';
            selectTipo.value = '';
            aplicarFiltros();
        });
    }
    
    // ===================================
    // VALIDACIÓN DEL FORMULARIO
    // ===================================
    
    if (formulario) {
        formulario.addEventListener('submit', function(e) {
            const camposRequeridos = formulario.querySelectorAll('input[required], select[required]');
            let formularioValido = true;
            
            camposRequeridos.forEach(campo => {
                if (!campo.value.trim()) {
                    formularioValido = false;
                    campo.style.borderColor = '#ef4444';
                    
                    setTimeout(() => {
                        campo.style.borderColor = '';
                    }, 3000);
                }
            });
            
            if (!formularioValido) {
                e.preventDefault();
                mostrarMensaje('Por favor, complete todos los campos requeridos', 'error');
            }
        });
    }
    
    // ===================================
    // FUNCIÓN MOSTRAR MENSAJE
    // ===================================
    
    function mostrarMensaje(texto, tipo = 'success') {
        const mensajesContainer = document.querySelector('.mensajes-container');
        
        if (!mensajesContainer) {
            const container = document.createElement('div');
            container.className = 'mensajes-container';
            document.querySelector('.contenido-dispositivos').insertBefore(
                container, 
                document.querySelector('.main-container-dispositivos')
            );
        }
        
        const mensaje = document.createElement('div');
        mensaje.className = `mensaje ${tipo}`;
        mensaje.innerHTML = `
            <i class="fa-solid fa-${tipo === 'success' ? 'check' : 'exclamation'}-circle"></i>
            <span>${texto}</span>
            <button class="cerrar-mensaje">&times;</button>
        `;
        
        document.querySelector('.mensajes-container').appendChild(mensaje);
        
        // Botón cerrar
        mensaje.querySelector('.cerrar-mensaje').addEventListener('click', function() {
            mensaje.remove();
        });
        
        // Auto-cerrar
        setTimeout(() => {
            mensaje.remove();
        }, 5000);
    }
    
    // ===================================
    // CONFIRMAR ELIMINACIÓN
    // ===================================
    
    const formsEliminar = document.querySelectorAll('form[onsubmit*="confirm"]');
    formsEliminar.forEach(form => {
        form.addEventListener('submit', function(e) {
            const nombre = this.closest('tr').cells[0].textContent;
            if (!confirm(`¿Está seguro de eliminar el dispositivo "${nombre}"?\n\nEsta acción no se puede deshacer.`)) {
                e.preventDefault();
            }
        });
    });
    
    // ===================================
    // ANIMACIÓN DE ENTRADA
    // ===================================
    
    const elementos = document.querySelectorAll('.form-panel, .list-panel');
    elementos.forEach((elemento, index) => {
        elemento.style.animation = `fadeIn 0.5s ease ${index * 0.1}s both`;
    });
    
    // ===================================
    // RESALTAR CAMPOS AL HACER FOCUS
    // ===================================
    
    const inputs = document.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
            this.parentElement.style.transition = 'transform 0.2s ease';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
        });
    });
    
    // ===================================
    // SCROLL SUAVE PARA FORMULARIO LARGO
    // ===================================
    
    const formPanel = document.querySelector('.form-panel');
    if (formPanel) {
        formPanel.addEventListener('wheel', function(e) {
            e.stopPropagation();
        });
    }
    
});

// ===================================
// ANIMACIÓN CSS ADICIONAL
// ===================================

const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideUp {
        from {
            opacity: 1;
            transform: translateY(0);
        }
        to {
            opacity: 0;
            transform: translateY(-20px);
        }
    }
`;
document.head.appendChild(style);