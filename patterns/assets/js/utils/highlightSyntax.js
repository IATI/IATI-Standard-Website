import $ from 'jquery';
import '../libs/highlight.min';

export default function highlightSyntax (selector) {

    hljs.initHighlighting();

    if (selector) {
        document.querySelectorAll(selector).forEach((block) => {
            hljs.highlightBlock(block);
        });
    }
}
