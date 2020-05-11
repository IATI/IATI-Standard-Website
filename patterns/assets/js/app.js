import $ from 'jquery';

import skipLinks from './utils/skipLinks';
import iframer from './utils/iframer';
import mNav from './utils/mNav';
import sNav from './utils/mNav';
import searchTrigger from './utils/searchTrigger';
import nestedNav from './utils/nestedNav';
import megaMenu from './utils/megaMenu';
import counter from './utils/counter';
import setupNotices from './utils/setupNotices';
import setupBasicScroll from './utils/setupBasicScroll';

function globals () {

    // iframe video in body content
    iframer();

    // Scroll animation
    setupBasicScroll();

    // Small Screen Navigation
    mNav(
        '#navigation-primary-toggle',
        'navigation-primary-toggle--active',
        '#navigation-primary',
        'navigation-primary--active'
    );

    // Small Screen Navigation
    sNav(
        '#navigation-secondary-toggle',
        'navigation-secondary-toggle--active',
        '#navigation-secondary',
        'navigation-secondary--active'
    );

    // Search trigger
    searchTrigger(
        '.header-search__trigger',
        '.header-search',
        'header-search--active',
        '.header-search__close'
    );

    // accessible megamenu
    megaMenu();

    // nested nav
    nestedNav();

    // Load EventBrite if the window is larger than 500px, which is our $b-vp breakpoint
    if ($(window).width() > 500) {
        var targetID = 'eventbrite-widget-container';
        $.getScript("https://www.eventbrite.co.uk/static/widgets/eb_widgets.js", function( data, textStatus, jqxhr ) {
            var exampleCallback = function() {
                console.log('Registration complete!');
            };
            window.EBWidgets.createWidget({
                // Required
                widgetType: 'checkout',
                eventId: '33395177876',
                iframeContainerId: targetID,
                // Optional
                iframeContainerHeight: 285,  // Widget height in pixels
                onOrderComplete: exampleCallback  // Method called when an order has successfully completed
            });
        });
    }
    // Modify behaviour of Register button depending on window width
    $('#button-register').click(function(event) {
        if ($(window).width() > 500) {
            event.preventDefault();
            $('html, body').animate({
              scrollTop: $('#'+targetID).offset().top
            }, 300);
        }
    });

    $('.js-move').click(function(event) {
        event.preventDefault();
        var target = $(this).attr('data-target');
        $('#' + target).scrollView();
    });

    // counter for the homepage numbers
    counter([
        '#stat-activities',
        '#stat-publishers',
    ]);

    // Show / Hide {
    // Used on the codelist template 09-1a-codelist.html
    $('.show-hide-trigger').on('click', function(event) {
        event.preventDefault();
        $(this).text($(this).text() == 'Hide -' ? 'Expand +' : 'Hide -').prev().toggleClass('show-hide-target--hidden');
    });

    // Notices
    setupNotices();
}

$(function run () {
    console.log('ᕕ( ᐛ )ᕗ Running...');
    globals();
});

$.fn.scrollView = function () {
    return this.each(function () {
        $('html, body').animate({
            scrollTop: $(this).offset().top
        }, 600);
    });
}
