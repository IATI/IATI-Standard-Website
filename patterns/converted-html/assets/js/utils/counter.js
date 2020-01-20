/*
 Inc v1.0.0
 (c) 2014 Depth Development. http://depthdev.com
 License: Apache 2.0
 https://codepen.io/depthdev/pen/fFuKH
*/

'use strict';

function Inc(obj) {
	var elem = obj.elem;
	var input = (elem.nodeName.toLowerCase() === 'input') ? true: false;
	var value = parseFloat(elem.getAttribute('data-inc-value')) || 0;
	var duration = parseInt(elem.getAttribute('data-inc-duration')) || 0;
	var delay = parseInt(elem.getAttribute('data-inc-delay')) || 0;
	var decimal = ((obj.decimal > 2) ? 2 : obj.decimal) || 0;
	var currency = obj.currency || '';
	var speed = ((obj.speed < 30) ? 30 : obj.speed) || 30;
	var count = 0;
	var increment = value / (duration / speed);
	var interval = null;
	var regex = /\B(?=(\d{3})+(?!\d))/g;
	var run = function() {
		count += increment;
		if (count < value) {
			(input) ? elem.value = currency + (count).toFixed(decimal).toString().replace(regex, ',') : elem.innerHTML = currency + (count).toFixed(decimal).toString().replace(regex, ',');
		} else {
			clearInterval(interval);
			(input) ? elem.value = currency + (value).toFixed(decimal).toString().replace(regex, ',') : elem.innerHTML = currency + (value).toFixed(decimal).toString().replace(regex, ',');
		}
	};
	setTimeout(function() {
		interval = setInterval(run.bind(this), speed);
	}.bind(this), delay);
	this.reset = function() {
		clearInterval(interval);
		value = parseFloat(elem.getAttribute('data-inc-value')) || 0;
		duration = parseInt(elem.getAttribute('data-inc-duration')) || 0;
		increment = value / (duration / speed);
		delay = parseInt(elem.getAttribute('data-inc-delay')) || 0;
		count = 0;
		interval = setInterval(run, speed);
	}.bind(this);
} // Inc

// export default function counter (){
function counter (){
	var elems = [
		document.querySelector('#stat-activities'),
		document.querySelector('#stat-publishers')
	];
	var objs = [];

	for (var i = 0, l = elems.length; i < l; i++) {
		objs.push(
			new Inc({
				elem: elems[i],
				speed: 30,
				decimal: 0,
			})
		);
	}
	elems[0].addEventListener('click', function() {
		objs[0].reset();
	});
	elems[1].addEventListener('click', function() {
		objs[1].reset();
	});
}