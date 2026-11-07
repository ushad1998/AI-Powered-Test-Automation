# AI-Powered Test Automation

## Project Overview

AI-Powered Test Automation is a Python-based tool that converts plain-English test instructions into automated browser tests.

The application uses Google Gemini to understand a user's test instruction and generate a structured test plan. It then validates that plan and executes the steps in a real browser using Playwright.

At the end, it displays whether the test passed or failed.

## Technologies Used

- **Python 3.12** – Main programming language
- **Google Gemini API** – Converts natural-language instructions into structured test steps
- **Playwright** – Automates browser interactions
- **Pydantic** – Validates generated test plans
- **python-dotenv** – Loads API credentials from environment variables

## ScreenShots
<img src="screenshots/Screenshot%20(128).png" alt="Project Screenshot" width="800">
<img src="screenshots/Screenshot%20(130).png" alt="Project Screenshot" width="800">
<img src="screenshots/Screenshot%20(133).png" alt="Project Screenshot" width="800">
<img src="screenshots/Screenshot%20(134).png" alt="Project Screenshot" width="800">
<img src="screenshots/Screenshot%20(135).png" alt="Project Screenshot" width="800">

## How It Works

1. The user enters a test instruction in plain English.
2. Gemini analyzes the instruction and generates a structured test plan.
3. Pydantic validates the generated test plan.
4. Playwright opens the browser and executes the steps.
5. The application reports the execution status as PASS or FAIL.

### Architecture

```text
Plain-English Test Instruction
              |
              v
       Gemini AI Planner
              |
              v
      Structured Test Plan
              |
              v
      Pydantic Validation
              |
              v
     Playwright Execution
              |
              v
       Test Result Report
          PASS / FAIL
```

## Project Structure

```text
ai-powered-test-automation/
│
├── config/
│   └── settings.py
│
├── src/
│   ├── __init__.py
│   ├── ai_planner.py
│   ├── browser_executor.py
│   ├── element_finder.py
│   ├── test_schema.py
│   ├── reporter.py
│   └── main.py
│
├── tests/
│   └── test_runner.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd ai-powered-test-automation
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Install Playwright browser

```bash
playwright install chromium
```

## Gemini API Configuration

Create a `.env` file in the project root directory.

Add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key
```

The application uses `gemini-2.5-flash` by default.

**Important:** Never upload your `.env` file or expose your API key on GitHub.

## Running the Application

From the project root directory, run:

```bash
python -m src.main
```

Enter a natural-language test instruction when prompted.

## Example Test Instructions

### Example 1: Verify a website title

```text
Open https://phptravels.com/demo and verify that the page title contains PHPTRAVELS.
```

### Example 2: Verify visible page content

```text
Open https://example.com and verify that the page contains the text Example Domain.
```

### Example 3: Test a form

```text
Open https://www.selenium.dev/selenium/web/web-form.html, enter "CloudQA test" into the field labeled "Text input", click the button named "Submit", and verify that the page contains the text "Received!".
```

## Supported Browser Actions

The current implementation supports:

- `navigate` – Open a website URL.
- `click` – Click an element.
- `fill` – Enter text into an input field.
- `assert_text` – Verify that expected text is visible.
- `assert_title` – Verify the browser page title.
- `wait` – Wait for a specified duration.

Element identification currently supports role, label, placeholder, text, test ID, and CSS selectors.

## Test Results

The application displays:

- Generated test plan
- Individual step execution results
- Actual page title or verification details where applicable
- Final PASS or FAIL status

## Approach and Design Decisions

The application uses AI to interpret natural-language instructions and generate structured test steps rather than generating executable Python code.

This separates test planning from browser execution. Pydantic validates the generated actions before Playwright executes them, helping prevent invalid or unsupported actions from reaching the browser executor.

The browser automation logic is handled by Python and Playwright, keeping execution controlled by the application.

## Limitations

- The tool currently supports a limited set of browser actions.
- Ambiguous or incomplete instructions may produce an incorrect test plan.
- Dynamic websites may require more specific element identification.
- Some websites may block automated browser access.
- Login flows requiring credentials are not automatically configured.
- Gemini API availability, rate limits, and network connectivity can affect test generation.
- The tool does not guarantee successful automation for every website or natural-language instruction.

## Future Improvements

- Support additional browser actions.
- Improve element identification and recovery.
- Generate detailed execution reports.
- Add screenshot capture for failed steps.
- Expand automated test coverage.
- Support additional browser types.

## Security

API credentials are stored in a local `.env` file and should be excluded from version control using `.gitignore`.
