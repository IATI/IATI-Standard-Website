import $ from 'jquery';

export default function gaExtras (selector = 'a[href]') {

    $(document).on('click keypress', selector, function (e) {

        const ga = window.ga;
        const DOWNLOAD = 'Download';
        const regex = /\.[a-zA-Z]{3,4}$/g;

        if (ga && ga.create && isValidAction(e)) {
            const link = $(this).attr('href');
            const label = $(this).data('event-label');
            const category = DOWNLOAD;
            const is_file = link.match(regex);

            if (!is_file) {
                return;
            }

            const doLink = () => {
                location.href = link;
                clearTimeout(linkTimeout);
            }
            const linkTimeout = setTimeout(doLink, 1500);

            ga('send', {
                hitType: 'event',
                eventCategory: category,
                eventAction: link,
                eventLabel: label,
                hitCallback: doLink,
            });

            e.preventDefault();
        }
    });

    // test for valid click or enter key press
    function isValidAction(e) {
        return e.key === 'Enter' || e.type === 'click';
    }

}
