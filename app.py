import os
# Suppress Tkinter warnings
os.environ['TK_SILENCE_DEPRECATION'] = '1'

from dash import Dash
from layout import layout
from pdf_export import export_page_to_pdf
from flask import send_file, request
import io
from callbacks import register_callbacks

app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.layout = layout()

# Register all callbacks
register_callbacks(app)

@server.route("/export-pdf")
def export_pdf():
    base_url = request.host_url.rstrip("/")
    pdf = export_page_to_pdf(base_url)

    return send_file(
        io.BytesIO(pdf),
        mimetype="application/pdf",
        as_attachment=True,
        download_name="business_deck_process.pdf",
    )

if __name__ == "__main__":
    app.run(debug=True)