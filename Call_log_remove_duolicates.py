import pytesseract
from PIL import ImageGrab
import time
import datetime
import logging


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure pytesseract path to where the Tesseract executable is located
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\omagdysa\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def capture_and_read_captions(area):
    try:
        # Capture a specific screen area
        screenshot = ImageGrab.grab(bbox=area)
        # Use OCR to extract text
        text = pytesseract.image_to_string(screenshot)
        return text.strip()
    except Exception as e:
        logging.error(f"Error capturing or reading captions: {e}")
        return ""

def remove_duplicates(input_file, output_file):
    # Step 1: Open the input file in read mode
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    # Step 2: Use a list to store unique lines while maintaining order
    seen_lines = set()
    unique_lines = []
    for line in lines:
        if line not in seen_lines:
            seen_lines.add(line)
            unique_lines.append(line)
    
    # Step 3: Add empty lines before specific keywords
    unique_lines = add_empty_line_before_keywords(unique_lines)
    
    # Step 4: Write the unique lines to the output file
    with open(output_file, 'w') as file:
        file.writelines(unique_lines)

def add_empty_line_before_keywords(lines):
    keywords = ["(External)", "(Nokia)"]
    modified_lines = []
    for line in lines:
        if any(keyword in line for keyword in keywords):
            modified_lines.append("\n")  # Add an empty line
        modified_lines.append(line)
    return modified_lines

def get_screen_area():
    print("Enter the screen area coordinates where captions appear.")
    print("Recommended default values: left_x=100, top_y=800, right_x=1800, bottom_y=1000")
    
    left_x = int(input("Enter left_x (default 100): ") or 100)
    top_y = int(input("Enter top_y (default 800): ") or 800)
    right_x = int(input("Enter right_x (default 1800): ") or 1800)
    bottom_y = int(input("Enter bottom_y (default 1000): ") or 1000)

    return (left_x, top_y, right_x, bottom_y)

def main():
    # Prompt user to enter screen area coordinates
    caption_area = get_screen_area()
    sleep_interval = 1  # seconds
    last_caption = ""

    current_date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    raw_file_path = f"D:\\Autmation\\Call-Log_{current_date}_raw.txt"
    processed_file_path = f"D:\\Autmation\\Call-Log_{current_date}.txt"

    try:
        with open(raw_file_path, "a") as file:
            logging.info("Script started. Press Ctrl+C to stop.")
            while True:
                captions = capture_and_read_captions(caption_area)
                if captions and captions != last_caption:
                    print(captions)
                    file.write(captions + "\n")
                    last_caption = captions
                time.sleep(sleep_interval)
    except KeyboardInterrupt:
        logging.info("Script stopped by user.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

    # Process the raw file to remove duplicates and add empty lines before specific keywords
    remove_duplicates(raw_file_path, processed_file_path)
    print(f"Processed file saved at: {processed_file_path}")

if __name__ == "__main__":
    main()
    input("Press Enter to exit...")