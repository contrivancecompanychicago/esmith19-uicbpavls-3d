"""SQLite-backed integration for diabetes XR research data."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional


DB_PATH = Path(__file__).resolve().parent.parent / "data" / "diabetes_xr.db"


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS diabetes_analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT,
            device TEXT,
            focus TEXT,
            risk_index REAL,
            glucose_mg_dL REAL,
            hba1c_pct REAL,
            insulin_resistance_index REAL,
            inflammatory_load REAL,
            beta_cell_stress REAL,
            pathway_summary TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def save_analysis(payload: Dict[str, Any], profile: Dict[str, Any]) -> Dict[str, Any]:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    payload_data = payload or {}
    conn.execute(
        """
        INSERT INTO diabetes_analyses (
            patient_id,
            device,
            focus,
            risk_index,
            glucose_mg_dL,
            hba1c_pct,
            insulin_resistance_index,
            inflammatory_load,
            beta_cell_stress,
            pathway_summary
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            profile.get("patient_id") or payload_data.get("patient_id") or "T2D-001",
            profile.get("device") or "Samsung XR",
            profile.get("focus") or "Molecular basis of diabetes disease research",
            float(profile.get("risk_index") or 0.0),
            float(payload_data.get("glucose_mg_dL") or 0.0),
            float(payload_data.get("hba1c_pct") or 0.0),
            float(payload_data.get("insulin_resistance_index") or 0.0),
            float(payload_data.get("inflammatory_load") or 0.0),
            float(payload_data.get("beta_cell_stress") or 0.0),
            json.dumps(profile.get("signals") or [], ensure_ascii=False),
        ),
    )
    conn.commit()
    row_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return {"id": row_id, "status": "saved"}


def get_recent_analyses(limit: int = 10) -> List[Dict[str, Any]]:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute(
        """
        SELECT id, patient_id, device, focus, risk_index, glucose_mg_dL, hba1c_pct,
               insulin_resistance_index, inflammatory_load, beta_cell_stress,
               pathway_summary, created_at
        FROM diabetes_analyses ORDER BY id DESC LIMIT ?
        """,
        (limit,),
    )
    rows = cursor.fetchall()
    conn.close()

    records = []
    for row in rows:
        records.append(
            {
                "id": row[0],
                "patient_id": row[1],
                "device": row[2],
                "focus": row[3],
                "risk_index": row[4],
                "glucose_mg_dL": row[5],
                "hba1c_pct": row[6],
                "insulin_resistance_index": row[7],
                "inflammatory_load": row[8],
                "beta_cell_stress": row[9],
                "pathway_summary": json.loads(row[10]) if row[10] else [],
                "created_at": row[11],
            }
        )
    return records
