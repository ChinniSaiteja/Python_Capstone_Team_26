# Python_Capstone_Team_26
AI-powered Waste Sorting &amp; Recycling Assistant

## Subsystem 4 - Data Management & AI Guidance (Ha Le Thu)

**Classes (Home Assignment 1):** `database/models.py`

| Class | Table | Responsibility |
|---|---|---|
| `WasteCategory` | `waste_categories` | recyclable / compostable / landfill (validated in setter) |
| `WasteItem` | `waste_items` | one label the classifier can return, with Pfand flag |
| `DisposalRule` | `disposal_rules` | bin type + instruction per item and region (Dortmund) |
| `DatabaseManager` | all tables | `database/db.py` - the only place with SQL |

Each class has a constructor (`__init__`), initialisation methods (`from_dict()`, `to_dict()`, `initialize()`) and encapsulation (private attributes with `@property` getters and setters that validate input).

**Data:** `data/waste_guidance.json` - 72 Dortmund disposal rules (source: EDG Entsorgung Dortmund).
**Database design:** see [docs/DATABASE.md](docs/DATABASE.md).

