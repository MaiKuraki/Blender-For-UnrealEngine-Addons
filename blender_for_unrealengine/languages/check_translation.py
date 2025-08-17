# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------

import bpy

class skeleton_member_bones():
    def __init__(self, name: str, bones: list[str]):
        self.name = name
        self.bones = bones

    def get_name(self):
        return self.name

    def get_bones(self):
        return self.bones

class skeleton_data():
    def __init__(self, armature: bpy.types.Object):
        self.members = {}
        self.armature = armature

    def add_member(self, name: str, bones: list[str]):
        self.members[name] = skeleton_member_bones(name, bones)

    def get_armature(self) -> bpy.types.Object:
        return self.armature

    def get_members(self) -> list[skeleton_member_bones]:
        return self.members
    
    def get_selected_body_members(self) -> list[skeleton_member_bones]:
        result_members = []
        if self.armature:
            selected_bones = bpy.context.selected_pose_bones 
            if selected_bones:
                for bone in selected_bones:
                    for member_key in self.members:
                        member = self.members[member_key]
                        member: skeleton_member_bones
                        if member not in result_members:
                            if bone.name in member.get_bones():
                                result_members.append(member)
        return result_members



def get_active_armature():
    selected_object = bpy.context.object  # Obtenir l'objet sélectionné
    if selected_object:
        if selected_object.type == "ARMATURE":
            return selected_object

def get_active_skeleton_data() -> skeleton_data:
    armature = get_active_armature()
    if armature:
        my_skeleton_data = get_skeleton_data(armature)
        return my_skeleton_data
    return None

def get_skeleton_data(armature: bpy.types.Object) -> skeleton_data:

import json
from pathlib import Path
from typing import Dict, List, Tuple

def find_translations_dir() -> Path:
    """Trouve le dossier des traductions"""
    script_dir = Path(__file__).parent
    
    # Chercher le dossier local_list
    possible_dirs = [
        script_dir / "local_list",           # Dans le même dossier
        script_dir.parent / "local_list",    # Dossier parent
        script_dir / ".." / "local_list",    # Explicite parent
    ]
    
    for dir_path in possible_dirs:
        if dir_path.exists() and dir_path.is_dir():
            print(f"📁 Dossier trouvé: {dir_path.resolve()}")
            return dir_path
    
    print("❌ Dossier local_list non trouvé!")
    print("Dossiers vérifiés:")
    for dir_path in possible_dirs:
        print(f"  - {dir_path.resolve()} (existe: {dir_path.exists()})")
    
    # Lister le contenu du dossier script pour debug
    print(f"\n📂 Contenu du dossier script ({script_dir}):")
    try:
        for item in script_dir.iterdir():
            print(f"  - {item.name} ({'dir' if item.is_dir() else 'file'})")
    except Exception as e:
        print(f"  Erreur: {e}")
    
    return None

def load_json_file(filepath: Path) -> Dict:
    """Charge un fichier JSON"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé: {filepath}")
        return {}
    except json.JSONDecodeError as e:
        print(f"❌ Erreur JSON dans {filepath}: {e}")
        return {}

def check_translation_files():
    """Vérifie la cohérence des fichiers de traduction"""
    
    # Trouver le dossier des traductions
    translations_dir = find_translations_dir()
    if not translations_dir:
        return
    
    source_file = translations_dir / "en_US.json"
    
    # Charger le fichier source (en_US.json)
    print("📋 Chargement du fichier source en_US.json...")
    source_data = load_json_file(source_file)
    
    if not source_data:
        print("❌ Impossible de charger le fichier source!")
        return
    
    # Extraire les clés et textes originaux du fichier source
    source_keys = set(source_data.keys())
    source_originals = {key: value[0] for key, value in source_data.items() if isinstance(value, list) and len(value) >= 2}
    
    print(f"✅ Fichier source chargé: {len(source_keys)} clés trouvées")
    print()
    
    # Fichiers à vérifier
    translation_files = ["fr_FR.json", "ru_RU.json", "zh_HANS.json"]
    
    errors_found = False
    
    for file_name in translation_files:
        print(f"🔍 Vérification de {file_name}...")
        file_path = translations_dir / file_name
        
        # Charger le fichier de traduction
        translation_data = load_json_file(file_path)
        
        if not translation_data:
            continue
            
        translation_keys = set(translation_data.keys())
        
        # 1. Vérifier les clés manquantes
        missing_keys = source_keys - translation_keys
        if missing_keys:
            errors_found = True
            print(f"  ❌ Clés manquantes ({len(missing_keys)}):")
            for key in sorted(missing_keys)[:5]:  # Afficher les 5 premières
                print(f"    - {key}")
            if len(missing_keys) > 5:
                print(f"    ... et {len(missing_keys) - 5} autres")
        
        # 2. Vérifier les clés en trop
        extra_keys = translation_keys - source_keys
        if extra_keys:
            errors_found = True
            print(f"  ❌ Clés en trop ({len(extra_keys)}):")
            for key in sorted(extra_keys)[:5]:  # Afficher les 5 premières
                print(f"    - {key}")
            if len(extra_keys) > 5:
                print(f"    ... et {len(extra_keys) - 5} autres")
        
        # 3. Vérifier que les textes originaux correspondent
        original_mismatch = []
        for key in translation_keys & source_keys:  # Clés communes
            if key in source_originals and isinstance(translation_data[key], list) and len(translation_data[key]) >= 2:
                source_original = source_originals[key]
                translation_original = translation_data[key][0]
                
                if source_original != translation_original:
                    original_mismatch.append({
                        'key': key,
                        'source': source_original,
                        'translation_file': translation_original
                    })
        
        if original_mismatch:
            errors_found = True
            print(f"  ❌ Textes originaux différents ({len(original_mismatch)}):")
            for mismatch in original_mismatch[:3]:  # Afficher les 3 premiers
                print(f"    - {mismatch['key']}:")
                print(f"      Source: '{mismatch['source']}'")
                print(f"      {file_name}: '{mismatch['translation_file']}'")
            if len(original_mismatch) > 3:
                print(f"    ... et {len(original_mismatch) - 3} autres")
        
        # 4. Résumé pour ce fichier
        if not missing_keys and not extra_keys and not original_mismatch:
            print(f"  ✅ {file_name} est cohérent avec en_US.json")
        
        print()
    
    # Résumé global
    if errors_found:
        print("❌ Des incohérences ont été trouvées dans les fichiers de traduction!")
    else:
        print("✅ Tous les fichiers de traduction sont cohérents!")

def generate_missing_keys_template():
    """Génère un template pour les clés manquantes"""
    translations_dir = find_translations_dir()
    if not translations_dir:
        return
    
    source_file = translations_dir / "en_US.json"
    source_data = load_json_file(source_file)
    
    if not source_data:
        return
    
    for file_name in ["fr_FR.json", "ru_RU.json", "zh_HANS.json"]:
        file_path = translations_dir / file_name
        translation_data = load_json_file(file_path)
        
        if not translation_data:
            continue
            
        source_keys = set(source_data.keys())
        translation_keys = set(translation_data.keys())
        missing_keys = source_keys - translation_keys
        
        if missing_keys:
            template_file = translations_dir / f"missing_keys_{file_name}"
            template_data = {}
            
            for key in sorted(missing_keys):
                if key in source_data:
                    original_text = source_data[key][0]
                    template_data[key] = [original_text, "TODO: Traduire"]
            
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, ensure_ascii=False, indent=4)
            
            print(f"📝 Template généré: {template_file}")
        else:
            print(f"✅ Aucune clé manquante pour {file_name}")

if __name__ == "__main__":
    print("🌍 Vérificateur de cohérence des traductions")
    print("=" * 50)
    
    # Vérifier la cohérence
    check_translation_files()
    
    print()
    print("📝 Génération des templates pour les clés manquantes...")
    generate_missing_keys_template()