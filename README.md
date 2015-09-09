cloacina
=======

Tools for downloading from the LexisNexis API

Currently, `cloacina` includes high-level interfaces for several LexisNexis
endpoint and operations, including:

- authentication

- getting the number of results available for a given source for a given day

- downloading and formatting all articles for a given source for a given day


Usage
-----

Run a test to download some days of BBC Monitoring articles like this:
`python bbc_test_download.py`

To modify the sources and dates downloaded, modify the `source_list.csv` file,
which is actually a tab-delimited file with source\tstartdate\tenddate.

If you're a memeber of the Open Event Data Alliance, get in touch with me for
the test username/password.
