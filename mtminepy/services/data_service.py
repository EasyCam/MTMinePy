# mtminepy/services/data_service.py
import pandas as pd
import io
import json
import random

def load_dataset(file_obj, filename):
    try:
        if filename.endswith('.csv'):
            return pd.read_csv(file_obj)
        elif filename.endswith('.xlsx'):
            return pd.read_excel(file_obj)
        elif filename.endswith('.txt'):
            content = file_obj.read().decode('utf-8')
            lines = [l.strip() for l in content.splitlines() if l.strip()]
            return pd.DataFrame({'text': lines})
        elif filename.endswith('.md'):
            content = file_obj.read().decode('utf-8')
            lines = [l.strip() for l in content.splitlines() if l.strip()]
            return pd.DataFrame({'text': lines})
        elif filename.endswith('.json'):
            try:
                return pd.read_json(file_obj)
            except:
                file_obj.seek(0)
                content = file_obj.read().decode('utf-8')
                data = json.loads(content)
                if isinstance(data, list):
                    return pd.DataFrame(data)
                elif isinstance(data, dict):
                    return pd.DataFrame([data])
                else:
                    return pd.DataFrame({'text': [str(data)]})
    except Exception as e:
        print(f"Error loading file: {e}")
        return None
    return None

def generate_synthetic_data():
    data = []
    for l in ["en", "cn", "ja", "fr", "de"]:
        for i in range(20):
            data.append({"text": f"Sample text in {l} number {i} for analysis.", "lang_true": l, "category": random.choice(["A", "B"])})
    return pd.DataFrame(data)
