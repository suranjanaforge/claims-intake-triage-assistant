# ClaimPilot – AI-Powered Claims Intake & Triage Assistant

An AI-assisted insurance claims intake and triage application designed to streamline the initial claim review process through structured information extraction, document comparison, missing-information detection and discrepancy identification.

## Overview

Processing insurance claims often involves reviewing unstructured descriptions, checking supporting documents, identifying missing information and verifying whether the details provided across different sources are consistent.

**ClaimPilot** aims to simplify this initial process by providing a centralised workspace where users can submit claim information, analyse supporting documents and review an organised triage summary.

The application uses Google's Gemini API to assist with claim analysis and presents the results through an interactive Streamlit interface.

It is designed as a decision-support tool for human reviewers, not as an automated claim approval or rejection system.

## Key Features

### 1. Claim Information Intake
- Accepts natural-language descriptions of insurance incidents.
- Provides a structured workspace for entering claim information.
- Supports the use of sample claims for demonstration and testing.

### 2. Supporting Document Analysis
- Demonstrates claim analysis using supporting sample documents.
- Uses document information alongside the claim description.
- Helps compare details across different sources.

### 3. AI-Assisted Claim Classification
- Analyses the submitted claim and identifies its likely category.
- Supports categories such as:
  - Motor Insurance
  - Health Insurance
  - Property Insurance
  - Travel Insurance
  - Other / Unknown

### 4. Structured Information Extraction
Organises relevant information into structured fields, such as:
- Claimant details
- Policy information
- Incident date and time
- Incident location
- Vehicle or asset identification
- Incident description

### 5. Missing Information Detection
Identifies information that may be required for further claim processing and highlights potential gaps in the submitted details.

### 6. Discrepancy Identification
Compares information available across the claim description and supporting documents to identify possible inconsistencies, such as conflicting incident dates.

### 7. Triage Summary
Presents an organised overview of the analysis, including:
- Claim classification
- Extracted information
- Missing information
- Potential conflicts
- Recommended next steps

### 8. Human Review Support
Keeps the final assessment with a human reviewer. AI-generated findings are intended to assist investigation and verification rather than replace professional judgement.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive web application and user interface |
| Google Gemini API | AI-assisted claim analysis |
| Google Gen AI SDK | Communication with Gemini models |
| HTML / CSS | Interface styling and visual customisation |
| JSON | Structured data and evaluation records |
| Git & GitHub | Version control and project management |

## Application Workflow

The application follows a simple claims-intake workflow:

1. **Input:** The user provides a claim description.
2. **Document Collection:** Supporting information or sample documents are made available.
3. **Analysis:** The application processes the available claim information using the configured Gemini model.
4. **Extraction:** Relevant claim details are organised into structured fields.
5. **Validation:** Missing information and potential inconsistencies are identified.
6. **Triage:** A structured summary and recommended follow-up actions are presented.
7. **Human Review:** A reviewer examines the results and determines the appropriate next steps.

## Project Structure

```text
ClaimPilot/
│
├── app.py
│   └── Main Streamlit application
│
├── style.css
│   └── Custom application styling
│
├── evaluate.py
│   └── Evaluation script
│
├── sample_claims.json
│   └── Synthetic sample claim dataset
│
├── evaluation_results.json
│   └── Sample evaluation results
│
├── failure_cases.md
│   └── Documented limitations and failure scenarios
│
├── input_output_schema.json
│   └── Input and output structure
│
├── prompt_experiments.json
│   └── Prompt experimentation notes
│
├── requirements.txt
│   └── Python dependencies
│
├── .gitignore
│   └── Files excluded from version control
│
└── README.md
    └── Project documentation
```

*The project structure may be updated as additional features are introduced.*

## Installation and Setup

Follow these steps to run ClaimPilot locally.

### Prerequisites

- Python 3.10 or later
- Git
- A Google Gemini API key
- Visual Studio Code (recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/suranjanaforge/claims-intake-triage-assistant.git
```

Navigate into the project directory:

```bash
cd YOUR-REPOSITORY
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API Key

Create a folder named `.streamlit` in the project directory.

Inside it, create a file named `secrets.toml`:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Replace the placeholder with your actual API key.

**Important:** Never commit your API key, `.env` file or `secrets.toml` to GitHub.

### 5. Run the Application

```bash
python -m streamlit run app.py
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

## Evaluation and Testing

The project includes a small synthetic dataset and an evaluation script to assess selected claim-analysis behaviours.

The evaluation resources include:

- `sample_claims.json` – Synthetic test cases.
- `evaluate.py` – Script used to run the evaluation.
- `evaluation_results.json` – Recorded evaluation results.
- `failure_cases.md` – Known limitations and documented failure scenarios.

The evaluation focuses on claim-type classification and conflict detection.

These results are intended as preliminary testing and should not be interpreted as production-level performance benchmarks.

## Limitations and Future Improvements

ClaimPilot is a demonstration-stage application. Some areas that can be improved include:

- More comprehensive document parsing and OCR support.
- Improved extraction from varied document formats.
- Detection of inconsistencies across additional claim fields.
- Better handling of ambiguous and relative dates.
- Expanded labelled datasets for more reliable evaluation.
- More detailed field-level evidence tracing.
- User authentication and role-based access.
- Audit logs and reviewer feedback mechanisms.
- Improved error handling and model fallback mechanisms.

## Responsible AI and Data Privacy

ClaimPilot is designed to support human decision-making.

- Synthetic data should be used for demonstrations and testing.
- Real customer information should not be entered into an unsecured demonstration environment.
- AI-generated classifications and extracted information must be verified.
- Potential discrepancies should be treated as review flags, not proof of fraud.
- The application does not make final decisions regarding claim approval, rejection, liability, fraud, policy coverage or payouts.

## Project Objective

The objective of ClaimPilot is to demonstrate how AI-assisted information extraction, structured data processing and discrepancy identification can improve the initial stages of insurance claims handling.

By bringing claim information and supporting evidence into one organised interface, the project aims to make preliminary claim review more efficient, transparent and easier to manage.

---

**Developed as an academic project in Artificial Intelligence and Software Development.**

*ClaimPilot – Making Claims Intake More Structured, Transparent and Efficient.*
