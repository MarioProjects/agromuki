function active_current_nav(nav_actual) {
    // Debemos poner la clase active-nav-link a nuestros nav-item (desktop y móvil) con la clase verduras_nav_item
    // También debemos eliminar active-nav-link de los elementos que lo tenían
    // Debemos hacer lo mismo con la clase opacity-75 y opacity-100
    let links_activos_previos = $(".active-nav-link");
    links_activos_previos.removeClass("active-nav-link");
    links_activos_previos.removeClass("opacity-100");
    links_activos_previos.addClass("opacity-75");

    nav_actual.addClass("active-nav-link");
    nav_actual.removeClass("opacity-75");
    nav_actual.addClass("opacity-100");
}

function random_animation_speed(clase, animation_speeds) {
    // Para animar cada botón con una duración diferente le asignamos la clase que controla la duración
    // de forma aleatoria. La clase animate__animated tiene una velocidad por defecto de 1s
    // por eso la dejamos "" (https://animate.style/)
    $(clase).each(function () {
        $(this).addClass(animation_speeds[~~(Math.random() * animation_speeds.length)]);
    });

}

function display_numero(numero) {
    // Dado un numero, lo formateamos (como cadena de texto), para que cada 3 números exista espacio y se
    // pueda leer mejor -> Ejemplo: 34843 => 34 843
    return numero.toString().replace(/(?!^)(?=(?:\d{3})+(?:\.|$))/gm, ' ')
}