# mtminepy/app.py
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='jieba')
warnings.filterwarnings("ignore", category=FutureWarning, module='torch')

import os
import io
import re
import base64
import json

from flask import Flask, render_template, request, jsonify, session, send_file, redirect, url_for
from flask_session import Session
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from collections import Counter

# --- Font Configuration for CJK Support ---
def configure_fonts():
    font_candidates = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'WenQuanYi Micro Hei', 'Noto Sans CJK SC']
    found_font = None
    
    system_fonts = {f.name for f in fm.fontManager.ttflist}
    for font in font_candidates:
        if font in system_fonts:
            found_font = font
            break
            
    if found_font:
        plt.rcParams['font.sans-serif'] = [found_font] + plt.rcParams['font.sans-serif']
        plt.rcParams['axes.unicode_minus'] = False
    else:
        plt.rcParams['font.family'] = 'sans-serif'

configure_fonts()

from .services.nlp_service import nlp_engine
from .services.data_service import load_dataset, generate_synthetic_data
from .services.ml_service import model_engine, compute_metrics, compute_distance_matrix
from .services.trans_service import get_trans, get_all_langs

# Resolve template and session directories relative to this file
_PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
_TEMPLATE_DIR = os.path.join(_PACKAGE_DIR, 'templates')


def create_app():
    """Application factory for the Flask app."""
    app = Flask(__name__, template_folder=_TEMPLATE_DIR)
    app.config['SECRET_KEY'] = 'mtminepy_secret_key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = os.path.join(os.getcwd(), '.mtminepy_session')
    Session(app)

    os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True)

    # Context Processor for Templates
    @app.context_processor
    def inject_globals():
        return dict(
            get_trans=get_trans,
            all_langs=get_all_langs(),
            session=session
        )

    def plot_to_base64(fig):
        img = io.BytesIO()
        fig.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        return base64.b64encode(img.getvalue()).decode()

    @app.route('/set_lang/<lang_code>')
    def set_lang(lang_code):
        session['ui_lang'] = lang_code
        return redirect(request.referrer or url_for('index'))

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/data', methods=['GET', 'POST'])
    def data_page():
        if request.method == 'POST':
            if 'file' in request.files:
                f = request.files['file']
                if f.filename != '':
                    df = load_dataset(f, f.filename)
                    if df is not None:
                        session['df'] = df
                        session['filename'] = f.filename
                        return jsonify({'status': 'success', 'rows': len(df), 'cols': list(df.columns)})
            
            if request.form.get('action') == 'generate':
                df = generate_synthetic_data()
                session['df'] = df
                return jsonify({'status': 'success', 'rows': len(df)})

        df_info = None
        if 'df' in session:
            df = session['df']
            df_info = {
                'rows': len(df),
                'columns': list(df.columns),
                'preview': df.head().to_html(classes='table table-striped table-hover', index=False)
            }
        return render_template('data.html', df_info=df_info)

    @app.route('/preprocess', methods=['GET', 'POST'])
    def preprocess_page():
        if 'df' not in session:
            return render_template('preprocess.html', error="No data loaded.")
        
        if request.method == 'POST':
            df = session['df']
            text_col = request.form.get('text_col')
            target_langs = request.form.getlist('langs')
            extract_dialogue = request.form.get('extract_dialogue') == 'true'
            pos_filter = request.form.getlist('pos_filter')
            
            df['detected_lang'] = df[text_col].apply(lambda x: nlp_engine.detect_lang_safe(str(x)))
            if target_langs:
                df = df[df['detected_lang'].isin(target_langs)]
            
            tokens = []
            for _, row in df.iterrows():
                text = str(row[text_col])
                
                if extract_dialogue:
                    dialogues = re.findall(r'\u300c(.*?)\u300d|"(.*?)"', text)
                    dialogues = [d[0] or d[1] for d in dialogues if d[0] or d[1]]
                    row['dialogue'] = " ".join(dialogues)
                    row['narrative'] = re.sub(r'\u300c.*?\u300d|".*?"', '', text)
                
                toks = nlp_engine.tokenize(text, row['detected_lang'], pos_filter=pos_filter)
                tokens.append(toks)
            
            session['tokens'] = tokens
            session['clean_text'] = [" ".join(t) for t in tokens]
            session['filtered_df'] = df
            
            return jsonify({'status': 'success', 'count': len(df)})

        return render_template('preprocess.html', columns=list(session['df'].columns))

    @app.route('/export/<fmt>')
    def export_data(fmt):
        if 'filtered_df' not in session:
            return "No data to export", 400
        
        df = session['filtered_df'].copy()
        if 'clean_text' in session:
            df['clean_text'] = session['clean_text']
        
        buffer = io.BytesIO()
        if fmt == 'csv':
            df.to_csv(buffer, index=False)
            mimetype = 'text/csv'
            fname = 'mtmine_export.csv'
        elif fmt == 'json':
            df.to_json(buffer, orient='records', force_ascii=False)
            mimetype = 'application/json'
            fname = 'mtmine_export.json'
        else:
            return "Invalid format", 400
            
        buffer.seek(0)
        return send_file(buffer, mimetype=mimetype, as_attachment=True, download_name=fname)

    @app.route('/explore', methods=['GET', 'POST'])
    def explore_page():
        if 'tokens' not in session:
            return render_template('explore.html', error="Run preprocessing first.")
        
        if request.method == 'POST':
            action = request.form.get('action')
            
            all_tokens = [t for sublist in session['tokens'] for t in sublist]
            if not all_tokens:
                return jsonify({'html': 'No valid tokens found.', 'nodes': [], 'data': []})

            if action == 'kwic':
                keyword = request.form.get('keyword')
                if not keyword: return jsonify({'html': ''})
                res_df = model_engine.get_kwic(session['tokens'], keyword)
                return jsonify({'html': res_df.to_html(classes='table table-sm', index=False) if not res_df.empty else 'No matches.'})
                
            elif action == 'crosstab':
                group_col = request.form.get('group_col')
                top_n = int(request.form.get('top_n', 20))
                
                data = []
                groups = session['filtered_df'][group_col].tolist()
                for i, toks in enumerate(session['tokens']):
                    grp = groups[i] if i < len(groups) else 'Unknown'
                    for t in toks:
                        data.append({'Group': grp, 'Word': t})
                
                if not data:
                    return jsonify({'plot': ''})

                df_long = pd.DataFrame(data)
                top_words = df_long['Word'].value_counts().head(top_n).index
                df_filtered = df_long[df_long['Word'].isin(top_words)]
                
                if df_filtered.empty:
                    return jsonify({'echarts_option': None})

                ct = pd.crosstab(df_filtered['Word'], df_filtered['Group'])
                
                heatmap_json = model_engine.get_echarts_heatmap_json(
                    ct, 
                    x_labels=list(ct.columns),
                    y_labels=list(ct.index),
                    title=f"Word Frequency by {group_col}"
                )
                return jsonify({'echarts_option': heatmap_json})

            elif action == 'network_json':
                G = model_engine.get_cooc_network(session['tokens'])
                return jsonify(model_engine.get_echarts_network_json(G))
                
            elif action == 'wordcloud_json':
                c = Counter(all_tokens)
                data = [{"name": k, "value": v} for k, v in c.most_common(100)]
                return jsonify({'data': data})

        try:
            metrics_df = compute_metrics(session['tokens'])
            stats_html = metrics_df.describe().to_html(classes='table table-sm')
        except Exception as e:
            stats_html = f"Error computing metrics: {e}"
        
        return render_template('explore.html', stats=stats_html)

    @app.route('/metric', methods=['GET', 'POST'])
    def metric_page():
        if 'clean_text' not in session:
            return render_template('metric.html', error="Run preprocessing first.")
        
        if not any(session['clean_text']) or all(t.strip() == '' for t in session['clean_text']):
            return render_template('metric.html', error="Processed text is empty. Please adjust preprocessing filters.")

        if request.method == 'POST':
            metric_name = request.form.get('metric')
            
            metric_map = {
                "Euclidean": "euclidean",
                "Manhattan (Cityblock)": "cityblock",
                "Chebyshev": "chebyshev",
                "Minkowski (p=3)": "minkowski",
                "Mahalanobis": "mahalanobis",
                "Cosine": "cosine",
                "Correlation": "correlation",
                "Canberra": "canberra",
                "Bray-Curtis": "braycurtis",
                "SqEuclidean": "sqeuclidean",
                "Jaccard": "jaccard",
                "Hamming": "hamming",
                "KL Divergence": "kl_divergence",
                "Hsim (Yang, 2007)": "Hsim",
                "Close (Shao, 2011)": "Close",
                "Esim (Wang, 2013)": "Esim"
            }
            
            internal_metric = metric_map.get(metric_name, "euclidean")
            
            X_full, _ = model_engine.vectorize(session['clean_text'], method='tfidf', max_features=500)
            
            matrix, X_sub, is_sim = compute_distance_matrix(X_full, internal_metric, p=3)
            
            if is_sim:
                S = matrix
                D = 1.0 - S
                title = f"{metric_name} Similarity Matrix"
            else:
                D = matrix
                S = 1.0 / (1.0 + D)
                title = f"{metric_name} Distance Matrix"
                
            heatmap_json = model_engine.get_echarts_heatmap_json(
                D if not is_sim else S,
                title=title
            )
            
            from sklearn.manifold import MDS
            mds = MDS(n_components=2, dissimilarity="precomputed", random_state=42)
            coords = mds.fit_transform(D)
            
            df_viz = pd.DataFrame(coords, columns=['x', 'y'])
            
            hue = None
            if 'filtered_df' in session and isinstance(session['filtered_df'], pd.DataFrame):
                 df_sub = session['filtered_df']
                 if len(df_sub) >= len(df_viz):
                     if 'detected_lang' in df_sub.columns:
                         df_viz['Language'] = df_sub.iloc[:len(df_viz)]['detected_lang'].values
                         hue = 'Language'
            
            if not hue:
                df_viz['cluster'] = 'All'
                
            mds_json = model_engine.get_echarts_scatter_json(df_viz)
            
            return jsonify({
                'heatmap_option': heatmap_json,
                'mds_option': mds_json
            })

        return render_template('metric.html')

    @app.route('/model', methods=['GET', 'POST'])
    def model_page():
        if 'clean_text' not in session:
            return render_template('model.html', error="Run preprocessing first.")
        
        if not any(session['clean_text']) or all(t.strip() == '' for t in session['clean_text']):
            return render_template('model.html', error="Processed text is empty. Please adjust preprocessing filters.")

        if request.method == 'POST':
            action = request.form.get('action')
            
            ngram_val = request.form.get('ngram_range', '1,1')
            n_min, n_max = map(int, ngram_val.split(','))
            ngram_range = (n_min, n_max)
            
            try:
                X, vectorizer = model_engine.vectorize(session['clean_text'], ngram_range=ngram_range)
            except ValueError:
                return jsonify({'html': 'Error: Vocabulary is empty. Adjust filters.'})
            
            if action == 'cluster':
                algo = request.form.get('algorithm')
                n = int(request.form.get('n_clusters', 3))
                labels = model_engine.run_clustering(X, algo, n)
                
                proj_method = request.form.get('projection', 'pca')
                coords = model_engine.run_projection(X, proj_method)
                
                df_viz = pd.DataFrame(coords, columns=['x', 'y'])
                df_viz['cluster'] = labels
                
                return jsonify({'cluster_json': model_engine.get_echarts_scatter_json(df_viz)})
                
            elif action == 'topic':
                n = int(request.form.get('n_topics', 5))
                model, dist = model_engine.run_topic_model(X, 'lda', n)
                vocab = vectorizer.get_feature_names_out()
                
                topics_html = ""
                for i, topic in enumerate(model.components_):
                    top = [vocab[j] for j in topic.argsort()[:-10:-1]]
                    topics_html += f"<b>Topic {i+1}:</b> {', '.join(top)}<br>"
                
                stm_html = ""
                covariate = request.form.get('covariate')
                if covariate and covariate != 'None':
                    meta = session['filtered_df'][covariate]
                    stm_res = model_engine.run_stm_analysis(dist, meta)
                    stm_html = stm_res.to_html(classes='table table-sm', index=False)
                    
                return jsonify({'html': topics_html + "<hr>" + stm_html})
                
            elif action == 'classify':
                label_col = request.form.get('label_col')
                algo = request.form.get('algorithm')
                use_boruta = request.form.get('use_boruta') == 'true'
                
                y = session['filtered_df'][label_col].astype(str)
                
                if use_boruta:
                    X = model_engine.run_boruta(X, y)
                
                acc, report, cm, y_test, preds = model_engine.train_classifier(X, y, algo)
                
                labels = sorted(list(set(y_test) | set(preds)))
                heatmap_json = model_engine.get_echarts_heatmap_json(
                    cm, 
                    x_labels=labels,
                    y_labels=labels,
                    title="Confusion Matrix"
                )
                heatmap_json['xAxis']['name'] = 'Predicted'
                heatmap_json['yAxis']['name'] = 'True'
                
                return jsonify({
                    'text': f"Accuracy: {acc:.2%}\n\n{report}",
                    'echarts_option': heatmap_json
                })

        cols = list(session['filtered_df'].columns)
        return render_template('model.html', columns=cols)

    return app
