'''
This module combines the website hosted in htdocs into a single exportable HTML archive
'''

from tqdm import tqdm

# Load in primary HTML
with open('launcher_code.html', 'r', encoding='utf8') as file:
    lines = file.readlines()

def load_stylesheet(html_line) -> str:
    '''
    This takes in an external stylesheet line from an HTMl doc
    and returns the CSS associated with that stylesheet
    :return: The css stylesheet referenced in line
    '''
    file_path = html_line.split('href=\"')[1]
    file_path = file_path.split('\"')[0]
    return open(file_path, 'r', encoding='utf-8', errors='ignore').read()

def load_script(html_line):
    '''
    This takes in an external JS script reference from an HTML doc
    and returns the JS associated with that stylesheet
    :return: The JS stylesheet referenced in line
    '''
    file_path  = html_line.split('src=\"')[1]
    file_path = file_path.split('\"')[0]
    return open(file_path, 'r', encoding='utf-8', errors='ignore').read()

# Scan for CSS and JS
out_lines = []
print('Merging Files...')
for line in tqdm(lines):
    if 'rel="stylesheet"' in line:
        out_lines.append('\n<!-- START INSERTION  -->\n')
        stylesheet = "<style>\n" + load_stylesheet(line) + "\n</style>\n"
        out_lines.append(stylesheet)
        out_lines.append('\n<!-- END INSERTION  -->\n')
    elif '<script' in line and 'src' in line:
        out_lines.append('\n<!-- START INSERTION  -->\n')
        out_lines.append('<script>\n' + load_script(line) + '\n</script>\n')
        out_lines.append('\n<!-- END INSERTION  -->\n')
    else:
        out_lines.append(line)

# Write script to file
print("Writing to file...")
with open('launcher_code_archive.html', 'w', encoding='utf-8', errors='ignore') as f:
    for line in out_lines:
        f.write(line)
