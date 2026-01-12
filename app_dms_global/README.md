\# DMS — Document Management System + AI Business Deck Generator



This project is a \*\*Document Management System (DMS)\*\* that helps users create a \*\*project workspace\*\*, upload documents (PDF/DOCX/XLSX), and generate:

\- standardized text versions of documents

\- extracted key insights (LLM)

\- memo sections (LLM)

\- financial charts from a template Excel model

\- a \*\*branded PowerPoint business deck\*\* with \*\*citations\*\* and embedded charts



The app is deployed on \*\*Render\*\* and includes a simple HTML user interface.

https://dms-app-gjpl.onrender.com/ 

---



\## Features



\- \*\*Project creation\*\* (type, sector, territory)

\- \*\*Multi-file upload\*\* with validation (size/type + project existence)

\- \*\*Document text extraction\*\*

&nbsp; - PDF (text layer)

&nbsp; - DOCX

&nbsp; - (XLSX handled by financial pipeline, not doc standardization)

\- \*\*LLM-powered insights \& memo drafting\*\*

\- \*\*Financial pipeline\*\*

&nbsp; - download a required Excel template

&nbsp; - extract summary metrics

&nbsp; - generate charts (PNG)

\- \*\*Deck generation\*\*

&nbsp; - deck content in Markdown (LLM)

&nbsp; - export to PPTX using a branded template

&nbsp; - citations per slide in footer

\- \*\*(Optional/Next)\*\* RAG search for grounded Q\&A



\\Documents\\dms

---



\## Tech Stack



\- \*\*Backend\*\*: FastAPI + Uvicorn

\- \*\*LLM\*\*: OpenAI API (via `utils/llm.py`)

\- \*\*Docs extraction\*\*: `pypdf`, `python-docx`

\- \*\*Finance\*\*: `pandas`, `openpyxl`, `matplotlib`

\- \*\*Deck\*\*: `python-pptx`

\- \*\*Frontend\*\*: simple HTML (`frontend/index.html`)

\- \*\*Deployment\*\*: Render



---



\## Repository Structure



```text

backend/

&nbsp; main.py

&nbsp; api/

&nbsp;   projects.py

&nbsp;   uploads.py

&nbsp;   templates.py

&nbsp; services/

&nbsp;   project\_service.py

&nbsp;   upload\_service.py

&nbsp;   pipeline\_service.py



scripts/

&nbsp; standardize\_documents.py

&nbsp; extract\_key\_insights.py

&nbsp; generate\_draft\_memo\_sections.py

&nbsp; generate\_structure\_overview.py

&nbsp; generate\_business\_deck.py

&nbsp; deck\_md\_to\_ppt.py

&nbsp; financial/

&nbsp;   extract\_financials.py

&nbsp;   generate\_financial\_charts.py



templates/

&nbsp; Brand\_Template.pptx

&nbsp; Financial\_Model\_Template.xlsx



frontend/

&nbsp; index.html

&nbsp; assets/

&nbsp;   logo.png



utils/

&nbsp; llm.py

&nbsp; chunker.py

&nbsp; paths.py (optional)

&nbsp; rag.py (optional)

