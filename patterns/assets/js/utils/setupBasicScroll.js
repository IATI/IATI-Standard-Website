import '../libs/basicScroll.min';

export default function setupBasicScroll(selector='.listing__body') {

    const elem = document.querySelector && document.querySelector(selector);

    if (elem) {
        const instance = basicScroll.create({
           elem: elem,
           from: 'top-top',
           to: 'bottom-bottom',
           direct: true,
           props: {
              '--translateY': {
                 from: '-20px',
                 to: '20px'
              }
           }
        });
        instance.start();
    }
}
