[[Muhammad Ahmad Nadeem]] 

[[Bytewise Chatbot platform]]

 this module is part of the initiative to develop [[AI assisted research writing tool]] 

#deadline #toSchedule 

- find the timesheet 
- learn how his codes work 
- get the codes and import them into my github repo 
- try testing and developing a bit 
- consider how these two moduels 
	- PDF2MD and Zotero read and write could be integrated into workflow for research writing assistance 

Hi Ahmad 



  

Thanks for your notes. What could you deliver online? There are different options when it comes to server space.  I think it would make sense to process your timesheet after we can see something working online. I remembered you did some coding on Zotero as well - can you share the GitHub folder and send me a summary of the work. 


Cheers

Simon


Bytewise PDF2MD_ORBS_Unified GitHub Repository 

This document outlines the functionality of the module found in this repository. In “PDF2MD_ORBS_Unified/backend/mineru/”, there is a file named “main.py”. This file contains the code for the backend. This backend is a unified version of the ORBS Grader backend and the backend of the Research Assistant. It serves two different frontends. One of the frontends can be found here: “PDF2MD_ORBS_Unified/frontend/notebook/index.html”. This frontend is for the ORBS Grader. The other frontend can be found here: “PDF2MD_ORBS_Unified/frontend/research/index.html”. This frontend is for the Bytewise Research Assistant. Moreover, there is also another HTML file that serves as the landing page on which you find two buttons leading to both the ORBS Grader frontend, as well as the Bytewise Research Assistant frontend. It can be found at: “PDF2MD_ORBS_Unified/frontend/index.html”.  In essence, the backend handles both the processing of the Research Assistant, as well as the ORBS Grader.   I am sure that the ORBS Grader can be explained by Karim, since it’s his module that I integrated into the same backend as mine. As for the Research Assistant, it takes a PDF file as an upload on the frontend’s Review Mode tab, uses Mineru to generate an MD file from which text is extracted and sent to an LLM via an API according to a system prompt that instructs the model to generate a 5–7-point summary. The points are then stored in a database alongside the MD file from which they have been generated (the MD file is downloadable via the Database tab on the frontend). The user can then go to the frontend’s Write tab to generate a discussion by entering in some text. The text is used to build a relevant prompt that is sent to the LLM, with the prompt being a string of all the points relevant to the text-entered, taken from the database. The Follow Up feature (a feature that lets you talk to the discussion that has been generated) still requires more development. Moreover, a vector database is yet to be implemented. RAG is not a part of the module yet.  Lastly, the entire backend is in Python. My frontend makes use of Vue.js.