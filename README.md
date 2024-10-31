# study_tracker
Simple MVP study tracker written in Python using Flask and JSON   
Written entirely using ChatGPT
Requires Python 3 and Flask to run  

## To Run ##
Unpack, navigate to app.py directory;  
run python app.py


## Prompt ##
Using python and flask frameworks for the website and JSON for data storage, help me design an MVP website that will help me track observational data about subjects in a study.  It should do the following:
1.  web portal with responsive navigation between a project browser, a subject browser, and an observation list. The portal should have a header and sections to allow for ad hoc changes like notifications for users. Populate at least two such sections with 100-150 words of lorem ipsum text.  
2.  the project browser will allow users to create and view the following data:  unique number(int), project title(str), short description(str), and a list of one to 100 tags(str) that are used to append to observational meta data.  
3.  the subject browser will allow users to create and view records about study subjects that are linked to projects via a key.  The records will include the following data:  project number(int) that is valid for an existing project, a unique subject number(int),  subject's first name(str), middle name(str), last name(str), nick name(str), phone number(str), email address(str) and URL(str) for an online photo.  The email address and phone number should have logic to check they match common conventions.  For phone number it should follow the ###-###-#### found in us phone numbers and for email it should follow the convention of string@string.string.  It should not allow any domain extensions that are not .net, .com, .org, .edu, or .gov.  
3.  the observation browser will allow users to create and view records about study observations that are linked to projects via a key and subjects via a key.  The records will include the following data:  project number(int) that is valid for an existing project, subject number(int) that is valid for an existing subject, and an observation(str) that is long text (1000 chars) and a unique observation id(int).  the observation browser page layout should include the option to select a subject and view their list of observations.  When viewing observations, the summary of the subject should be in view.    
