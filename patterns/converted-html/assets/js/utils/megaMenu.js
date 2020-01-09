import $ from 'jquery';
import '../libs/accessible-mega-menu';

export default function megaMenu (
    selector = '#navigation-primary',
    uuidPrefix = 'megamenu',
    menuClass = 'navigation-primary__items',
    topNavItemClass = 'navigation-primary__item--has-children',
    panelClass = 'navigation-megamenu',
    panelGroupClass = 'navigation-megamenu__col',
    hoverClass = 'hover',
    focusClass = 'focus',
    openClass = 'open',
    minWidth = 950
    ) {

    // clone the original nav for mobile and enhanced versions
    let original_nav = $(selector).clone(true, true);
    let enhanced_nav = $(selector).clone(true, true);
    let is_enhanced = false;

    // add a window event handler
    $(window).on('resize', e => { onResize()});

    // initialise with a resize call
    onResize();

    // on resize, check width and call appropriate function
    function onResize(e) {
        const is_min_width = window.matchMedia(`(min-width: ${minWidth}px)`).matches;

        console.log('onResize');


        if (is_min_width) {
            replaceMenuWithEnhanced();
        }
        else {
            replaceMenuWithOriginal();
        }
    }

    // if enhanced, replace curent nav with enhanced version
    function replaceMenuWithEnhanced() {
        console.log('replaceMenuWithEnhanced');
        enhanced_nav = $(selector).first().replaceWith(enhanced_nav);

        // initialise if not done so already
        if (!is_enhanced) {

            // accessible megamenu
            enhanced_nav.accessibleMegaMenu({
                // prefix for generated unique id attributes, which are required
                // to indicate aria-owns, aria-controls and aria-labelledby
                uuidPrefix: uuidPrefix,

                // CSS class used to define the megamenu styling
                menuClass: menuClass,

                // CSS class for a top-level navigation item in the megamenu
                topNavItemClass: topNavItemClass,

                // CSS class for a megamenu panel
                panelClass: panelClass,

                // CSS class for a group of items within a megamenu panel
                panelGroupClass: panelGroupClass,

                // CSS class for the hover state
                hoverClass: hoverClass,

                // CSS class for the focus state
                focusClass: focusClass,

                // CSS class for the open state
                openClass: openClass
            });

            // set flag and store for future switching
            is_enhanced = true;
            enhanced_nav = $(selector).first();
        }
    }

    function replaceMenuWithOriginal() {
        console.log('replaceMenuWithOriginal');
        // replace and store for future switching
        original_nav = $(selector).first().replaceWith(original_nav);
    }
}
