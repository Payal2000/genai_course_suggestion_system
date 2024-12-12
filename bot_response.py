from connections import openai_connection, pinecone_connection
from pinecone import Pinecone
from openai import OpenAI

def fetch_from_pinecone(skills: list):
    '''
    Function to fetch data from Pinecone and generate markdown table.
    '''
    try:
        # Pinecone
        pinecone_api_key, index_name = pinecone_connection()
        pinecone = Pinecone(api_key=pinecone_api_key)

        # OpenAI
        api_key = openai_connection()
        model = OpenAI(api_key=api_key)

        skills = str(skills)

        # Fetching data from Pinecone
        index = pinecone.Index(name=index_name)

        xq = model.embeddings.create(
            input=skills,
            model='text-embedding-ada-002',
        ).data[0].embedding

        courses = index.query(vector=xq, top_k=3, include_metadata=True)

        # Generate markdown table format programmatically
        markdown_output = []

        for course in courses['matches']:
            metadata = course['metadata']
            course_id = metadata['Course ID']
            course_name = metadata['Course Name']
            score = round(course['score'] * 100, 2)
        
            markdown_output.append(f"### {course_id}: {course_name}\n")
            markdown_output.append(f"**Score:** {score}%\n")
            markdown_output.append("| Instructor | Timings | CRN |")
            markdown_output.append("|------------|---------|-----|")
            for instructor, timing, crn in zip(metadata['Instructors'], metadata['Timings'], metadata['CRNs']):
                markdown_output.append(f"| {instructor} | {timing} | {crn} |")
            markdown_output.append("\n")

        markdown_result = "\n".join(markdown_output)

        # Return both matches and markdown for frontend display
        return courses['matches'], markdown_result

    except Exception as e:
        print("Exception in fetch_from_pinecone() function: ", e)
        return None, "failed"


def generate_response(question: str, context: str):
    '''
    Function to generate response from OpenAI using provided context.
    '''
    try:
        # OpenAI
        api_key = openai_connection()
        openai_client = OpenAI(api_key=api_key)

        # Prompt to OpenAI for generating analysis of the question
        prompt = f"Answer the question based on the recommendations provided in the context below. Answer in a professional manner without stating that context is involved.\n\nContext:\n{
            context}\n\nQuestion: {question}\n"

        # Generate response from OpenAI
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.0,
            max_tokens=1024,
        )

        # Extract and return the generated analysis from the response
        analysis = response.choices[0].message.content

        return analysis

    except Exception as e:
        print("Exception in generate_response() function: ", e)
        return "Failed to generate response."


if __name__ == "__main__":
    
    # Step 1: Fetch courses and display markdown on frontend
    skills = ['machine learning', 'data science', 'programming']
    matches, markdown_result = fetch_from_pinecone(skills)

    if markdown_result != "failed":
        print("Displaying Markdown Table:\n")
        # This will go to the frontend in a real application
        print(markdown_result)
    
    '''
    # Step 2: User asks a question
    question = "Does the best course teach fundamentals of leetcode?"
    # Use markdown result as context for the query
    response = generate_response(question, matches)

    print("Generated Response:\n")
    print(response)
    '''