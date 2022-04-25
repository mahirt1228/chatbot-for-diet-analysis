# chatbot-for-diet-analysis
This chatbot is developed in rasa framework. it recommends the food item to the user on the basis of their bmr,bmi as well as the physical factor.
This chatbot will give the diet_plan to the user in the pdf format in the chat itself.

How to run the chatbot in the broswer
-----------------------------------------------------------

=> open vscode 

=> by pressing ctrl+shift+p select your python interpretor of your anaconda environment

open project folder in visual studio code and open cmd

Here you need to open 3 cmd terminals

for training the model:

open 1st Terminal
 run commands in 1st terminal : 
	a)rasa train (this command will train the rasa model)
	b)rasa run -m models --enable-api --cors "*" (This command will start the server)
				or
	b)  rasa run --log-file out.log --cors * --enable-api

2nd Terminal run Command:
	a)rasa run actions (This command will start the actions server)

3rd Terminal run .command
	a) python web_app.py (This command will start the flask  server) 
							
