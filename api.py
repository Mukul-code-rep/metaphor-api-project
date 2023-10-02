from flask import Flask, request, jsonify
from document_search import DocumentSearch

app = Flask(__name__)


@app.route("/document_search", methods=["POST"])
def document_search():
    """
        Endpoint to perform a document search based on keywords extracted from the input text.

        Returns:
            str: String representation of search results.
    """
    try:
        # Extract the 'text' field from the JSON data received in the request
        data = dict(request.json)
        text = data["text"]

        # Remove the 'text' field from the dictionary to isolate other data
        del data["text"]
    except KeyError:
        # Handle the case where text is not present in the request data
        return jsonify({'error': 'Missing or incorrect input'}), 400
    else:
        # Create an instance of DocumentSearch
        search = DocumentSearch()

        # Perform document search and get results
        results = search.search_documents_from_keywords(text, **data)

        # Return the results with a 200 OK status
        return results, 200


if __name__ == "__main__":
    # Run the Flask app on port 5010 in debug mode
    app.run(port=5010, debug=True)