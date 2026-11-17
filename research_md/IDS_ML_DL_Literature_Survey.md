# IDS ML/DL Literature Survey (sir's document)

Literature Survey

Intrusion Detection Systems Using Machine Learning and Deep Learning

A review of 15 peer-reviewed open-access papers published 2024–2025

# Scope and Selection Criteria

This survey reviews fifteen journal papers on network intrusion detection using machine learning and deep learning, published in 2024 and 2025 and available as open-access PDFs. The scope is general network-based intrusion detection evaluated on benchmark traffic datasets such as NSL-KDD, UNSW-NB15, CIC-IDS2017 and CIC-IDS2018. The set includes classical machine learning pipelines, deep learning and Transformer models, ensemble and two-stage architectures, explainability-oriented studies, data-balancing methods, comparative studies and two surveys. The papers appear in IEEE Access (2), Frontiers journals (3), MDPI journals (6), Journal of Big Data, Scientific Reports, Computer Modeling in Engineering & Sciences and PeerJ Computer Science (one each).

Each entry reports the proposed methodology, performance metrics, dataset or testbed, limitations, two research gaps, tools and technologies, hardware (where stated) and an IEEE-format citation. Values are reproduced as stated by the authors. Where the text, tables or abstract of a paper disagree, or where a methodological issue is evident from the reported procedure, this is recorded under Limitations as an observation and is distinguished from limitations stated by the authors. Research gaps are taken from the authors' stated future work or limitations unless otherwise indicated.

# Reviewed Papers

## 1. A Comparative Study of Using Deep Learning Algorithms in Network Intrusion Detection

## 2. A deep learning/machine learning approach for anomaly based network intrusion detection

## 3. A Hybrid Split-Attention and Transformer Architecture for High-Performance Network Intrusion Detection

## 4. A recurrent neural network for network-based intrusion detection

## 5. Current Status and Challenges and Future Trends of Deep Learning-Based Intrusion Detection Models

## 6. Deep Learning vs. Machine Learning for Intrusion Detection in Computer Networks: A Comparative Study

## 7. Design and Analysis of an Effective Architecture for Machine Learning Based Intrusion Detection Systems

## 8. Detecting Unbalanced Network Traffic Intrusions With Deep Learning

## 9. Enhancing Intrusion Detection Systems Using a Deep Learning and Data Augmentation Approach

## 10. Evaluating machine learning-based intrusion detection systems with explainable AI: enhancing transparency and interpretability

## 11. FPE-Transformer: A Feature Positional Encoding-Based Transformer Model for Attack Detection

## 12. Machine learning-based network intrusion detection for big and imbalanced data using oversampling, stacking feature embedding and feature extraction

## 13. Network-based intrusion detection using deep learning technique

## 14. Unveiling machine learning strategies and considerations in intrusion detection systems: a comprehensive survey

## 15. XI2S-IDS: An Explainable Intelligent 2-Stage Intrusion Detection System

**Table 1:**

| Title of Paper | A Comparative Study of Using Deep Learning Algorithms in Network Intrusion Detection |

| Authors / Year | S. Elsayed, K. Mohamed, M. A. Madkour (2024) |

| Proposed Methodology | A comparative study of six deep learning architectures (DNN, CNN, RNN, LSTM, GRU and a hybrid CNN-LSTM) for binary and five-class intrusion detection on NSL-KDD. The authors state that no new algorithm is proposed. Numerical features are standardized with StandardScaler and the three categorical features (protocol_type, service, flag) are one-hot encoded, which expands the 41 original features to 122. The data are split 80/20 into training and test sets, and 20% of the training portion is held out for validation. Hyperparameters (units, filters, kernel sizes, dropout) are tuned with Keras Tuner; the selected models are trained for 100 epochs with batch size 5000 and the Adam optimizer, using binary or categorical cross-entropy. |

| Performance Metrics | Accuracy, precision, recall and F1-score with confusion matrices. Binary task: GRU 99.54% accuracy (recall 99.67%, F1 99.56%, precision 99.46%), LSTM 99.41%, DNN 99.39%, CNN 99.38%, RNN 99.10%, hybrid CNN-LSTM 98.94%. Multi-class task: DNN 99.34% (recall 99.33%, F1 99.34%, precision 99.36%), CNN 99.39% (99.385% in the text), LSTM 99.39%, RNN 99.25%, hybrid CNN-LSTM 97.96%. |

| Dataset / Testbed Used | NSL-KDD (KDDTrain+, KDDTest+ and KDDTest-21) with 41 features and five classes (Normal, DoS, Probe, R2L, U2R). Per-subset record counts are given in a table that was not available in the text reviewed. |

| Limitations | Evaluation is confined to a single benchmark (NSL-KDD); no cross-dataset or real-traffic testing is reported. The paper has no dedicated limitations section. Observation: the multi-class accuracies reported in the text for CNN (99.385%) and LSTM (99.39%) are higher than that of the DNN (99.34%), yet the conclusion names the DNN as the most effective multi-class model. |

| Research Gaps | 1. Recent architectures such as Transformers have not been compared with the six models; the authors list this as future work.
2. Results are limited to NSL-KDD under offline conditions; the authors identify evaluation on additional datasets and adaptation to real network environments as open work. |

| Tools and Technologies Used | Google Colaboratory, Python 3.10.12, TensorFlow/Keras 2.14.0, Keras Tuner, NumPy, Pandas, scikit-learn. |

| Hardware Used | Intel Core i7-8650U CPU at 1.90 GHz, 16 GB RAM, Intel UHD Graphics 620, 512 GB SSD, Windows 10 Pro (64-bit); model training used a Tensor Processing Unit (TPU) on Google Colab. |

| Citation (IEEE) | S. Elsayed, K. Mohamed, and M. A. Madkour, "A Comparative Study of Using Deep Learning Algorithms in Network Intrusion Detection," IEEE Access, vol. 12, pp. 58851-58870, 2024, doi: 10.1109/ACCESS.2024.3389096. |

**Table 2:**

| Title of Paper | A deep learning/machine learning approach for anomaly based network intrusion detection |

| Authors / Year | R. Almuhanna, S. Dardouri (2025) |

| Proposed Methodology | A hybrid ensemble of XGBoost, Random Forest, a graph neural network (GNN), an LSTM and an autoencoder for anomaly-based network intrusion detection. Preprocessing includes label encoding, StandardScaler normalization, two engineered features (Packet_Length_Ratio and Packet_Size_Diff, not defined in the text) and SMOTE for class imbalance. Data are split 70/15/15 (train/validation/test) with stratification. The ensemble applies weighted soft voting, with weights derived from each model's validation accuracy; the autoencoder flags anomalies from reconstruction error (MSE, threshold 0.01). Reported settings: XGBoost 100 estimators, depth 6, learning rate 0.1; Random Forest 200 trees; LSTM with two 128-unit layers; GNN with three graph-convolution layers (64/128/256 units); autoencoder with 128/64/32 units. |

| Performance Metrics | The ensemble reports precision, recall and F1-score of 1.00 for every class on the test set. Stratified 5-fold cross-validation gives an average accuracy of 93.7% (SD 1.2%). Inference time is about 2.4 ms per instance. Component results: LSTM validation accuracy 99.99% after 10 epochs, Random Forest 100% precision/recall/F1 across classes, autoencoder reconstruction loss below 0.0006, GNN final training loss 0.2864. |

| Dataset / Testbed Used | CICIDS2017 with 80 raw features and 5,661,486 entries. After removing 5,734 rows with missing values and 562,314 duplicates, 5,093,438 instances remain. |

| Limitations | Stated by the authors: possible overfitting to the training distribution; computational overhead and latency for real-time use on edge/IoT devices; baselines taken from literature that used different datasets and protocols; zero-day detection not evaluated. Observations: the headline 100% result conflicts with the 93.7% cross-validation accuracy reported in the same section; the dataset size is given as both 5.6 million and 2.8 million records; the number of classes is given as 15 in one place and 12 in another; the ensemble combination rule is not fully specified. |

| Research Gaps | 1. Interpretability, adversarial robustness (evasion and poisoning), federated learning and adaptation to concept drift remain unaddressed; the authors list SHAP/LIME explainability, adversarial evaluation and adaptive learning as future work.
2. Baselines are compared only contextually, and validation is limited to CICIDS2017; the authors propose re-running baselines under identical conditions and testing on CSE-CIC-IDS2018. |

| Tools and Technologies Used | Software and libraries are not named in the paper. |

| Hardware Used | Intel Core i7 CPU (model not stated) and 64 GB RAM; GPU use is not confirmed. |

| Citation (IEEE) | R. Almuhanna and S. Dardouri, "A deep learning/machine learning approach for anomaly based network intrusion detection," Front. Artif. Intell., vol. 8, Art. no. 1625891, 2025, doi: 10.3389/frai.2025.1625891. |

**Table 3:**

| Title of Paper | A Hybrid Split-Attention and Transformer Architecture for High-Performance Network Intrusion Detection |

| Authors / Year | G. Zhu, Y. Yu, X. Deng, Y. Dai, Z. Li (2025) |

| Proposed Methodology | TransNeSt combines a ResNeSt-style split-attention block adapted to one-dimensional traffic features (1x1 and 3x1 convolutions, cardinality 2, radix 2, four sequential blocks) with a Transformer encoder (4 heads, feed-forward dimension 256, dropout 0.3, RMSNorm) and a [CLS]-token classification head trained with categorical cross-entropy. A separate WGAN is trained for each minority class to generate synthetic samples. Preprocessing comprises feature selection, one-hot encoding, zero imputation and min-max normalization, with a stratified 80/20 split. Regularization uses dropout, weight decay (Adam with L2), augmentation and early stopping. |

| Performance Metrics | F1-score / accuracy of TransNeSt: NSL-KDD 99.04% / 99.05%; UNSW-NB15 91.92% / 91.90%; CIC-IDS2017 99.18% / 99.19%; CICIoT2023 97.85% / 97.85%. Ablation (ResNeSt alone, F1): 97.30%, 88.03%, 97.52% and 95.23% on the same four datasets. On CICIoT2023 the Transformer alone reaches 95.44% F1 and a ResNet-Transformer baseline 96.21%. Selected per-class F1: NSL-KDD U2R 65.38% and R2L 89.39%; CICIoT2023 BruteForce 82.42% and Web 79.30%. |

| Dataset / Testbed Used | NSL-KDD (41 features, 122 after encoding; U2R 0.17%, R2L 2.50%), UNSW-NB15 (42 features, 196 after encoding), CIC-IDS2017 (78 features after removing six metadata fields) and CICIoT2023 (46 features). Total record counts are given only in tables that were not available as text. |

| Limitations | Stated by the authors: the split-attention mechanism is computationally demanding for resource-constrained edge deployment; the model is a black box without intrinsic interpretability; TransNeSt is the most computationally intensive model tested. Observations: no repeated runs or significance tests are reported; the encoder is described as four layers in one section and as two stacked iterations in another; parameter counts, training time and inference latency are not given in the text. |

| Research Gaps | 1. Deployment on IoT and edge devices requires model compression; the authors propose pruning, quantization and knowledge distillation.
2. Minority-class detection remains weaker (U2R, BruteForce, Web) and the model lacks explanation of its decisions; the authors list SHAP/LIME explainability and adaptation to federated learning as future work. |

| Tools and Technologies Used | Python 3.10, PyTorch 2.1.2, CUDA 11.8, Ubuntu 22.04; other libraries are not named. |

| Hardware Used | 12-core Intel Xeon Silver 4214R at 2.40 GHz and an NVIDIA GeForce RTX 3080 Ti with 12 GB VRAM; system RAM is not stated. |

| Citation (IEEE) | G. Zhu, Y. Yu, X. Deng, Y. Dai, and Z. Li, "A Hybrid Split-Attention and Transformer Architecture for High-Performance Network Intrusion Detection," Comput. Model. Eng. Sci., vol. 145, no. 3, pp. 4317-4348, 2025, doi: 10.32604/cmes.2025.074349. |

**Table 4:**

| Title of Paper | A recurrent neural network for network-based intrusion detection |

| Authors / Year | A. Berhanu, S. Chockalingam, J. Abawajy, S. A. Mengiste, S. A. Algamdi, D. Ashenafi (2025) |

| Proposed Methodology | An optimized LSTM-RNN for binary classification (benign vs. malicious) of network traffic. Preprocessing removes zero-value columns, null rows and duplicates, one-hot encodes the protocol feature, ordinal-encodes the label, normalizes the features and applies feature selection (correlation analysis or tree-based importance; the paper does not state which). SMOTE balances minority attack classes. The network uses LSTM layers with 80 hidden units, dropout 0.3, sigmoid output, Adam optimizer, learning rate 0.01, batch size 32, 300 epochs and binary cross-entropy loss, trained by back-propagation through time. An 80/20 train/test split is stated for CIC-IDS-2018. |

| Performance Metrics | CIC-IDS-2018: accuracy 99.94%, precision 99.98%, recall 99.93%, F1-score 99.95%, false alarm rate 0.036% (5 false positives, 21 false negatives). NSL-KDD: accuracy 99.42%, precision 99.20%, recall 99.69%, F1-score 99.45% (31 false positives, 103 false negatives). The comparison table lists six prior studies with accuracies between 95.00% and 99.87%. |

| Dataset / Testbed Used | CIC-IDS-2018 (more than 80 flow-based features) and NSL-KDD (41 traffic features plus label and difficulty score). Record counts and class distributions are shown only in figures; the text gives no sizes. |

| Limitations | Stated by the authors: the model has not been tested in live enterprise or industrial environments, and SMOTE adds minor computational overhead. Observations: SMOTE is applied before the train/test split, which can leak synthetic samples into the test set; the abstract's 99.94% accuracy and 99.98% precision appear in the Results as training and validation accuracy, so the test-set status of the headline figures is unclear; no runtime or latency is reported despite claims of real-time suitability; the model is binary although the abstract refers to DoS, Probe, U2R and R2L categories. |

| Research Gaps | 1. Multiclass attack classification (for example DDoS, SQL injection and malware) is not addressed; the authors list this as future work.
2. Interpretability, continuous retraining under changing traffic and comparison with attention-based Transformer models are open, as stated by the authors; live-network validation is also missing. |

| Tools and Technologies Used | Not stated in the paper. |

| Hardware Used | Not stated in the paper. |

| Citation (IEEE) | A. Berhanu, S. Chockalingam, J. Abawajy, S. A. Mengiste, S. A. Algamdi, and D. Ashenafi, "A recurrent neural network for network-based intrusion detection," PeerJ Comput. Sci., vol. 11, Art. no. e3306, 2025, doi: 10.7717/peerj-cs.3306. |

**Table 5:**

| Title of Paper | Current Status and Challenges and Future Trends of Deep Learning-Based Intrusion Detection Models |

| Authors / Year | Y. Wu, B. Zou, Y. Cao (2024) |

| Proposed Methodology | A review (no new model) of deep learning-based intrusion detection models from literature published between 2018 and 2024. It covers data preprocessing techniques and then seven model families: deep autoencoders, deep belief networks, deep neural networks, convolutional neural networks, recurrent neural networks (LSTM, GRU, bidirectional), generative adversarial networks and Transformers, together with BERT-based and GPT-based models. The review closes with challenges and future research directions. |

| Performance Metrics | No original experimental results. The surveyed studies report accuracy, precision, recall, F1-score, false positive rate, detection rate, false alarm rate and ROC AUC; the review has no dedicated metrics section, and the authors note that some studies report a single metric only. |

| Dataset / Testbed Used | The review catalogues KDDCup99, NSL-KDD, UNSW-NB15, CIC-IDS2017, Kyoto 2006+, ISCX2012 and MQTTset2020, and also mentions CIC IoT 2023, TON_IoT and ZYELL-NCTU NetTraffic-1.0. No dataset was used by the authors. |

| Limitations | The paper does not state the databases searched, the search strategy, the inclusion criteria or the number of papers reviewed, so the selection cannot be reproduced; it describes its literature window as seven years in one place and five years in another. It reports no original experiments. Limitations of the reviewed methods that it records include outdated datasets, class imbalance, high computational cost, overfitting and weak U2R/R2L detection. |

| Research Gaps | 1. Up-to-date, real-network datasets and approaches that generalize across domains are lacking; the authors point to regular dataset updates, adversarial training, transfer learning and federated learning.
2. Deployment on resource-constrained systems and in cyber-physical settings (SCADA, UAV networks) is open; the authors propose pruning, quantization, knowledge distillation and lightweight architectures. |

| Tools and Technologies Used | No implementation tools are named; the review describes techniques such as SMOTE, GAN, VAE and PCA. |

| Hardware Used | Not applicable (review). GPUs, cloud GPU services, FPGA, Edge TPU and NVIDIA Jetson Nano are mentioned only as deployment options. |

| Citation (IEEE) | Y. Wu, B. Zou, and Y. Cao, "Current Status and Challenges and Future Trends of Deep Learning-Based Intrusion Detection Models," J. Imaging, vol. 10, no. 10, Art. no. 254, 2024, doi: 10.3390/jimaging10100254. |

**Table 6:**

| Title of Paper | Deep Learning vs. Machine Learning for Intrusion Detection in Computer Networks: A Comparative Study |

| Authors / Year | M. L. Ali, K. Thakur, S. Schmeelk, J. Debello, D. Dragos (2025) |

| Proposed Methodology | A comparison of six classical machine learning models (logistic regression, Gaussian naive Bayes, random forest, KNN, decision tree, SVM) and three deep learning models (MLP, CNN, LSTM) on CICIDS2017. Preprocessing removes 308,381 duplicates, imputes 353 missing values with column means, removes rows with infinite values, merges labels into groups (for example Web Attack, DoS, Other), selects features with a 0.85 absolute-correlation threshold and scales them with StandardScaler. A stratified split is followed by SMOTE; hyperparameters are tuned by random search. Layer counts, optimizer, learning rate, batch size and epochs of the deep models are not reported. |

| Performance Metrics | Machine learning (accuracy / average F1): random forest 99.88% / 97.46%, decision tree 99.83% / 97.76%, KNN 99.36% / 97.62%, logistic regression 96.91% / 73.96%, naive Bayes 64.59% / 48.70%. Deep learning (accuracy / macro F1): MLP 97% / 0.82, CNN 98% / 0.83, LSTM 98% / 0.84. No SVM figures are given. Training time, inference latency and memory use are not reported. |

| Dataset / Testbed Used | CICIDS2017 with 2,830,743 rows and 79 columns before cleaning. The post-cleaning size, class counts, split ratio and SMOTE output size are not stated. |

| Limitations | Stated by the authors: CICIDS2017 is generated in a controlled environment and may not reflect real-world variability; some attack classes are under-represented; CNN and LSTM may be too heavy for real-time use on constrained devices. Observations: the abstract states that CNN and LSTM outperform traditional models, whereas random forest (99.88%) exceeds both (98%); two sections report different F1 values for the same models; the order of SMOTE relative to the train/test split is not stated, so leakage cannot be excluded; the promised efficiency evaluation is not reported. |

| Research Gaps | 1. Deep and classical models are compared without reported architectures, hyperparameters or compute cost, which limits reproducibility and the assessment of real-time suitability.
2. Authors identify hybrid deep/traditional models, unsupervised and semi-supervised learning, and robustness under adversarial or noisy data as unexplored directions. |

| Tools and Technologies Used | scikit-learn 1.6.1 and Pandas; the deep learning framework is not named. |

| Hardware Used | Not stated in the paper. |

| Citation (IEEE) | M. L. Ali, K. Thakur, S. Schmeelk, J. Debello, and D. Dragos, "Deep Learning vs. Machine Learning for Intrusion Detection in Computer Networks: A Comparative Study," Appl. Sci., vol. 15, no. 4, Art. no. 1903, 2025, doi: 10.3390/app15041903. |

**Table 7:**

| Title of Paper | Design and Analysis of an Effective Architecture for Machine Learning Based Intrusion Detection Systems |

| Authors / Year | N. Alromaihi, M. Rouached, A. Akremi (2025) |

| Proposed Methodology | A two-layer deployment architecture in which a proxy server inspects all incoming traffic. The first layer selects one of two ML models according to traffic load (a faster model above an administrator-set threshold, a more accurate model otherwise); the second layer applies a highly accurate ML-based NIDS before traffic reaches the server. Detection combines signatures with behaviour-based analysis. Six models are evaluated: AdaBoost, Voting, Stacking, SVM, Random Forest and XGBoost. Settings: 80/20 split, 5-fold cross-validation, GridSearchCV, SelectKBest and VarianceThreshold feature selection, StandardScaler, RandomUnderSampler for class balance. |

| Performance Metrics | Accuracy (CIC-MalMem-2022 / CIC-IDS-2018 / CIC-IDS-2017): Stacking 99.98% / 99.61% / 99.86%; Random Forest 99.98% / 99.64% / 99.40%; Voting 99.96% / 99.58% / 99.31%; AdaBoost 99.94% / 99.11% / 98.64%; SVM 99.93% / 97.41% / 94.04%; XGBoost 99.96% / 99.73% / 99.84% with test times of 0.01-0.04 s. Under adversarial evaluation on CIC-IDS-2018, XGBoost reaches 99.57-99.63% without retraining and 99.75% with retraining. |

| Dataset / Testbed Used | CIC-MalMem-2022 (534 duplicate rows removed, 25 features retained), CIC-IDS-2018 (5,000 records per file from ten files, reduced to 32,713 samples, 72 features) and CIC-IDS-2017 (50,000 records per file from eight files, reduced to 66,757 samples, 30 features). |

| Limitations | Stated by the authors: a much larger real-world dataset is needed; data augmentation may be required to avoid overfitting; the architecture has not been deployed in a real setting; retraining is required after changes in topology, device types or traffic volume. Observations: the abstract names Stacking as the most accurate model, but Random Forest matches it on CIC-MalMem-2022 and exceeds it on CIC-IDS-2018 in the reported table; the identity of the two first-layer models and the choice of threshold are not specified; only test times are reported, with no throughput measurements. |

| Research Gaps | 1. The architecture is validated offline on sampled subsets of public datasets; evaluation in a real business network is proposed as future work.
2. Automatic blocking of malicious IPs through firewalls with a threat-intelligence feed, evaluation on UNSW-NB15 and deep learning alternatives remain to be explored, as stated by the authors. |

| Tools and Technologies Used | Python (3.10.0 objects cited), Google Colab, pandas, psutil, pickle, XGBoost 3.0.0; scikit-learn is implied by the function names but is not named. |

| Hardware Used | HP laptop with Intel Core i7-8550U, 16 GB RAM, Windows 11; GPU use is not stated. |

| Citation (IEEE) | N. Alromaihi, M. Rouached, and A. Akremi, "Design and Analysis of an Effective Architecture for Machine Learning Based Intrusion Detection Systems," Network, vol. 5, no. 2, Art. no. 13, 2025, doi: 10.3390/network5020013. |

**Table 8:**

| Title of Paper | Detecting Unbalanced Network Traffic Intrusions With Deep Learning |

| Authors / Year | S. Pavithra, K. V. Vikas (2024) |

| Proposed Methodology | The paper applies the Difficult Set Sampling Technique (DSSTE), which combines nearest-neighbour and k-means clustering to remove redundant majority-class samples and to synthesize minority-class samples, to rebalance CICIDS2017. A Random Forest Regressor is used as a feature extractor and an LSTM as the main classifier; XGBoost, AlexNet and Mini-VGGNet are trained for comparison. XGBoost parameters are tuned by grid search. |

| Performance Metrics | Accuracy: LSTM 96.73% (best), XGBoost 93.4%, AlexNet 93%. The text reports precision, recall, F1-score and confusion matrices for the models but gives no accuracy figure for Mini-VGGNet; per-class values are shown in tables and figures not available as text. |

| Dataset / Testbed Used | CICIDS2017 (benign and attack classes including DoS Hulk, DDoS, GoldenEye, Slowhttptest, Slowloris, FTP-Patator, SSH-Patator, PortScan, Web Attack variants, Bot, Infiltration and Heartbleed). Record counts and the train/test split are not given in the text reviewed. |

| Limitations | The paper has no limitations section. Observations: the DSSTE description is repeated in two subsections; AlexNet and Mini-VGGNet are image architectures applied to tabular traffic features without a stated adaptation; only one dataset is used; real-time operation is mentioned as a future direction but is not evaluated. |

| Research Gaps | 1. Real-time deployment of the trained model on live traffic is not evaluated; the conclusion identifies it as a next step.
2. Validation on additional datasets and on class-level metrics for rare attacks is absent, so the benefit of DSSTE for minority classes is not demonstrated in the text. |

| Tools and Technologies Used | Python and scikit-learn on Windows 11. |

| Hardware Used | Intel Xeon E-2124 at 3.30 GHz, 32 GB RAM, 64-bit system. |

| Citation (IEEE) | S. Pavithra and K. V. Vikas, "Detecting Unbalanced Network Traffic Intrusions With Deep Learning," IEEE Access, vol. 12, pp. 74096-74107, 2024, doi: 10.1109/ACCESS.2024.3405187. |

**Table 9:**

| Title of Paper | Enhancing Intrusion Detection Systems Using a Deep Learning and Data Augmentation Approach |

| Authors / Year | R. Mohammad, F. Saeed, A. A. Almazroi, F. S. Alsubaei, A. A. Almazroi (2024) |

| Proposed Methodology | Five convolutional and recurrent architectures are evaluated with and without data augmentation: (1) Conv1D(128)-MaxPool-Conv1D(64)-MaxPool-Dense(128)-Dropout-Dense(64)-Softmax; (2) architecture 1 with an extra dense layer; (3) CNN + GRU; (4) CNN + GRU + bidirectional LSTM; (5) CNN + two bidirectional LSTM layers. Inputs are min-max normalized and categorical features are one-hot encoded; the Adam optimizer starts at a learning rate of 0.001 with a custom scheduler. Augmentation oversamples each class to equal size using SMOTE on the training data (the paper also states that it was applied to the test portion), with stratified K-fold validation (K not stated). |

| Performance Metrics | Binary: UNSW-NB15 about 95% and CIC-IDS-2017 about 96% accuracy. Multi-class: UNSW-NB15 (10 classes) 82% before and 74% after augmentation; CIC-IDS-2017 (15 classes) architecture 1 98% before and 85% after augmentation, architecture 5 98% before and 92% after; 5G-NIDD (9 classes) 97% (architecture 1) and 98% (architecture 5) after augmentation; FLNET2023 (11 classes) 100% for both. Examples of weak classes: Web Attack XSS precision 0.53 and Web Attack Brute Force recall 0.15 on CIC-IDS-2017 after augmentation. |

| Dataset / Testbed Used | UNSW-NB15 (257,673 records, 10 classes), CIC-IDS-2017 (2,830,540 records in the paper's table, 15 classes), 5G-NIDD (nine classes; size not stated) and FLNET2023 (11 classes; size not stated). |

| Limitations | Stated by the authors: low accuracy on minority classes; augmentation lowered overall accuracy on UNSW-NB15; the more complex architectures cost time, computation and memory; the simulated 5G-NIDD and FLNET2023 data may not represent real intrusions. Observations: the paper reports augmentation on the test portion, which can inflate results; the abstract states up to 91% for augmented CIC-IDS-2017 while the table gives 92%; the input length (196) disagrees with the first layer output shape (192); only after-augmentation tables are given for 5G-NIDD and FLNET2023. |

| Research Gaps | 1. Augmentation did not uniformly improve results and its effect on minority classes such as SQL injection and XSS remains weak, indicating the need for class-specific approaches (stated by the authors).
2. Other deep learning architectures should be tested across a broader range of datasets, as the authors state, and the realism of simulated 5G and federated-learning traffic needs validation. |

| Tools and Technologies Used | Not stated (only the Adam optimizer is named). |

| Hardware Used | Not stated. |

| Citation (IEEE) | R. Mohammad, F. Saeed, A. A. Almazroi, F. S. Alsubaei, and A. A. Almazroi, "Enhancing Intrusion Detection Systems Using a Deep Learning and Data Augmentation Approach," Systems, vol. 12, no. 3, Art. no. 79, 2024, doi: 10.3390/systems12030079. |

**Table 10:**

| Title of Paper | Evaluating machine learning-based intrusion detection systems with explainable AI: enhancing transparency and interpretability |

| Authors / Year | V. Z. Mohale, I. C. Obagbuwa (2025) |

| Proposed Methodology | Five classifiers (Decision Tree, Gaussian Naive Bayes, CatBoost, XGBoost, MLP) are trained on UNSW-NB15 and explained post hoc. Preprocessing removes duplicates, applies Recursive Feature Elimination and correlation analysis, min-max scaling, one-hot and label encoding, and SMOTE (a later section states that sampling was ignored). Explanations use SHAP (global and local), LIME (local, mainly MLP and CatBoost) and ELI5 permutation importance (mainly Decision Tree). A deployment of XGBoost with SHAP in a simulated enterprise network is described without setup details or quantitative results. |

| Performance Metrics | Accuracy / precision / recall / F1 / ROC-AUC / FPR / FNR: Decision Tree 87% / 0.85 / 0.88 / 0.86 / 0.92 / 0.07 / 0.12; CatBoost 87% / 0.86 / 0.88 / 0.87 / 0.94 / 0.07 / 0.12; XGBoost 86.87% / 0.85 / 0.88 / 0.86 / 0.93 / 0.08 / 0.11; MLP 85.98% / 0.84 / 0.87 / 0.85 / 0.91 / 0.09 / 0.13; Gaussian Naive Bayes 73% / 0.70 / 0.75 / 0.72 / 0.83 / 0.15 / 0.25. |

| Dataset / Testbed Used | UNSW-NB15: 2,540,044 records across four CSV files (49 features); the training and testing partitions of 175,341 and 82,332 records are used in the experiments. |

| Limitations | Stated by the authors: XAI integration needs extra computing resources and expertise; evaluation relies on a single dataset; false negatives may hide advanced threats. Observations: the abstract lists Random Forest and Logistic Regression, which do not appear in the methods or results; the abstract and Table 4 differ for XGBoost's FPR and FNR; the feature count is 49 in one section and 39 numeric features in another; the abstract states nine attack types whereas the dataset section lists ten categories including Normal. |

| Research Gaps | 1. Explanations are provided only for classical models; extending the approach to CNN and RNN architectures with attention or saliency-based explanations is proposed by the authors.
2. Lightweight XAI methods compatible with real-time detection, and evaluation in cloud, IoT and mobile network settings, remain open; the authors also note the limited number of cross-dataset comparative studies. |

| Tools and Technologies Used | SHAP, LIME, ELI5, scikit-learn, XGBoost and CatBoost; versions are not reported. |

| Hardware Used | Not reported. |

| Citation (IEEE) | V. Z. Mohale and I. C. Obagbuwa, "Evaluating machine learning-based intrusion detection systems with explainable AI: enhancing transparency and interpretability," Front. Comput. Sci., vol. 7, Art. no. 1520741, 2025, doi: 10.3389/fcomp.2025.1520741. |

**Table 11:**

| Title of Paper | FPE-Transformer: A Feature Positional Encoding-Based Transformer Model for Attack Detection |

| Authors / Year | H. C. Zaim, E. N. Yolacan (2025) |

| Proposed Methodology | An encoder-only Transformer with four stages (feature positional encoding, encoder, pooling, classification head). The feature positional encoding (FPE) assigns each input feature its own sine/cosine encoding with a per-feature frequency term, in place of one shared encoding. FPE is compared with uniform positional encoding (UPE) and standard positional encoding (PE) for binary and multi-class tasks. For NSL-KDD only numeric features are used; Borderline-SMOTE oversamples attacks and k-NN (k = 3) downsamples benign traffic for the binary task. For CIC-IDS2017, four features are chosen by Random Forest importance. Settings: one encoder layer, two heads, dropout 0.1, batch size 100, 20 epochs, Adam with learning rate 0.001. |

| Performance Metrics | Accuracy (FPE / UPE / PE): NSL-KDD binary 0.899 / 0.873 / 0.870; CIC-IDS2017 binary 0.917 / 0.876 / 0.871; NSL-KDD multi-class 0.773 / 0.757 / 0.758; CIC-IDS2017 multi-class 0.906 / 0.865 / 0.864. Reported loss for FPE: 0.35, 0.18, 0.13 and 0.26 in the same order. Precision, recall and F1-score are not reported. |

| Dataset / Testbed Used | NSL-KDD (training subset of 125,972 and test subset of 22,543 samples) and CIC-IDS2017 (about 2,672,997 samples recorded over one week at 10 Gbps). |

| Limitations | The authors do not state limitations explicitly. Observations: only accuracy and loss are reported, with no precision, recall, F1 or per-class results; repeated runs and significance tests are not reported; model dimension, feed-forward size and the train/test ratio are not stated; multi-class NSL-KDD accuracy of 77.3% is comparatively low; only four CIC-IDS2017 features are used. |

| Research Gaps | 1. Attack-specific behaviour is not modelled by the attention mechanism; the authors propose optimizing multi-head attention for this purpose and strengthening detection of anomalies over time.
2. The model uses one data source and is evaluated on two datasets; integration of multiple data sources and use of past attack knowledge for adaptability are listed by the authors as future work. |

| Tools and Technologies Used | Python 3.10.12, PyTorch, Google Colab. |

| Hardware Used | Google Colab environment with a 2.9 GHz CPU, 12.68 GB RAM and 107.72 GB disk; GPU not stated. |

| Citation (IEEE) | H. C. Zaim and E. N. Yolacan, "FPE-Transformer: A Feature Positional Encoding-Based Transformer Model for Attack Detection," Appl. Sci., vol. 15, no. 3, Art. no. 1252, 2025, doi: 10.3390/app15031252. |

**Table 12:**

| Title of Paper | Machine learning-based network intrusion detection for big and imbalanced data using oversampling, stacking feature embedding and feature extraction |

| Authors / Year | M. A. Talukder, M. M. Islam, M. A. Uddin, K. F. Hasan, S. Sharmin, S. A. Alyami, M. A. Moni (2024) |

| Proposed Methodology | An eight-step pipeline: cleaning (missing, infinite and duplicate rows; merging low-instance classes; down-casting numeric types), z-score standardization, random oversampling (RO), stacking feature embedding (SFE) that appends K-Means and Gaussian Mixture clustering outputs as meta-features, PCA to 10 components, 10-fold cross-validation, classification with Decision Tree, Random Forest, Extra Trees and XGBoost, and evaluation by accuracy, precision, recall, F1, confusion matrix and ROC/AUC. |

| Performance Metrics | Accuracy with SFE-PCA features: UNSW-NB15 binary RF/ET 99.59%, DT 98.97%, XGB 98.81%; UNSW-NB15 multi-class RF/ET 99.95%; CIC-IDS2017 binary ET 99.95%, RF 99.94%; CIC-IDS2017 multi-class DT/RF/ET 99.99%; CIC-IDS2018 DT/ET 99.94%, RF 99.93%, XGB 99.87%. Without SFE-PCA (all features), UNSW-NB15 multi-class accuracy falls to 85.38-87.73%. |

| Dataset / Testbed Used | UNSW-NB15 (257,673 records in the processed set; nine attack categories plus Normal), CIC-IDS2017 (2,830,743 records; 80.3% benign) and CIC-IDS2018 (10% per-class sample of 933,277 records, 80 features, 15 classes). |

| Limitations | Stated by the authors: deep learning models and optimization techniques were not used. Observations: the text and tables disagree for CIC-IDS2017 multi-class accuracy (99.91% vs. 99.99%) and for XGBoost on CIC-IDS2018 (98.87% vs. 99.87%); the text reports an XGBoost AUC of 84.85% on CIC-IDS2018, which is inconsistent with its 99.87% accuracy; oversampling is described before the cross-validation folds, so leakage of replicated samples across folds is not excluded by the description. |

| Research Gaps | 1. The literature reviewed relies on older datasets (KDDCUP'99, NSL-KDD), neglects data balancing, uses full feature sets and omits time-complexity analysis; the paper positions SFE as addressing these.
2. Extension to deep learning models (DNN, RNN, hybrid architectures) on the same framework is identified by the authors as future work. |

| Tools and Technologies Used | Python with TensorFlow, Keras, Pandas, scikit-learn, NumPy, Seaborn, Matplotlib and imbalanced-learn, run in Jupyter Notebook via Anaconda Navigator. |

| Hardware Used | Cloud virtual machine with 8 cores, 64 GB RAM and 40 GB disk; CPU model and GPU not specified. |

| Citation (IEEE) | M. A. Talukder, M. M. Islam, M. A. Uddin, K. F. Hasan, S. Sharmin, S. A. Alyami, and M. A. Moni, "Machine learning-based network intrusion detection for big and imbalanced data using oversampling, stacking feature embedding and feature extraction," J. Big Data, vol. 11, Art. no. 33, 2024, doi: 10.1186/s40537-024-00886-w. |

**Table 13:**

| Title of Paper | Network-based intrusion detection using deep learning technique |

| Authors / Year | M. Farhan, H. Waheed ud din, S. Ullah, M. S. Hussain, M. A. Khan, T. Mazhar, U. F. Khattak, I. H. Jaghdam (2025) |

| Proposed Methodology | A sequential deep neural network with ReLU activation and Extra Trees Classifier feature selection for binary intrusion detection. Features are standardized, SMOTE balances the classes, and the Extra Trees Classifier (importance threshold 0.021) reduces the 43 input features to eight (including sttl, dttl, ct_state_ttl and ct_srv_dst). The DNN is trained for 100 epochs with batch size 50 on a 70/30 train/test split. |

| Performance Metrics | Binary classification accuracy 97.93% with precision, recall and F1-score of 97%; ROC AUC 0.99 for both classes; 5-fold cross-validation mean accuracy 97.2% (SD 0.5). The confusion matrix reports 15,255 true negatives, 35,666 true positives, 1,466 false positives and 216 false negatives. |

| Dataset / Testbed Used | UNSW-NB15 with 175,341 records and 43 input features plus a binary label. |

| Limitations | The paper has no limitations section. Observation: the accuracy computed from the reported confusion-matrix counts is about 96.8% (50,921 of 52,603 test samples), which differs from the stated 97.93%. The study is binary only, uses a single dataset, and does not report software versions or hardware. |

| Research Gaps | 1. Multiclass attack classification is not covered; the authors list it as future work.
2. Real-time deployment, adversarial robustness, explainability, ensemble or transfer learning, and federated learning are not examined and are proposed by the authors as extensions. |

| Tools and Technologies Used | Not stated in the paper. |

| Hardware Used | Not stated in the paper. |

| Citation (IEEE) | M. Farhan, H. Waheed ud din, S. Ullah, M. S. Hussain, M. A. Khan, T. Mazhar, U. F. Khattak, and I. H. Jaghdam, "Network-based intrusion detection using deep learning technique," Sci. Rep., vol. 15, Art. no. 25550, 2025, doi: 10.1038/s41598-025-08770-0. |

**Table 14:**

| Title of Paper | Unveiling machine learning strategies and considerations in intrusion detection systems: a comprehensive survey |

| Authors / Year | A. H. Ali, M. Charfeddine, B. Ammar, B. B. Hamed, F. Albalwy, A. Alqarafi, A. Hussain (2024) |

| Proposed Methodology | A survey of machine learning and deep learning approaches to intrusion detection in peer-reviewed work since 2020. It discusses the main ML and DL algorithms, benchmark datasets, evaluation metrics and open challenges, and summarizes 16 studies in a comparison table. According to the survey's own figure, 45% of the reviewed methods use only ML, 40% only DL and 13% hybrid approaches. |

| Performance Metrics | No original results. The survey explains the confusion matrix, accuracy, precision, recall (TPR), false alarm rate, true negative rate, F-measure, false discovery rate and Matthews correlation coefficient, and mentions false negative rate, convergence behaviour and computational time. |

| Dataset / Testbed Used | Catalogued datasets: KDD Cup '99, NSL-KDD, Kyoto 2006+, UNSW-NB15, CICIDS2017, CSE-CICIDS2018, CIC IoT 2023, CIC-MalMem-2022 and IoT Intrusion 2020, with their feature counts. |

| Limitations | The survey states no limitations of its own. It does not report the databases searched, the search strings, the selection criteria or the total number of papers reviewed. Observations: the method percentages in its figure sum to 98%; NSL-KDD is described with 24 attributes in one section and 41 in the dataset table; the definitions of false alarm rate and false discovery rate overlap. It reports that 41% of reviewed methods were tested on outdated datasets. |

| Research Gaps | 1. Reviewed methods generally fail on zero-day attacks, rely on outdated datasets and degrade on imbalanced classes; the authors call for regular testing on updated datasets and better per-attack performance in real settings.
2. A lightweight, low-complexity IDS framework is needed; the authors list zero-day detection, feature engineering, deep reinforcement learning, adversarial defences, SHAP-based explainability, transfer learning and two-level per-packet/per-flow classification as trends. |

| Tools and Technologies Used | Not applicable (survey). |

| Hardware Used | Not applicable (survey). |

| Citation (IEEE) | A. H. Ali, M. Charfeddine, B. Ammar, B. B. Hamed, F. Albalwy, A. Alqarafi, and A. Hussain, "Unveiling machine learning strategies and considerations in intrusion detection systems: a comprehensive survey," Front. Comput. Sci., vol. 6, Art. no. 1387354, 2024, doi: 10.3389/fcomp.2024.1387354. |

**Table 15:**

| Title of Paper | XI2S-IDS: An Explainable Intelligent 2-Stage Intrusion Detection System |

| Authors / Year | M. M. Mahmoud, Y. O. Youssef, A. A. Abdel-Hamid (2025) |

| Proposed Methodology | A two-stage IDS. Preprocessing removes address features and null records, adds a total-bytes feature, standardizes numeric features and one-hot encodes categorical ones. Stage I is a binary classifier: eight ML models tuned with Optuna are compared and LightGBM is selected, with SHAP providing global explanations. Stage II classifies attack records only (normal records removed) with BI-LSTM or CNN-BI-LSTM, each with and without SMOTE; BI-LSTM with SMOTE is selected. Records labelled normal in Stage I receive label -1 and skip Stage II. The binary stage uses an 80/20 split, and a 75/25 split of the training data forms the validation set for Stage II. |

| Performance Metrics | Overall accuracy, two-stage vs. single-stage: CICIDS2017 0.9981 vs. 0.9945; UNSW-NB15 0.9774 vs. 0.9754. Stage I: LightGBM false negative rate 0.0004 (CICIDS2017) and 0.019 (UNSW-NB15). Per-class F1: Bot 0.76 vs. 0.63 and DoS Slowhttptest 0.97 on CICIDS2017; Analysis 0.12 and Backdoor 0.15 on UNSW-NB15 (single-stage 0 for both). False negative rate for Heartbleed fell from 100% to 20% and for Infiltration from 100% to 33%. |

| Dataset / Testbed Used | CICIDS2017 (2,273,097 normal and 557,646 attack records, 14 attack classes) and UNSW-NB15 (2,540,047 records, about 87% normal, 49 features, nine attack classes; the full dataset rather than the 257,673-record subset). |

| Limitations | Stated by the authors: SMOTE may cause overfitting because synthetic samples may not match real attacks; SHAP's computational cost may hinder real-time use; real-time evaluation was not performed. Observation: the Exploits class F1 is lower in the two-stage model (0.60) than in the single-stage model (0.69), although the text describes the two-stage result as an improvement; Stage II accuracy for the four deep learning variants is not available in the text reviewed. |

| Research Gaps | 1. False negatives in the binary stage and confusion among highly correlated attack categories in Stage II remain; the authors propose further reduction and refinement.
2. Performance under live network conditions is untested; the authors list real-time evaluation as future work. |

| Tools and Technologies Used | Python 3.7.13, TensorFlow 1.13.2, scikit-learn 1.0.2, Optuna, SHAP, LightGBM, XGBoost. |

| Hardware Used | Intel i7 CPU (model not stated), 16 GB RAM and an NVIDIA RTX 2080 Ti GPU. |

| Citation (IEEE) | M. M. Mahmoud, Y. O. Youssef, and A. A. Abdel-Hamid, "XI2S-IDS: An Explainable Intelligent 2-Stage Intrusion Detection System," Future Internet, vol. 17, no. 1, Art. no. 25, 2025, doi: 10.3390/fi17010025. |