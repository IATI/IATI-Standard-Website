$(function () {
    $('.js-displaylocationfield').each(function() {
        var $container = $(this);
        var $toggle = $container.find('.js-display_location select');
        var page_field = $container.find('.js-page');

        if ($toggle.val() == 'all') {
            page_field.slideUp(0);
        }

        $toggle.on('change', function () {
            if ($toggle.val() != 'all') {
                page_field.slideDown();
            }
            else {
                page_field.slideUp();
            }
        });
    });
});
