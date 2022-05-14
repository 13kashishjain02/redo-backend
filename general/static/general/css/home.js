// Flickity Slider Initialization and Customization

$('.carousel-container').each(function() {
    var $carousel = $(this).find('.main-carousel').flickity({
        cellAlign: 'left',
        contain: true,
        pageDots: false,
        wrapAround: true,
        prevNextButtons: false,
        cellSelector: '.carousel-cell'
    });

    // previous
    $(this).find('.prev_arrow').on('click', function() {
        $carousel.flickity('previous');
    });
    // next
    $(this).find('.next_arrow').on('click', function() {
        $carousel.flickity('next');
    });
})