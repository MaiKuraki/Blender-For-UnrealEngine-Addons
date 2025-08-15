import bpy
import json
import os
from os import listdir
from os.path import isfile, join
from typing import Dict, Optional, Tuple
import importlib
from . import config
from . import utils

if "bpl" in locals():
    importlib.reload(config)
if "bbpl" in locals():
    importlib.reload(utils)

tooltips_dictionary: Dict[str, str] = {}
interface_dictionary: Dict[str, str] = {}
new_data_dictionary: Dict[str, str] = {}
current_language = ""


def UpdateDict(local: str, tooltips: bool = True, interface: bool = True, new_data: bool = True):
    # Try to found lang file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    lang_path = os.path.join(dir_path, "old_local_list")
    onlyfiles = [f for f in listdir(lang_path) if isfile(join(lang_path, f))]

    for file in onlyfiles:
        if file == local+".json":
            with open(os.path.join(lang_path, file)) as json_file:
                data = json.load(json_file)

                if tooltips:
                    for key, value in data['tooltips'].items():
                        tooltips_dictionary[key] = value

                if interface:
                    for key, value in data['interface'].items():
                        interface_dictionary[key] = value

                if new_data:
                    for key, value in data['new_data'].items():
                        new_data_dictionary[key] = value


def InitLanguages(locale: str):
    if bpy.context:
        prefs = bpy.context.preferences
        view = prefs.view

        tooltips_dictionary.clear()
        interface_dictionary.clear()
        new_data_dictionary.clear()

        UpdateDict("en_US")  # Get base lang
        # Update base lang with local lang if file exist
        UpdateDict(locale, view.use_translate_tooltips, view.use_translate_interface, view.use_translate_new_dataname)

def CheckCurrentLanguage():
    from bpy.app.translations import locale  # Change with language
    if current_language != locale:
        InitLanguages(locale)

# Translate function
def Translate_Tooltips(phrase: str) -> str:
    """
    Translate the give phrase into Blender’s current language.
    """
    CheckCurrentLanguage()

    if phrase in tooltips_dictionary:
        return tooltips_dictionary[phrase]
    else:
        print("Error, in languages text ID not found: " + phrase)
        return phrase

def Translate_Interface(phrase: str) -> str:
    """
    Translate the give phrase into Blender’s current language.
    """
    CheckCurrentLanguage()

    if phrase in interface_dictionary:
        return interface_dictionary[phrase]
    else:
        print("Error, in languages text ID not found: " + phrase)
        return phrase

def Translate_NewData(phrase: str) -> str:
    """
    Translate the give phrase into Blender’s current language.
    """
    CheckCurrentLanguage()

    if phrase in new_data_dictionary:
        return new_data_dictionary[phrase]
    else:
        print("Error, in languages text ID not found: " + phrase)
        return phrase

def tt(phrase: str) -> str:
    return Translate_Tooltips(phrase)

def ti(phrase: str) -> str:
    return Translate_Interface(phrase)

def td(phrase: str) -> str:
    return Translate_NewData(phrase)



# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    translations_dict: Optional[Dict[str, Dict[Tuple[Optional[str], str], str]]] = utils.construct_translations_dict()
    bpy.app.translations.register(__name__, translations_dict)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    bpy.app.translations.unregister(__name__)