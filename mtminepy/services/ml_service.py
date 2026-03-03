# mtminepy/services/ml_service.py
import numpy as np
import pandas as pd
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import PCA, LatentDirichletAllocation, NMF, FactorAnalysis
from sklearn.manifold import TSNE, MDS
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN, SpectralClustering
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from scipy.spatial.distance import pdist, squareform, cdist
from scipy.special import rel_entr
import statsmodels.api as sm
import importlib.util
import networkx as nx

# --- Metric Functions ---
def compute_metrics(tokens_list):
    metrics = []
    
    # Check for lexical_diversity
    has_ld = importlib.util.find_spec("lexical_diversity") is not None
    ld = None
    if has_ld:
        try:
            from lexical_diversity import lex_div as ld_module
            ld = ld_module
        except: pass

    for tokens in tokens_list:
        if len(tokens) == 0:
            metrics.append({"Guiraud": 0, "Sichel": 0, "TTR": 0, "Yule's K": 0})
            continue
        try:
            if ld:
                g = ld.guiraud(tokens)
                s = ld.sichel(tokens)
                if isinstance(s, tuple): s = s[0]
                ttr = ld.ttr(tokens)
            else:
                raise ImportError("lexical_diversity not found")

            counts = Counter(tokens)
            m1 = sum(counts.values())
            m2 = sum([freq ** 2 for freq in counts.values()])
            k = 10000 * (m2 - m1) / (m1 ** 2)
        except:
            N = len(tokens)
            V = len(set(tokens))
            g = V / (N ** 0.5) if N > 0 else 0
            counts = Counter(tokens)
            hapax = sum(1 for k,v in counts.items() if v == 1)
            s = hapax / V if V > 0 else 0
            ttr = V / N if N > 0 else 0
            k = 0
        metrics.append({"Guiraud": g, "Sichel": s, "TTR": ttr, "Yule's K": k})
    return pd.DataFrame(metrics)

# --- Advanced Distance & Similarity Engine ---
def compute_distance_matrix(X, metric, **kwargs):
    if hasattr(X, 'toarray'): X = X.toarray()
    n = X.shape[0]
    
    if n > 500: 
        indices = np.random.choice(n, 300, replace=False)
        X = X[indices]
        n = 300
    
    matrix = np.zeros((n, n))
    is_similarity = False
    
    if metric == "Hsim":
        is_similarity = True
        for i in range(n):
            diff = np.abs(X - X[i]) 
            term = 1.0 / (1.0 + diff)
            matrix[i] = np.mean(term, axis=1)
            
    elif metric == "Close":
        is_similarity = True
        for i in range(n):
            diff = np.abs(X - X[i])
            term = np.exp(-diff)
            matrix[i] = np.mean(term, axis=1)
            
    elif metric == "Esim":
        is_similarity = True
        eps = 1e-9
        for i in range(n):
            diff = np.abs(X - X[i])
            summ = np.abs(X + X[i])
            denom = diff + (summ / 2.0) + eps
            term = np.exp(- diff / denom)
            matrix[i] = np.mean(term, axis=1)

    elif metric == "kl_divergence":
        is_similarity = False
        X_prob = X + 1e-9
        X_prob = X_prob / X_prob.sum(axis=1, keepdims=True)
        for i in range(n):
            for j in range(i, n):
                val = (np.sum(rel_entr(X_prob[i], X_prob[j])) + np.sum(rel_entr(X_prob[j], X_prob[i]))) / 2
                matrix[i,j] = matrix[j,i] = val
                
    else:
        is_similarity = False
        try:
            if metric == "mahalanobis":
                if X.shape[1] > X.shape[0]:
                    pca = PCA(n_components=min(X.shape[0]-1, 50))
                    X_pca = pca.fit_transform(X)
                    VI = np.linalg.pinv(np.cov(X_pca.T))
                    matrix = squareform(pdist(X_pca, metric='mahalanobis', VI=VI))
                else:
                    VI = np.linalg.pinv(np.cov(X.T))
                    matrix = squareform(pdist(X, metric='mahalanobis', VI=VI))
            
            elif metric == "minkowski":
                p_val = kwargs.get('p', 3)
                matrix = squareform(pdist(X, metric='minkowski', p=p_val))
                
            else:
                matrix = cdist(X, X, metric=metric)
                
        except Exception as e:
            print(f"Error calculating {metric}: {e}. Fallback to Euclidean.")
            matrix = cdist(X, X, metric='euclidean')

    return matrix, X, is_similarity

def compute_custom_similarity(X, metric):
    if metric in ["Hsim", "Close", "Esim"]:
        m, x_sub, _ = compute_distance_matrix(X, metric)
        return m, x_sub
    else:
        m, x_sub, _ = compute_distance_matrix(X, "Hsim") 
        return m, x_sub

# --- Modeling Wrapper ---
class ModelEngine:
    def vectorize(self, texts, method="tfidf", max_features=1000, ngram_range=(1,1)):
        if method == "tfidf":
            vectorizer = TfidfVectorizer(max_features=max_features, ngram_range=ngram_range)
        else:
            vectorizer = CountVectorizer(max_features=max_features, ngram_range=ngram_range)
        X = vectorizer.fit_transform(texts)
        return X, vectorizer

    def run_clustering(self, X, algorithm="kmeans", n_clusters=3, **kwargs):
        if hasattr(X, 'toarray'): X_dense = X.toarray()
        else: X_dense = X
        
        if algorithm == "kmeans":
            model = KMeans(n_clusters=n_clusters)
        elif algorithm == "agglomerative":
            model = AgglomerativeClustering(n_clusters=n_clusters)
        elif algorithm == "spectral":
            model = SpectralClustering(n_clusters=n_clusters)
        elif algorithm == "dbscan":
            model = DBSCAN(eps=kwargs.get('eps', 0.5), min_samples=kwargs.get('min_samples', 5))
        
        labels = model.fit_predict(X_dense)
        return labels

    def run_projection(self, X, method="pca"):
        if hasattr(X, 'toarray'): X_dense = X.toarray()
        else: X_dense = X
        n_samples = X_dense.shape[0]

        try:
            if method == "pca":
                proj = PCA(n_components=2).fit_transform(X_dense)
            elif method == "tsne":
                perplex = min(30, max(1, n_samples - 1))
                if n_samples < 2: 
                    proj = PCA(n_components=2).fit_transform(X_dense)
                else:
                    proj = TSNE(n_components=2, perplexity=perplex).fit_transform(X_dense)
            elif method == "umap":
                try:
                    import umap.umap_ as umap
                    n_neighbors = min(15, max(2, n_samples - 1))
                    if n_samples < 3:
                         proj = PCA(n_components=2).fit_transform(X_dense)
                    else:
                         proj = umap.UMAP(n_components=2, n_neighbors=n_neighbors).fit_transform(X_dense)
                except:
                    proj = PCA(n_components=2).fit_transform(X_dense)
            elif method == "lda":
                proj = FactorAnalysis(n_components=2).fit_transform(X_dense)
        except Exception as e:
             print(f"Projection error ({method}): {e}. Falling back to PCA.")
             proj = PCA(n_components=2).fit_transform(X_dense)
             
        return proj

    def run_boruta(self, X, y):
        try:
            from boruta import BorutaPy
            rf = RandomForestClassifier(n_jobs=-1, class_weight='balanced', max_depth=5)
            feat_selector = BorutaPy(rf, n_estimators='auto', verbose=0, random_state=1)
            
            if hasattr(X, 'toarray'): X = X.toarray()
            feat_selector.fit(X, y)
            X_filtered = feat_selector.transform(X)
            
            if X_filtered.shape[1] == 0:
                print("Boruta selected 0 features. Reverting to original features.")
                return X
            return X_filtered
            
        except ImportError:
            print("Boruta not found")
            return X
        except Exception as e:
            print(f"Boruta error: {e}")
            return X

    def run_ca(self, X):
        try:
            import prince
            ca = prince.CA(n_components=2, n_iter=3, copy=True, check_input=True, engine='sklearn', random_state=42)
            
            if hasattr(X, 'toarray'): X = X.toarray()
            X = np.abs(X) 
            X = np.nan_to_num(X)
            X_df = pd.DataFrame(X)
            X_df = X_df + 1e-9
            
            ca = ca.fit(X_df)
            return ca.row_coordinates(X_df)
        except ImportError:
            print("Prince (CA) not found")
            return None
        except AttributeError as e:
            print(f"Prince/Sklearn compatibility error: {e}")
            return None
        except Exception as e:
            print(f"CA Error: {e}")
            return None

    def run_topic_model(self, X, algorithm="lda", n_topics=5):
        if algorithm == "lda":
            model = LatentDirichletAllocation(n_components=n_topics, random_state=42)
        else:
            model = NMF(n_components=n_topics, random_state=42)
        
        doc_topic_dist = model.fit_transform(X)
        return model, doc_topic_dist

    def run_stm_analysis(self, doc_topic_dist, metadata_col):
        if metadata_col.dtype == 'object':
            le = LabelEncoder()
            y_data = le.fit_transform(metadata_col.astype(str))
        else:
            y_data = metadata_col.values
            
        n_topics = doc_topic_dist.shape[1]
        results = []
        for topic_idx in range(n_topics):
            X_cov = sm.add_constant(y_data)
            ols = sm.OLS(doc_topic_dist[:, topic_idx], X_cov).fit()
            coef = ols.params[1] if len(ols.params) > 1 else 0
            p_val = ols.pvalues[1] if len(ols.pvalues) > 1 else 1.0
            results.append({"Topic": f"Topic {topic_idx+1}", "Coef": coef, "P-Value": p_val})
        return pd.DataFrame(results).sort_values("P-Value")

    def train_classifier(self, X, y, algo="svm"):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        is_dense_required = algo in ["lda", "qda"]
        if is_dense_required and hasattr(X_train, 'toarray'):
            X_train = X_train.toarray()
            X_test = X_test.toarray()
            
        if algo == "svm": clf = SVC()
        elif algo == "rf": clf = RandomForestClassifier()
        elif algo == "lda": clf = LinearDiscriminantAnalysis()
        elif algo == "qda": clf = QuadraticDiscriminantAnalysis()
        elif algo == "c50": clf = DecisionTreeClassifier(criterion="entropy")
        elif algo == "elastic": clf = LogisticRegression(penalty='elasticnet', solver='saga', l1_ratio=0.5, max_iter=1000)
        elif algo == "knn": clf = KNeighborsClassifier()
        else: clf = LogisticRegression()
        
        clf.fit(X_train, y_train)
        preds = clf.predict(X_test)
        
        acc = accuracy_score(y_test, preds)
        report = classification_report(y_test, preds)
        cm = confusion_matrix(y_test, preds)
        
        return acc, report, cm, y_test, preds

    def get_kwic(self, tokens_list, keyword, window=5):
        results = []
        for i, toks in enumerate(tokens_list):
            for j, t in enumerate(toks):
                if keyword in t:
                    left = toks[max(0, j-window):j]
                    right = toks[j+1:min(len(toks), j+window+1)]
                    results.append({
                        "DocID": i,
                        "Left": " ".join(left),
                        "Keyword": t,
                        "Right": " ".join(right)
                    })
                    if len(results) > 200: break
            if len(results) > 200: break
        return pd.DataFrame(results)

    def get_cooc_network(self, tokens_list, top_n=30):
        bigrams = []
        for toks in tokens_list:
            if len(toks) > 1:
                for i in range(len(toks)-1):
                    bigrams.append((toks[i], toks[i+1]))
        
        c = Counter(bigrams)
        common = c.most_common(top_n)
        
        G = nx.Graph()
        for (u, v), w in common:
            G.add_edge(u, v, weight=w)
            
        try:
            from networkx.algorithms import community
            communities = community.greedy_modularity_communities(G)
            for i, comm in enumerate(communities):
                for node in comm:
                    G.nodes[node]['group'] = i
        except:
            pass
            
        return G

    def get_echarts_network_json(self, G):
        nodes = []
        links = []
        categories = []
        
        groups = set()
        for n in G.nodes():
            g = G.nodes[n].get('group', 0)
            groups.add(g)
        
        sorted_groups = sorted(list(groups))
        for g in sorted_groups:
            categories.append({"name": f"Group {g}"})
            
        d = dict(G.degree)
        max_d = max(d.values()) if d else 1
        
        for n in G.nodes():
            size = 10 + (d[n] / max_d) * 40
            nodes.append({
                "name": str(n),
                "value": d[n],
                "symbolSize": size,
                "category": G.nodes[n].get('group', 0),
                "draggable": True
            })
            
        for u, v, data in G.edges(data=True):
            links.append({
                "source": str(u),
                "target": str(v),
                "value": data.get('weight', 1)
            })
            
        return {"nodes": nodes, "links": links, "categories": categories}

    def get_echarts_scatter_json(self, df_viz):
        group_col = None
        if 'cluster' in df_viz.columns:
            group_col = 'cluster'
        elif 'Language' in df_viz.columns:
            group_col = 'Language'
        
        if not group_col:
            df_viz['group'] = 'All'
            group_col = 'group'
        
        series = []
        groups = df_viz[group_col].unique()
        
        for g in sorted(groups):
            data = df_viz[df_viz[group_col] == g][['x', 'y']].values.tolist()
            series.append({
                "name": str(g),
                "type": "scatter",
                "data": data,
                "symbolSize": 10,
                "emphasis": {
                    "focus": "series"
                }
            })
            
        return {
            "legend": {"data": [str(g) for g in sorted(groups)], "bottom": 0},
            "xAxis": {"scale": True},
            "yAxis": {"scale": True},
            "series": series
        }

    def get_echarts_heatmap_json(self, matrix, x_labels=None, y_labels=None, title="Heatmap"):
        if hasattr(matrix, 'values'):
            if x_labels is None: x_labels = list(matrix.columns)
            if y_labels is None: y_labels = list(matrix.index)
            matrix = matrix.values
            
        rows, cols = matrix.shape
        
        if x_labels is None: x_labels = [str(i) for i in range(cols)]
        if y_labels is None: y_labels = [str(i) for i in range(rows)]
        
        data = []
        min_val = float(np.min(matrix))
        max_val = float(np.max(matrix))
        
        for i in range(rows):
            for j in range(cols):
                val = float(matrix[i, j])
                data.append([j, i, val])
                
        return {
            "title": {"text": title, "left": "center"},
            "tooltip": {"position": "top"},
            "grid": {"height": "80%", "top": "10%", "left": "10%", "right": "10%"},
            "xAxis": {"type": "category", "data": x_labels, "splitArea": {"show": True}, "axisLabel": {"show": False} if rows > 20 or cols > 20 else {"show": True}},
            "yAxis": {"type": "category", "data": y_labels, "splitArea": {"show": True}, "axisLabel": {"show": False} if rows > 20 or cols > 20 else {"show": True}},
            "visualMap": {
                "min": min_val,
                "max": max_val,
                "calculable": True,
                "orient": "horizontal",
                "left": "center",
                "bottom": "0%"
            },
            "series": [{
                "name": title,
                "type": "heatmap",
                "data": data,
                "label": {"show": True} if rows < 20 and cols < 20 else {"show": False},
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowColor": "rgba(0, 0, 0, 0.5)"
                    }
                }
            }]
        }

model_engine = ModelEngine()
