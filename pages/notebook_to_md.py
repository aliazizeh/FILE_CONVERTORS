import streamlit as st
import nbformat
from nbconvert import MarkdownExporter
from traitlets.config import Config

# --- Page Setup ---
st.set_page_config(page_title="Notebook -> Markdown", page_icon="📓")

def convert_notebook_to_md(notebook_file, strip_code=False):
    """
    Converts uploaded .ipynb file to Markdown string.
    """
    # Decode bytes to string
    notebook_content = notebook_file.getvalue().decode("utf-8")
    notebook_node = nbformat.reads(notebook_content, as_version=4)

    # Configuration for the Exporter
    c = Config()
    if strip_code:
        # Configuration to remove code inputs
        c.MarkdownExporter.exclude_input = True
        c.MarkdownExporter.exclude_input_prompt = True
        c.MarkdownExporter.exclude_output_prompt = True
    
    # Create the exporter
    exporter = MarkdownExporter(config=c)
    
    # Convert
    body, resources = exporter.from_notebook_node(notebook_node)
    return body

# --- UI Layout ---
st.title("📓 Jupyter Notebook to Markdown Tool")
st.markdown("Upload a **.ipynb** file to convert it into a **.md** report.")

# --- Sidebar Controls ---
st.sidebar.header("Configuration")
remove_code = st.sidebar.checkbox(
    "Remove Code Cells?", 
    value=False,
    help="Check this to strip out all Python code, keeping only text, tables, and graphs."
)

# --- Main Interface ---
uploaded_file = st.file_uploader("Upload Notebook", type=["ipynb"])

if uploaded_file:
    st.info(f"File loaded: `{uploaded_file.name}`")
    
    if st.button("Convert to Markdown", type="primary"):
        with st.spinner("Converting..."):
            try:
                md_output = convert_notebook_to_md(uploaded_file, strip_code=remove_code)
                
                st.success("Conversion Complete!")
                
                # Create Output Filename
                new_filename = uploaded_file.name.replace(".ipynb", ".md")
                
                # Download Button
                st.download_button(
                    label="📥 Download .md File",
                    data=md_output,
                    file_name=new_filename,
                    mime="text/markdown"
                )
                
                with st.expander("Preview Content"):
                    st.text(md_output[:1000] + "\n\n[...truncated for preview...]")
                    
            except Exception as e:
                st.error(f"Error: {e}")