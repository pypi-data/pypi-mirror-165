from dataclasses import replace
from posixpath import split
from pdfminer.high_level import extract_text
from datetime import datetime, date

#libraries to extract name
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

#Libraries to extract phone number
import re

import docx2txt


"""""
RESERVED_WORDS = [
    'school',
    'college',
    'univers',
    'academy',
    'faculty',
    'institute',
    'faculdades',
    'Schola',
    'schule',
    'lise',
    'lyceum',
    'lycee',
    'polytechnic',
    'kolej',
    'ünivers',
    'okul',
    'Universidad',
    'Politecnica'
]
SKILLS_DB = [
    "SQL & SAS",
    "Data Analysis",
    "agile development methodologies",
    "certified uiPath application developer",
    "Certified Automation Anywhere Application Developer",
    "Project management",
    'machine learning',
    'data science',
    'python',
    'word',
    'excel',
    'English',
    'c#',
    'c++'
    'sql',
    'matlab',
    'rpa',
    'javascript',
    'android',
    'office',
    'angular',
    'uipath',
    'tensorflow',
    'java',
    'github',
    'ruby',
    'vue',
    'arduino',
    'mysql',
    'power BU',
    'ios',
    'photoshop',
    'illustrator',
    'networking',
    'cisco',
    'windows',
    'linux',
    "no-sql",
    "fierebase",
    "amazon",
    "aws",
    "azure ",
    "backend",
    "frontend",
    "flask"
    "ioninc",
    "bootstrap",
    "flutter",
    "mobil ui",
    "native android development",
    "html",
    "mvvm",
    "retrofit",
    "junit ",
    "android native with kotlin and java",
    "scrum",
    "software development"
    "ioninc",
    "ojective-c",
    ".net",
    "visual basic",
    "jquery",
    "web developer",
    "php",
    "ajax",
    "css",
    "unity 3d",
    "spring boot",
    "mvc",
    "agile methodologies",
    "intelliJ idea",
    "poo",
    "artificial intelligence",
    "big fata",
    "sql-mysql"
    "typescript",
    "andorid jetpack",
    "java",
    "react",
    "java basics",
    "network ccna",
    "ccnp",
    "servers"
]

LANGUAGE_DB = [
'Mandarin',   
'Spanish',
'English',
"Ingles",
"Español",
'Hindi',
'Arabic',
'Portuguese',
'Bengali',
'Russian',
'Japanese',
'Punjabi',
'German',
'Javanese',
'Wu',
'Malay',
'Telugu',
'Vietnamese',
'Korean',
'French',
'Marathi',
'Tamil',
'Urdu',
'Turkish',
'Italian',
'Yue',
'Thai',
'Gujarati',
'Jin',
'Southern Min',
'Persian',
'Polish',
'Pashto',
'Kannada',
'Xiang',
'Malayalam',
'Sundanese',
'Hausa',
'Odia',
'Burmese',
'Hakka',
'Ukrainian',
'Bhojpuri',
'Tagalog',
'Yoruba',
'Maithili',
'Uzbek',
'Sindhi',
'Amharic',
'Fula',
'Romanian',
'Oromo',
'Igbo'
]

NAMES_DB = [
'Aldo',
'Humberto',
'Saul',    
'James',
'Robert',
'John',
'Michael',
'David',
'William',
'Richard',
'Joseph',
'Thomas',
'Charles',
'Christopher',
'Daniel',
'Matthew',
'Anthony',
'Mark',
'Donald',
'Steven',
'Paul',
'Andrew',
'Joshua',
'Kenneth',
'Kevin',
'Brian',
'George',
'Timothy',
'Ronald',
'Edward',
'Jason',
'Jeffrey',
'Ryan',
'Jacob',
'Gary',
'Nicholas',
'Eric',
'Jonathan',
'Stephen',
'Larry',
'Justin',
'Scott',
'Brandon',
'Benjamin',
'Samuel',
'Gregory',
'Alexander',
'Frank',
'Patrick',
'Raymond',
'Jack',
'Dennis',
'Jerry',
'Tyler',
'Aaron',
'Jose',
'Adam',
'Nathan',
'Henry',
'Douglas',
'Zachary',
'Peter',
'Kyle',
'Ethan',
'Walter',
'Noah',
'Jeremy',
'Christian',
'Keith',
'Roger',
'Terry',
'Gerald',
'Harold',
'Sean',
'Austin',
'Carl',
'Arthur',
'Lawrence',
'Dylan',
'Jesse',
'Jordan',
'Bryan',
'Billy',
'Joe',
'Bruce',
'Gabriel',
'Logan',
'Albert',
'Willie',
'Alan',
'Juan',
'Wayne',
'Elijah',
'Randy',
'Roy',
'Vincent',
'Ralph',
'Eugene',
'Russell',
'Bobby',
'Mason',
'Philip',
'Louis',
'Maria',
'Nushi',
'Mohammed',
'Muhammad',
'Mohamed',
'Wei',
'Mohammad',
'Ahmed',
'Yan',
'Ali',
'Abdul',
'Ana',
'Ying',
'Anna',
'Mary',
'Jean',
'Luis',
'Carlos',
'Antonio',
'Hui',
'Elena',
'Francisco',
'Hong',
'Marie',
'Min',
'Lei',
'Ibrahim',
'Fatima',
'Aleksandr',
'Olga',
'Pedro',
'Rosa',
'Jorge',
'Yong',
'Elizabeth',
'Sergey',
'Patricia',
'Hassan',
'Anita',
'Manuel',
'Victor',
'Sandra',
'Ming',
'Miguel',
'Emmanuel',
'Ling',
'Sarah',
'Mario',
'Joao',
'Tatyana',
'Rita',
'Martin',
'Svetlana',
'Natalya',
'Qing',
'Ahmad',
'Martha',
'Andrey',
'Sunita',
'Andrea',
'Christine',
'Irina',
'Laura',
'Linda',
'Marina',
'Carmen',
'Ghulam',
'Vladimir',
'Barbara',
'Angela',
'Roberto',
'Peng',
'Ivan',
'Ekaterina',
'Qiang',
'Jesus',
'Susan',
'Sara',
'Noor',
'Mariam',
'Dmitriy',
'Zahra',
'Fatma',
'Fernando',
'Esther',
'Diana',
'Mahmoud',
'Rong',
'Santosh',
'Nancy',
'Musa',
'Anh',
'Omar',
'Jennifer',
'Claudia',
'Maryam',
'Gloria',
'Ruth',
'Teresa',
'Sanjay',
'Kyaw',
'Francis',
'Amina',
'Denis',
'Sunil',
'Eduardo',
'Abdullah',
'Grace',
'Anastasiya',
'Rafael',
'Ricardo',
'Aleksey',
'Gita',
'Jianhua',
'Karen',
'Masmaat',
'Xiaoyan',
'Rajesh',
'Mustafa',
'Eva',
'Bibi',
'Monica',
'Oscar',
'Andre',
'Catherine',
'Ramesh',
'Liping',
'Sonia',
'Mina',
'Manoj',
'Ashok',
'Rose',
'Alberto',
'Ning',
'Rekha',
'Aung',
'Alex',
'Suresh',
'Anil',
'Fatemeh',
'Julio',
'Zhen',
'Simon',
'Paulo',
'Juana',
'Irene',
'Vijay',
'Syed',
'Mehmet',
'Angel',
'Julia',
'Victoria',
'Cheng',
'Lakshmi',
'Francisca',
'Veronica',
'Roman',
'Ismail',
'Margaret',
'Luz',
'Anne',
'Silvia',
'Kamal',
'Raju',
'Sergio',
'Lisa',
'Marta',
'Nadezhda',
'Marco',
'Alice',
'Asha',
'Xiang',
'Isabel',
'Zainab',
'Michelle',
'Long',
'Michel',
'Pierre',
'Saleh',
'Haiyan',
'Felix',
'Salma',
'Hector',
'Manju',
'Joyce',
'Margarita',
'Joel',
'Jessica',
'Lucia',
'Pavel',
'Nadia',
'Mariya',
'Jianping',
'Jacqueline',
'Halima',
'Nan',
'Rama',
'Rebecca',
'Julie',
'Vera',
'Vinod',
'Khalid',
'Ramon',
'Janet',
'Sharon',
'Suman',
'Jane',
'Lihua',
'Shanti',
'Abubakar',
'Aisha',
'Zaw',
'Paula',
'Bruno',
'Monika',
'Maksim',
'Mamadou',
'Judith',
'Mostafa',
'Chris',
'Helen',
'Nikolay',
'Rina',
'Zhiqiang',
'Marcos',
'Mária',
'Norma',
'Anton',
'Raul',
'Cristina',
'Xiaohong',
'Antonia',
'Betty',
'Alejandro',
'Nelson',
'Igor',
'Evgeniy',
'Adriana',
'Amir',
'Pablo',
'Regina',
'Rajendra',
'Brenda',
'Linh',
'Sani',
'Hussein',
'Gul',
'Mikhail',
'Jaime',
'Nicole',
'Sima',
'Giuseppe',
'Dinesh',
'Tatiana',
'Bernard',
'Lijun',
'Sita',
'Javier',
'Shan',
'Hasan',
'Yuliya',
'Moses',
'Agnes',
'Cesar',
'Xiaoli',
'Usha',
'Alfredo',
'Meng',
'Jianguo',
'Kiran',
'Khaled',
'Carol',
'Rani',
'Yusuf',
'Xiaoping',
'Rakesh',
'Isaac',
'Luiz',
'Josephine',
'Krishna',
'Mohamad',
'Erika',
'Blanca',
'Jianjun',
'Deborah',
'Amanda',
'Natalia',
'Gladys',
'Florence',
'Usman',
'Lijuan',
'Abdullahi',
'Stephanie',
'Tingting',
'Saeed',
'Edgar',
'Maya',
'Mahdi',
'Khadija',
'Valentina',
'Ruben',
'Tuan',
'Thanh',
'Doris',
'Fatoumata',
'Darya',
'Rene',
'Cecilia',
'Umar',
'Cynthia',
'Gustavo',
'Kim',
'Lucas',
'Zin',
'Xuan',
'Moussa',
'Amit',
'Mona',
'Xiaoling',
'Dilip',
'Caroline',
'Muhammed',
'Claude',
'Elisabeth',
'Yuanyuan',
'Beatrice',
'Edwin',
'Xiaodong',
'Hung',
'Kristina',
'Christina',
'Ajay',
'Alina',
'Denise',
'Vladymyr',
'Daniela',
'Pushpa',
'Joan',
'Leonardo',
'Aleksandra',
'Ravi',
'Virginia',
'Hamid',
'Alain',
'António',
'Lyubov',
'Xiaoming',
'Alicia',
'Mohan',
'Hans',
'Xing',
'Ann',
'Laoshi',
'Santos',
'Nicolas',
'Felipe',
'Amal',
'Bekele',
'Donna',
'Dina',
'Hugo',
'Yolanda',
'Laxmi',
'Munni',
'Maryia',
'Beatriz',
'Urmila',
'Mukesh',
'Brigitte',
'Radha',
'Evelyn',
'Emma',
'Kenji',
'Galina',
'Diego',
'Viktor',
'Arun',
'Alexandra',
'Alfred',
'Nykolai',
'Armando',
'Sunday',
'Edith',
'Jingjing',
'Samira',
'Zhiyong',
'Hiroshi',
'Gabriela',
'Savitri',
'Rachel',
'Adrian',
'Shankar',
'Carla',
'Miriam',
'Gopal',
'Yanping',
'Lyudmila',
'Lalita',
'Magdalena',
'Xiaohua',
'Anwar',
'Sushila',
'Jianming',
'Amy',
'Mercy',
'Irma',
'Xiaofeng',
'Marcelo',
'Abdel',
'Karim',
'Rodrigo',
'Pamela',
'Sangita',
'Agus',
'Weidong',
'Jacques',
'Jeanne',
'Joy',
'Ganesh',
'Ingrid',
'Nirmala',
'Sumitra',
'Juliana',
'Mahesh',
'Nina',
'Xiaojun',
'Viktoriya',
'Rahul',
'Petra',
'Zhiming',
'Nikita',
'Shuang',
'Yasmin',
'Qiong',
'Ayşe',
'Phuong',
'Melissa',
'Quan',
'Wilson',
'Trang',
'Giovanni',
'Hang',
'Elias',
'Zhigang',
'Adama',
'Jamila',
'Osman',
'Piotr',
'Savita',
'Xiaoying',
'Oksana',
'Raja',
'Dorothy',
'Zhiwei',
'Sultan',
'Ernesto',
'Jianfeng',
'Xiaohui',
'Xiaomei',
'Oleg',
'Ruslan',
'Shu',
'Diane',
'Andres',
'Song',
'Shirley',
'Hongmei',
'Adamu',
'Manoel',
'Xuemei',
'Shiv',
'Enrique',
'Mariana',
'Serhei',
'Monique',
'Vanessa',
'Prakash',
'Jitendra',
'Dominique',
'Susana',
'Annie',
'Saroj',
'Ahmet',
'Bashir',
'Elsa',
'Samir',
'Sarita',
'Chunyan',
'Lidia',
'Guillermo',
'Jinhua',
'Luisa',
'Karin',
'Hongwei',
'Andreas',
'Leila',
'Weiwei',
'Helena',
'Philippe',
'Vicente',
'Dongmei',
'Konstantin',
'Tania',
'Pascal',
'Aziz',
'Martina',
'Fred',
'Tamara',
'Tony',
'Naseem',
'Lucy',
'Surendra',
'Jyoti',
'Pauline',
'Marc',
'Zhihua',
'Sabina',
'Guadalupe',
'Salim',
'Amar',
'Lydia',
'Mahendra',
'Guoqiang',
'Lee',
'Seyyed',
'Ayesha',
'Muhamad',
'Karina',
'Salah',
'Ilya',
'Josef',
'Leticia',
'Aicha',
'Michele',
'Nasir',
'Sadia',
'Josefa',
'Narayan',
'Kavita',
'Pramod',
'Sofia',
'Hari',
'Alexey',
'Blessing',
'Hossein',
'Tina',
'Claudio',
'Nathalie',
'Hongyan',
'Xiaoyu',
'Sam',
'Karl',
'Mamta',
'Mercedes',
'Shigeru',
'Kathleen',
'Farida',
'Hawa',
'Sakina',
'Jianxin',
'Marcel',
'Yvan',
'Guohua',
'Myat',
'Emine',
'Tara',
'Francesco',
'Nurul',
'Nana',
'Sayed',
'Jay',
'Abraham',
'Nour',
'Imran',
'Iman',
'Lwin',
'Jamal',
'Thao',
'Wolfgang',
'Nam',
'Manuela',
'Jianzhong',
'Raquel',
'Artur',
'Uma',
'Louise',
'Nabil',
'Hilda',
'Punam',
'Abdoulaye',
'Wendy',
'Ian',
'Stella',
'Elvira',
'Valerie',
'Eman',
'Subhash',
'Sylvia',
'Jeff',
'Carolina',
'Olha',
'Tomasz',
'Masoumeh',
'Zhijun',
'Anastasia',
'Pradip',
'Tadesse',
'Andrei',
'Adel',
'Werner',
'Ursula',
'Clara',
'Lina',
'Charlotte',
'Angelina',
'Cong',
'Tomas',
'Yanling',
'Zhihong',
'Jim',
'Valentyna',
'Hamza',
'Shanshan',
'Than',
'Lilian',
'Francois',
'Rodolfo',
'Melanie',
'Dipak',
'Marlene',
'Ashraf',
'Gerardo',
'Sheila',
'Rana',
'Weihua',
'Kalpana',
'Simone',
'Orlando',
'Marwa',
'Arif',
'Eunice',
'Farzana',
'Parvati',
'Angelo',
'Amadou',
'Robin',
'Rashid',
'Abel',
'Ranjit',
'Alexandre',
'Yuhua',
'Madina',
'Kamla',
'Fabio',
'Mariama',
'Liming',
'Prem',
'Mustapha',
'Sabine',
'Wenjun',
'Aida',
'Yanhong',
'Lihong',
'Klaus',
'Junjie',
'Ran',
'Heba',
'Shah',
'Son',
'Sharmin',
'Minh',
'Yvonne',
'Jianmin',
'Thuy',
'Habiba',
'Therese',
'Jenny',
'Mike',
'Nada',
'Xiaolin',
'Vasylyi',
'Manfred',
'Marcia',
'Shobha',
'Tian',
'Umesh',
'Solomon',
'Asmaa',
'Jimmy',
'Paulina',
'Aminata',
'Nora',
'Ravindra',
'Sophie',
'Joanna',
'Weimin',
'Yanhua',
'Sylvie',
'Xiaoqing',
'Jianwei',
'Sachiko',
'Raimundo',
'Laila',
'Pankaj',
'Reza',
'Roland',
'Emily',
'Habib',
'Smt',
'Mohsen',
'Angelica',
'Liliana',
'Phyo',
'Hatice',
'Yingying',
'Lyudmyla',
'Isabelle',
'José',
'Tim',
'Durga',
'Naresh',
'Wenjie',
'Nguyen',
'Arjun',
'Shyam',
'Herbert',
'Olivier',
'Haibo',
'Kseniya',
'Hanan',
'Amin',
'Renu',
'Masako',
'Xian',
'Priyanka',
'Weiping',
'Nasreen',
'Salvador',
'Martine',
'Judy',
'Maha',
'Basanti',
'Theresa',
'Nusrat',
'Shahid',
'Stefan',
'Lingling',
'Marcin',
'Sebastian',
'Josefina',
'Gilberto',
'Huimin',
'Artyom',
'Shakuntala',
'Samina',
'Rosario',
'Qinghua',
'Kassa',
'Pramila',
'Kathy',
'Rabia',
'Nestor',
'Katsumi',
'Paola',
'Ernest',
'Yuriy',
'Yousef',
'Lixin',
'Zhihui',
'Sheikh',
'Kimberly',
'Luciano',
'Krzysztof',
'Hoang',
'Faisal',
'Dmitry',
'Alma',
'Aliyu',
'Yanyan',
'Chunhua',
'Xiaomin',
'Hieu',
'Yoko',
'Dolores',
'Leonard',
'Xiaowei',
'Weiming',
'Marilyn',
'Bharat',
'Katarzyna',
'Shila',
'Sabrina',
'Arturo',
'Dora',
'Gerhard',
'Haiying',
'Cristian',
'Laksmi',
'Nasrin',
'Kamala',
'Joaquim',
'Julius',
'Saraswati',
'Ganga',
'Chandra',
'Maurice',
'Tien',
'Kirill',
'Rosemary',
'Elaine',
'Marianne',
'Cheryl',
'Hana',
'Helga',
'Wenjing',
'Zhenhua',
'Liying',
'Faith',
'Heather',
'Heinz',
'Halyna',
'Zhijian',
'Sandeep',
'Satish',
'Ellen',
'Haitao',
'Sangeeta',
'Bernadette',
'Noel',
'Guoliang',
'Huong',
'Deepak',
'Christophe',
'Zhiping',
'Kailash',
'Lorena',
'Samia',
'Yumei',
'Issa',
'Lila',
'Yuping',
'Chantal',
'Thierry',
'Xiaoxia',
'Jianhui',
'Rustam',
'Ester',
'Aldo'		
]
"""""


#Here we extract all the information of resumes either pdf documents or word documents
#The information is commvert into a string varibale
def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

def extract_text_from_docx(docx_path):
    txt = docx2txt.process(docx_path)
    if txt:
        return txt.replace('\t', ' ')
    return None
def extract_text_from_docx_pdf(path):
    
    #print("PATH: "+path)
    isItPdf = re.findall(".*\.(PDF|pdf)+",path)
    #print(isItPdf)
    isItWord = re.findall(".*\.docx+",path)
    #print(isItWord)
    if(isItPdf):
       #print("THE FILE IS PDF")
        txt= extract_text_from_pdf(path)
    elif(isItWord):
        #print("THE FILE IS WORD")
        txt= extract_text_from_docx(path)
    
    #print("resume size: ",len(txt))
    return txt
 




#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#Extractin names from the text
def extract_names(txt,NAMES_DB):
    resumeSplited = txt.split("\n")
    #print("names size--------------")
    #print(resumeSplited)


    flagBreak = False
    number_iterations=0
    nameFound = "Name not found! :("
    for name in NAMES_DB:
        if flagBreak:
            break
        #print("Looking for the name: "+name)
        for line in resumeSplited:
            number_iterations+=1


            line = line.strip()
            words = line.split(" ")

            numberOfWords = line.split(" ")

            
            if len(numberOfWords)==2:
                if words[0].capitalize()==name or words[1].capitalize()==name:
                    nameFound = line
                    #print("---------------------------------------------------------")
                    #print(nameFound)
                    flagBreak = True
                    break
            elif len(numberOfWords)==3:
                if words[0].capitalize()==name or words[1].capitalize()==name or words[2].capitalize()==name:
                    nameFound = line
                    #print("---------------------------------------------------------")
                    #print(nameFound)
                    flagBreak = True
                    break
            elif len(numberOfWords)==4:
                if words[0].capitalize()==name or words[1].capitalize()==name or words[2].capitalize()==name or words[3].capitalize()==name:
                    nameFound = line
                    #print("---------------------------------------------------------")
                    #print(nameFound)
                    flagBreak = True
                    break
            
            """""
            if words[0].capitalize()==name:
                if len(numberOfWords)>=2:
                    nameFound = line
                    #print("---------------------------------------------------------")
                    #print(nameFound)
                    flagBreak = True
                    break
                """""
    #print("number of iterations: "+str(number_iterations))
    #print ("final name:"+ nameFound)
    return nameFound

        




 #//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#Extracting phone number
PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
def extract_phone_number(resume_text):
    phone = re.findall(PHONE_REG, resume_text)
 
    if phone:
        number = ''.join(phone[0])
 
        if resume_text.find(number) >= 0 and len(number) <20:
            return number
    return "No phone number found"



#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#Extracting email
EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
def extract_emails(resume_text):
    emails = re.findall(EMAIL_REG, resume_text)

    if len(emails) == 1:
        #print("Es un solom correo")
        email = emails[0]

    elif len(emails) > 1:
        email = ", ".join(emails)
    else:
        email = "not email found"
    #print(email)
    return email

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#Extracting skills

def extract_skills(input_text,SKILLS_DB):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(input_text)
    
 
    # remove the stop words
    filtered_tokens = [w for w in word_tokens if w not in stop_words]
 
    # remove the punctuation
    filtered_tokens = [w for w in word_tokens if w.isalpha()]
 
    # generate bigrams and trigrams (such as artificial intelligence)
    bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))
    
 
    # we create a set to keep the results in.
    found_skills = set()
 
    # we search for each token in our skills database
    for token in filtered_tokens:
        if token.lower() in SKILLS_DB:
            found_skills.add(token)
 
    # we search for each bigram and trigram in our skills database
    for ngram in bigrams_trigrams:
        if ngram.lower() in SKILLS_DB:
            found_skills.add(ngram)
    
    
    
    
    found_skillsList = list(found_skills)

    #print("Len of skills list: "+str(len(found_skills)))
    
    if len(found_skillsList)>0:
        skills = ", ".join(found_skillsList)
    else:
        skills= "No skills found"
    
 
    return skills

#Extracting Education
def extract_education(input_text,RESERVED_WORDS):
    organizations = []
 
    # first get all the organization names using nltk
    for sent in nltk.sent_tokenize(input_text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == 'ORGANIZATION':
                organizations.append(' '.join(c[0] for c in chunk.leaves()))
 
    # we search for each bigram and trigram for reserved words
    # (college, university etc...)
    education = set()
    for org in organizations:
        for word in RESERVED_WORDS:
            if org.lower().find(word) >= 0:
                education.add(org)
    
    educationList = list(education)

    if len(educationList)>0:
        educationString = ",".join(education)
    else:
        educationString = "No education information found"
 
    return educationString


#Extract Languajes

def extract_languages(input_text,LANGUAGE_DB):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(input_text)

    languagesList =[]

    for language in LANGUAGE_DB:
        if language in word_tokens:
            languagesList.append(language)
    
    if len(languagesList)>0:
        languages = ",".join(languagesList)
    else:
        languages="No languages found"
    
    return languages



#Here we are looking for any word that makes a reference to experience at the begining of the line
EXPERIENCE_TITLE_REG = re.compile(r'^(experience|experiencia profesional|work experience|e x p e r i e n c e|w o r k   e x p e r i e n c e|jobs){1}')
OTHER_TITLE_REG= re.compile(r'^(education|bachelor\'s degree|schooling|studies|skills|knowledge|certifications|courses and certifications|languages|hobbies|educación|e d u c a t i o n|c e r t i f i c a t i o n s)$')

def extract_Experience(input_text):
    
    resumeSplitted = input_text.split("\n")
    
    #print(type(resumeSplitted))
    
    #this flag is to detect if the some of the keywords that make a reference to experience was found
    experienceTitleFlag = False
    exeprience = ""
    for index,line in enumerate(resumeSplitted):
        #print("line len: "+str(len(line)))
        line = line.strip().lower()

        #here the lines with blank space are discarted
        if len(line) > 1:
            
            
            experienceTitle = re.findall(EXPERIENCE_TITLE_REG,line)
            #print(line)
            if experienceTitle:
                #print("---------------------------")
                #print(index)
                #print(experienceTitle)
                experienceTitleFlag = True
            #print("Flag = "+str(experienceTitleFlag))

            if experienceTitleFlag:

                #if the experiencias key word was found now is time to determine from where to where is the experience section
                #we achive this looking for key word of other section like education languages etc if we find some of this key word means that is
                #the end of the experience section
                other_title = re.findall(OTHER_TITLE_REG,line)
        
                if(other_title):
                    #print("othe section found")
                    #print(line)
                    break
                else:
                    #print(len(line))
                    #print(line)
                    exeprience +=line+"\n"
    return exeprience
                    
#This function base on 2 regex one that point the posible titles that could has the desired section
#and the second one is a regex that point all the other posible section that could be in the resume but we dont want
def ExtractResumeSection(input_text,desire_section_title_regex,unwanted_section_title_regex):
    resumeSplitted = input_text.split("\n")
    print(resumeSplitted)
    
    #print(type(resumeSplitted))
    
    #this flag is to detect if the some of the keywords that make a reference to EDUCATION was found
    titleSectionFlag = False
    sectionText = ""
    for index,line in enumerate(resumeSplitted):
        #print("line len: "+str(len(line)))
        line = line.strip().lower()

        #here the lines with blank space are discarted
        if len(line) > 1:
            
            #here we will look if the section that we desire extract the text exist  base on the regex function that we pass
            desireTitle = re.findall(desire_section_title_regex,line)
            #print(line)
            if desireTitle:
                #print("---------------------------")
                #print(index)
                #print(experienceTitle)
                titleSectionFlag = True
            #print("Flag = "+str(experienceTitleFlag))

            if titleSectionFlag:

                #if the EDUCATIONS key word was found now is time to determine from where to where is the EDUCATION section
                #we achive this looking for key word of other section like EXPERINCE languages etc if we find some of this key word means that is
                #the end of the EDUCATION section
                other_title = re.findall(unwanted_section_title_regex,line)
        
                if(other_title):
                    #print("othe section found")
                    #print(line)
                    break
                else:
                    #print(len(line))
                    #print(line)
                    sectionText +=line+"\n"
    return sectionText
def Years_of_experience(monthStr,Year):
    Year = int(Year)
    monthStr=monthStr.lower()
    monthInt=0
    if monthStr == 'january' or monthStr == 'jan':
        monthInt = 1

    elif monthStr == 'february' or monthStr == 'feb':
        monthInt = 2

    elif monthStr == 'march' or monthStr == 'mar':
        monthInt = 3

    elif monthStr == 'april' or monthStr == 'apr':
        monthInt = 4

    elif monthStr == 'may' or monthStr == 'jan':
        monthInt = 5

    elif monthStr == 'june' or monthStr == 'jun':
        monthInt = 6

    elif monthStr == 'july' or monthStr == 'jul':
        monthInt = 7

    elif monthStr == 'august' or monthStr == 'aug':
        monthInt = 8

    elif monthStr == 'september' or monthStr == 'sep':
        monthInt = 9

    elif monthStr == 'october' or monthStr == 'oct':
        monthInt = 10

    elif monthStr == 'november' or monthStr == 'nov':
        monthInt = 11

    elif monthStr == 'december' or monthStr == 'dec':
        monthInt = 12

    else:
        print("Error 404")

    day = 1

    DateJ = str(day) + "/" + str(monthInt) + "/" + str(Year)

    # Validation of the Date of Birth entered
    try:

        DateJ = datetime.strptime(DateJ, '%d/%m/%Y')
    except:
        print("The entered date is not correct, the format must be (dd/mm/yyyy)")
        exit()

    yearJ = DateJ.year
    monthJ = DateJ.month
    dayJ = DateJ.day

    # Actual Date
    dateA = datetime.today()

    yearA = dateA.year
    monthA = dateA.month
    dayA = dateA.day

    monthAdditional = 0
    if (dayJ > dayA):
        import calendar

        lastDay = calendar.monthrange(yearJ, monthJ)[1]
        dayA = dayA + lastDay
        monthAdditional = 1

    days = dayA - dayJ

    additionalYear = 0
    if (monthJ > monthA):
        monthA = monthA + 12
        additionalYear = 1

    months = monthA - (monthJ + monthAdditional)
    years = yearA - (yearJ + additionalYear)
    print(str(years) + " Years " + str(months) + " Months " + str(days) + " Days")
    result = str(years) + " Years " + str(months) + " Months " + str(days) + " Days"

    return result

"""""
def Years_of_experience(monthStr,Year):
    Year = int(Year)
    monthStr=monthStr.lower()
    monthInt=0
    if monthStr == 'january' or monthStr == 'jan':
        monthInt = 1

    elif monthStr == 'february' or monthStr == 'feb':
        monthInt = 2

    elif monthStr == 'march' or monthStr == 'mar':
        monthInt = 3

    elif monthStr == 'april' or monthStr == 'apr':
        monthInt = 4

    elif monthStr == 'may' or monthStr == 'jan':
        monthInt = 5

    elif monthStr == 'june' or monthStr == 'jun':
        monthInt = 6

    elif monthStr == 'july' or monthStr == 'jul':
        monthInt = 7

    elif monthStr == 'august' or monthStr == 'aug':
        monthInt = 8

    elif monthStr == 'september' or monthStr == 'sep':
        monthInt = 9

    elif monthStr == 'october' or monthStr == 'oct':
        monthInt = 10

    elif monthStr == 'november' or monthStr == 'nov':
        monthInt = 11

    elif monthStr == 'december' or monthStr == 'dec':
        monthInt = 12

    else:
        print("Error 404")

    day = 1
    star = date(Year, monthInt, day)
    today = date.today()
    result = today.year-star.year

    return result
"""""
   


