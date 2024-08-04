import yaml
import json

def load_template(template_file):
    with open(template_file, 'r') as f:
        return yaml.safe_load(f)

def load_config(config_file):
    with open(config_file, 'r') as f:
        return json.load(f)

def merge_data(template, config):
    merged = {}
    for key, value in template.items():
        if isinstance(value, dict):
            merged[key] = merge_data(value, config.get(key, {}))
        elif isinstance(value, list):
            merged[key] = []
            for item in value:
                if isinstance(item, dict):
                    merged[key].append(merge_data(item, config.get(key, {})))
                else:
                    merged[key].append(item)
        elif isinstance(value, str) and value.startswith('{{') and value.endswith('}}'):
            # Handle dynamic insertion for {{ key }} placeholders
            placeholder = value[2:-2].strip()
            if placeholder in config:
                merged[key] = config[placeholder]
            else:
                merged[key] = value  # If key not found in config, retain template value
        else:
            merged[key] = value  # Preserve template value if not a placeholder
    return merged

def write_yaml(output_file, data):
    with open(output_file, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)

if __name__ == "__main__":
    template = load_template('template.yaml')
    config = load_config('config.json')
    merged_data = merge_data(template, config)
    write_yaml('output.yaml', merged_data)
    print("YAML configuration generated successfully.")