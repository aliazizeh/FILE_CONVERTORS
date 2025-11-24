import streamlit as st

# --- Page Config ---
st.set_page_config(
    page_title="Reporting Toolkit",
    page_icon="🛠️",
    layout="centered"
)

# --- Main Content ---
st.title("🛠️  Notebook Reporting Toolkit")

st.markdown("""
### Welcome
This application centralizes the reporting workflow from notebook. 
Use the sidebar to navigate between the standalone utilities.

---

### 📂 Available Modules

#### 1️⃣ **Notebook to Markdown**
* **Input:** Jupyter Notebook (`.ipynb`)
* **Output:** Markdown Report (`.md`)
* **Features:** Option to strip code cells for clean management reports.

#### 2️⃣ **Markdown to Word**
* **Input:** Markdown Report (`.md`)
* **Output:** Microsoft Word (`.docx`)
* **Features:** Preserves LaTeX formulas (e.g., $dS_t$), tables, and structure.

---

### 🚀 Workflow Recommendation
1.  **Analyze:** Run your analysis in Colab/Jupyter.
2.  **Export:** Download the `.ipynb` file.
3.  **Convert:** Go to the **Notebook to MD** page to get your raw text.
4.  **Format:** Go to the **MD to Word** page to finalize the document.
""")

st.info("👈 Select a tool from the sidebar to begin.")