# Import the streamlit library and alias it as st (industry convention for convenience)
import time
import streamlit as st
from knowledge_base import KnowledgeBaseService

# Display a large title on the web page
st.title("Knowledge Base Update Service")

# Create a file uploader component
# label: text displayed above the uploader
# type: restrict to text files only (.txt)
# accept_multiple_files: set to False to allow only one file at a time
uploader_file = st.file_uploader(
    "Please upload a TXT file",
    type=["txt"],
    accept_multiple_files=False
)

# If the session_state does not have a 'service' key, create a new one
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

# Check if the user has selected a file
# If uploader_file is not None, execute the indented code
if uploader_file is not None:

    # Get basic file information
    file_name = uploader_file.name                # Get the file name
    file_type = uploader_file.type                # Get the MIME type
    file_size = uploader_file.size / 1024         # Get file size in bytes, convert to KB

    # Display a subheading with the file name
    # f"..." is a formatted string literal; variables inside {} are inserted
    st.subheader(f"File name: {file_name}")

    # Display the file format and size (rounded to two decimal places)
    st.write(f"Format: {file_type} | Size: {file_size:.2f} KB")

    # Read the file content
    # .getvalue() returns binary data
    # .decode("utf-8") converts binary data to human‑readable text
    text = uploader_file.getvalue().decode("utf-8")

    with st.spinner("Uploading file to the knowledge base..."):
        time.sleep(1)
        result = st.session_state["service"].upload_by_string(text, file_name)
        st.write(result)