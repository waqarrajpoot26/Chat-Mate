from flask import Flask , render_template , request , redirect , jsonify
from aiml import Kernel
from py2neo import Graph , Node , NodeMatcher
import nlp_implemantation 
import os
import socket
from nltk import ne_chunk,pos_tag,word_tokenize,sent_tokenize
from Web_Scraping import get_Query
import relations 
import bert_implementation 

app = Flask(__name__ , template_folder='templates')
graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))
user_value = ''
set_ip = ''


@app.route("/")
def Home():
    return render_template('Front.html')
@app.route("/registration")
def register():
    return render_template('Signup.html')
@app.route("/getsignin")
def getsignin():
    return render_template('Login.html')
@app.route("/chatbox")
def chatbox():
    return render_template('Chatbox.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    global user_value
    global set_ip
    if request.method == 'POST':
        print("login called")
        email = request.form['email']
        password = request.form['password']
        ipAdress = get_ip()
        matcher = NodeMatcher(graph)
        user = matcher.match("Client", email=email,password=password).first()
        set_ip = graph.run(f"MATCH (n:Client{{email: \"{email}\", password: \"{password}\"}}) set n.ip= \"{ipAdress}\" return n.ip")
        usrname1 = graph.run(f"MATCH (n:Client{{email: \"{email}\", password: \"{password}\"}}) return n.username")
        print("sign in",user)
        print("Confirm: ", set_ip , usrname1)
        if user:
             usrname1 = list(usrname1)
             username = usrname1[0][0]
             my_bot.setPredicate('name',str(username))
             my_bot.setPredicate('myip',str(set_ip))
             return redirect("/chatbox")
    return render_template('Login.html') 
        
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        print("signup called")
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        number = request.form['number']
        ip = get_ip()
        user = Node("Client", username=username, password=password, email=email, number=number, ip=ip)
        graph.create(user)
        print("sign up",user)
        if user:
            return redirect('/login')
    return render_template('Signup.html')


my_bot = Kernel()
bot_name="ChatMate"
my_bot.setBotPredicate("name", bot_name)
def load_aiml_files(my_bot):
    aiml_directory = "data"
    aiml_files = [os.path.join(aiml_directory, file) for file in os.listdir(aiml_directory) if file.endswith(".aiml")]
    for aiml_file in aiml_files:
        my_bot.learn(aiml_file)

load_aiml_files(my_bot)


def chat_bot_reply(message):
    try:
        response = my_bot.respond(message)
        return response
    except: 
        return None

@app.route('/get_response', methods=['POST'])
def get_response():
    response=''
    message = request.json['message']
    auto = nlp_implemantation.autospell_corrector(message)
    print(auto)
    sents = sent_tokenize(auto)
    prev_response = ""
    for query in sents:
        query = nlp_implemantation.autospell_corrector(query)
        nlp_implemantation.NER(query)
        print("query",query)
        bot_response = chat_bot_reply(query)
        response = response + '' + bot_response
        print(response)
        # web scrapping and wordnet
        if response == '' or "unknown" in response or "I have never been asked that before." in response or "tried searching the web?" in response or "no answer for that" in response or "do not know" in  response or "deeper algorithm" in response or "My brain contains more than 22,000 patterns, but not one that matches your last input." in response or "do not recognize" in response or "I need time to formulate the reply." in response:
            response = ''
            web_resonse = get_Query(query)
            if web_resonse:
                prev_response = prev_response + '' + web_resonse
                response =response + "" + prev_response
            else:
                r = sent_tokenize(response)[0]
                Postags = pos_tag(word_tokenize(r))
                for tag in Postags:
                    if tag[1].startswith('N') or  tag[1].startswith('V') :
                        prev_response = prev_response + "" + nlp_implemantation.get_word_definition(tag[0])
                        response =response +""+ prev_response
        else:
            prev_response +=response
            response = prev_response
        prev_response = response
    return jsonify({'response': response})

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    s = s.getsockname()[0]
    netaddres = ''
    count = 0
    for bit in s:
        if bit == '.':
            count = count + 1
        netaddres = netaddres + bit
        if count == 3:
            return netaddres

ip = get_ip()
print("IP Address:", ip)

if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0', port='8080')
