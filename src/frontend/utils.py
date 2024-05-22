from datetime import datetime

def hex_to_rgb(hex_color, alpha=1.0):
    hex_color = hex_color.lstrip('#')
    rgb_color = tuple(int(hex_color[i:i+2], 16)/255 for i in (0, 2, 4))
    return rgb_color + (alpha,)

def get_time():
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M')
    return formatted_time