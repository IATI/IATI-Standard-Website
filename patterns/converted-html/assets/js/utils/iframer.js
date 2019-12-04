// Allow iframes in content to be wrapped in responsive code
import $ from 'jquery';

export default function iframer (selector = '.is-typeset iframe', wrapperClass = 'media-video-wrapper') {
    $(selector).wrap(`<div class="${wrapperClass}"/>`);
}
