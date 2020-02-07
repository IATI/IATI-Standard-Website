$(function () {
    var admin_class = 'body.menu-settings';
    var form_action = 'settings/navigation/';
    var selector = 'footer .actions';

    // return if we're not in the right place
    if (!$(admin_class).find('form[action*="' + form_action + '"]')) {
        return;
    }

    // grab the selector, back out if not present
    var element = $(selector);
    if (!element.length) {
        return
    }

    // add message to admin block
    var message = '<li class="help-block help-warning navigation-save-advice">\
                       <strong>Note:</strong> saved navigation content will be updated immediately on the live site\
                   </li>';
    element.after(message);
});
