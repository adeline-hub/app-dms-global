# generate_financial_charts.py - Updated with proper matplotlib setup
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

import argparse
import pandas as pd
import matplotlib
# Set the backend BEFORE importing pyplot
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

def generate_financial_charts(project_name):
    BASE = Path(f"projects/{project_name}")
    RAW = BASE / "raw_docs"
    OUT = BASE / "financial/charts"
    OUT.mkdir(parents=True, exist_ok=True)

    # Your chart generation code here...
    # Make sure to close all figures properly
    
    plt.figure()
    # ... create chart ...
    chart_path = OUT / "revenue.png"
    plt.savefig(chart_path, dpi=150)
    plt.close('all')  # Close ALL figures to free memory
    
    return str(chart_path)