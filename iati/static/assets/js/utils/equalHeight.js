import $ from 'jquery';

export default function equalHeight (parent, child) {
    $(parent).each(function eachParent (parentIndex, parentElement) {
        const children  = $(parentElement).find(child);
        children.each(function eachChild (childIndex, childElement) {
            $(childElement).height('auto');
        });
        if (children.length > 1 && $(children[0]).position().top === $(children[1]).position().top) {
            const heights = children.map(function getHeights (i, el) {
                return $(el).height();
            });
            const maxHeight = Math.max.apply(null, heights);
            children.height(maxHeight);
        }
    });
}
