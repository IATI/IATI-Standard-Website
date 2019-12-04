// Setup Skiplinks http://viget.com/inspire/skip-link-primer

export default function skipLinks () {

   // define a function that adds a tabindex of -1 and sends focus to the container
    function skipTo () {
        const dest = document.querySelector(this.getAttribute('href'));
        dest.classList.remove('-nofocus');
        dest.focus();
    }

    // get all the skip links
    const skippers = document.querySelectorAll('[data-js="skiplink"]');

    // loop over the links and bind the click event
    for (let i = 0, len = skippers.length; i < len; i++) {
        skippers[i].addEventListener('click', skipTo);
    }

}
