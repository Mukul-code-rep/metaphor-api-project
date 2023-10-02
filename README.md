# metaphor-api-project
This project functions as an expansion to the existing endpoints of Metaphor AI's API. It introduces a new endpoint that enables users to search for documents with similar content to the one they upload.

## About the project
This project leverages various libraries and APIs to facilitate document search and similarity analysis. The primary goal is to enhance the capabilities of Metaphor AI's API by introducing a new endpoint that allows users to search for documents with content similar to the ones they upload.

### Result Class
- The `Result` class represents a search result, encapsulating essential information such as title, URL, ID, author, and published date. This class ensures a structured and comprehensive representation of each document.

### DocumentSearch Class
- The `DocumentSearch` class serves as the core component responsible for searching documents based on keywords and performing similarity analysis.
- **Initialization**: The class initializes by loading a spaCy model with a Textrank extension for text processing and incorporating the Metaphor API client using the provided API key.
- **Keyword Extraction**: The `keyword_extraction` method extracts keywords from the input text, employing `spaCy`'s `Textrank` to identify relevant phrases and removing stopwords for improved accuracy.
- **Search Documents from Keywords**: The `search_documents_from_keywords` method conducts a comprehensive search using Metaphor AI's API. It performs keyword searches, extracts relevant document details, `vectorizes` keywords and titles, employs `k-nearest neighbors` for similarity analysis, and ranks the results based on user preferences or defaults to the top 10.

### Integration with Flask
To enhance usability and provide a user interface for the document search functionality, the project includes a Flask web application. The Flask app incorporates the `DocumentSearch` class to expose an endpoint for users to perform document searches based on keywords extracted from input text.

### Flask App Functionality
**Endpoint (`/document_search`)**: The app defines a Flask route for the `/document_search` endpoint, accessible via HTTP POST requests.

 JSON Data Fields:
 - `text`: str (required) - the text of the document that needs to be parsed
 - `num_results`: int (optional)
 - `include_domains`: list[str] (optional)
 - `exclude_domains`: list[str] (optional)
 - `start_crawl_date`: str (optional)
 - `end_crawl_date`: str (optional)
 - `start_published_date`: str (optional)
 - `end_published_date`: str (optional)

## Dependencies
The project relies on several external libraries, including nltk, spacy, pytextrank, re, metaphor_python, scikit-learn, and a custom helper module with functions like `quick_sort` and `binary_search`.

## Installation and Environment
This project assumes the installation of python.

The dependencies for the project can be downloaded this command in the terminal:
```Bash
pip install -r requirements.txt
```

To configure a personalized Metaphor API key, users can modify the current `METAPHOR_KEY` value within the `config.env` file to store their unique API key. Subsequently, users can verify that the `METAPHOR_KEY` variable is correctly sourced from the `config.env` file by following these steps.
```Bash
set -a
source config.env
set +a
```

## Usage
To run the API, user can simply run the following command.
```Bash
python3 api.py
```
OR
```Bash
python api.py
```

To see a test example for the `DocumentSearch` class, user can run the following command.
```Bash
python3 document_search.py
```
OR
```Bash
python document_search.py
```

## Extensibility
The modular structure of the project allows for easy extensibility and integration with other APIs or functionalities. Users can customize the behavior by adjusting parameters and implementing additional features.

## Conclusion
This endeavor offers a resilient and adaptable solution for individuals looking to explore documents through keyword searches and conduct similarity analysis. The amalgamation of spaCy, the Metaphor API, and machine learning elements aims to deliver precise and effective outcomes.
