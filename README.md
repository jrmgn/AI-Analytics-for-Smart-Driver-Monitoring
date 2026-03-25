This activity was developed to provide an automated, AI-driven oversight tool for fleet management. It integrates three core AI domains, Telematics Analytics, Natural Language Processing (NLP), and Optical Character Recognition (OCR), into a centralized Streamlit dashboard. The goal is to help fleet managers monitor driver performance, analyze passenger feedbacks, and verify driver licenses in one place.

Key Features
1. Driver Telemetry & Risk Analytics
Analyzes raw driving data (acceleration, braking, speeding).
Generates a Risk Score for each driver to identify safety trends.
Visualizes data using interactive bar charts and highlighted dataframes.

2. Passenger Feedback Sentiment
Uses TextBlob to analyze the emotional tone of passenger comments.
Features a Hybrid Logic system: Even if the AI score is slightly positive, it uses "Safety Keyword Flagging" (speeding, unsafe) to alert managers to critical issues.
Includes a Neutral Zone to flag ambiguous reviews for manual human review.

3. License Verification & Forgery Detection
Uses OpenCV and Tesseract OCR to extract text from license scans.
Implements a two-step verification process:
  Regex Pattern Matching: Checks for a valid ID format (ABC-1234).
  Header Detection: Requires the document to explicitly contain the words "DRIVER LICENSE."
