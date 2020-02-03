$(function () {
    var message = '<li class="help-block help-warning navigation-save-advice"><strong>Note:</strong> saved navigation content will be updated immediately on the live site</li>';
    var selector = 'footer .actions';

    // grab the selector, back out if not present
    var element = $(selector);
    if (!element.length) {
        return
    }

    // add message to admin block
    element.after(message);
});
