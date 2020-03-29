$( document ).ready(function() {
    $('.calificacion').on('click', function (e) {
        $('#idProducto').val($(this).data("idproducto"));
        $('#calificacion').val($(this).data("calificacion"));
        $('#codigo_desplegado').text($(this).data("idproducto"));
        $('#nombre_producto').text('Calificar ' + $(this).data("nombre"));
       });

    $('.verMas').on('click', function (e) {
        $('#nombreDesplegado').text($(this).data("nombre"));
        $('#productoId').text($(this).data("idproducto"));
        $('#productoNombre').text($(this).data("nombre"));
        $('#link1').attr("href", $(this).data("link1"));
        $('#link1').text($(this).data("link1"));
        $('#link2').attr("href", $(this).data("link2"));
        $('#link2').text($(this).data("link2"));
        $('#categoria').text($(this).data("categoria"));
        $('#precio').text("$" + $(this).data("precio") + " USD");
        $('#piezas').text($(this).data("npiezas"));
        $('#observaciones').text($(this).data("observaciones"));
       });
    
});