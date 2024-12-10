# Web scraping with BeautifulSoup

import PyPDF2
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd  

def scrape_iframe_page(main_url):
    """
    Scrapes an HTML page for course details by fetching iframe content.

    Args:
        main_url (str): URL of the main page containing the iframe.

    Returns:
        pd.DataFrame: A DataFrame containing course details.
    """
    try:
        # Fetch the main page
        response = requests.get(main_url)
        if response.status_code != 200:
            print(f"Failed to fetch main page. Status code: {response.status_code}")
            return pd.DataFrame()

        # Parse the main page and find the iframe source
        soup = BeautifulSoup(response.text, 'html.parser')
        iframe = soup.find('iframe')
        if not iframe or 'src' not in iframe.attrs:
            print("No iframe found or iframe src missing.")
            return pd.DataFrame()

        iframe_url = iframe['src']

        # Fetch the iframe content
        iframe_response = requests.get(iframe_url)
        if iframe_response.status_code != 200:
            print(f"Failed to fetch iframe content. Status code: {iframe_response.status_code}")
            return pd.DataFrame()

        # Parse the iframe content
        iframe_soup = BeautifulSoup(iframe_response.text, 'html.parser')
        course_data = []

        # Find the table(s) and extract rows
        tables = iframe_soup.find_all('table', class_='table table-striped')
        for table in tables:
            rows = table.find_all('tr')[1:]  # Skip the header row
            for row in rows:
                cells = row.find_all('td')
                if len(cells) < 4:  # Ensure the row has enough cells
                    continue
                name = cells[0].text.strip()
                crn = cells[1].text.strip()
                timing = cells[2].text.strip()
                instructor = cells[3].text.strip()
                course_data.append({
                    'Course Name': name,
                    'CRN': crn,
                    'Instructor': timing,
                    'Timings': instructor
                })

        # Convert to a DataFrame
        df = pd.DataFrame(course_data)
        # Filter rows to keep only up to and including the target course name
        target_course_name = "TELE 5330-01 Data Networking"
        df = df.loc[:df[df["Course Name"] == target_course_name].index[-1]]
        return df

    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()

# Example Usage
main_url = 'http://newton.neu.edu/spring2025/'
courses_df = scrape_iframe_page(main_url)

# Check if the DataFrame has content
if not courses_df.empty:
    print("\nExtracted Course Data:\n")
    print(courses_df.to_string(index=False))  # Pretty print without indices
else:
    print("No course data found.")


# Split the 'Course Name' column into 'CourseID' and the rest of the name
courses_df['CourseID'] = courses_df['Course Name'].str.extract(r'(^[A-Z]+ \d{4})')
courses_df['Course Name'] = courses_df['Course Name'].str.replace(r'^[A-Z]+ \d{4}-\d{2} ', '', regex=True)
# Display the updated DataFrame
courses_df.head()

def extract_and_clean_pdf_text(pdf_path):
    """
    Extracts text from a PDF, cleans it by removing unwanted lines,
    and normalizes spaces.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Cleaned and filtered text content from the PDF.
    """
    cleaned_text = ""

    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:
                # Extract text from the page
                page_text = page.extract_text()

                # Step 1: Remove lines containing unwanted patterns
                cleaned_lines = [
                    line for line in page_text.splitlines()
                    if not (
                        "Prerequisite(s)" in line or
                        "Corequisite(s)" in line or
                        "minimum grade of" in line or
                        ("of B-" in line.strip() and len(line.strip()) <= 10)
                    )
                ]

                # Step 2: Normalize spaces (replace non-breaking spaces with regular spaces)
                normalized_lines = [line.replace("\u00A0", " ") for line in cleaned_lines]

                # Append the cleaned text for the current page
                cleaned_text += "\n".join(normalized_lines) + "\n"

    except Exception as e:
        print(f"An error occurred: {e}")

    return cleaned_text


def extract_course_description(course_id, pdf_text):
    """
    Extracts the course description for the given course_id from the cleaned PDF text.
    Stops at the start of the next course (e.g., lines starting with INFO, CSYE, DAMG, etc.).

    Args:
        course_id (str): The course ID to search for.
        pdf_text (str): The cleaned text content of the PDF.

    Returns:
        str: The course description, or "Description not found" if the course ID is not found.
    """
    # Find the start of the course description
    start_index = pdf_text.find(course_id)
    if start_index != -1:
        # Extract text from start_index onward
        subsequent_text = pdf_text[start_index:]

        # Find the next course ID using a regex
        match = re.search(r"\n(INFO|CSYE|DAMG)\s", subsequent_text)
        end_index = match.start() if match else len(subsequent_text)

        # Extract the relevant description
        description = subsequent_text[:end_index]

        # Remove the course ID and title from the description
        description = description.split("\n", 1)[-1].strip()
        return description
    return "Description not found"


# Example usage
pdf_path = "/content/sample_data/CourseDescriptions.pdf"
cleaned_pdf_text = extract_and_clean_pdf_text(pdf_path)

# Optional: Save cleaned text to a .txt file
output_txt_path = "/content/sample_data/CleanedCourseDescriptions.txt"
with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
    txt_file.write(cleaned_pdf_text)

print(f"Cleaned PDF text has been saved to {output_txt_path}")

# Extract course descriptions using the cleaned PDF text
courses_df["Course Description"] = courses_df["CourseID"].apply(lambda x: extract_course_description(x, cleaned_pdf_text))


# Save the extracted data to a CSV file
output_csv_path = "/content/sample_data/ExtractedCourseDescriptions.csv"
courses_df.to_csv(output_csv_path, index=False, encoding='utf-8')

print(f"Extracted course descriptions have been saved to {output_csv_path}")