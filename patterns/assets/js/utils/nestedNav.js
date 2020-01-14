import $ from 'jquery';

export default function nestedNav (
    selector = '[data-nested-list]',
    openClass = 'open',
    triggerSelector = '[data-nested-nav-toggle]',
    itemSelector = '[data-nested-nav-item]',
    listSelector = '[data-nested-nav-child-list]',
    ) {
    const nav = $(selector);
    if (!nav.length) {
        return;
    }

    const trigger = $(triggerSelector);
    trigger.on('click', e => {
        e.preventDefault();
        const target_trigger = $(e.target);
        const item = target_trigger.closest(itemSelector);
        const list = item.children(listSelector);

        // toggle the open state of this item
        item.toggleClass(openClass);
        list.toggleClass(openClass);
    });
}
