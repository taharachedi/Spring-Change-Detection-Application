"""
script that hold the configuration of our application
"""
from pathlib import Path

# ─── Streamlit page settings ──────────────────────────────────────────────────
PAGE_TITLE: str = "Spring Change Detection"
PAGE_ICON: str = "🚗"
PAGE_LAYOUT: str = "wide"
INITIAL_SIDEBAR_STATE: str = "auto"

# ─── Upload restrictions ──────────────────────────────────────────────────────
UPLOAD_CONFIG = {
    "allowed_extension": ['xlsx', 'xls'],
    "max_file_size" : 200,
    "sheet_name": "PTA",
    "skip_rows": [1]
    }

# ─── Columns Data ────────────────────────────────────────────────────
REQUIRED_COLUMNS: dict = {
    "mass": "Masse suspendue en charge de référence",
    "reference": "Référence"
}

VP_COLUMNS_KEY: list = [
        "Moteur", "Boite", "Niveau",
        "Plaque de protection tôle sous GMP",
        "Pavillon multifonction", "2e PLC Gauche",
        "Chauffage additionnel type WEBASTO"   
        ]

VU_COLUMNS_KEY: list =[
    "Moteur", "Boite", "Niveau", "Plaque de conception"
]

# ─── Root Path ────────────────────────────────────────────────────
ROOT_PATH = Path(__file__).resolve().parent.parent