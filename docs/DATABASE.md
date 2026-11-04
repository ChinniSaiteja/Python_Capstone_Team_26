# Database Design – Team 26 (Waste Sorting & Recycling Assistant)

**Owner:** Ha Le Thu – Subsystem 4: Data Management & AI Guidance
**DBMS:** SQLite (default, nothing to install) or MySQL 8 - switch with `DB_ENGINE` in `.env`
**Schema:** `database/schema_sqlite.sql`, `database/schema_mysql.sql` (created automatically by `DatabaseManager.initialize()`)
**Rule:** all SQL lives in `database/db.py` (`DatabaseManager`). Other subsystems never write SQL – they call `DatabaseManager` methods.

---

## 1. Overview (8 tables)

```
waste_categories 1 ──< waste_items 1 ──< disposal_rules >── 0..1 admin_users
                            │
                            ├──< classifications 1 ── 0..1 user_feedback
                            │
                            └──< ai_guidance

ai_usage_log  (stand-alone, one row per day)
```

| # | Table | What it stores | Written by | Read by |
|---|-------|----------------|------------|---------|
| 1 | `admin_users` | Municipal staff accounts (hashed passwords) | Ha Le Thu (seed) | Backend (login) |
| 2 | `waste_categories` | recyclable / compostable / landfill | Ha Le Thu (seed, fixed) | Everyone |
| 3 | `waste_items` | Every label the classifier can return | Ha Le Thu (seed) | Backend |
| 4 | `disposal_rules` | Bin + instruction per item and region | Ha Le Thu (seed), admins | Backend → Web |
| 5 | `classifications` | One row per analysed photo (no image!) | Backend | Dashboard |
| 6 | `user_feedback` | "Wrong result?" answers | Backend | Dashboard, Classifier (evaluation) |
| 7 | `ai_guidance` | Cached OpenAI answers | Ha Le Thu (GuidanceService) | Backend → Web |
| 8 | `ai_usage_log` | OpenAI calls per day | Ha Le Thu (GuidanceService) | Ha Le Thu (daily limit) |

---

## 2. Tables in detail

### 1. `admin_users`
| Column | Type | Notes |
|---|---|---|
| id | INT PK | |
| username | VARCHAR(50) UNIQUE NOT NULL | |
| password_hash | VARCHAR(255) NOT NULL | e.g. `werkzeug.security.generate_password_hash` |
| region | VARCHAR(50) | region this admin manages, default `Dortmund` |
| created_at | DATETIME | |

### 2. `waste_categories`
| Column | Type | Notes |
|---|---|---|
| id | INT PK | |
| name | VARCHAR(20) UNIQUE | **only** `recyclable`, `compostable`, `landfill` |
| description | VARCHAR(255) | |

### 3. `waste_items`
| Column | Type | Notes |
|---|---|---|
| id | INT PK | |
| category_id | INT FK → waste_categories | |
| label | VARCHAR(100) UNIQUE | **must match the classifier label exactly** (lowercase, e.g. `glass jar`) |
| is_deposit | BOOLEAN | `TRUE` = Pfand bottle → return to store |

### 4. `disposal_rules`
| Column | Type | Notes |
|---|---|---|
| id | INT PK | |
| item_id | INT FK → waste_items | |
| region | VARCHAR(50) | MVP: only `Dortmund`; more cities = more rows, no code change |
| bin_type | VARCHAR(100) | e.g. `Glass container`, `Biotonne (brown bin)` |
| instruction | TEXT | short text shown to the user |
| updated_by | INT FK → admin_users, NULL | last admin who edited |
| updated_at | DATETIME | auto-updated |

Constraint: `UNIQUE (item_id, region)` → one rule per item per region.

### 5. `classifications`
| Column | Type | Notes |
|---|---|---|
| id | INT PK | |
| item_id | INT FK → waste_items, NULL | NULL when the label is not in our DB (→ OpenAI fallback) |
| predicted_label | VARCHAR(100) | raw label from the classifier |
| confidence | DECIMAL(5,4), NULL | 0–1 (e.g. `0.9200`), NULL if not available |
| status | VARCHAR(20) | `completed` / `uncertain` / `failed` |
| region | VARCHAR(50) | region selected by the user |
| created_at | DATETIME | |

Privacy: **no image or image path is stored**, only the result.

### 6. `user_feedback`
| Column | Type | Notes |
|---|---|---|
| id | INT PK | |
| classification_id | INT FK → classifications, UNIQUE | max 1 feedback per classification |
| is_correct | BOOLEAN | |
| correct_label | VARCHAR(100), NULL | filled when `is_correct = FALSE` |
| created_at | DATETIME | |

### 7. `ai_guidance`
| Column | Type | Notes |
|---|---|---|
| id | INT PK | |
| item_id | INT FK → waste_items | |
| question | VARCHAR(500), NULL | NULL = default explanation; text = user follow-up question |
| answer | TEXT | OpenAI answer (shown as "AI-generated") |
| created_at | DATETIME | |

Before calling OpenAI we check this table first (cache) → lower cost and faster.

### 8. `ai_usage_log`
| Column | Type | Notes |
|---|---|---|
| id | INT PK | |
| usage_date | DATE UNIQUE | |
| request_count | INT | +1 per OpenAI call; stop when daily limit is reached |

---

## 3. How other subsystems use the database

All access goes through `DatabaseManager` (and `GuidanceService` for AI).

| Who | Method | Returns |
|---|---|---|
| **Backend (Sai Teja)** | `get_rule(label, region="Dortmund")` | `{"label", "category", "is_deposit", "region", "bin_type", "instruction"}` or `None` |
| **Backend** | `save_classification(label, confidence, status, region)` | new `classification_id` |
| **Backend** | `save_feedback(classification_id, is_correct, correct_label=None)` | `None` |
| **Backend** | `GuidanceService.explain(label)` / `ask_ai(label, question)` | answer text (cached or from OpenAI) |
| **Dashboard (Kanika)** | `get_stats(region, date_from=None, date_to=None)` | see below |
| **Classifier (Azam)** | `get_all_items()` | list of the 72 known labels → classifier labels must match these |

### `get_stats()` result (for Plotly charts)
```json
{
  "total_items": 124,
  "by_category": {"recyclable": 80, "compostable": 30, "landfill": 14},
  "recycling_rate": 0.645,
  "per_day": [{"date": "2026-11-04", "count": 12}],
  "uncertain_count": 9,
  "wrong_feedback_count": 5
}
```

### Example SQL behind it
```sql
-- items per category
SELECT c.name, COUNT(*) AS total
FROM classifications cl
JOIN waste_items w      ON w.id = cl.item_id
JOIN waste_categories c ON c.id = w.category_id
WHERE cl.region = 'Dortmund'
GROUP BY c.name;

-- items per day
SELECT DATE(created_at) AS day, COUNT(*) AS total
FROM classifications
WHERE region = 'Dortmund'
GROUP BY DATE(created_at)
ORDER BY day;
```

---

## 4. Agreements we need from the team

1. **Azam:** send the final list of classifier labels (lowercase, English). Each label must exist in `waste_items`.
2. **Sai Teja:** confidence is sent as a float 0–1 (not 0–100); status is one of `completed / uncertain / failed`.
3. **Kanika:** dashboard uses only the `get_stats()` JSON above – tell Ha if you need another chart.
4. **Everyone:** DB password and OpenAI key go in `.env` (never pushed to GitHub).

---

## 5. Quick start for teammates

```bash
pip install -r requirements.txt
cp .env.example .env          # default DB_ENGINE=sqlite -> nothing else to set up
python demo_data_management.py                # creates the database and loads 72 Dortmund rules
```

In your own code:
```python
from database.db import DatabaseManager
db = DatabaseManager()
db.initialize()                                   # safe to call every start
db.get_rule("glass jar")                          # disposal guidance
db.save_classification("glass jar", 0.92)         # returns classification_id
db.get_stats("Dortmund")                          # dashboard data
```
No manual SQL import is needed - tables and data are created automatically.

---

## 6. Optional: setting up MySQL locally

Each team member uses their **own** MySQL user and password on their own machine (never shared, never committed).

Run once as `root` (terminal `mysql -u root -p` or DBeaver SQL editor, one statement at a time):
```sql
CREATE DATABASE IF NOT EXISTS waste_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'waste_user'@'localhost' IDENTIFIED BY 'YourPassword1!';
GRANT ALL PRIVILEGES ON waste_db.* TO 'waste_user'@'localhost';
SHOW GRANTS FOR 'waste_user'@'localhost';
```
Password tips: MySQL may require 8+ characters with upper case, lower case, a number and a special character. Avoid `#`, spaces and quotes (they break `.env`).

Then in your `.env`:
```
DB_ENGINE=mysql
DB_USER=waste_user
DB_PASSWORD=YourPassword1!
DB_NAME=waste_db
```
Run `python demo_data_management.py` - tables and the 72 rules are created automatically.

DBeaver tip: if you get `Public Key Retrieval is not allowed`, set `allowPublicKeyRetrieval=true` and `useSSL=false` in *Driver properties*.
