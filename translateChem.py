from translate import Translator

def translate(chem, language):
    translator = Translator(to_lang=language)
    translation = translator.translate(chem)
    return(translation)