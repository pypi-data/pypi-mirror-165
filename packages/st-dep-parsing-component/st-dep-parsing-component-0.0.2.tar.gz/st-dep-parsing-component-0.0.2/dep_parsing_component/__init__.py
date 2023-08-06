import os
import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = True

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("my_component"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "dep_parsing_component",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("dep_parsing_component", path=build_dir)


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def dep_parsing_component(data, key=None):
    """Create a new instance of "my_component".

    Parameters
    ----------
    name: str
        The name of the thing we're saying hello to. The component will display
        the text "Hello, {name}!"
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    int
        The number of times the component's "Click Me" button has been clicked.
        (This is the value passed to `Streamlit.setComponentValue` on the
        frontend.)

    """
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    component_value = _component_func(data=data, key=key)

    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.
    return component_value


# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run my_component/__init__.py`
if not _RELEASE:
    import streamlit as st
    st.set_page_config(layout="wide")
    st.subheader("Depedency Parsing Component")
    nltk=[{'words': [{'text': 'i', 'tag': 'NN', 'id': 0}, {'text': 'like', 'tag': 'NN', 'id': 1}, {'text': 'this', 'tag': 'NNS', 'id': 2}, {'text': 'tree', 'tag': 'NN', 'id': 3}, {'text': '.', 'tag': '.', 'id': 4}], 'arcs': [{'start': 0, 'end': 3, 'label': 'nn', 'dir': 'left'}, {'start': 1, 'end': 3, 'label': 'nn', 'dir': 'left'}, {'start': 2, 'end': 3, 'label': 'nn', 'dir': 'left'}, {'start': 3, 'end': 4, 'label': 'punct', 'dir': 'right'}], 'text': 'i like this tree.'}]
    spacy=[{'words': [{'text': 'i', 'tag': 'PRON', 'id': 0}, {'text': 'like', 'tag': 'VERB', 'id': 1}, {'text': 'this', 'tag': 'DET', 'id': 2}, {'text': 'tree', 'tag': 'NOUN', 'id': 3}, {'text': '.', 'tag': 'PUNCT', 'id': 4}], 'arcs': [{'start': 0, 'end': 1, 'label': 'nsubj', 'dir': 'left'}, {'start': 2, 'end': 3, 'label': 'det', 'dir': 'left'}, {'start': 3, 'end': 1, 'label': 'dobj', 'dir': 'right'}, {'start': 4, 'end': 1, 'label': 'punct', 'dir': 'right'}]}]
    stanza=[{'words': [{'text': 'i', 'tag': 'PRON', 'id': 0}, {'text': 'like', 'tag': 'VERB', 'id': 1}, {'text': 'this', 'tag': 'DET', 'id': 2}, {'text': 'tree', 'tag': 'NOUN', 'id': 3}, {'text': '.', 'tag': 'PUNCT', 'id': 4}], 'arcs': [{'start': 1, 'end': 0, 'label': 'nsubj', 'dir': 'right'}, {'start': 3, 'end': 2, 'label': 'det', 'dir': 'right'}, {'start': 1, 'end': 3, 'label': 'obj', 'dir': 'left'}, {'start': 1, 'end': 4, 'label': 'punct', 'dir': 'left'}]}]

    st.write('nltk')
    
    dep_parsing_component(nltk[0])
    st.write('stanza')
    dep_parsing_component(stanza[0],'k2')
    st.write('spacy')
    dep_parsing_component(spacy[0],'k3')  