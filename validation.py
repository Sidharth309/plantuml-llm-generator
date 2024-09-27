import re

def validate_plantuml(plantuml_code):
    """
    Validate PlantUML code to ensure basic syntax is correct.
    """
    # Basic validation for class diagrams
    if not re.search(r'@startuml', plantuml_code) or not re.search(r'@enduml', plantuml_code):
        return False, "Missing @startuml or @enduml tags."

    if not re.search(r'class \w+', plantuml_code):
        return False, "No classes defined in the PlantUML diagram."

    return True, None
