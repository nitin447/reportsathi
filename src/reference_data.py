# General adult reference ranges (FALLBACK ONLY). Labs differ, so the range
# printed on the report always takes priority.
# ranges: {"any": (low, high)} or {"male": ..., "female": ...}; None = open-ended.

COUNT_UNITS = {"/cumm": 1, "/mm3": 1, "/ul": 1, "cells/cumm": 1,
               "10^3/ul": 1000, "x10^3/ul": 1000, "10^9/l": 1000, "10^3/cumm": 1000}
PLT_UNITS = {**COUNT_UNITS, "lakh/cumm": 100000, "lakhs/cumm": 100000, "lac/cumm": 100000}

REFERENCE = {
    "hemoglobin": {
        "name": "Hemoglobin", "unit": "g/dL",
        "aliases": ["hemoglobin", "haemoglobin", "hb", "hgb"],
        "units": {"g/dl": 1, "g%": 1},
        "ranges": {"male": (13.0, 17.0), "female": (12.0, 15.5)},
    },
    "wbc": {
        "name": "WBC Count", "unit": "/cumm",
        "aliases": ["wbc", "wbc count", "total wbc count", "total leucocyte count",
                    "total leukocyte count", "tlc", "white blood cell count"],
        "units": COUNT_UNITS,
        "ranges": {"any": (4000, 11000)},
    },
    "platelets": {
        "name": "Platelet Count", "unit": "/cumm",
        "aliases": ["platelet count", "platelets", "plt"],
        "units": PLT_UNITS,
        "ranges": {"any": (150000, 450000)},
    },
    "mcv": {
        "name": "MCV", "unit": "fL",
        "aliases": ["mcv", "mean corpuscular volume"],
        "units": {"fl": 1},
        "ranges": {"any": (80.0, 100.0)},
    },
    "mch": {
        "name": "MCH", "unit": "pg",
        "aliases": ["mch", "mean corpuscular hemoglobin"],
        "units": {"pg": 1},
        "ranges": {"any": (27.0, 33.0)},
    },
    "mchc": {
        "name": "MCHC", "unit": "g/dL",
        "aliases": ["mchc", "mean corpuscular hemoglobin concentration"],
        "units": {"g/dl": 1},
        "ranges": {"any": (32.0, 36.0)},
    },
    "rdw": {
        "name": "RDW", "unit": "%",
        "aliases": ["rdw", "rdw cv", "red cell distribution width"],
        "units": {"%": 1},
        "ranges": {"any": (11.5, 14.5)},
    },
    "ferritin": {
        "name": "Serum Ferritin", "unit": "ng/mL",
        "aliases": ["ferritin", "serum ferritin"],
        "units": {"ng/ml": 1, "ug/l": 1},
        "ranges": {"male": (30.0, 400.0), "female": (13.0, 150.0)},
    },
    "vitamin_d": {
        "name": "Vitamin D (25-OH)", "unit": "ng/mL",
        "aliases": ["vitamin d", "vitamin d 25 oh", "vitamin d (25-oh)", "25 oh vitamin d",
                    "25-hydroxy vitamin d", "vit d"],
        "units": {"ng/ml": 1, "nmol/l": 0.4},
        "ranges": {"any": (30.0, 100.0)},
    },
    "vitamin_b12": {
        "name": "Vitamin B12", "unit": "pg/mL",
        "aliases": ["vitamin b12", "vit b12", "b12", "cobalamin"],
        "units": {"pg/ml": 1},
        "ranges": {"any": (200.0, 900.0)},
    },
    "glucose_fasting": {
        "name": "Fasting Glucose", "unit": "mg/dL",
        "aliases": ["fasting glucose", "fasting blood sugar", "fbs", "glucose fasting",
                    "blood sugar fasting"],
        "units": {"mg/dl": 1, "mmol/l": 18.0},
        "ranges": {"any": (70.0, 99.0)},
    },
    "hba1c": {
        "name": "HbA1c", "unit": "%",
        "aliases": ["hba1c", "glycosylated hemoglobin", "glycated hemoglobin",
                    "hemoglobin a1c", "a1c"],
        "units": {"%": 1},
        "ranges": {"any": (4.0, 5.6)},
    },
    "cholesterol_total": {
        "name": "Total Cholesterol", "unit": "mg/dL",
        "aliases": ["total cholesterol", "cholesterol total", "cholesterol"],
        "units": {"mg/dl": 1},
        "ranges": {"any": (None, 199.0)},
    },
    "ldl": {
        "name": "LDL Cholesterol", "unit": "mg/dL",
        "aliases": ["ldl", "ldl cholesterol", "ldl-c"],
        "units": {"mg/dl": 1},
        "ranges": {"any": (None, 99.0)},
    },
    "hdl": {
        "name": "HDL Cholesterol", "unit": "mg/dL",
        "aliases": ["hdl", "hdl cholesterol", "hdl-c"],
        "units": {"mg/dl": 1},
        "ranges": {"male": (40.0, None), "female": (50.0, None)},
    },
    "triglycerides": {
        "name": "Triglycerides", "unit": "mg/dL",
        "aliases": ["triglycerides", "triglyceride", "tg"],
        "units": {"mg/dl": 1},
        "ranges": {"any": (None, 149.0)},
    },
    "tsh": {
        "name": "TSH", "unit": "mIU/L",
        "aliases": ["tsh", "thyroid stimulating hormone"],
        "units": {"miu/l": 1, "uiu/ml": 1},
        "ranges": {"any": (0.4, 4.0)},
    },
    "creatinine": {
        "name": "Serum Creatinine", "unit": "mg/dL",
        "aliases": ["creatinine", "serum creatinine"],
        "units": {"mg/dl": 1, "umol/l": 0.0113},
        "ranges": {"male": (0.7, 1.3), "female": (0.6, 1.1)},
    },
    "uric_acid": {
        "name": "Uric Acid", "unit": "mg/dL",
        "aliases": ["uric acid", "serum uric acid"],
        "units": {"mg/dl": 1},
        "ranges": {"male": (3.4, 7.0), "female": (2.4, 6.0)},
    },
    "alt": {
        "name": "ALT (SGPT)", "unit": "U/L",
        "aliases": ["alt", "sgpt", "alt (sgpt)", "alanine aminotransferase"],
        "units": {"u/l": 1, "iu/l": 1},
        "ranges": {"any": (7.0, 56.0)},
    },
    "ast": {
        "name": "AST (SGOT)", "unit": "U/L",
        "aliases": ["ast", "sgot", "ast (sgot)", "aspartate aminotransferase"],
        "units": {"u/l": 1, "iu/l": 1},
        "ranges": {"any": (10.0, 40.0)},
    },
    "bilirubin_total": {
        "name": "Total Bilirubin", "unit": "mg/dL",
        "aliases": ["total bilirubin", "bilirubin total", "bilirubin"],
        "units": {"mg/dl": 1},
        "ranges": {"any": (0.3, 1.2)},
    },
    "sodium": {
        "name": "Sodium", "unit": "mmol/L",
        "aliases": ["sodium", "serum sodium", "na"],
        "units": {"mmol/l": 1, "meq/l": 1},
        "ranges": {"any": (135.0, 145.0)},
    },
    "potassium": {
        "name": "Potassium", "unit": "mmol/L",
        "aliases": ["potassium", "serum potassium", "k"],
        "units": {"mmol/l": 1, "meq/l": 1},
        "ranges": {"any": (3.5, 5.0)},
    },
    "calcium": {
        "name": "Calcium", "unit": "mg/dL",
        "aliases": ["calcium", "serum calcium", "total calcium"],
        "units": {"mg/dl": 1},
        "ranges": {"any": (8.6, 10.2)},
    },
}