import streamlit as st
import re
import google.generativeai as genai

class ielts_generator:
    def __init__(self):
        self.ielts_content = "<html><head><style>body {font-family: Arial, sans-serif;}</style></head><body>"
        
    def add_heading(self, text, level=1):
        self.ielts_content += f"<h{level} style='color: #333333;'>{text}</h{level}>"
    
    def add_paragraph(self, text):
        self.ielts_content += f"<p>{text}</p>"
        
    def generate_content(self, prompt_parts):
        genai.configure(api_key="AIzaSyDx7Vykf8bDqi5tLZlsr0HKi0xEKnnhzL4")  # Replace with your actual API key

        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]

        model = genai.GenerativeModel(model_name="gemini-pro",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)

        response = model.generate_content(prompt_parts)
        return response.text
    
    def save_ielts(self):
        # Apply CSS styles to the generated text
        self.ielts_content += "<div style='font-family: Arial, sans-serif; color: #333333;'>"
        self.ielts_content += "</div></body></html>"
        return self.ielts_content

def validate_email(email):
    email_regex = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$"
    return bool(re.match(email_regex, email))

# Custom CSS
custom_css = """
<style>
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
}
.container {
    max-width: 800px;
    margin: 50px auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 10px;
    background-color: #f9f9f9;
}
.title {
    text-align: center;
    text-transform: uppercase;
}
.button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 10px;
}
.button:hover {
    background-color: #45a049;
}
</style>
"""
logo_html = """
<div style='text-align: center;'>
    <img src='sir_sami.jpg' alt='Sir Sami Logo' style='width: 200px; height: auto;'/>
</div>
"""
st.markdown(logo_html, unsafe_allow_html=True)
            
st.markdown(custom_css, unsafe_allow_html=True)

st.markdown("<h1 class='title'>Sir Sami Ielts Expert</h1>", unsafe_allow_html=True)

st.markdown("<h8 class='title'>for more info please contact # 0345-3153330</h8>", unsafe_allow_html=True)

name = st.text_input("Please enter your full name:")
email_address = st.text_input("Please enter your email address:")
phone = st.text_input("Please enter your phone number (optional):")
ielts_prompt = st.text_input("Ask Anything About IELTS")

if st.button("Generate IELTS Info"):
    if not name or not email_address:
        st.warning("Name and email address are required.")
    elif not validate_email(email_address):
        st.warning("Invalid email format. Please enter a valid email address.")
    else:
        with st.spinner("Generating your IELTS information..."):
            info_generator = ielts_generator()
            info_generator.add_heading(name, level=1)
            info_generator.add_paragraph(f"Contact Information:")
            info_generator.add_paragraph(f"* Email: {email_address}")
            info_generator.add_paragraph(f"* Phone: {phone}")

            try:
                ielts_prompt = info_generator.generate_content(ielts_prompt)
                
                # Check if the generated content is related to IELTS
                if "IELTS" in ielts_prompt:
                    info_generator.add_heading("IELTS", level=2)
                    info_generator.add_paragraph(ielts_prompt.strip())

                    ielts_content = info_generator.save_ielts()
                    st.subheader("Generated IELTS Content")
                    st.markdown(ielts_content, unsafe_allow_html=True)
                else:
                    st.warning("Your data is not related to IELTS.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

st.markdown("</div>", unsafe_allow_html=True)
