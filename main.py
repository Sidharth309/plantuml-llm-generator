import os
from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import plantuml
from validation import validate_plantuml

app = Flask(__name__)

# Loading the LLAMA 3.1 model
model_name = "mlabonne/Meta-Llama-3.1-8B-Instruct-abliterated"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Function to prompt the LLM to generate PlantUML
def generate_plantuml(description):
    prompt = f"Generate a PlantUML class diagram based on the following description: {description}\n"
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model.generate(inputs, max_length=1024)
    
    generated_plantuml = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_plantuml

@app.route('/generate', methods=['POST'])
def generate():
    """Endpoint for receiving domain description and generating PlantUML."""
    user_input = request.json.get('description', '')

    if not user_input:
        return jsonify({"error": "Description is required."}), 400

    # Generating PlantUML using the LLM
    generated_plantuml = generate_plantuml(user_input)

    # Validating PlantUML syntax
    valid, errors = validate_plantuml(generated_plantuml)
    
    if not valid:
        return jsonify({
            "error": "Generated PlantUML is invalid.",
            "details": errors
        }), 400

    # Rendering the PlantUML diagram if it's valid
    diagram_url = plantuml.render_plantuml(generated_plantuml)

    return jsonify({
        "plantuml_code": generated_plantuml,
        "diagram_url": diagram_url
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
