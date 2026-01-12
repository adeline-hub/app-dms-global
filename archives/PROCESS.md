A.	ARCHITECTURE	
dash-seasonal-template/
│
├── app.py
├── layout.py
├── seasonal.py
├── pdf_export.py
├── requirements.txt
├── render.yaml
│
├── assets/
│   ├── seasonal.css
│   ├── handline.svg
│   ├── handarrow.svg
│   └── logo.png
│
├── app_dms_global/              👈 DMS ENGINE (COPIED)
│   ├── backend/
│   ├── scripts/
│   │   ├── __init__.py          ✅ REQUIRED
│   │   ├── standardize_documents.py
│   │   ├── project_reasoning.py
│   │   ├── generate_structure_overview.py
│   │   ├── generate_business_deck.py
│   │   ├── deck_md_to_ppt.py
│   │   └── pipeline.py          ✅ YOUR ORCHESTRATOR
│   ├── templates/
│   ├── utils/
│   └── requirements.txt         (optional, see below)
│
└── README.md

B.	RUN LOCALLY
POWER SHELL
	python -m venv venv
	venv\Scripts\Activate
	pip install -r requirements.txt
	python app.py
Open: http://127.0.0.1:8050
