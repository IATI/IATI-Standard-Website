// From http://docs.wagtail.io/en/v2.0/advanced_topics/customisation/extending_draftail.html#creating-new-entities with modifications
// Included into the CMS via home/wagtail_hooks.py, this file adds a custom button into the rich text editor.
// This button creates two prompt windows, one which asks for text and another for an ID.
// Using those two pieces of information, an <a> element with href equal to #ID is created.
// If the user has highlighted some text prior to clicking the button, the text prompt is automatically filled.

const React = window.React;
const Modifier = window.DraftJS.Modifier;
const EditorState = window.DraftJS.EditorState;


class AnchorSource extends React.Component {
    componentDidMount() {
        const { editorState, entityType, onComplete } = this.props;

        const content = editorState.getCurrentContent();
        const selection = editorState.getSelection();
        const anchorKey = selection.getAnchorKey();
        const currentContent = editorState.getCurrentContent();
        const currentBlock = currentContent.getBlockForKey(anchorKey);
        const start = selection.getStartOffset();
        const end = selection.getEndOffset();
        const selectedText = currentBlock.getText().slice(start, end);

        const anchorText = window.prompt('Skip link display text', selectedText);

        if(anchorText){

          const anchorHref = window.prompt('Anchor point ID');

          if (anchorHref){
            // Uses the Draft.js API to create a new entity with the right data.
            const contentWithEntity = content.createEntity(entityType.type, 'IMMUTABLE', {
                href: "#"+anchorHref,
            });
            const entityKey = contentWithEntity.getLastCreatedEntityKey();

            // We also add some text for the entity to be activated on.
            const text = `${anchorText}`;

            const newContent = Modifier.replaceText(content, selection, text, null, entityKey);
            const nextState = EditorState.push(editorState, newContent, 'insert-characters');

            onComplete(nextState);
          }else{
            onComplete(editorState);
          }
        }else{
          onComplete(editorState);
        }

    }

    render() {
        return null;
    }
}

const Anchor = (props) => {
    const { entityKey, contentState } = props;
    const data = contentState.getEntity(entityKey).getData();

    return React.createElement('a', {
        role: 'button',
    }, props.children);
};

window.draftail.registerPlugin({
    type: 'ANCHOR',
    source: AnchorSource,
    decorator: Anchor,
});
