import streamlit as st
import os
import subprocess
import tempfile
import shutil

# --- Page Setup ---
st.set_page_config(page_title="Markdown -> Word", page_icon="📄")

def is_pandoc_installed():
    """Checks if pandoc is available in the system path."""
    return shutil.which("pandoc") is not None

def convert_md_to_docx(input_bytes):
    """
    Saves uploaded bytes to a temp file, runs pandoc, and returns output path.
    """
    # Create a temporary directory to avoid file conflicts
    temp_dir = tempfile.mkdtemp()
    
    input_path = os.path.join(temp_dir, "input.md")
    output_path = os.path.join(temp_dir, "output.docx")

    # Write input bytes to disk
    with open(input_path, "wb") as f:
        f.write(input_bytes)

    # Run Pandoc
    try:
        # -s: standalone (full doc structure)
        # -o: output file
        cmd = ["pandoc", input_path, "-s", "-o", output_path]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return output_path, None
    except subprocess.CalledProcessError as e:
        return None, str(e)

# --- UI Layout ---
st.title("📄 Markdown to Word Tool")
st.markdown("Upload a **.md** file to convert it into a **.docx** document (preserving Formulas & Tables).")

# --- Dependency Check ---
if not is_pandoc_installed():
    st.error("❌ **Pandoc is not installed.**")
    st.warning("This tool requires Pandoc to handle the conversion.")
    st.info("Download it here: https://pandoc.org/installing.html")
    st.stop()

# --- Main Interface ---
uploaded_file = st.file_uploader("Upload Markdown", type=["md"])

if uploaded_file:
    if st.button("Convert to Word", type="primary"):
        with st.spinner("Running Pandoc..."):
            
            # Run Conversion
            file_bytes = uploaded_file.getvalue()
            result_path, error = convert_md_to_docx(file_bytes)

            if error:
                st.error(f"Conversion Failed: {error}")
            else:
                st.success("Conversion Successful!")
                
                # Read generated file for download
                with open(result_path, "rb") as f:
                    doc_bytes = f.read()
                
                # Cleanup temp files
                shutil.rmtree(os.path.dirname(result_path), ignore_errors=True)
                
                # Download Button
                new_filename = uploaded_file.name.replace(".md", ".docx")
                st.download_button(
                    label="📥 Download .docx File",
                    data=doc_bytes,
                    file_name=new_filename,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )