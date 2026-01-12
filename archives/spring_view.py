from dash import html

def spring_process_view():
    return html.Div(
        className="spring-process-view",
        children=[

            html.H1(
                "Build a Business Deck\nfrom Your Documents",
                className="spring-title"
            ),

            html.Div(
                className="process-map",
                children=[

                    process_block(
                        "INPUT",
                        "Collect raw material",
                        side="left"
                    ),

                    process_block(
                        "STRUCTURE",
                        "Organize & interpret",
                        side="right"
                    ),

                    process_block(
                        "PROCESS",
                        "Run pipeline\nSilent compute",
                        center=True
                    ),

                    process_block(
                        "OUTPUT",
                        "Reveal the story",
                        side="left"
                    )
                ]
            ),

            spring_actions()
        ]
    )


def process_block(title, subtitle, side=None, center=False):
    classes = ["process-block"]
    if side:
        classes.append(f"side-{side}")
    if center:
        classes.append("center")

    return html.Div(
        className=" ".join(classes),
        children=[
            html.Div(title, className="block-title"),
            html.Div(subtitle, className="block-subtitle"),
            html.Div(className="block-line")
        ]
    )


def spring_actions():
    return html.Div(
        className="spring-actions",
        children=[
            html.Button("Download Business Deck"),
            html.Button("View Logs"),
            html.Button("Tech Note")
        ]
    )