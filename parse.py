import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Google Generative AI with the API key
genai.configure(api_key=API_KEY)

def parse_with_gemini(dom_chunks, parse_description):
    """Parse content with Gemini model."""
    parsed_results = []
    try:
        # Initialize the model
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

        # Process each chunk with the user's parse description
        for i, chunk in enumerate(dom_chunks, start=1):
            prompt = f"{parse_description}\n\nContent:\n{chunk}"

            # Generate the response
            response = model.generate_content(prompt)
            
            # Collect and append the result
            result = response.text if response else ""
            parsed_results.append(result)
            print(f"Parsed batch {i} of {len(dom_chunks)}")

    except Exception as e:
        print(f"An error occurred during Gemini parsing: {str(e)}")
        parsed_results.append(f"Error: {str(e)}")

    # Join all parsed results into a single string for display
    return "\n".join(parsed_results)
