import streamlit as st
from helper import (
    get_matches,
    resize_image,
    print_stars,
    get_matches_from_image,
    facets,
)
from config import (
    TOP_K,
    IMAGE_RESIZE_FACTOR,
    SERVER,
    PORT,
    DEBUG,
)

limit = 10

title = "📝 PDF search with Jina"

st.set_page_config(page_title=title, layout="wide")

# Sidebar
st.sidebar.title("Options")

input_media = st.sidebar.radio(label="Search with...", options=["text", "image"])


if DEBUG:
    with st.sidebar.expander("Debug"):
        server = st.text_input(label="Server", value=SERVER)
        port = st.text_input(label="Port", value=PORT)
else:
    server = SERVER
    port = PORT

st.sidebar.title("About")

st.sidebar.markdown(
    """This example lets you search a library of PDFs using text or image. It's powered by the [Jina](https://github.com/jina-ai/jina/) neural search framework.
"""
)

st.sidebar.markdown(
    "[Repo link](https://github.com/alexcg1/jina-multimodal-fashion-search)"
)

# Main area
st.title(title)

if input_media == "text":
    text_query = st.text_input(label="Search term", placeholder="Blue dress")
    text_search_button = st.button("Search")
    if text_search_button:
        matches = get_matches(
            input=text_query,
            limit=limit,
            server=server,
            port=port,
        )
        print(matches)

elif input_media == "image":
    image_query = st.file_uploader(label="Image file")
    image_search_button = st.button("Search")
    if image_search_button:
        matches = get_matches_from_image(
            input=image_query,
            limit=limit,
            server=server,
            port=port,
        )

if "matches" in locals():
    for match in matches:
        icon_cell, info_cell = st.columns([1,5])
        icon_cell.image("./icon.png")
        icon_cell.markdown(f"**{match.tags['uri']}**")
        if hasattr(match, "text"):
            info_cell.markdown(match.text)
        elif hasattr(match, "blob"):
            info_cell.markdown("blob")
        else:
            info_cell.markdown("don't know if text or image")
        st.markdown("---")
        # pic_cell, desc_cell, price_cell = st.columns([1, 6, 1])

        # image = resize_image(match.uri, resize_factor=IMAGE_RESIZE_FACTOR)

        # pic_cell.image(image, use_column_width="auto")
        # desc_cell.markdown(
            # f"##### {match.tags['productDisplayName']} {print_stars(match.tags['rating'])}"
        # )
        # desc_cell.markdown(
            # f"*{match.tags['masterCategory']}*, *{match.tags['subCategory']}*, *{match.tags['articleType']}*, *{match.tags['baseColour']}*, *{match.tags['season']}*, *{match.tags['usage']}*, *{match.tags['year']}*"
        # )
        # price_cell.button(key=match.id, label=str(match.tags["price"]))