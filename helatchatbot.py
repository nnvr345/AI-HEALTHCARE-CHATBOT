import tkinter as tk
import webbrowser
import random
from tkinter import Canvas
import speech_recognition as sr


# Dictionary containing predefined responses for different user inputs
responses = {
    "hi": ["Hello!", "Hi there!", "Hey!"],
    "how are you": ["I'm doing well, thank you!", "Great, thanks for asking!"],
    "bye": ["Goodbye!", "See you later!", "Bye!"],
    "symptom checker": "Please input your symptoms separated by commas.",
    "book appointment": "Click here to book an appointment!",
    "disease information": "Please enter the disease name.",

}
# Database of symptoms, diseases, and medication information (for demonstration)

symptom_db = {
    "fever": {
        "description": "An elevated body temperature.",
        "related_diseases": [
            "common cold",
            "influenza",
            "COVID-19",
            "typhoid fever",
            "malaria",
        ],
        "medication": "Take rest and drink plenty of fluids.",
    },
    "cough": {
        "description": "Expelling air from the lungs with a sudden sharp sound.",
        "related_diseases": [
            "common cold",
            "influenza",
            "pneumonia",
            "bronchitis",
            "asthma",
            "COPD",
        ],
        "medication": "Use cough syrup and warm liquids.",
    },
    "headache": {
        "description": "A continuous pain in the head.",
        "related_diseases": [
            "migraine",
            "tension headache",
            "sinusitis",
            "cluster headache",
        ],
        "medication": "Take pain relievers and get enough sleep.",
    },
    "fatigue": {
        "description": "Feeling of extreme tiredness or lack of energy.",
        "related_diseases": [
            "anemia",
            "chronic fatigue syndrome",
            "fibromyalgia",
            "depression",
        ],
        "medication": "Rest, balanced diet, regular exercise.",
    },
    "nausea": {
        "description": "Feeling of discomfort in the stomach with an inclination to vomit.",
        "related_diseases": [
            "food poisoning",
            "viral gastroenteritis",
            "migraine",
            "pregnancy",
        ],
        "medication": "Stay hydrated, eat bland foods, medications if severe.",
    },
    "shortness of breath": {
        "description": "Difficulty in breathing; feeling of suffocation or tightness in the chest.",
        "related_diseases": [
            "asthma",
            "pneumonia",
            "COPD",
            "anxiety disorders",
            "heart failure",
        ],
        "medication": "Bronchodilators, inhalers, oxygen therapy as per cause.",
    },
    "abdominal pain": {
        "description": "Pain or discomfort felt in the area between the chest and pelvis.",
        "related_diseases": [
            "appendicitis",
            "gastroenteritis",
            "ulcers",
            "gallstones",
            "kidney stones",
        ],
        "medication": "Pain relievers, antibiotics if bacterial infection, surgery in severe cases.",
    },
    "joint pain": {
        "description": "Discomfort, aches, or soreness in any part of the body where two or more bones meet.",
        "related_diseases": ["arthritis", "fibromyalgia", "gout", "Lyme disease"],
        "medication": "Pain relievers, anti-inflammatory drugs, physical therapy.",
    },
    "dizziness": {
        "description": "A sensation of lightheadedness, unsteadiness, or faintness.",
        "related_diseases": ["vertigo", "dehydration", "anemia", "inner ear problems"],
        "medication": "Rest, hydration, medications as per the cause.",
    },
    "rash": {
        "description": "Change in the skin’s appearance, often characterized by redness, itching, or irritation.",
        "related_diseases": [
            "allergies",
            "eczema",
            "psoriasis",
            "measles",
            "chickenpox",
        ],
        "medication": "Topical creams, antihistamines, steroids as per the cause.",
    },
    "sore throat": {
        "description": "Pain, scratchiness, or irritation of the throat often worsened by swallowing.",
        "related_diseases": ["common cold", "flu", "strep throat", "mononucleosis"],
        "medication": "Rest, hydration, lozenges, pain relievers.",
    },
    "vomiting": {
        "description": "Forcefully expelling the stomach’s contents through the mouth.",
        "related_diseases": [
            "gastroenteritis",
            "food poisoning",
            "pregnancy",
            "viral infections",
        ],
        "medication": "Stay hydrated, eat bland foods, medications if severe.",
    },
    "diarrhea": {
        "description": "Frequent and watery bowel movements.",
        "related_diseases": [
            "food poisoning",
            "viral gastroenteritis",
            "bacterial infections",
            "IBS",
        ],
        "medication": "Stay hydrated, eat bland foods, medications if severe.",
    },
    "chest pain": {
        "description": "Pain or discomfort felt anywhere along the front of the body between the neck and upper abdomen.",
        "related_diseases": [
            "heart attack",
            "angina",
            "pneumonia",
            "GERD",
            "panic attack",
        ],
        "medication": "Depends on the cause; immediate medical attention for suspected heart issues.",
    },
    "back pain": {
        "description": "Pain felt in the back, which may originate from muscles, nerves, bones, or other structures in the spine.",
        "related_diseases": [
            "muscle strain",
            "herniated disc",
            "spinal stenosis",
            "kidney stones",
        ],
        "medication": "Rest, pain relievers, hot or cold therapy, physical therapy.",
    },
    "sweating": {
        "description": "Increased perspiration often due to heat, exercise, or emotional stress.",
        "related_diseases": [
            "hyperhidrosis",
            "menopause",
            "anxiety disorders",
            "infections",
        ],
        "medication": "Depends on the underlying cause; may involve antiperspirants or medical treatment.",
    },
    "swelling": {
        "description": "Enlargement or puffiness in a body part due to fluid retention or inflammation.",
        "related_diseases": ["injuries", "edema", "infections", "allergic reactions"],
        "medication": "Depends on the cause; may involve rest, elevation, compression, or medications.",
    },
    "muscle weakness": {
        "description": "Reduced strength or inability to exert force with muscles.",
        "related_diseases": [
            "muscle diseases",
            "neuromuscular disorders",
            "thyroid disorders",
        ],
        "medication": "Physical therapy, medication as per underlying condition.",
    },
    "vision problems": {
        "description": "Difficulties with sight, including blurriness, double vision, or vision loss.",
        "related_diseases": ["myopia", "cataracts", "glaucoma", "macular degeneration"],
        "medication": "Corrective lenses, surgery, medication as per eye condition.",
    },
    "irregular heartbeat": {
        "description": "Abnormal heart rhythm, palpitations, or sensations of skipped or extra heartbeats.",
        "related_diseases": [
            "arrhythmia",
            "heart disease",
            "anxiety",
            "thyroid disorders",
        ],
        "medication": "Depends on the cause; may involve medications or procedures.",
    },
    "swollen glands": {
        "description": "Enlargement or tenderness in the lymph nodes, often in the neck, armpits, or groin.",
        "related_diseases": ["infections", "cancers", "immune system disorders"],
        "medication": "Treat the underlying cause; may involve antibiotics or other medications.",
    },

}


# Expanded disease database
disease_db = {
    "common cold": {
        "description": "A viral infection affecting the nose and throat.",
        "medication": "Rest, hydration, over-the-counter cold medications.",
    },
    "influenza": {
        "description": "A highly contagious viral infection affecting the respiratory system.",
        "medication": "Rest, hydration, antiviral medications.",
    },
    "COVID-19": {
        "description": "A contagious viral infection caused by SARS-CoV-2.",
        "medication": "Isolation, medical care, vaccination.",
    },
    "typhoid fever": {
        "description": "A bacterial infection causing high fever, diarrhea, and abdominal pain.",
        "medication": "Antibiotics, hydration, rest.",
    },
    "malaria": {
        "description": "A mosquito-borne infectious disease causing fever, chills, and flu-like symptoms.",
        "medication": "Antimalarial drugs, prevention of mosquito bites.",
    },
    "pneumonia": {
        "description": "Infection that inflames air sacs in one or both lungs, which may fill with fluid.",
        "medication": "Antibiotics, oxygen therapy, rest.",
    },
    "bronchitis": {
        "description": "Inflammation of the lining of the bronchial tubes.",
        "medication": "Rest, hydration, cough medicine.",
    },
    "asthma": {
        "description": "A condition in which a person airways become inflamed, narrow, and swell, and produce extramucus.",
        "medication": "Inhalers, corticosteroids, long-term control medications.",
    },
    "COPD": {
        "description": "A chronic inflammatory lung disease that causes obstructed airflow.",
        "medication": "Bronchodilators, corticosteroids, oxygen therapy.",
    },
    "migraine": {
        "description": "A type of headache characterized by severe throbbing pain, often accompanied by nausea and sensitivity to light and sound.",
        "medication": "Pain relievers, rest in a quiet, dark room.",
    },
    "tension headache": {
        "description": "A common type of headache often related to stress or muscle tension.",
        "medication": "Pain relievers, relaxation techniques.",
    },
    "sinusitis": {
        "description": "Inflammation or swelling of the tissue lining the sinuses.",
        "medication": "Nasal decongestants, antibiotics (if bacterial), saline nasal spray.",
    },
    "cluster headache": {
        "description": "Severe headaches that occur in clusters, often on one side of the head.",
        "medication": "Oxygen therapy, sumatriptan injections, preventive medications.",
    },
    "anemia": {
        "description": "A condition in which there is a deficiency of red cells or of hemoglobin in the blood.",
        "medication": "Iron supplements, vitamin supplements, blood transfusions.",
    },
    "chronic fatigue syndrome": {
        "description": "A disorder characterized by extreme fatigue that does not improve with rest.",
        "medication": "Symptom-based treatment, lifestyle changes, therapy.",
    },
    "fibromyalgia": {
        "description": "A disorder characterized by widespread musculoskeletal pain, fatigue, and tenderness in localized areas.",
        "medication": "Pain relievers, antidepressants, physical therapy.",
    },
    "food poisoning": {
        "description": "Illness caused by consuming contaminated food or drink.",
        "medication": "Hydration, rest, anti-nausea medication if needed.",
    },
    "viral gastroenteritis": {
        "description": "Inflammation of the stomach and intestines caused by a virus.",
        "medication": "Hydration, rest, anti-diarrheal medication.",
    },
    "pregnancy": {
        "description": "State of carrying a developing embryo or fetus within the female body.",
        "medication": "Prenatal vitamins, regular check-ups.",
    },

}


# Function to open the appointment booking website
def open_appointment_website():
    # Replace this URL with the actual URL of the appointment booking website
    booking_url = "https://docpulse.com/products/online-doctor-appointment-app/"
    webbrowser.open_new(booking_url)


# Function to simulate symptom checking
def send_text_message(user_message):

    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, "You: " + user_message + "\n\n")

    if user_message == "exit":
        root.destroy()
    elif user_message in responses:
        chat_log.insert(
            tk.END, "ChatBot: " + random.choice(responses[user_message]) + "\n\n"
        )
    elif user_message.startswith("disease information"):
        disease_name = user_message.replace("disease information ", "")
        if disease_name in disease_db:
            response = f"Details for {disease_name}:\n"
            response += f"Description: {disease_db[disease_name]['description']}\n"
            response += f"Medication: {disease_db[disease_name]['medication']}\n\n"
        else:
            response = f"No information available for {disease_name}\n\n"
        chat_log.insert(tk.END, "ChatBot: " + response)
    elif "symptom checker" in user_message:
        chat_log.insert(tk.END, "ChatBot: " + responses["symptom checker"] + "\n\n")
        user_symptoms = user_message.replace("symptom checker ", "")
        symptoms_list = [symptom.strip() for symptom in user_symptoms.split(",")]
        response = check_symptoms(symptoms_list)
        chat_log.insert(tk.END, "ChatBot: " + response + "\n\n")
    elif user_message == "book appointment":
        chat_log.insert(tk.END, "ChatBot: " + responses[user_message] + "\n\n")
        open_appointment_website()
    else:
        chat_log.insert(
            tk.END,
            "ChatBot: I'm sorry, I didn't understand that. Please try again.\n\n",
        )

    chat_log.config(state=tk.DISABLED)
    chat_log.yview(tk.END)

# Function to simulate symptom checking
def check_symptoms(symptoms):
    matched_diseases = []
    medication_suggestions = []

    for symptom in symptoms:
        if symptom in symptom_db:
            matched_diseases.extend(symptom_db[symptom]["related_diseases"])
            medication_suggestions.append(symptom_db[symptom]["medication"])

    if matched_diseases:
        all_diseases = list(set(matched_diseases))
        response = ""

        for disease in all_diseases:
            if disease in disease_db:
                response += f"Details for {disease}:\n"
                response += f"Description: {disease_db[disease]['description']}\n"
                response += f"Medication: {disease_db[disease]['medication']}\n\n"
            else:
                response += f"No information available for {disease}\n\n"

        return response
    else:
        return "Your symptoms do not match any specific condition. Please consult a healthcare professional."


# Function to handle voice inputs
def send_voice_message():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Speak something.")
        audio = recognizer.listen(source)

    try:
        user_message_voice = recognizer.recognize_google(audio).lower()
        print(f"You said: {user_message_voice}")
        send_text_message(user_message_voice)  # Pass the recognized voice input to the text message handler
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError:
        print("Could not request results. Check your internet connection.")

def activate_voice_input():
    send_voice_message()

def send_message(event=None):
    user_message = user_input.get().lower()

    if user_message == 'exit':
        root.destroy()
    else:
        send_text_message(user_message)

# GUI setup
root = tk.Tk()
root.title("Medical ChatBot")
root.geometry("400x500")
root.configure(bg="#e0e0e0")

# Create a gradient background
canvas = Canvas(root, width=400, height=500)
canvas.pack()

canvas.create_rectangle(0, 0, 400, 500, fill="#87CEEB")  # Pik
canvas.create_rectangle(0, 0, 400, 250, fill="#87CEEB")  # Pink

# Create GUI components
chat_log = tk.Text(
    root,
    bd=0,
    bg="#ffffff",
    height="10",
    width=300,
    font=("Arial", 10),
    wrap="word",
    fg="#000000",
)
chat_log.config(state=tk.DISABLED)
scrollbar = tk.Scrollbar(root, command=chat_log.yview, cursor="arrow")
chat_log["yscrollcommand"] = scrollbar.set

user_input = tk.Entry(root, bd=0, bg="#ffffff", font=("Arial", 10), fg="#000000")
user_input.bind("<Return>", send_message)

# Updated button backgrounds to use #808000 color
send_button = tk.Button(
    root,
    text="Send",
    width="9",
    height="2",
    bd=0,
    bg="#adaeda",  # Updated button color
    activebackground="#adaeda",  # Updated active background color
    fg="#5d1717",
    font=("Arial", 10),
    command=send_message,
)

voice_button = tk.Button(
    root,
    text="Voice",
    width="9",
    height="2",
    bd=0,
    bg="#adaeda",  # Updated button color
    activebackground="#adaeda",  # Updated active background color
    fg="#5d1717",
    font=("Arial", 10),
    command=activate_voice_input,
)

appointment_button = tk.Button(
    root,
    text="Book Appointment",
    width="14",
    height="2",
    bd=0,
    bg="#adaeda",  # Updated button color
    activebackground="#adaeda",  # Updated active background color
    fg="#5d1717",
    font=("Arial", 10),
    command=open_appointment_website,
)

# Place components on the window
chat_log.place(x=6, y=6, height=386, width=388)
scrollbar.place(x=394, y=6, height=386)
user_input.place(x=6, y=401, height=40, width=390
)
send_button.place(x=320, y=450)  # Placed under the text input bar
voice_button.place(x=240, y=450)  # Placed under the text input bar
appointment_button.place(x=120, y=450)  # Placed under the text input bar

root.mainloop()
