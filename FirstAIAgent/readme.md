Hello! Welcome to my very first AI Agent project!

My goal is to create a web agent that looks great and can act as my planner, adding things to my calendar or suggesting things to me that I can do. The agent
will have access to one of my emails' google calendars, w4561927@gmail.com. I'll also keep track of the work I've done and how long I've spent on the work.

<br> <br> <br>





To-do: Adding some more basic UI enhancements, adding basic agent functionality where the agent can access my google calendar and add events and send me reminders, some system prompt engineering, and adding some sort of memory capability

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

11/30: Updated .gitignore file

12/1: Reviewed the basics of HTML and CSS, constructed the full baseline html file and most of the css file, studied up on prompt engineering before constructing the system prompt

12/2: Constructed the rest of the CSS file, researched more ways that web pages could be shaped and modified, begun learning the basics of how JavaScript works and how it works in tandem with HTML and CSS

12/3: Studied up on the basics of JavaScript, decided upon the basic functionality I wanted my webpage to have, constructed the first full JavaScript file with properties such as basic button functions, displaying error messages, and preventing certain functions from happening when the frontend is waiting for the backend response, troubleshooted a visual mistake where I fixed the allignment of the messages, began scoping out why my agent was only answering basic prompts and not longer ones

12/4: Fixed the issue of why the agent was only answering short prompts, I added an extra code node to my n8n pipeline that stringifies the JSON immediately before it gets sent back through the respond-to-webhook node.

12/5: Swapped some code around from the api_server.py and ai_response_generator.py files - it did not make sense to have a bit of logic in my api server file. Crafted the first version of the system prompt in the system_prompt.txt file, where I essentially asked for the bot to be a planner for me and to provide me recommendations as to how I can fill out parts of my schedule. Started troubleshooting an issue where the bot got stuck on the HTTP Post Request node where the API call to Claude does not seem to be made.

12/8: Fixed the issue where my bot gets stuck on the HTTP post request, there were some typos in my api_server.py and my ai_response_generator.py files. cleaned up some files and updated .gitignore, prettied up my UI by adding very small features for a bit more depth and implemented the color scheme I wanted for both dark mode and light mode, added voice-to-text capabilities, started constructing copy button but having issues with it appearing on screen correctly
