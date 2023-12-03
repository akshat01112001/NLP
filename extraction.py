# from tika import parser
# import pandas as pd

# def extract_text_from_resume(file):
#     # Read the resume file using Tika parser
#     parsed_data = parser.from_file(file)

#     # Extract the text content
#     text = parsed_data['content']

#     return text

# if __name__=='__main__':
#     extract_text_from_resume()

from tika import parser

def extract_resume_data(file_path):
    try:
        parsed_resume = parser.from_file(file_path)
        resume_text = parsed_resume["content"]
        
        # You can extract metadata if needed
        metadata = parsed_resume["metadata"]

        return resume_text, metadata
    except Exception as e:
        print("Error:", str(e))
        return None, None

if __name__ == "__main__":
    file_path = "CV.pdf"  # Replace with the path to your resume file.
    resume_text, metadata = extract_resume_data(file_path)

    if resume_text:
        print("Resume Text:")
        print(resume_text.strip())

    # if metadata:
    #     print("Metadata:")
    #     for key, value in metadata.items():
    #         print(f"{key}: {value}")
