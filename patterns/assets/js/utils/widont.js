// Prevent widows

export default function widont (target) {
    // This works as long as the last word is tag free (e.g. the last word is not a link, abbr, etc.)
    // Add acceptable punctuation to the regex as needed but avoid angle brackets <>
    const elements = document.querySelectorAll(target);
    for (let i = 0; i < elements.length; i++) {
        const el = elements[i];
        el.innerHTML = el.innerHTML.replace(/\s([\w.?!-()]+?)$/, '&nbsp;$1');
    }
}
