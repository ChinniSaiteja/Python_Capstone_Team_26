# AI-assisted Waste Sorting & Recycling Assistant

## 1. Team Overview

### Project

The project aims to support waste sorting and recycling by using an AI-based image classification system to identify waste items and provide appropriate disposal guidance for the Dortmund region.

### Team Members and Responsibilities

| Team Member | Subsystem | Main Responsibility |
|---|---|---|
|  Kanika Sehgal  | Web Interface | Develops the user interface for image upload, classification results, and disposal guidance. |
| Azam Rahmani    | ML / Image Classification | Develops and integrates the image classification model for identifying waste items. |
| Sai Teja Chinni | Backend & Application Integration | Connects the classifier, data management, and guidance components and prepares structured responses for the frontend. |
| Ha Le Thu       | Data Management & AI Guidance | Manages waste-related data and database operations and provides AI-assisted disposal guidance. |


## 2. System Design

### Overall System Architecture
    ```text
                         ┌─────────────────────┐
                         │    Web Interface    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Flask Backend    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  ML Classification  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                  ┌─────────────────────────────────┐
                  │ Backend & Application Integration│
                  └───────────────┬─────────────────┘
                                  │
                                  ▼
                  ┌─────────────────────────────────┐
                  │ Data Management & AI Guidance   │
                  └───────────────┬─────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                           ▼
              ┌───────────┐              ┌────────────┐
              │  Database │              │ OpenAI API │
              └───────────┘              └────────────┘
    ```

## Subsystem 1 - Frontend Interface (Kanika Sehgal)




## Subsystem 2 - Backend & Application Integration (Sai Teja Chinni)

The Backend & Application Integration subsystem connects the waste classification result with the data management and guidance components and prepares a consistent response for the frontend.

#### Implemented Classes

| Class | Responsibility |
|---|---|
| `ClassificationResultHandler` | Validates and normalizes the classification result received from the ML classifier. It handles the waste label, confidence, status, and region. |
| `GuidanceService` | Retrieves disposal guidance using the classified waste label and region and saves the classification result through the existing `DatabaseManager`. |
| `ResponseComposer` | Combines the classification result and disposal guidance into a structured API response for the frontend. |

#### UML Class Diagram

![Backend & Application Integration Class Diagram](docs/class_diagram_backend.png)

#### Backend Flow

```text
ML Classifier
      ↓
ClassificationResultHandler
      ↓
GuidanceService
      ↓
DatabaseManager
      ↓
ResponseComposer
      ↓
Frontend
```

The backend uses **Dortmund as the default region** and normalizes classification labels before processing them.

The subsystem is designed as a separate application-integration layer so that the classification logic, data management, and frontend communication remain loosely coupled.

#### Class Responsibilities

**ClassificationResultHandler**
- Validates the classifier output.
- Normalizes the waste label.
- Validates confidence values.
- Handles classification status.
- Applies the default region (`Dortmund`).

**GuidanceService**
- Uses the existing `DatabaseManager`.
- Retrieves disposal guidance based on waste label and region.
- Stores classification results.
- Coordinates the classification and guidance processing flow.

**ResponseComposer**
- Creates a stable response structure for the frontend.
- Includes classification information, disposal guidance, region, status, and classification ID.
- Keeps the frontend response format independent from the internal database implementation.

#### Testing

The backend integration subsystem is covered by automated tests in:

```text
tests/test_backend_integration.py
```

The current test suite contains 11 tests, covering validation, guidance retrieval, classification storage, response composition, and the complete backend integration flow.


## Subsystem 3 - Image Classifier Model (Azam Rahmani)
 




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

