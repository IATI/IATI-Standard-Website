import $ from 'jquery';

export default function mNav (trigger, target, targetActive, triggerClose, field = '[name=query]') {
    $(trigger).on('click', function(e) {
		e.preventDefault();
		$(target).addClass(targetActive);
        $(target).find(field).focus();
	});
    $(triggerClose).on('click', function(e) {
		e.preventDefault();
		$(target).removeClass(targetActive);
	});
}
