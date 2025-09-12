Zotero Migration:
·       Pyzotero library tested with API calls to understand how the initial portion of the script would work at the scale intended for the final application.
·       Google Drive and Github API calls tested to see how uploads can be managed programmatically for migrating the Zotero Library items to both Google Drive for data redundancy.
·       Combined concepts from the testing to write a Python script to download files from the Zotero library using API calls.
·       Script updated to generate statistics and logs relevant to the process so that the user can keep track of progress.
·       Many files went undetected due to not being top level items.
·       Script updated to look for child items as well. The number of items detected increased but still less than the expected number.
·       Script updated to have exponentially increased rate limits alongside a retrying mechanism. Files detection increased, but the range was below expectations.
·       Script updated further to perform webscraping techniques to look for any links that directly lead to PDFs. The number of files detected increased but still less than the expected number.
·       Script updated further to take HTML snapshots to ensure that there is some record of what may have gone wrong when a PDF fails to download due to reasons such as restricted access, for example. Number of PDFs below expected range.
·       Script updated further to create JSON files relevant to each Zotero library item so there is at least a record of the file, even when both the PDF download and HTML snapshot may fail. Number of PDFs detected unchanged from last update (below expected range).
·       Script updated to include a manifest of the entire process upon completion. Number of PDFs detected unchanged from last update (below expected range).
Conclusion from the points above: The script is best suited for Zotero libraries wherein PDFs are top level items stored directly in the online Zotero Library.
 
·       Approach changed due to exhausting multiple API-based options and not getting desired results: syncing the library locally to the user’s device and running a script to extract the PDFs from the directory containing all the Zotero-related data obtained from the sync.
·       Uploaded the files to Google Drive (All 1948 PDFs successfully obtained; Expected number matched).
Overall conclusion for the Zotero migration project: Successfully completed.
Mineru Reading:
·       Very limited documentation for Python due to the project being very new and under development.
·       The only proper reference to Python: demo.py.
·       Running the demo.py file locally without the entire repository being cloned over was not possible despite all the prerequisite installations performed.
·       Cloned repository to VS Code workspace.
·       Prerequisites installed.
·       Attempted to increase performance using CUDA (CPU-based processing for PyTorch is slower than it would be on CUDA-enabled GPUs; Essentially PyTorch models run faster on GPUs with a CUDA version that is 11.9+)
·       Project started running but failed after processing 5/1948 PDFs that were obtained from the Zotero Library due to the project’s inability to batch process properly.
·       Updated demo.py to support the processing of many files sequentially.
·       1927 PDFs successfully processed and translated into a series of table/graph screenshots, JSON files, annotated PDFs and Markdown files.  21 failed due to running into issues with Mineru’s pdfium2 dependency (may happen when a file is incompatible or corrupted).
·       The output folder came out to be around 14 GB.
·       To efficiently use storage, the Markdown files were separated using a script since the Markdown files contain plain text, which is relevant for reading PDFs into chatbots. The separated folder contains 1927 Markdown files with a size of ~167 MB.
 
Overall conclusion for the Mineru Reading project: Successfully set up reading, but integration into the Bytewise chatbot remains.
 
Bytewise Module:
Working on using OpenRouter to get responses from LLMs by sending text extracted from Markdown files after uploading a PDF on the “Review Mode” tab.


Saving the generated points and associated Markdown file of the overall text extracted from the PDF in a database. The items can be accessed via a “Database” tab.


Enabling the usage of the “Write New” tab so that the user can send a prompt and the papers from the database can be consulted according to their relevancy for generating a discussion. Follow-up questions relevant to the discussion can be sent to be evaluated by the LLM via OpenRouter. Follow-up feature still in development.


Adapting the code for Git Codespaces to enable online testing and development on GitHub. Issues with memory usage due to the limited resources on the free tier of Git CodeSpaces (Applied for Student Benefits on 14th August, 2025).
