# mtminepy/services/trans_service.py

TRANS = {
    # --- Navigation ---
    "title": {
        "en": "MTMinePy: Academic Text Mining Platform", "cn": "MTMinePy: \u5b66\u672f\u7ea7\u6587\u672c\u6316\u6398\u5e73\u53f0",
        "ja": "MTMinePy: \u30a2\u30ab\u30c7\u30df\u30c3\u30af\u30c6\u30ad\u30b9\u30c8\u30de\u30a4\u30cb\u30f3\u30b0", "ko": "MTMinePy: \ud559\uc220 \ud14d\uc2a4\ud2b8 \ub9c8\uc774\ub2dd",
        "ru": "MTMinePy: \u0410\u043a\u0430\u0434\u0435\u043c\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u0430\u043d\u0430\u043b\u0438\u0437 \u0442\u0435\u043a\u0441\u0442\u0430", "de": "MTMinePy: Akademische Textanalyse",
        "fr": "MTMinePy: Analyse de texte acad\u00e9mique", "it": "MTMinePy: Analisi del testo accademica",
        "es": "MTMinePy: Miner\u00eda de textos acad\u00e9mica", "pt": "MTMinePy: Minera\u00e7\u00e3o de texto acad\u00eamica"
    },
    "menu_home": {
        "en": "Home", "cn": "\u9996\u9875", "ja": "\u30db\u30fc\u30e0", "ko": "\ud648", "ru": "\u0413\u043b\u0430\u0432\u043d\u0430\u044f", 
        "de": "Startseite", "fr": "Accueil", "it": "Home", "es": "Inicio", "pt": "In\u00edcio"
    },
    "menu_data": {
        "en": "Data Management", "cn": "\u6570\u636e\u7ba1\u7406", "ja": "\u30c7\u30fc\u30bf\u7ba1\u7406", "ko": "\ub370\uc774\ud130 \uad00\ub9ac", "ru": "\u0423\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u0434\u0430\u043d\u043d\u044b\u043c\u0438",
        "de": "Datenverwaltung", "fr": "Gestion des donn\u00e9es", "it": "Gestione dati", "es": "Gesti\u00f3n de datos", "pt": "Gest\u00e3o de dados"
    },
    "menu_preprocess": {
        "en": "Preprocessing", "cn": "\u9884\u5904\u7406", "ja": "\u524d\u51e6\u7406", "ko": "\uc804\u52e8\ub9ac", "ru": "\u041f\u0440\u0435\u0434\u0432\u0430\u0440\u0438\u0442\u0435\u043b\u044c\u043d\u0430\u044f \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430",
        "de": "Vorverarbeitung", "fr": "Pr\u00e9traitement", "it": "Pre-elaborazione", "es": "Preprocesamiento", "pt": "Pr\u00e9-processamento"
    },
    "menu_explore": {
        "en": "Exploration", "cn": "\u63a2\u7d22\u5206\u6790", "ja": "\u63a2\u7d22", "ko": "\ud0d0\uc0c9", "ru": "\u0420\u0430\u0437\u0432\u0435\u0434\u043a\u0430",
        "de": "Exploration", "fr": "Exploration", "it": "Esplorazione", "es": "Exploraci\u00f3n", "pt": "Explora\u00e7\u00e3o"
    },
    "menu_metric": {
        "en": "Metric Analysis", "cn": "\u5ea6\u91cf\u5206\u6790", "ja": "\u30e1\u30c8\u30ea\u30c3\u30af\u5206\u6790", "ko": "\uc9c0\ud45c \ubd84\uc11d", "ru": "\u041c\u0435\u0442\u0440\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u0430\u043d\u0430\u043b\u0438\u0437",
        "de": "Metrikanalyse", "fr": "Analyse m\u00e9trique", "it": "Analisi metrica", "es": "An\u00e1lisis m\u00e9trico", "pt": "An\u00e1lise m\u00e9trica"
    },
    "menu_model": {
        "en": "Advanced Modeling", "cn": "\u9ad8\u7ea7\u5efa\u6a21", "ja": "\u9ad8\u5ea6\u306a\u30e2\u30c7\u30ea\u30f3\u30b0", "ko": "\uace0\uae09 \ubaa8\ub378\ub9c1", "ru": "\u0420\u0430\u0441\u0448\u0438\u0440\u0435\u043d\u043d\u043e\u0435 \u043c\u043e\u0434\u0435\u043b\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435",
        "de": "Erweiterte Modellierung", "fr": "Mod\u00e9lisation avanc\u00e9e", "it": "Modellazione avanzata", "es": "Modelado avanzado", "pt": "Modelagem avan\u00e7ada"
    },
    "lang_select": {
        "en": "Language", "cn": "\u8bed\u8a00", "ja": "\u8a00\u8a9e", "ko": "\uc5b8\uc5b4", "ru": "\u042f\u0437\u044b\u043a",
        "de": "Sprache", "fr": "Langue", "it": "Lingua", "es": "Idioma", "pt": "Idioma"
    },

    # --- Data ---
    "upload_label": {
        "en": "Upload Dataset", "cn": "\u4e0a\u4f20\u6570\u636e\u96c6", "ja": "\u30c7\u30fc\u30bf\u30bb\u30c3\u30c8\u3092\u30a2\u30c3\u30d7\u30ed\u30fc\u30c9", "ko": "\ub370\uc774\ud130\uc14b \uc5c5\ub85c\ub4dc", "ru": "\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u043d\u0430\u0431\u043e\u0440 \u0434\u0430\u043d\u043d\u044b\u0445",
        "de": "Datensatz hochladen", "fr": "T\u00e9l\u00e9charger", "it": "Carica", "es": "Subir", "pt": "Carregar"
    },
    "gen_sample_btn": {
        "en": "Generate Synthetic Data", "cn": "\u751f\u6210\u5408\u6210\u6570\u636e", "ja": "\u5408\u6210\u30c7\u30fc\u30bf\u3092\u751f\u6210", "ko": "\ud569\uc131 \ub370\uc774\ud130 \uc0dd\uc131", "ru": "\u0421\u043e\u0437\u0434\u0430\u0442\u044c \u0441\u0438\u043d\u0442\u0435\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u0434\u0430\u043d\u043d\u044b\u0435",
        "de": "Synthetische Daten generieren", "fr": "G\u00e9n\u00e9rer des donn\u00e9es", "it": "Genera dati", "es": "Generar datos", "pt": "Gerar dados"
    },

    # --- Preprocess ---
    "text_col_label": {"en": "Text Column", "cn": "\u6587\u672c\u5217", "ja": "\u30c6\u30ad\u30b9\u30c8\u5217"},
    "target_lang_label": {"en": "Target Languages", "cn": "\u76ee\u6807\u8bed\u8a00", "ja": "\u5bfe\u8c61\u8a00\u8a9e"},
    "extract_dialogue": {"en": "Extract Dialogue/Narrative", "cn": "\u63d0\u53d6\u5bf9\u8bdd/\u65c1\u767d", "ja": "\u4f1a\u8a71\u30fb\u5730\u306e\u6587\u3092\u62bd\u51fa"},
    "pos_filter_label": {"en": "POS Filter (Optional)", "cn": "\u8bcd\u6027\u8fc7\u6ee4 (\u53ef\u9009)", "ja": "\u54c1\u8a5e\u30d5\u30a3\u30eb\u30bf (\u30aa\u30d7\u30b7\u30e7\u30f3)"},
    "keep_nouns": {"en": "Keep Nouns", "cn": "\u4fdd\u7559\u540d\u8bcd", "ja": "\u540d\u8a5e\u306e\u307f"},
    "keep_verbs": {"en": "Keep Verbs", "cn": "\u4fdd\u7559\u52a8\u8bcd", "ja": "\u52d5\u8a5e\u306e\u307f"},
    "keep_adj": {"en": "Keep Adjectives", "cn": "\u4fdd\u7559\u5f62\u5bb9\u8bcd", "ja": "\u5f62\u5bb9\u8a5e\u306e\u307f"},
    "run_token_btn": {"en": "Run Tokenization", "cn": "\u8fd0\u884c\u5206\u8bcd", "ja": "\u30c8\u30fc\u30af\u30f3\u5316\u5b9f\u884c"},
    "export_csv": {"en": "Export CSV", "cn": "\u5bfc\u51fa CSV", "ja": "CSV \u30a8\u30af\u30b9\u30dd\u30fc\u30c8"},
    "export_json": {"en": "Export JSON", "cn": "\u5bfc\u51fa JSON", "ja": "JSON \u30a8\u30af\u30b9\u30dd\u30fc\u30c8"},

    # --- Explore ---
    "tab_stats": {"en": "Statistics", "cn": "\u57fa\u672c\u7edf\u8ba1", "ja": "\u7d71\u8a08\u60c5\u5831"},
    "tab_kwic": {"en": "KWIC", "cn": "KWIC", "ja": "KWIC"},
    "tab_network": {"en": "Network Graph", "cn": "\u5171\u73b0\u7f51\u7edc", "ja": "\u5171\u8d77\u30cd\u30c3\u30c8\u30ef\u30fc\u30af"},
    "tab_crosstab": {"en": "Group Analysis", "cn": "\u5206\u7ec4\u5206\u6790", "ja": "\u30b0\u30eb\u30fc\u30d7\u5206\u6790"},
    "search_ph": {"en": "Enter keyword...", "cn": "\u8f93\u5165\u5173\u952e\u8bcd...", "ja": "\u30ad\u30fc\u30ef\u30fc\u30c9\u3092\u5165\u529b..."},
    "search_btn": {"en": "Search", "cn": "\u641c\u7d22", "ja": "\u691c\u7d22"},
    "lex_stats_title": {"en": "Lexical Statistics", "cn": "\u8bcd\u6c47\u7edf\u8ba1", "ja": "\u8a9e\u5f59\u7d71\u8a08"},
    "wordcloud_title": {"en": "Word Cloud", "cn": "\u8bcd\u4e91", "ja": "\u30ef\u30fc\u30c9\u30af\u30e9\u30a6\u30c9"},
    "select_group_col": {"en": "Group Column", "cn": "\u5206\u7ec4\u5217", "ja": "\u30b0\u30eb\u30fc\u30d7\u5217"},
    "top_n_words": {"en": "Top N Words", "cn": "\u524d N \u4e2a\u8bcd", "ja": "\u4e0a\u4f4d N \u8a9e"},

    # --- Model ---
    "tab_unsup": {"en": "Unsupervised Learning", "cn": "\u65e0\u76d1\u7763\u5b66\u4e60", "ja": "\u6559\u5e2b\u306a\u3057\u5b66\u7fd2"},
    "tab_sup": {"en": "Supervised Learning", "cn": "\u76d1\u7763\u5b66\u4e60", "ja": "\u6559\u5e2b\u3042\u308a\u5b66\u7fd2"},
    "run_model_btn": {"en": "Run Model", "cn": "\u8fd0\u884c\u6a21\u578b", "ja": "\u30e2\u30c7\u30eb\u5b9f\u884c"},
    "run_boruta": {"en": "Run Boruta Feature Selection", "cn": "\u8fd0\u884c Boruta \u7279\u5f81\u9009\u62e9", "ja": "Boruta \u7279\u5fb4\u9078\u629e\u3092\u5b9f\u884c"},
    "label_col": {"en": "Label Column", "cn": "\u6807\u7b7e\u5217", "ja": "\u30e9\u30d9\u30eb\u5217"},
    "select_covariate": {"en": "Select Covariate (STM)", "cn": "\u9009\u62e9\u534f\u53d8\u91cf (STM)", "ja": "\u5171\u5909\u91cf\u306e\u9078\u629e (STM)"},
    "task_label": {"en": "Task", "cn": "\u4efb\u52a1", "ja": "\u30bf\u30b9\u30af"},
    "algo_label": {"en": "Algorithm", "cn": "\u7b97\u6cd5", "ja": "\u30a2\u30eb\u30b4\u30ea\u30ba\u30e0"},
    "proj_label": {"en": "Projection", "cn": "\u964d\u7ef4\u6295\u5f71", "ja": "\u6295\u5f71"},
    "clusters_label": {"en": "Num Clusters", "cn": "\u805a\u7c7b\u6570", "ja": "\u30af\u30e9\u30b9\u30bf\u30fc\u6570"},
    "topics_label": {"en": "Num Topics", "cn": "\u4e3b\u9898\u6570", "ja": "\u30c8\u30d4\u30c3\u30af\u6570"},
    "classifier_label": {"en": "Classifier", "cn": "\u5206\u7c7b\u5668", "ja": "\u5206\u985e\u5668"},
    "ngram_label": {"en": "N-gram Range", "cn": "N-gram \u8303\u56f4", "ja": "N-gram \u7bc4\u56f2"},
    "unigram": {"en": "Unigram (1-gram)", "cn": "\u4e00\u5143 (1-gram)", "ja": "\u30e6\u30cb\u30b0\u30e9\u30e0"},
    "bigram": {"en": "Bigram (2-gram)", "cn": "\u4e8c\u5143 (2-gram)", "ja": "\u30d0\u30a4\u30b0\u30e9\u30e0"},
    "trigram": {"en": "Trigram (3-gram)", "cn": "\u4e09\u5143 (3-gram)", "ja": "\u30c8\u30ea\u30b0\u30e9\u30e0"},
    
    # --- Metric Analysis ---
    "metric_config": {"en": "Configuration", "cn": "\u914d\u7f6e", "ja": "\u8a2d\u5b9a"},
    "metric_select": {"en": "Distance / Similarity Metric", "cn": "\u8ddd\u79bb / \u76f8\u4f3c\u5ea6\u5ea6\u91cf", "ja": "\u8ddd\u96e2 / \u985e\u4f3c\u5ea6\u30e1\u30c8\u30ea\u30c3\u30af"},
    "metric_formula": {"en": "Mathematical Formula", "cn": "\u6570\u5b66\u516c\u5f0f", "ja": "\u6570\u5f0f"},
    "compute_btn": {"en": "Compute & Visualize", "cn": "\u8ba1\u7b97\u5e76\u53ef\u89c6\u5316", "ja": "\u8a08\u7b97\u3068\u53ef\u8996\u5316"},
    "tab_heatmap": {"en": "Heatmap Analysis", "cn": "\u70ed\u529b\u56fe\u5206\u6790", "ja": "\u30d2\u30fc\u30c8\u30de\u30c3\u30d7\u5206\u6790"},
    "tab_mds": {"en": "MDS Projection", "cn": "MDS \u6295\u5f71", "ja": "MDS \u6295\u5f71"},
    "metric_geo": {"en": "Geometric Distances", "cn": "\u51e0\u4f55\u8ddd\u79bb", "ja": "\u5e7e\u4f55\u5b66\u7684\u8ddd\u96e2"},
    "metric_stat": {"en": "Statistical & Correlation", "cn": "\u7edf\u8ba1\u4e0e\u76f8\u5173\u6027", "ja": "\u7d71\u8a08\u3068\u76f8\u95a2"},
    "metric_info": {"en": "Information Theoretic", "cn": "\u4fe1\u606f\u8bba", "ja": "\u60c5\u5831\u7406\u8ad6"},
    "metric_custom": {"en": "Academic Custom", "cn": "\u5b66\u672f\u81ea\u5b9a\u4e49", "ja": "\u30a2\u30ab\u30c7\u30df\u30c3\u30af\u30ab\u30b9\u30bf\u30e0"},
    "metric_other": {"en": "Other", "cn": "\u5176\u4ed6", "ja": "\u305d\u306e\u4ed6"},
    "heatmap_ph": {"en": "Select a metric and click Compute to generate heatmap.", "cn": "\u9009\u62e9\u5ea6\u91cf\u5e76\u70b9\u51fb\u8ba1\u7b97\u4ee5\u751f\u6210\u70ed\u529b\u56fe\u3002", "ja": "\u30e1\u30c8\u30ea\u30c3\u30af\u3092\u9078\u629e\u3057\u3066\u8a08\u7b97\u3092\u30af\u30ea\u30c3\u30af\u3057\u3001\u30d2\u30fc\u30c8\u30de\u30c3\u30d7\u3092\u751f\u6210\u3057\u307e\u3059\u3002"},
    "mds_ph": {"en": "MDS Projection will appear here.", "cn": "MDS \u6295\u5f71\u5c06\u663e\u793a\u5728\u8fd9\u91cc\u3002", "ja": "MDS \u6295\u5f71\u304c\u3053\u3053\u306b\u8868\u793a\u3055\u308c\u307e\u3059\u3002"},
    
    # --- Home ---
    "home_welcome": {"en": "Welcome to MTMinePy", "cn": "\u6b22\u8fce\u4f7f\u7528 MTMinePy", "ja": "MTMinePy \u3078\u3088\u3046\u3053\u305d"},
    "home_subtitle": {"en": "A High-Performance Multilingual Text Mining Platform (Flask Edition).", "cn": "\u9ad8\u6027\u80fd\u591a\u8bed\u8a00\u6587\u672c\u6316\u6398\u5e73\u53f0 (Flask \u7248)\u3002", "ja": "\u9ad8\u6027\u80fd\u591a\u8a00\u8a9e\u30c6\u30ad\u30b9\u30c8\u30de\u30a4\u30cb\u30f3\u30b0\u30d7\u30e9\u30c3\u30c8\u30d5\u30a9\u30fc\u30e0 (Flask \u7248)\u3002"},
    "home_start_msg": {"en": "Start by uploading your dataset in the Data Management section.", "cn": "\u8bf7\u5148\u5728\u6570\u636e\u7ba1\u7406\u90e8\u5206\u4e0a\u4f20\u60a8\u7684\u6570\u636e\u96c6\u3002", "ja": "\u30c7\u30fc\u30bf\u7ba1\u7406\u30bb\u30af\u30b7\u30e7\u30f3\u3067\u30c7\u30fc\u30bf\u30bb\u30c3\u30c8\u3092\u30a2\u30c3\u30d7\u30ed\u30fc\u30c9\u3057\u3066\u958b\u59cb\u3057\u3066\u304f\u3060\u3055\u3044\u3002"},
    "home_btn": {"en": "Get Started", "cn": "\u5f00\u59cb\u4f7f\u7528", "ja": "\u59cb\u3081\u308b"},
    "feat_multi": {"en": "Multilingual", "cn": "\u591a\u8bed\u8a00\u652f\u6301", "ja": "\u591a\u8a00\u8a9e\u5bfe\u5fdc"},
    "feat_multi_desc": {"en": "Support for Chinese, English, Japanese, and 10+ languages.", "cn": "\u652f\u6301\u4e2d\u6587\u3001\u82f1\u6587\u3001\u65e5\u6587\u7b49 10 \u591a\u79cd\u8bed\u8a00\u3002", "ja": "\u4e2d\u56fd\u8a9e\u3001\u82f1\u8a9e\u3001\u65e5\u672c\u8a9e\u306a\u3069 10 \u4ee5\u4e0a\u306e\u8a00\u8a9e\u3092\u30b5\u30dd\u30fc\u30c8\u3002"},
    "feat_academic": {"en": "Academic Metrics", "cn": "\u5b66\u672f\u5ea6\u91cf", "ja": "\u30a2\u30ab\u30c7\u30df\u30c3\u30af\u30e1\u30c8\u30ea\u30af\u30b9"},
    "feat_academic_desc": {"en": "Guiraud, Sichel, Hsim, Close, Esim, and more.", "cn": "\u5305\u542b Guiraud, Sichel, Hsim, Close, Esim \u7b49\u3002", "ja": "Guiraud, Sichel, Hsim, Close, Esim \u306a\u3069\u3002"},
    "feat_ml": {"en": "Advanced ML", "cn": "\u9ad8\u7ea7\u673a\u5668\u5b66\u4e60", "ja": "\u9ad8\u5ea6\u306a\u6a5f\u68b0\u5b66\u7fd2"},
    "feat_ml_desc": {"en": "Boruta, UMAP, STM, Elastic Net integration.", "cn": "\u96c6\u6210 Boruta, UMAP, STM, Elastic Net \u7b49\u3002", "ja": "Boruta, UMAP, STM, Elastic Net \u306e\u7d71\u5408\u3002"},
    
    # --- Data Management ---
    "data_title": {"en": "Data Management", "cn": "\u6570\u636e\u7ba1\u7406", "ja": "\u30c7\u30fc\u30bf\u7ba1\u7406"},
    "data_upload_title": {"en": "Upload Dataset", "cn": "\u4e0a\u4f20\u6570\u636e\u96c6", "ja": "\u30c7\u30fc\u30bf\u30bb\u30c3\u30c8\u306e\u30a2\u30c3\u30d7\u30ed\u30fc\u30c9"},
    "data_upload_btn": {"en": "Upload", "cn": "\u4e0a\u4f20", "ja": "\u30a2\u30c3\u30d7\u30ed\u30fc\u30c9"},
    "data_gen_title": {"en": "Generate Synthetic Data", "cn": "\u751f\u6210\u5408\u6210\u6570\u636e", "ja": "\u5408\u6210\u30c7\u30fc\u30bf\u306e\u751f\u6210"},
    "data_gen_btn": {"en": "Generate Sample Data", "cn": "\u751f\u6210\u6837\u672c\u6570\u636e", "ja": "\u30b5\u30f3\u30d7\u30eb\u30c7\u30fc\u30bf\u306e\u751f\u6210"},
    "data_loaded_msg": {"en": "Data Loaded: {rows} rows, {cols} columns.", "cn": "\u6570\u636e\u5df2\u52a0\u8f7d\uff1a{rows} \u884c\uff0c{cols} \u5217\u3002", "ja": "\u30c7\u30fc\u30bf\u304c\u30ed\u30fc\u30c9\u3055\u308c\u307e\u3057\u305f\uff1a{rows} \u884c\uff0c{cols} \u5217\u3002"},
    
    # --- Preprocess ---
    "preprocess_success": {"en": "Processed {count} rows.", "cn": "\u5df2\u5904\u7406 {count} \u884c\u3002", "ja": "{count} \u884c\u304c\u51e6\u7406\u3055\u308c\u307e\u3057\u305f\u3002"},
    "preprocess_export_title": {"en": "Data Export", "cn": "\u6570\u636e\u5bfc\u51fa", "ja": "\u30c7\u30fc\u30bf\u306e\u30a8\u30af\u30b9\u30dd\u30fc\u30c8"},
    "processing_msg": {"en": "Processing...", "cn": "\u5904\u7406\u4e2d...", "ja": "\u51e6\u7406\u4e2d..."},
}

def get_trans(key, lang='en'):
    return TRANS.get(key, {}).get(lang, TRANS.get(key, {}).get('en', key))

def get_all_langs():
    return {
        "en": "English", "cn": "\u4e2d\u6587 (Chinese)", "ja": "\u65e5\u672c\u8a9e (Japanese)",
        "ko": "\ud55c\uad6d\uc5b4 (Korean)", "ru": "\u0420\u0443\u0441\u0441\u043a\u0438\u0439 (Russian)", "de": "Deutsch (German)",
        "fr": "Fran\u00e7ais (French)", "it": "Italiano (Italian)", "es": "Espa\u00f1ol (Spanish)",
        "pt": "Portugu\u00eas (Portuguese)"
    }
