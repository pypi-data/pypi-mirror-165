from bs4 import BeautifulSoup

def replace_html(file_path, var_name, new_value):
    try:
        new_text = ''
        # Open html file for reading
        with open(file_path) as html_file:
            soup = BeautifulSoup(html_file.read(), features='html.parser')
            new_text = []
            for content in soup.contents:
                new_text.append(str(content).replace(var_name, new_value))
            new_text = '\n'.join(new_text)
        # Write new contents to html file
        with open(file_path, mode='w') as new_html_file:
            new_html_file.write(new_text)

        return True, new_text
    except Exception as e:
        msg = str(e)
        return False, msg