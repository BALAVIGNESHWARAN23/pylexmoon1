import streamlit as st
import fitz  # PyMuPDF
import openai
from dotenv import load_dotenv
from google.cloud import translate_v2 as translate
import os
import base64
from PIL import Image

load_dotenv()

openai.api_key = os.getenv("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")
file_path = '/demo.txt'
file_path_tamil = '//Users/rishisundaram/Desktop/LawApp/tamiltext.txt'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("APP-CRED")




def read_pdf(file):
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

def write_to_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def write_to_file_tamil(file_path_tamil, content):
    with open(file_path_tamil, 'w', encoding='utf-8') as file:
        file.write(content)

def translate_text(text, target_language='ta'):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']


def main():
    st.set_page_config(
    page_icon=":gear:",
    layout="wide",
    initial_sidebar_state="expanded"
)



    
    st.title("Welcome to Lexmoon Summarizer")
    
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    submit_button = st.button("Submit")
    if uploaded_file is not None and submit_button:

        #Upload the PDF File
        pdf_text = read_pdf(uploaded_file)
        # st.title("PDF Content")
        # st.text_area('',pdf_text, height=400)


        #Summarize the PDF
        format_content = summarize_text(pdf_text)
        write_to_file(file_path,format_content)

        #Translate the Summary
        translate_text_tamil = translate_text(format_content)

        #Format the Tamil Content
        tamil_formatted_String = formatter(translate_text_tamil,format_content)
        write_to_file_tamil(file_path_tamil,tamil_formatted_String)

        #Print all the Content
        #st.text_area("Summarized content",format_content,height=400)
        #st.text_area("Translated content",translate_text_tamil,height=400)
        #st.text_area("Translated Content", tamil_formatted_String,height=300)

        col1, col2 = st.columns(2)
        with col1:
            st.title("English Summary")
            st.write(format_content)

        with col2:
            st.title("Tamil Summary")
            st.write(tamil_formatted_String)
            
        


def summarize_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": '''You are a document summarizer.. The document alone will be given in the user message. You should follow this rule:

The below mentioned flow describes the format in which the output passage should be
printed.
  ⁠a. The Case Title should be at the top of the output.
⁠  ⁠b. It should mention if it’s a petition or if it’s an appeal
⁠  ⁠c. Next comes the facts about this case which are the evidences, word of
mouth etc.,
⁠  ⁠d. then comes the issues that arise from the evidences and the reality check
⁠  ⁠e. In case of an appeal the judgements or previous hearings on this case is
reviewed. Also you must add the Judgement even though it might be the previous hearings.
⁠f. Next is the Judge’s observations on this case and the Laws applicable for this
case are reviewed over the observations.
⁠g. Then at the end the conclusion or the final judgement of this case is said at
the final point of this passage.
             
Try to avoid characters like * anywhere in the passage

Here is an example summary to be given as response. The response alone should be given with no additional content or explanation.:
Case: Anirudh Kumar Dwivedi and another vs. Principal Judge, Family Court and another


In the case of Anirudh Kumar Dwivedi and another vs. Principal Judge, Family Court and another, the petitioners challenged the order of the Principal Judge, Family Court, Allahabad dated 9.11.2011. The case revolves around a marriage that took place on 7.7.1997 between the petitioners, who later filed for dissolution of marriage due to allegations of cruelty and dowry demands. Concurrently, criminal cases under various sections of the IPC and the Dowry Prohibition Act were initiated.

Following an FIR against petitioner no.1, the case was referred to the Mediation & Conciliation Centre by the High Court, where the parties agreed to a mutual divorce and settled on a permanent alimony of Rs. 3,00,000/- for the wife. This compromise was filed as part of the ongoing divorce petition in the Family Court. Despite this, the Family Court delayed in issuing a decree of divorce, leading the petitioners to file multiple writ petitions under Article 227 of the Constitution, seeking directives for the Family Court to comply with the compromise.

Despite a clear directive from the High Court to finalize the divorce based on the compromise, the Principal Judge, Family Court, persisted in unnecessary procedural delays and inconsistencies, including referring the case to Lok Adalat and requiring an amendment application. Eventually, the Principal Judge used a Supreme Court ruling in Anil Kumar Jain vs. Maya Jain to justify a six-month waiting period post-amendment, disregarding the compromise agreement and prior High Court orders.

The High Court, expressing frustration with the Family Court's actions, reiterated that the mandatory six-month period should be considered from the date the compromise application was filed (17.4.2010), which had already elapsed by the time of its orders on 28.7.2011 and 18.10.2011. The High Court condemned the Principal Judge's disregard for judicial directives and mandated that the Family Court decide the case based on the compromise within one month from the presentation of the certified order. Consequently, the impugned order dated 19.11.2011 was set aside, and the write petition was allowed.

'''},
            {"role": "user", "content": text}
        ],
        max_tokens=1500  # Adjust this based on how detailed you want the summary to be
    )
    return response['choices'][0]['message']['content']





def formatter(tamil_text, english_text):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f'''
You are responsible for formatting content that is given to you. You will be give a Tamil summary and an Englisgh summary as well.
This is the english summary {english_text}
You have to compare both of these texts and bring the tamil translation to the same exact format as the english one. Remeber they both
the same content but in different languages. Remove the * symbol before giving the output.

For Example this is the order in which it should be:
a.first the case would be displayed with the heading வழக்கு:
b.second comes the tamil translation of either Appleal or a Petition as mentioned in the english text and also it should be in a seperate line.
c.The Facts are then printed under the heading உண்மைகள்:
d.The issues are displayed under the heading சிக்கல்கள்: 
e.The hearing or Judgements all must be displayed under the heading தீர்ப்புகள்:
f.All the judges observations are under the heading நீதிபதியின் அவதானிப்புகள்: 
g.All the Laws reviewed are under மறு ஆய்வு செய்யப்பட்ட சட்டங்கள்: 
h.Conclusion is always under the heading முடிவு: 

'''},
            {"role": "user", "content": tamil_text}
        ],
        max_tokens=1500  # Adjust this based on how detailed you want the summary to be
    )
    return response['choices'][0]['message']['content']

 

if __name__ == "__main__":
    main()



st.markdown(
    r"""
    <style>
    .stDeployButton {
            visibility: hidden;
        }
    </style>
    """, unsafe_allow_html=True
)
