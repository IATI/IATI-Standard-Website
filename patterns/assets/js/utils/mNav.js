import $ from 'jquery';

export default function mNav (trigger, triggerActive, target, targetActive) {
    $(trigger).on('click', function(e) {
		e.preventDefault();
		$(this).toggleClass(triggerActive);
		$(target).toggleClass(targetActive);
	});
}