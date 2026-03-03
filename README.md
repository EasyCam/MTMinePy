# MTMinePy - Multilingual Text Miner with Python

[![PyPI version](https://badge.fury.io/py/mtminepy.svg)](https://pypi.org/project/mtminepy/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

**MTMinePy** is a Python-based academic text mining platform inspired by MTMineR. It is a comprehensive Flask web application designed for powerful text mining and analysis, supporting interactive visualization and advanced modeling.

## Key Features
- **Advanced NLP**: Integrated with `jieba`, `HanLP`, `LTP`, `Spacy`, and `NLTK`.
- **Multilingual**: Native support for 10+ languages including Chinese, English, Japanese, and more.
- **Interactive Visualization**: Powered by **ECharts**, supporting responsive force-directed networks, dynamic word clouds, and interactive scatter plots.
- **Academic Metric Analysis**: Supports advanced distance functions (Hsim, Close, Esim) and high-end visualization.
- **Advanced Modeling**: Comprehensive suite of Unsupervised (Clustering, Topic Modeling) and Supervised learning algorithms.

## Screenshots

### Chinese Analysis
| Co-occurrence Network | Word Cloud | Clustering |
|:---:|:---:|:---:|
| ![Chinese Network](images/中文共现网络.png) | ![Chinese WordCloud](images/中文词云.png) | ![Chinese Clustering](images/中文聚类.png) |

### English Analysis
| Co-occurrence Network | Word Cloud | Clustering |
|:---:|:---:|:---:|
| ![English Network](images/英文共现网络.png) | ![English WordCloud](images/英文词云.png) | ![English Clustering](images/英文聚类.png) |

## Installation

### Install from PyPI (Recommended)

```bash
pip install mtminepy
```

To install with all optional NLP backends (Janome, spaCy, HanLP, LTP, UMAP, Boruta, etc.):

```bash
pip install mtminepy[full]
```

### Install from source

```bash
git clone https://github.com/EasyCam/MTMinePy.git
cd MTMinePy
pip install -e .
```

## Usage

### Run from command line

After installation, run directly:

```bash
mtminepy
```

Access the dashboard at `http://localhost:5000`.

### Command-line options

```bash
mtminepy --help
mtminepy --port 8080          # Custom port
mtminepy --host 127.0.0.1    # Bind to localhost only
mtminepy --debug              # Flask debug mode
mtminepy --version            # Show version
```

### Run from Python

```python
from mtminepy.app import create_app

app = create_app()
app.run(host='0.0.0.0', port=5000)
```

## Advanced Capabilities

### Modeling Algorithms
MTMinePy supports a wide range of standard machine learning algorithms for text analysis:
*   **Feature Engineering**: TF-IDF, Bag of Words (CountVectorizer), N-gram support.
*   **Unsupervised Learning**:
    *   **Topic Modeling**: Latent Dirichlet Allocation (LDA), Non-negative Matrix Factorization (NMF), STM (Structural Topic Model).
    *   **Clustering**: K-Means, Agglomerative (Hierarchical), DBSCAN, Spectral Clustering.
    *   **Dimensionality Reduction**: PCA, t-SNE, UMAP, Factor Analysis.
*   **Supervised Learning** (Classification):
    *   Support Vector Machines (SVM)
    *   Random Forest
    *   Linear Discriminant Analysis (LDA)
    *   Quadratic Discriminant Analysis (QDA)
    *   Logistic Regression (Elastic Net)

### Mathematical Models (Distance & Similarity)
MTMinePy supports advanced metrics for academic research:

#### Advanced Custom Similarity Measures
1.  **Hsim (Yang Fengzhao, 2007)**
    $$ Hsim(x_i, x_j) = \frac{1}{n} \sum_{k=1}^n \frac{1}{1+|x_{ik}-x_{jk}|} $$
    
2.  **Close (Shao Changsheng, et al., 2011)**
    $$ Close(x_i, x_j) = \frac{1}{n} \sum_{k=1}^n e^{-|x_{ik}-x_{jk}|} $$

3.  **Esim (Wang Xiaoyang, et al., 2013)**
    $$ Esim(x_{ik}, x_{jk}) = \frac{1}{n} \sum_{k=1}^d \omega_k e^{-\frac{|x_{ik}-x_{jk}|}{|x_{ik}-x_{jk}|+|x_{ik}+x_{jk}|/2}} $$
