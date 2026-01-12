from dash import html, dcc

def seasonal_score():
    seasons = [
        {
            "label": "SUMMER",
            "title": "Input", 
            "note": "Collect project info",
            "offset": "offset-0",
            "season_id": "summer",
            "action": summer_action(),
        },
        {
            "label": "AUTUMN",
            "title": "Structure",
            "note": "Collect raw material", 
            "offset": "offset-1",
            "season_id": "autumn",
            "action": autumn_action(),
        },
        {
            "label": "WINTER",
            "title": "Process",
            "note": "Run pipeline computation",
            "offset": "offset-0", 
            "season_id": "winter",
            "action": winter_action(),  # Pipeline activation button
        },
        {
            "label": "SPRING",
            "title": "Output",
            "note": "Download final deck",
            "offset": "offset-1",
            "season_id": "spring", 
            "action": spring_action(),  # Only download button
        },
    ]

    return html.Div(
        className="seasonal-score",
        children=[
            html.Div(
                className=f"season-block {s['offset']}",
                children=[
                    # annotation (left)
                    html.Div(
                        className="season-annotation",
                        children=[
                            html.Div(s["note"], className="annotation-text"),
                            html.Div(className="annotation-arrow"),
                        ],
                    ),

                    # season text
                    html.Div(s["label"], className="season-label"),
                    html.Div(s["title"], className="season-title"),
                    html.Div(className="season-line"),

                    # Action area (right under the line)
                    s["action"] if s["action"] else None,
                ],
            )
            for s in seasons
        ],
    )


# ---------- SEASON ACTION COMPONENTS ----------

def summer_action():
    return html.Div(
        className="season-action",
        children=[
            dcc.Input(
                id="sector-input",
                placeholder="Sector",
                className="inline-input"
            ),
            html.Button(
                "OK", 
                id="sector-submit-btn",
                className="inline-ok"
            ),
            dcc.Input(
                id="territory-input",
                placeholder="Territory (country / region / world)",
                className="inline-input"
            ),
            html.Button(
                "OK", 
                id="territory-submit-btn",
                className="inline-ok"
            ),
            html.Div(id="summer-status", className="status-message"),
        ]
    )


def autumn_action():
    return html.Div(
        className="season-action",
        children=[
            dcc.Upload(
                id="upload-documents",
                children=html.Button(
                    "UPLOAD DOCUMENTS",
                    className="inline-button"
                ),
                multiple=True,
            ),
            html.Div(id="autumn-status", className="status-message"),
        ]
    )


def winter_action():
    """Winter: Pipeline activation button with processing info"""
    return html.Div(
        className="season-action",
        children=[
            html.Button(
                "RUN PIPELINE",
                id="run-pipeline-btn",
                className="inline-button winter-btn",
            ),
            html.Div(id="winter-status", className="status-message processing-info"),
        ]
    )


def spring_action():
    """Spring: Only download button with deck info"""
    return html.Div(
        className="season-action",
        children=[
            html.Button(
                "DOWNLOAD DECK",
                id="download-deck-btn",
                className="inline-button spring-btn",
                disabled=True,  # Initially disabled
            ),
            dcc.Download(id="download-deck"),
            html.Div(id="spring-status", className="status-message deck-info"),
        ]
    )