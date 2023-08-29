import openai
from linkedin_scraper import Person, actions
from selenium import webdriver
from flask import Flask,request , render_template
import os 
app = Flask(__name__)


memory =  [{'name': 'https://www.linkedin.com/in/pradeep-saini-4689a9172/', 'details': """Person Pradeep Saini
1st degree connection
1st

About
Programmer
Programmer

Experience
([Experience(institution_name='Zenop · Internship', linkedin_url='https://www.linkedin.com/company/92588942/', website=None, industry=None, type=None, headquarters=None, company_size=None, founded=None, from_date='Jun 2023', to_date='Aug 2023', description='Skills: Prompt Engineering · Artificial Intelligence (AI) · FastAPI · OpenAi · Large Language Models (LLM) · Multi-agent Systems · Python (Programming Language)\nSkills:Prompt Engineering · Artificial Intelligence (AI) · FastAPI · OpenAi · Large Language Models (LLM) · Multi-agent Systems · Python (Programming Language)', position_title='Back End Developer', duration='3 mos', location='Bengaluru, Karnataka, India · Remote')],)

Education
([Education(institution_name='JECRC University', linkedin_url='https://www.linkedin.com/company/2782627/', 
website=None, industry=None, type=None, headquarters=None, company_size=None, founded=None, from_date='Sep 
2022', to_date='Jul 2024', description='Activities and societies: Volleyball , Tech Club\nActivities and societies: Volleyball , Tech Club\nSkills: Python (Programming Language) · Django\nSkills:Python (Programming Language) · Django', degree='Master of Computer Applications - MCA, Computer Programming'), Education(institution_name='Sunstone', linkedin_url='https://www.linkedin.com/company/15098539/', website=None, industry=None, type=None, headquarters=None, company_size=None, founded=None, from_date='Sep 2022', to_date='Jun 2024', description='', degree='Master of Computer Applications - MCA, Artificial Intelligence'), Education(institution_name='Maharishi Dayanand Saraswati University, Ajmer', linkedin_url='https://www.linkedin.com/company/15106469/', website=None, industry=None, type=None, headquarters=None, company_size=None, founded=None, from_date='Jan 2019', to_date='Jul 2022', description='Grade: 76.18%\nGrade: 76.18%\nSkills: Python (Programming Language) · Django\nSkills:Python (Programming Language) · Django', degree='Bachelors Of Computer Application, Computer Science')],)

Interest
([],)

Accomplishments
[]""",'output':[]}]
def add_memory(url,person):
    dic = {
        "name": url ,
        "details": person
    }
    
    memory.append(dic)
    print(memory)
def check_memory(name):
    for i in memory:
        if name in i['name']:
            return i['details']
    else:
        return None
def save_output_in_memory(output,name):
    for i in memory:
        if name in i['name']:
            if len(i['output']) <3:
                i['output'].insert(0,output)
                data  = i['output']
                return data
            else:
                return i['output']
    
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/output',methods=['GET','POST']) 
def output():
    url = request.form.get('url')
    already_Store = check_memory(url)
    if already_Store is None:
        email = os.environ.get('email')
        password = os.environ.get('password')
        driver = webdriver.Chrome()
        actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
        person = Person(f"{url}", driver=driver)
        add_memory(url,person)
        output = call_ai(already_Store,url)
        return output
    else :
        output = call_ai(already_Store,url)
        return output
def call_ai(person,url):
    # api_key = os.environ.get('OPENAI_API_KEY')

# Initialize the OpenAI API client
    openai.api_key = "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"
    prompt = f"""You Are A Best Ai Tool who can generate a short paragraph for linkedin About section .
             You have the ability to understand the parameter according to a list or python generated output . 
             this output have very short details on about his name ,college , Experience and his skills .
             so being a smart reader you have to understand all parameters and generate a summary of  on his given details and make sure the output format  is like a person expressing about himself or give a interview and interviewer asking tell me about yourself.
             details : {person}
    """

    # Generate a response using the OpenAI GPT-3.5 Turbo model
    # response = openai.Completion.create(
    #     engine="text-davinci-003",  # GPT-3.5 Turbo engine
    #     prompt=prompt,
    #     max_tokens=500,  # Adjust the length of the generated response
    #     stop=None,  # You can specify a stop word to end the response if needed
    # )

    # Extract and print the generated answer
    # answer = response.choices[0].text.strip()
    answer = ''' I am Pradeep Saini, a seasoned software developer with experience ranging from remote internships with Zenop, working as frontend developer, to Masters in Computer Application focusing on Artificial Intelligence from Sunstone. My skillset also include expertise in Prompt Engineering, Artificial Intelligence (AI), FastAPI, OpenAi, Large Language Models (LLM) and Multi-agent Systems. I had also successfully cleared my Bachelors of Computer Applications from Maharishi Dayanand Saraswati University, Ajmer with a grade of 76.18%. I have a massive passion for programming and am always exploring the frontiers of the ever-changing Technology-scape.'''
    data = save_output_in_memory(answer,url)
    return render_template('output.html',url= url, output= data)

if __name__ == "__main__":
    app.run(debug=True)
