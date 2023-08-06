
def cleanText(text):
    text = text
    text = text.replace(',', '')
    text = text.replace('\r', ' ')
    text = text.replace('\n', ' ')
    text = text.replace('\n\n', ' ')
    text = text.replace('\\n', ' ')
    text = text.replace('\\n\\n', ' ')
    text = text.replace(':&nbsp;', ' ')
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&gt;', '>')
    text = text.replace('&lt;', '<')
    text = text.replace('&eacute;', 'e')
    text = text.replace('&ecirc;', 'e')
    text = text.replace('&egrave;', 'e')
    text = text.replace('souffrance', '')
    text = text.replace('Merci', '')
    text = text.strip()

    return text
