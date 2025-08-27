# A script to clean up Notion's HTML exports for publishing on GitHub Pages.
# It organizes image files, removes inline CSS, and links to an external stylesheet.


import os
import sys
import shutil
from bs4 import BeautifulSoup

def process_html(html_path, output_path, media_dir_name="media"):
    """
    Parses an HTML file to move styles to an external sheet and update image links.

    Args:
        html_path (str): Path to the input index.html file.
        output_path (str): Path to save the processed index.processed.html file.
        media_dir_name (str): The name of the subdirectory for images.
    """
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        # 1. Find and remove all inline <style> tags
        soup.find_all('style')[0].decompose()
        print("Removed an inline <style> block.")

        # 2. Add a link to an external stylesheet in the <head>
        head = soup.head
        if head:
            new_stylesheet_link = soup.new_tag('link', rel='stylesheet', href='style.css')
            head.append(new_stylesheet_link)
            print("Added link to external 'style.css'.")
        else:
            print("Warning: <head> tag not found. Could not add stylesheet link.")

        # 3. Update all image sources to point to the new media directory
        for img_tag in soup.find_all('img'):
            original_src = img_tag.get('src', '')
            if original_src and not original_src.startswith(('http://', 'https://')):
                # Create the new path by joining the media directory and the original filename
                img_filename = os.path.basename(original_src)
                new_src = os.path.join(media_dir_name, img_filename).replace('\\', '/')
                img_tag['src'] = new_src
                print(f"Updated image source: '{original_src}' -> '{new_src}'")

        # 4. Write the modified HTML to the output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"\nSuccessfully created processed file: {output_path}")

    except FileNotFoundError:
        print(f"Error: The file '{html_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred during HTML processing: {e}")

def main():
    """
    Main function to handle file operations and orchestrate the processing.
    """
    # Check for command-line argument
    if len(sys.argv) < 2:
        print("Error: Please provide the directory path as an argument.")
        print("Example usage: python process_file.py ./pages/")
        sys.exit(1)

    input_dir = sys.argv[1]

    # Validate the directory path
    if not os.path.isdir(input_dir):
        print(f"Error: The path '{input_dir}' is not a valid directory.")
        sys.exit(1)

    # Define paths
    media_dir_name = "media"
    media_dir_path = os.path.join(input_dir, media_dir_name)
    html_file_path = os.path.join(input_dir, "index.html")
    output_html_path = os.path.join(input_dir, "index.html")

    # Create the media subdirectory if it doesn't exist
    os.makedirs(media_dir_path, exist_ok=True)
    print(f"Ensured media directory exists at: {media_dir_path}")

    # Supported image file extensions
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')

    # Move all image files to the /media subdirectory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(image_extensions):
            source_path = os.path.join(input_dir, filename)
            destination_path = os.path.join(media_dir_path, filename)
            try:
                shutil.move(source_path, destination_path)
                print(f"Moved '{filename}' to '{media_dir_name}/'")
            except Exception as e:
                print(f"Could not move '{filename}'. Reason: {e}")

    # Process the HTML file
    if os.path.exists(html_file_path):
        process_html(html_file_path, output_html_path, media_dir_name)
    else:
        print(f"Error: 'index.html' not found in the directory '{input_dir}'.")

if __name__ == "__main__":
    main()
