# jayne

A plagiarism detector for thugs.

Extracts text from PDF files, compares contents, and outputs a similarity score. Optionally outputs a list of passages exhibiting the greatest similarity.

## REQUIREMENTS

Tested on python 3.6. Other versions may work. Deviate from this at your own peril.

Needs the following packages:

 - fuzzywuzzy
 - nltk
 - PyPDF2
 - python-Levenshtein
 - singledispatch
 - six

(or just install `requirements.txt`)

## USAGE

Try
```
python3 jayne -d=pdfdir
```
where `pdfdir` holds some PDFs.

## TODO:

 - Give more detailed results
 - Concurrency
 - Analyze similarity in a way that is not completely idiotic
