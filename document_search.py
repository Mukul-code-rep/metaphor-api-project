# Package imports

import nltk
import spacy
import pytextrank
import re
from metaphor_python import Metaphor
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
import os
from helper import quick_sort, binary_search

# nltk.download("stopwords")


class Result:
    """
        Class representing a search result.

        Attributes:
            title (str): Title of the document.
            url (str): URL of the document.
            id (str): ID of the document.
            author (str): Author of the document.
            published_date (str): Published date of the document.
    """

    def __init__(self, title: str, url: str, id: str, author: str | None, published_date: str | None) -> None:
        """
            Initialize a Result object.

            Args:
                title (str): Title of the document.
                url (str): URL of the document.
                id (str): ID of the document.
                author (str, optional): Author of the document. Defaults to None.
                published_date (str, optional): Published date of the document. Defaults to None.
        """
        self.__title = title
        self.__url = url
        self.__id = id
        self.__author = author
        self.__published_date = published_date

    def __str__(self) -> str:
        """
            String representation of the Result object.

            Returns:
                str: String representation.
        """
        result = f"Title: {self.__title}\nURL: {self.__url}\nid: {self.__id}\n"
        if self.__author:
            result += f"Author: {self.__author}\n"
        if self.__published_date:
            result += f"Published Date: {self.__published_date[:10]}\n"
        return result


class DocumentSearch:
    """
        Class for searching documents based on keywords and performing similarity analysis.
    """
    def __init__(self) -> None:
        """
            Initialize a DocumentSearch object.
        """
        # Load spaCy model with textrank extension
        self.__model = spacy.load("en_core_web_sm")
        self.__model.add_pipe("textrank")

        # Initialize Metaphor API client
        self.__metaphor = Metaphor(os.environ.get("METAPHOR_KEY"))

    def keyword_extraction(self, text: str) -> list[str]:
        """
            Extract keywords from the input text.

            Args:
                text (str): Input text.

            Returns:
                list[str]: List of extracted keywords.
        """
        text = text.replace("\n", " ").lower()
        
        try:
            stopwords = nltk.corpus.stopwords.words('english')
        except:
            pass
        else:
            text_list = text.split(" ")
            quick_sort(stopwords, 0, len(stopwords)-1)

            # Remove stopwords
            for i in range(len(text_list)-1, -1, -1):
                if binary_search(stopwords, text_list[i]) == 0:
                    text_list.pop(i)
            text = " ".join(text_list)

        # Use spaCy textrank to extract phrases
        results = self.__model(text)._.phrases
        keywords = [result.text for result in results]
        return keywords

    def search_documents_from_keywords(self, text: str, **kwargs) -> str:
        """
            Search for documents based on keywords and perform similarity analysis.

            Args:
                text (str): Input text.
                **kwargs: Additional keyword arguments passed to the Metaphor API.

            Returns:
                str: String representation of the search results.
        """

        # Extract keywords from the input text
        keywords = self.keyword_extraction(text)

        results, titles = {}, []

        # Perform a keyword search using Metaphor API with additional keyword arguments
        for keyword in keywords:
            result = self.__metaphor.search(keyword, type='keyword', **kwargs).results
            for res in result:
                results[re.compile(r'<[^>]+>').sub('', res.title)] = {
                                "url": res.url,
                                "author": res.author,
                                "published_date": res.published_date,
                                "id": res.id
                }
                titles.append(re.compile(r'<[^>]+>').sub('', res.title))

        # Vectorize keywords and titles
        vectorizer = TfidfVectorizer()
        keywords_encoded = vectorizer.fit_transform(keywords)
        titles_encoded = vectorizer.transform(titles)

        # Use k-nearest neighbors for similarity analysis
        knn = NearestNeighbors(n_neighbors=len(keywords), metric='cosine')
        knn.fit(keywords_encoded)

        similarities, indices = knn.kneighbors(titles_encoded)

        # Create a list of tuples containing sum of similarities and index
        ranking_list = [(sum(similarities[i]), i) for i in range(len(similarities))]
        quick_sort(ranking_list, 0, len(ranking_list)-1, modify=True)

        # Limit the number of results based on user-specified preference or default to top 10
        if "num_results" in kwargs:
            ranking_list = ranking_list[:kwargs["num_results"]]
        else:
            ranking_list = ranking_list[:10]

        # Create Result objects for top ranking results
        ranking_results = []
        for elem in ranking_list:
            title = titles[elem[1]]
            ranking_results.append(
                Result(
                    title=title,
                    url=results[title]['url'],
                    id=results[title]['id'],
                    author=results[title]['author'],
                    published_date=results[title]['published_date']
                )
            )

        # Generate a string representation of the search results
        similar_docs = ""
        for item in ranking_results:
            similar_docs += item.__str__() + "\n"

        return similar_docs


def main():
    # Example usage
    doc_search = DocumentSearch()
    input_text = "IBM, or International Business Machines Corporation, is a globally renowned technology and consulting company. Founded in 1911, IBM has played a pivotal role in shaping the information technology industry. The company is headquartered in Armonk, New York, and operates in over 170 countries.\
\
IBM is recognized for its innovation and has a rich history of contributing to technological advancements. From the development of the first hard disk drive to the creation of the iconic IBM mainframe and the introduction of the personal computer, IBM has consistently been at the forefront of technological progress.\
\
The company's commitment to research and development is evident through its many patents and breakthroughs. IBM has been a leader in artificial intelligence (AI), cloud computing, and quantum computing. Watson, IBM's AI platform, has gained fame for its capabilities in natural language processing, machine learning, and data analytics.\
\
In addition to its technological prowess, IBM is a major player in the business and technology consulting space. The company provides a wide range of services, including IT infrastructure services, software development, and business strategy consulting, making it a trusted partner for organizations seeking digital transformation.\
\
IBM's dedication to corporate responsibility is reflected in its initiatives for environmental sustainability, diversity and inclusion, and community engagement. The company emphasizes ethical business practices and is committed to creating a positive impact on society.\
\
With a legacy spanning over a century, IBM continues to evolve and adapt to the ever-changing landscape of technology. As a global leader, IBM remains a symbol of innovation, reliability, and forward-thinking in the world of information technology."

    result = doc_search.search_documents_from_keywords(input_text)
    print(result)


if __name__ == "__main__":
    main()
