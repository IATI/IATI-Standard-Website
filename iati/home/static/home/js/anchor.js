const React = window.React;
const Modifier = window.DraftJS.Modifier;
const EditorState = window.DraftJS.EditorState;


class AnchorSource extends React.Component {
    componentDidMount() {
        const { editorState, entityType, onComplete } = this.props;

        const content = editorState.getCurrentContent();
        const selection = editorState.getSelection();

        const anchorHref = window.prompt('Anchor ID');
        const anchorText = window.prompt('Anchor display test');

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
