import $ from 'jquery';

import highlightSyntax from './utils/highlightSyntax';

function globals () {

    // init syntax highlighter
    highlightSyntax('code pre');
}

$(function run () {
    console.log('ᕕ( ᐛ )ᕗ Running...');
    globals();
});
