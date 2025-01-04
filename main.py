import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_gemini

# Streamlit UI
st.title("AI Web Scraper")

# Step 1: Website URL input
url = st.text_input("Enter Website URL")

# Step 1: Scrape the Website
if st.button("Scrape Website"):
    if url:
        st.write("Scraping the website...")

        try:
            # Scrape the website content
            dom_content = scrape_website(url)
            body_content = extract_body_content(dom_content)
            cleaned_content = clean_body_content(body_content)

            # Store the cleaned DOM content in Streamlit session state
            st.session_state.dom_content = cleaned_content

        except Exception as e:
            st.error(f"An error occurred during scraping: {e}")

# Display the scraped content if it exists
if "dom_content" in st.session_state:
    with st.expander("Scraped Content (Always Visible)", expanded=True):
        st.text_area("DOM Content", st.session_state.dom_content, height=300)

    # Step 2: Parse Content based on Description
    parse_description = st.text_area("Describe what you want to parse")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content...")

            try:
                # Split the content into manageable chunks and parse with Gemini
                dom_chunks = split_dom_content(st.session_state.dom_content)
                parsed_result = parse_with_gemini(dom_chunks, parse_description)

                # Display the parsed output separately
                st.subheader("Parsed Output")
                st.write(parsed_result)

            except Exception as e:
                st.error(f"An error occurred during parsing: {e}")
