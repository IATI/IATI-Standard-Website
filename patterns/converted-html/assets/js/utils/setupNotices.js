import $ from 'jquery';

export default function setupNotices(
	selector = '[data-notice]',
	trigger = '[data-notice-dismiss]'
) {

	$(trigger).on('click', e => {
		e.preventDefault();
		const notice = $(e.target).closest(selector).first();
		if (notice) {
			dismissNotice(notice);
		}
	});

	function dismissNotice(notice) {
		const id = notice.attr('id');
		setCookie(id, 'dismissed');
		notice.slideUp(300, ()=> {
			notice.remove();
		});
	}

	function getCookie(key) {
		var keyValue = document.cookie.match('(^|;) ?' + key + '=([^;]*)(;|$)');
		return keyValue ? keyValue[2] : null;
	}

	function setCookie(key, value) {
	    var today = new Date();
	    var expire = new Date();
	    expire.setTime(today.getTime() + 3600000 * 24 * 14);
	    document.cookie = key + "=" + encodeURI(value) + ";expires=" + expire.toGMTString() + ';path=/';
	}
};
