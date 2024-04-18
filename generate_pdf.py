from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
import re

# Define styles
styles = getSampleStyleSheet()
title_style = styles["Title"]
title_style.fontSize = 16
title_style.alignment = TA_CENTER
body_style = styles["BodyText"]
code_style = ParagraphStyle(name='Code', fontName='Courier', fontSize=10, textColor=colors.blue)

# Create PDF
def create_pdf(file_path):
    c = canvas.Canvas("python_cheat_sheet.pdf", pagesize=letter)
    width, height = letter
    format_text(file_path, c, height)
    c.save()

def get_code_snippets(content):
    codes = []
    pattern = re.compile(r'\d+\..*?(?=\n\d+\.|\bWorking\b)', re.DOTALL)
    matches = pattern.findall(content)
    for match in matches:
        # Remove section numbering and title
        code_snippet = re.sub(r'^\d+\..*?\n|([A-Z].*?:.*?\n)|(\n)+$', '', match)
        codes.append(code_snippet.strip())
    return codes

def write_title(title, c, height):
    c.setFont(title_style.fontName, title_style.fontSize)
    c.drawString(50, height, title)

def write_subtitle(subtitle, c, height):
    c.setFont(title_style.fontName, title_style.fontSize - 2)
    c.setFillColor(colors.red)  # Set the fill color to red
    subtitle_height = 30  # Adjust this value as needed
    c.drawString(30, height - subtitle_height, subtitle)
    c.setFillColor(colors.black)  # Reset the fill color to black
    return subtitle_height

def write_subtitle_item(subtitle_item, c, height):
    c.setFont(title_style.fontName, body_style.fontSize + 3)
    c.setFillColor(colors.green)  # Set the fill color to green
    subtitle_item_height = 20  # Adjust this value as needed
    c.drawString(50, height - subtitle_item_height, subtitle_item)
    c.setFillColor(colors.black)  # Reset the fill color to black
    return subtitle_item_height

def write_code_snippet(c, code, height, code_width=100):
    c.setFont(code_style.fontName, code_style.fontSize)
    c.setFillColor(colors.blue)  # Set the fill color to blue
    code_height = 15  # Adjust this value as needed
    c.drawString(code_width, height - code_height, code)
    c.setFillColor(colors.black)  # Reset the fill color to black
    return code_height

def write_comment(c, comment, height):
    c.setFont(body_style.fontName, body_style.fontSize)
    c.setFillColor(colors.black)  # Set the fill color to orange
    comment_height = 20  # Adjust this value as needed
    c.drawString(20, height - comment_height, comment)
    c.setFillColor(colors.black)  # Reset the fill color to black
    return comment_height


def format_text(file_path, c, height):
    subtitle_pattern = r'^Working.*(?<!:)$'  # Pattern to match lines starting with 'Working'
    subtitle_item_pattern = r'^\d+.'
    pattern = r"^\s{4}.+"

    with open(file_path, "r", encoding='utf-8') as file:
        content = file.read()
        code_snippets = get_code_snippets(content)
        lines_of_code = []
        for snippet in code_snippets:
            lines_of_code.extend(snippet.split('\n'))

                
        lines = content.split("\n")
        title_height = letter[1] - 50
        lines_per_page = 35  # Number of lines per page
        current_line = 0  # Counter to keep track of the current line
        current_page = 1  # Counter to keep track of the current page

        initial_height = letter[1] - 80  # Initial height for text content
        write_title(lines[0], c, title_height)

        height = initial_height  # Set the height to the initial height

        for line in lines[6: len(lines) - 5]:
            if current_line >= lines_per_page:  # Check if the current page is full
                c.showPage()  # Start a new page
                current_page += 1
                height = initial_height  # Reset the height to the initial height for the new page
                write_title(lines[0], c, title_height)  # Rewrite the title on the new page
                current_line = 0  # Reset the current line counter for the new page

            if re.match(subtitle_pattern, line):
                subtitle_height = write_subtitle(line, c, height)
                height -= subtitle_height
            elif re.match(subtitle_item_pattern, line):
                subtitle_item_height = write_subtitle_item(line, c, height)
                height -= subtitle_item_height
            elif line.strip() in lines_of_code or re.match(pattern, line):
                code_height = write_code_snippet(c, line, height, code_width=100)
                height -= code_height
                
            else:
                comment_height = write_comment(c, line, height)
                height -= comment_height

            current_line += 1


create_pdf("article.txt")
