import zlib

def compress_plantuml(text):
    """Helper function to compress the PlantUML text into a URL-compatible format."""
    zlibbed_str = zlib.compress(text.encode('utf-8'))
    compressed_string = zlibbed_str[2:-4]
    return encode64(compressed_string)

def render_plantuml(plantuml_code):
    """
    Render the PlantUML diagram using an online PlantUML server.
    Converts PlantUML text into a URL that can be rendered in a browser.
    """
    plantuml_server_url = "http://www.plantuml.com/plantuml/img/"
    compressed_plantuml = compress_plantuml(plantuml_code)
    diagram_url = plantuml_server_url + compressed_plantuml
    return diagram_url

def encode64(data):
    """Encoding the data to base64, which is required by PlantUML servers."""
    base64_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
    encoded = ''
    for i in range(0, len(data), 3):
        if i + 2 == len(data):
            b1, b2 = data[i], data[i + 1]
            encoded += base64_chars[b1 >> 2]
            encoded += base64_chars[((b1 & 0x3) << 4) | (b2 >> 4)]
            encoded += base64_chars[(b2 & 0xF) << 2]
            encoded += '='
        elif i + 1 == len(data):
            b1 = data[i]
            encoded += base64_chars[b1 >> 2]
            encoded += base64_chars[(b1 & 0x3) << 4]
            encoded += '=='
        else:
            b1, b2, b3 = data[i], data[i + 1], data[i + 2]
            encoded += base64_chars[b1 >> 2]
            encoded += base64_chars[((b1 & 0x3) << 4) | (b2 >> 4)]
            encoded += base64_chars[((b2 & 0xF) << 2) | (b3 >> 6)]
            encoded += base64_chars[b3 & 0x3F]
    return encoded
