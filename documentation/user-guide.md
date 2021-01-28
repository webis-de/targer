# User guide

## Frontend

After installation, the frontend web interface can be accessed.
It consists of two parts: [Analyze](#analyze-tab) and [Search](#search-tab).

### Analyze tab

In the Analyze tab, a document can be classified.
Enter the text into the text field, select annotations you want to display on the right side and click on the "Analyze" button.
The text will then be processed in two steps:

1. Entities are tagged by spaCy's entity tagger.
2. Arguments structure is tagged by the TARGER [backend](#backend).

After annotation, the text will be highlighted with annotations below the text field.

### Search tab

From the Search tab, you can search the document database for arguments.
Adjust the minimum confidence with the slider.
If you click on a search snippet, the text can be analyzed in the Analyze tab.

## Backend

After installation, you can use the REST-like API endpoints or access the Swagger API documentation at the `/apidocs` subpath.
