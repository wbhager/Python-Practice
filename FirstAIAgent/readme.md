Hello! Welcome to my very first AI Agent project!

My goal is to create a web agent that looks great and can act as my planner, adding things to my calendar or suggesting things to me that I can do. The agent
will have access to one of my emails' google calendars, w4561927@gmail.com. I'll also keep track of the work I've done and how long I've spent on the work.

<br> <br> <br>



To-do: Re-add gitignore, add .env and:
__pycache__/
*.pyc

To-do 2: Begin constructing a bare-bones UI so that the user can interact with the agent, connect the ui to n8n and then connect n8n to my python backend, 
come up with idea for what I want my agent to be able to do, add a system prompt to the ai_response_generator file 

<br> <br> <br>


Project layout:

FirstAIAgent/
    api/
        api_server.py
    logic/
        ai_response.generator.py
        agent.py
        model.py
    memory/
        buffer.py
        summary.py
    templates/
        system_prompt.txt
        qa_prompt.py
    ui/
        index.html
        style.css
        app.js
        favicon.ico

<br> <br> <br>



History on the project:

11/3: Initialized project, created 2 branches, one for each of the new files I created (chat-ui.py and ai-response-generator.py), pushed changes on one of the branches, merged branch to main 

11/4: Added gitignore file with my .env file, moved the gitignore file to the root folder, organized misc. files in root folder and finished setting up my git repository, generated the claude key (I plan to use Claude 3 Sonnet and input $15 beforehand, it will give me approximately 1 million tokens worth to work with)

11/5: Added credits to Claude, read up on output token generation 

11/10: Added code so that I should be able to make an API call to claude-sonnet, but having an issue with an anthropic bug saying I don't have it installed when
I know that I do 

11/14: Debugging bug saying that I still don't have claude installed, went about fixing this in several ways but still no found solutions. Removed special character from original directory name to limit the kinds of unnecessary errors that could be causing issues for me

11/16: Spent some more time debugging, renamed file names to remove special characters to limit unnecessary errors

11/17: Initialized and began writing code for my api_server.py file that will use to establish the n8n connection, finally fixed the bug from earlier (the model I was trying to use was not supported anymore, so I switched to a newer model), read up on ways to construct my agent project, settled with a final layout of my project, read up on the basics of JavaScript

11/18: Initialized docker server with n8n, read up on host servers and ports, read up on how I can establish the full pipeline from UI to n8n to python to model to python to n8n to UI

11/19: Learned more about webhooks, testing the first webhook trigger node and tried to determine why I was receiving error 404s and why URL only worked with port 5680 and not 5678

11/23: Tested post request success by sending messages n8n from the terminal, studied up on the basics of UI development and watched online videos outlining the
of web development and html, initialized one html file, javascript file, and css file 

11/24: Finalized idea for what I want my agent to be (planner/suggestor), more UI studying, updated index.html with bare-bones code
to bring to life a user interface for my agent that I intend to make look like some sort of chat bot, created a favicon for my website

11/25: Learned about webhook responses, added a webhook response node to the n8n workflow, Studied up on servers and api calls, learned the basics of how Claude's call-and-response message system works, constructed the api_server.py file

11/28: Continued researching webhooks, APIs, and servers, worked on getting the backend to connect to n8n (REWORD)

11/30: Added to .gitignore

12/1: Constructed the baseline html file and most of the css file
