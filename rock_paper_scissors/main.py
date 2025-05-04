from flask import Flask, render_template , session , redirect , request
import random

app = Flask(__name__)
app.secret_key = 'Rock_Paper_scissors'
connection = []

@app.route('/' , methods = ['GET'])
def home():
    if (request.method == 'GET') and (request.args.get('id') in connection) and (request.args.get('id')):
        if user_input := request.args.get('choice'):
            dic = { 1 : "rock" , 2 : "paper" , 3 : "scissor"}
        
            cpu_input = lambda: random.randint(1, 3)
            cpu_ans = dic[cpu_input()]
          #------game part------
            if((user_input == 'rock' and cpu_ans =='scissor') or (user_input == 'paper' and cpu_ans == 'rock') or (user_input == 'scissor' and cpu_ans == 'paper')):
                result = f"Player win"

            elif((user_input == 'scissor' and cpu_ans =='rock') or (user_input == 'rock' and cpu_ans == 'paper') or (user_input == 'paper' and cpu_ans == 'scissor')):
                result = f"Player lose"

            elif(user_input == cpu_ans):
                result = f"Draw!"
            else:
                result = f"WARNING : Invalid Choice!!!!"
   
            return render_template('Game_page.html', id=request.remote_addr, result =result, user_input=user_input, cpu_ans = cpu_ans )
        else:
            return render_template('Game_page.html', id=request.remote_addr)
    else:
        if request.remote_addr not in connection:
            connection.append(request.remote_addr)
        return redirect(f'/?id={request.remote_addr}')

if __name__ =="__main__":
    app.run(debug=True)