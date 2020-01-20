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
    minWidth = 1000
    ) {

    const isMinWidth = window.matchMedia(`(min-width: ${minWidth}px)`).matches;

    if (isMinWidth) {

        // accessible megamenu
        $(selector).accessibleMegaMenu({
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

    }
}
