(function() {
    // Limpiar toda la sesión
    sessionStorage.clear();
    localStorage.removeItem('usuario');
    localStorage.removeItem('token');
    localStorage.removeItem('sesion_activa');

    console.log('Sesión cerrada correctamente');

    // Redirigir manualmente al login después de 1 segundo
    setTimeout(() => {
    if (typeof loginUrl !== 'undefined') {
        window.location.href = loginUrl;
    } else {
        // Fallback por si loginUrl no está definido
        window.location.href = '/account/login/';
    }
}, 1000);

})();
