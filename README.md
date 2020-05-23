# TextScraping
# 5/23/2020
# Use at your own risk

Implementation of Google's Cloud Vision API to data scrape text fields from screencaptures

# This is prototype code and not a complete solution

There are two python scripts ValorantVision.py, which is used to generate a .CSV file containing extracted text from screen shots, 
and ValorantPlotter.py, which plots a few figures of interest.

At miniumum two edits must be completed for this code to function:

1) A google cloud vision API credentials file needs to be present in the same directory and referenced in the ValorantVision.py script (line 59)
2) The username whose data you attempting to scrape must be edited in the the ValorantVision.py script (line 8)

