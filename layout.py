from dash import html, dcc
from seasonal import seasonal_score

def layout():
    return html.Div(
        className="app-container",
        children=[

            html.Div(
                className="page-header",
                children=[
                    html.H1("Build a Business Deck"),
                    html.H2("Application · Data Management System"),
                ],
            ),

            # Seasonal blocks with integrated actions
            seasonal_score(),

            html.Div(
                "This interface visualizes a data transformation process. "
                "Generated outputs are indicative and non-contractual.",
                className="disclaimer",
            ),

            html.Div(
                className="page-footer",
                children=[
                    html.A(
                        "Export PDF",
                        href="/export-pdf",
                        target="_blank",
                    ),

                    html.A(
                        html.Img(
                            src="/assets/logo.png",
                            className="brand-logo",
                        ),
                        href="#",
                        target="_blank",
                    ),

                    html.Button("Tech note", id="tech-note-btn"),
                ],
            ),
            
            # Hidden stores for data and pipeline status
            dcc.Store(id="current-sector", data=""),
            dcc.Store(id="current-territory", data=""),
            dcc.Store(id="uploaded-files", data=[]),
            dcc.Store(id="pipeline-status", data={"running": False, "completed": False}),
            dcc.Store(id="deck-path", data=""),  # Store the generated deck path
        ],
    )