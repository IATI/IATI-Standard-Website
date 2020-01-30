$(function () {
    var inited = false;
    var admin_class = 'body.menu-settings';
    var container_class = 'ul.objects';
    var form_action = 'settings/navigation/primarymenu';
    var streamfield_class = '.block_field.stream-field';
    var module_class = '.navigation__meganav';
    var parent_class = '.c-sf-container';
    var button_class = '.c-sf-add-button[id*="prependmenu-openclose"], .c-sf-add-button[id*="appendmenu-openclose"]';

    // return if we're not in the right place
    if (!$(admin_class).find('form[action*="' + form_action + '"]')) {
        return;
    }

    // grab the container, back out if not present
    var element = $(container_class);
    if (!element.length) {
        return
    }

    // set interval to test for existing modules
    // tried to use MutationObserver for this instead of isetInterval, but ended up with recursion issues
    setInterval(toggle_add_button_visibility, 1000);

    // test if a module exists, if so hide the add button
    // modules that are added and then discarded stay in the dom but hidden, so need to check for visibility
    function toggle_add_button_visibility() {
        $(streamfield_class).each(function(i, elem) {
            var modules = $(this).find(module_class);
            if (modules.length > 0) {
                var container = modules.first().closest(parent_class);
                if (modules.first().is(':visible')) {
                    container.find(button_class).not('[id*="columns"]').each(function(i, elem) {
                        if ($(this).is(':visible')) {
                            $(this).css('visibility', 'hidden');
                        }
                    });
                }
                else {
                    $(this).find(button_class).not('[id*="columns"]').each(function(i, elem) {
                        $(this).css('visibility', 'visible');
                    });
                }
            }
        });
    }
});
