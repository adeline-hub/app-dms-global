from dash import Input, Output, State, dcc, html, callback, ctx
import base64
import time
from pathlib import Path
import os
import shutil  


# Try to import pipeline, but create mock if not available
try:
    from app_dms_global.scripts.pipeline import run_pipeline
except ImportError:
    print("⚠️ Pipeline module not found. Using mock pipeline.")
    def run_pipeline(project_id, sector, territory, input_dir, output_dir):
        print(f"Mock pipeline: {project_id}, {sector}, {territory}")
        time.sleep(2)
        output_path = Path(output_dir) / f"{project_id}-investors.pptx"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(f"Mock deck for {project_id}")
        return str(output_path)

def register_callbacks(app):

    # Summer: Set sector and territory
    @app.callback(
        Output("current-sector", "data"),
        Output("current-territory", "data"), 
        Output("summer-status", "children"),
        Input("sector-submit-btn", "n_clicks"),
        Input("territory-submit-btn", "n_clicks"),
        State("sector-input", "value"),
        State("territory-input", "value"),
        State("current-sector", "data"),
        State("current-territory", "data"),
        prevent_initial_call=True
    )
    
    
    def set_project_info(sector_clicks, territory_clicks, sector_input, territory_input, current_sector, current_territory):
        button_id = ctx.triggered_id if ctx.triggered_id else ""
        
        updated_sector = current_sector
        updated_territory = current_territory
        status_message = ""
        
        if button_id == "sector-submit-btn" and sector_input and sector_input.strip():
            updated_sector = sector_input
            status_message = f"✅ Sector set: {sector_input}"
        
        elif button_id == "territory-submit-btn" and territory_input and territory_input.strip():
            updated_territory = territory_input
            status_message = f"✅ Territory set: {territory_input}"
        
        if updated_sector and updated_territory:
            status_message = f"✅ Project: {updated_sector} in {updated_territory}"
        
        return updated_sector, updated_territory, status_message

    # Autumn: File upload
    @app.callback(
        Output("uploaded-files", "data"),
        Output("autumn-status", "children"),
        Input("upload-documents", "contents"),
        State("upload-documents", "filename"),
        State("uploaded-files", "data"),
        prevent_initial_call=True
    )
    def handle_upload(contents, filename, existing_files):
        if contents:
            if isinstance(contents, list):
                saved_files = []
                for content, fname in zip(contents, filename):
                    content_type, content_string = content.split(',')
                    decoded = base64.b64decode(content_string)
                    
                    BASE = Path("projects/current_project/raw_docs")
                    BASE.mkdir(parents=True, exist_ok=True)
                    
                    file_path = BASE / fname
                    with open(file_path, 'wb') as f:
                        f.write(decoded)
                    saved_files.append(fname)
                
                file_list = ", ".join(saved_files[:3])
                if len(saved_files) > 3:
                    file_list += f" and {len(saved_files) - 3} more"
                
                new_files = existing_files + saved_files if existing_files else saved_files
                return new_files, f"✅ Uploaded {len(saved_files)} files: {file_list}"
            
            else:
                content_type, content_string = contents.split(',')
                decoded = base64.b64decode(content_string)
                
                BASE = Path("projects/current_project/raw_docs")
                BASE.mkdir(parents=True, exist_ok=True)
                
                file_path = BASE / filename
                with open(file_path, 'wb') as f:
                    f.write(decoded)
                
                new_files = existing_files + [filename] if existing_files else [filename]
                return new_files, f"✅ Uploaded: {filename}"
        
        return existing_files, ""
    print("✅ ALL CALLBACKS REGISTERED SUCCESSFULLY")
    
    # Winter: Run pipeline (MAIN callback - controls everything)
    @app.callback(
        Output("pipeline-status", "data"),
        Output("winter-status", "children"),
        Output("download-deck-btn", "disabled"),
        Output("spring-status", "children"),
        Input("run-pipeline-btn", "n_clicks"),
        State("current-sector", "data"),
        State("current-territory", "data"),
        State("uploaded-files", "data"),
        prevent_initial_call=True
    )
    def handle_pipeline(run_clicks, sector, territory, uploaded_files):
        print("=" * 50)
        print("🔴 PIPELINE CALLBACK TRIGGERED!")
        print(f"   run_clicks: {run_clicks}")
        print(f"   sector: '{sector}'")
        print(f"   territory: '{territory}'")
        print(f"   uploaded_files: {uploaded_files}")
        print("=" * 50)
        
        # Default return values
        pipeline_data = {"running": False, "completed": False}
        winter_msg = ""
        download_disabled = True
        spring_msg = ""
        
        if run_clicks:
            if not sector or not territory:
                winter_msg = "❌ Please set Sector and Territory first"
                return pipeline_data, winter_msg, download_disabled, spring_msg
            
            if not uploaded_files:
                winter_msg = "❌ Please upload documents first"
                return pipeline_data, winter_msg, download_disabled, spring_msg
            
            winter_msg = "⏳ Running pipeline... This may take a minute..."
            spring_msg = "⏳ Processing..."
            
            try:
                import matplotlib
                matplotlib.use('Agg')
                
                deck_path = run_pipeline(
                    project_id="current_project",
                    sector=sector,
                    territory=territory,
                    input_dir="projects/current_project/raw_docs",
                    output_dir="projects/current_project/outputs"
                )
                
                pipeline_data = {"running": False, "completed": True, "deck_path": deck_path}
                winter_msg = "✅ Pipeline completed!"
                download_disabled = False
                spring_msg = "✅ Deck ready! Click download button above."
                
            except Exception as e:
                error_msg = str(e)
                print(f"Pipeline error: {error_msg}")
                
                if "429" in error_msg or "rate_limit" in error_msg.lower():
                    winter_msg = "❌ Rate limit reached. Please wait and try again."
                else:
                    winter_msg = f"❌ Error: {error_msg[:100]}..."
                
                pipeline_data["error"] = error_msg
                spring_msg = "❌ Pipeline failed."
        
        return pipeline_data, winter_msg, download_disabled, spring_msg

    # Spring: Download deck (with GDPR auto-cleanup)
    @app.callback(
        Output("download-deck", "data"),
        Output("spring-status", "children", allow_duplicate=True),
        Input("download-deck-btn", "n_clicks"),
        State("pipeline-status", "data"),
        prevent_initial_call=True
    )
    def handle_download(download_clicks, pipeline_status):
        if download_clicks:
            if pipeline_status.get("completed"):
                deck_path = pipeline_status.get("deck_path", "")
                if deck_path and Path(deck_path).exists():
                    
                    # Schedule GDPR cleanup after download
                    import threading
                    import shutil
                    
                    def cleanup_after_delay():
                        time.sleep(30)  # Wait 30 seconds for download to complete
                        project_dir = Path("projects/current_project")
                        folders = ["raw_docs", "standardized", "outputs", "insights", "deck", "financial", "memo"]
                        
                        for folder in folders:
                            folder_path = project_dir / folder
                            if folder_path.exists():
                                shutil.rmtree(folder_path)
                                folder_path.mkdir(parents=True, exist_ok=True)
                        
                        print("🗑️ GDPR auto-cleanup completed - all project data deleted")
                    
                    # Start cleanup in background
                    threading.Thread(target=cleanup_after_delay, daemon=True).start()
                    
                    return (
                        dcc.send_file(deck_path),
                        "✅ Downloading... (data auto-deletes in 30s for GDPR)"
                    )
                else:
                    return (
                        None,
                        "❌ Deck file not found."
                    )
            else:
                return (
                    None,
                    "❌ Pipeline not completed yet."
                )
        
        return None, ""