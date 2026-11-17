# 06_Ali_2025_Appl_Sci_DL_vs_ML_IDS

_Source PDF, 19 pages. Auto-converted._

Academic Editor: David Megías
Received: 19 January 2025
Revised: 8 February 2025
Accepted: 10 February 2025
Published: 12 February 2025
Citation: Ali, M.L.; Thakur, K.;
Schmeelk, S.; Debello, J.; Dragos, D.
Deep Learning vs. Machine Learning
for Intrusion Detection in Computer
Networks: A Comparative Study.
Appl. Sci. 2025, 15, 1903. https://
doi.org/10.3390/app15041903
Copyright: © 2025 by the authors.
Licensee MDPI, Basel, Switzerland.
This article is an open access article
distributed under the terms and
conditions of the Creative Commons
Attribution (CC BY) license
(https://creativecommons.org/
licenses/by/4.0/).
Article
Deep Learning vs. Machine Learning for Intrusion Detection in
Computer Networks: A Comparative Study
Md Liakat Ali 1,*
, Kutub Thakur 2, Suzanna Schmeelk 2, Joan Debello 2 and Denise Dragos 2
1
Department of Computer Science & Physics, Rider University, Lawrenceville, NJ 08648, USA
2
College of Professional Studies, St. John’s University, New York, NY 11439, USA; thakurk@stjohns.edu (K.T.);
schmeels@stjohns.edu (S.S.); debelloj@stjohns.edu (J.D.); dragosd@stjohns.edu (D.D.)
*
Correspondence: mdali@rider.edu
Abstract: In response to the increasing volume of network traffic and the growing sophis-
tication of cyber threats, this study examines the use of deep learning-based intrusion
detection systems (IDSs) in large-scale network environments. Traditional IDS face chal-
lenges such as high false positive rates, complex feature engineering, and class imbalances
in datasets, all of which impede accurate threat detection. To overcome these limitations,
we implement various deep learning models, including multilayer perceptron (MLP),
convolutional neural network (CNN), and long short-term memory (LSTM), alongside
traditional machine learning algorithms such as logistic regression, naive Bayes, random
forest, K-nearest neighbors, and decision trees. A significant contribution of this study is the
application of the synthetic minority over-sampling technique (SMOTE) to address class im-
balance, enhancing the representativeness of the learning process. Additionally, we conduct
a comprehensive performance comparison of the models, incorporating correlation-based
feature selection and hyperparameter tuning to maximize detection accuracy. Our results
indicate that deep learning models, particularly CNN and LSTM, outperform traditional
machine learning approaches in cyber threat detection, achieving accuracy rates of 98%.
However, random forest achieves the highest accuracy at 99.9%, demonstrating its effec-
tiveness in structured intrusion detection tasks. Moreover, we evaluate computational
efficiency and practical deployment considerations, discussing trade-offs between accuracy
and resource consumption. These findings highlight the potential of deep learning-based
IDS for large-scale network security applications while addressing key challenges such
as interpretability and computational overhead. The study provides actionable insights
for selecting the most suitable IDS models based on specific network environments and
security requirements.
Keywords: cyber security; machine learning; deep learning; network intrusion detection;
data analysis; CICIDS2017; comparative analysis
1. Introduction
In recent years, the rapid advancement of information technology and the widespread
adoption of the internet have transformed how people live and work [1]. Digital technolo-
gies have become essential in various aspects of life, ranging from e-commerce [2] and social
media [3] to telemedicine and remote work [4]. However, this digital transformation [5]
has also heightened the vulnerability of computer networks to cyber threats, including
unauthorized access, data breaches, and other malicious activities [6]. Cybercriminals
continuously develop new techniques and strategies to exploit network vulnerabilities,
posing serious risks to individuals, businesses, and governments worldwide [7–9]. As a
Appl. Sci. 2025, 15, 1903
https://doi.org/10.3390/app15041903

Appl. Sci. 2025, 15, 1903
2 of 19
result, the demand for effective intrusion detection systems (IDS) capable of identifying
and mitigating cyberattacks in real time has increased [10]. Traditional IDS primarily rely
on rule-based or signature-based approaches to detect known threats [11]. These methods
function by comparing network traffic patterns against a database of predefined attack
signatures or rules describing malicious activities. While signature-based IDS have proven
effective against previously identified threats, they often struggle to detect novel or sophis-
ticated attacks that do not conform to existing patterns [12]. Moreover, rule-based methods
frequently generate a high number of false positives, increasing operational burdens and
reducing efficiency in network security management [13].
Rule-based intrusion detection systems (IDSs) frequently experience high false positive
rates because they depend on predefined signatures and rules, which struggle to adapt
to emerging attack patterns. Research indicates that these systems often produce an
overwhelming number of false alarms, straining security analysts and diminishing overall
system efficiency [11,12]. Although signature-based IDS excel at detecting known threats,
they struggle to identify zero-day attacks and emerging cyber threats. Consequently,
they demonstrate a considerable detection gap when faced with sophisticated adversarial
techniques [10,13]. Traditional IDS methods, including statistical anomaly detection and
expert-defined heuristics, demand significant manual configuration and have difficulty
adapting to evolving network environments. Recent studies suggest that these systems
struggle to scale efficiently as network traffic complexity grows [14,15].
Recently, machine learning techniques have been extensively employed to enhance
the accuracy, efficiency, and adaptability of intrusion detection systems (IDS) [16]. Unlike
traditional rule-based approaches, which rely on static signatures and predefined rules,
machine learning-based IDS analyze network traffic data dynamically [17]. These models
can autonomously learn and distinguish patterns of normal and abnormal behavior, allow-
ing them to detect previously unseen threats and adapt to evolving cyberattack strategies.
However, the effectiveness of machine learning models is often constrained by the complex-
ity of network traffic data and the dynamic nature of cyber threats [18]. High-dimensional
network data with non-linear dependencies makes it challenging to extract meaningful
features manually. Consequently, machine learning models require extensive feature engi-
neering, a labor-intensive process that involves selecting relevant attributes, transforming
raw data, and reducing dimensionality to optimize model performance. Despite these
efforts, feature engineering may not always effectively capture the intricate relationships
inherent in network traffic data, thereby limiting the model’s generalization capabilities.
Deep learning, a specialized subset of machine learning, has emerged as a powerful al-
ternative capable of addressing these limitations. Deep learning models, such as artificial
neural networks (ANNs), convolutional neural networks (CNNs), and recurrent neural
networks (RNNs), leverage multiple layers of artificial neurons to autonomously learn
hierarchical representations from large-scale, high-dimensional datasets [19–21]. These
models have demonstrated remarkable success across various domains, including image
recognition, natural language processing, and speech recognition, due to their ability to
capture complex patterns and feature dependencies. In the context of intrusion detection,
deep learning models eliminate the need for manual feature engineering by learning rep-
resentations directly from raw network traffic data [22]. This enables them to effectively
identify both known and novel attack patterns with greater accuracy and adaptability.
Furthermore, deep learning models can analyze temporal dependencies in sequential data,
making them particularly well suited for detecting evolving attack patterns in real-time
network monitoring. As a result, deep learning holds significant promise in advancing IDS
technologies and enhancing cybersecurity resilience in modern network environments [23].

Appl. Sci. 2025, 15, 1903
3 of 19
This research paper aims to assess the effectiveness of deep learning algorithms in
detecting network intrusions. Specifically, the study focuses on training artificial neural
networks, including convolutional neural networks (CNNs) and recurrent neural networks
(RNNs), using large volumes of network traffic data to distinguish between normal and
abnormal behavior patterns. CNNs are particularly effective in analyzing spatial patterns
in data, while RNNs excel at capturing temporal dependencies in sequential data [24].
By utilizing the unique strengths of these deep learning models, this research aims to
develop more accurate and robust intrusion detection systems. The performance of deep
learning methods will be compared to traditional machine learning techniques [25], such
as support vector machines and decision trees, to evaluate their relative effectiveness
in detecting network intrusions [26]. This comparison will involve analyzing various
performance metrics, including detection accuracy, false positive rate, and false negative
rate, to determine the overall efficiency of each approach.
A key novelty of this study lies in its comparative analysis of multiple machine learning
and deep learning models, offering a comprehensive understanding of their strengths and
weaknesses in intrusion detection. Furthermore, this research employs the synthetic minor-
ity over-sampling technique (SMOTE) for data balancing, addressing the class imbalance
issue that often hinders the performance of machine learning models. By augmenting the
dataset, SMOTE enhances the models’ ability to detect minority class intrusions, improving
overall detection accuracy. Another key contribution of this study is its evaluation of com-
putational efficiency and scalability, which are crucial for deploying deep learning-based
intrusion detection systems in real-world environments. The successful implementation
of deep learning algorithms [27] in intrusion detection systems [28] could lead to more
advanced and accurate security solutions, enhancing the overall cybersecurity landscape.
By better protecting computer networks from potential threats, this research has the po-
tential to contribute to the development of safer and more secure digital environments for
individuals, businesses, and governments alike. In addition, the insights gained from this
research could inform the development of novel deep learning-based methods for other
cybersecurity applications, such as malware detection [29], vulnerability assessment [30],
and spam filtering [31]. Moreover, this research project will discuss the scalability and
efficiency of deep learning-based intrusion detection systems [32] in real-world scenarios.
As network traffic volumes grow and the complexity of cyber threats evolves, it is essential
to ensure that intrusion detection systems can effectively process and analyze large-scale
data streams in a timely manner. This study will explore techniques for optimizing the
computational efficiency and resource utilization of deep learning models, such as parallel
processing, distributed training, and model compression. The key contributions of this
research are outlined as follows:
1.
The study explores the application of deep learning models, such as CNN and LSTM,
for detecting network intrusions, aiming to enhance the accuracy and effectiveness of
IDS in large-scale network environments.
2.
The research compares the performance of deep learning models to traditional ma-
chine learning techniques (e.g., logistic regression, naive Bayes, and random forest),
providing a comprehensive evaluation of their effectiveness in threat detection.
3.
The paper highlights the potential of deep learning-based IDS to improve cyberse-
curity practices by offering more advanced, accurate, and efficient threat detection
solutions, with insights that could inform the development of IDS for other applica-
tions, such as malware detection and vulnerability assessment.
4.
The research discusses the trade-offs between accuracy and computational overhead,
emphasizing the importance of scalability and resource utilization for deep learning-
based IDS in real-world environments.

Appl. Sci. 2025, 15, 1903
4 of 19
The remainder of the paper is structured as follows: Section 2 offers a comprehensive
literature review on network intrusion detection. Section 3 outlines the methodology,
including the overall design, dataset, data cleaning, and feature engineering procedures.
Section 4 presents the results and analysis, which are followed by a discussion in Section 5.
Lastly, Section 6 concludes the paper and highlights future research directions.
2. Literature Review of Network Intrusion Detection
The literature review section aims to offer an overview of existing research on intrusion
detection systems, with a focus on the use of machine learning and deep learning techniques.
This section will explore the evolution of intrusion detection systems, the challenges
encountered by traditional methods, the rise of machine learning and deep learning in this
area, and the current state-of-the-art approaches in network intrusion detection.
2.1. Evolution of Intrusion Detection Systems
Intrusion detection systems (IDS) have been a vital component of network security
since the 1980s. These systems were created to monitor and analyze network traffic to
detect potential security threats and malicious activities. Over time, IDS have evolved
significantly to keep up with the rapidly changing cybersecurity environment [33–35].
Initially, intrusion detection systems primarily relied on signature-based and rule-
based methods, which can be broadly classified into signature-based IDS and anomaly-
based IDS [36]. Signature-based IDS use predefined rules or patterns to identify known
attacks by comparing network traffic to a database of known attack signatures. While
signature-based systems have been effective against known threats, they struggle to detect
novel or sophisticated attacks that do not match established patterns. This limitation led to
the development of anomaly-based IDS, which identify potential intrusions by detecting
deviations from normal behavior [37]. These systems use statistical and machine learning
techniques to establish a baseline of typical network activity and flag deviations from this
baseline as potential security threats.
Despite advancements in anomaly-based IDS, they still face challenges in detecting
complex and evolving cyber threats. This has prompted researchers to investigate alterna-
tive approaches, such as machine learning and deep learning, to improve the adaptability
and accuracy of intrusion detection systems. Machine learning-based IDS analyze network
traffic data to learn and recognize patterns of normal and abnormal behavior without de-
pending on predefined rules or signatures. These approaches have demonstrated potential
in identifying previously unknown threats and adapting to changes in network behavior
over time.
2.2. Challenges in Traditional Intrusion Detection Systems
The effectiveness of traditional intrusion detection systems is limited by several fac-
tors, including the ever-evolving nature of cyber threats, the complexity of network traffic
data, and the high rates of false positives and negatives [38]. The dynamic nature of cyber
threats presents a major challenge for intrusion detection systems. Attackers continuously
develop new techniques and strategies to exploit vulnerabilities in network systems, mak-
ing signature-based methods less effective in detecting new attacks. This highlights the
need for more adaptive and flexible intrusion detection systems that can learn to identify
emerging patterns and threats.
In addition, the complexity of network traffic data poses a significant challenge for
intrusion detection systems. Network traffic data is often high-dimensional, noisy, and
diverse, which makes it difficult for traditional IDS to effectively analyze and identify
patterns of malicious activity. Moreover, manual feature engineering, which involves

Appl. Sci. 2025, 15, 1903
5 of 19
selecting relevant features and reducing the dimensionality of input data, can be time-
consuming and may not always capture the complex relationships and patterns within
network traffic. Another major challenge for traditional intrusion detection systems is the
high rate of false positives and negatives. False positives occur when the IDS incorrectly
flags normal network traffic as malicious, while false negatives happen when the IDS fails
to detect a genuine attack. Both issues can result in increased operational overhead and
diminished efficiency in network security management.
2.3. Machine Learning in Intrusion Detection
Machine learning techniques have been widely studied in network intrusion detection
since the 1990s [39]. Early research utilized algorithms such as decision trees [40], K-nearest
neighbors [41], and support vector machines (SVMs) [42] to classify network traffic as either
normal or malicious. While these methods improved detection rates compared to traditional
approaches, they still faced challenges in handling high-dimensional and imbalanced data.
To overcome these limitations, researchers have proposed various preprocessing techniques,
feature selection methods, and ensemble strategies to enhance the performance of machine
learning-based IDS [43]. Despite these advancements, machine learning methods may still
struggle to capture the complex patterns and relationships in network traffic data. As a
result, there has been growing interest in deep learning algorithms, which have shown
exceptional ability in learning hierarchical representations from high-dimensional data [44].
2.4. Deep Learning in Intrusion Detection
Deep learning algorithms, particularly artificial neural networks, have attracted con-
siderable attention in recent years due to their potential to enhance intrusion detection
systems [45]. Convolutional neural networks (CNNs) [46] and recurrent neural networks
(RNNs) [47] have proven effective in detecting network intrusions, with CNNs excelling at
learning spatial features and RNNs at learning temporal features.
Numerous studies have demonstrated the successful application of deep learning
techniques in network intrusion detection [48]. For example, Javaid et al. [49] used a
stacked autoencoder (SAE) to learn hierarchical features from the UNSW-NB15 dataset,
outperforming traditional machine learning methods. Similarly, Kim et al. [50] applied a
deep belief network (DBN) to detect intrusions in the KDD Cup 1999 dataset, highlighting
the capability of deep learning algorithms to handle high-dimensional data. More recently,
researchers have examined the use of advanced deep learning architectures [51], including
long short-term memory (LSTM) [52] and gated recurrent unit (GRU) networks [53], for
intrusion detection in network traffic data [54]. These models have shown promise in cap-
turing temporal dependencies in sequential data, which is especially relevant for analyzing
network traffic.
2.5. Hybrid Approaches in Intrusion Detection
In addition to standalone deep learning methods, hybrid approaches that combine
deep learning with traditional machine learning techniques have been suggested to improve
the performance of intrusion detection systems [55]. For instance, Wang et al. [56] developed
a hybrid model that integrated a CNN for feature extraction and an SVM for classification.
This model showed enhanced detection accuracy and lower false positive rates compared to
standalone methods. Similarly, Zhang et al. [57] proposed a hybrid model that combined an
LSTM network with a random forest classifier for intrusion detection using the CICIDS2017
dataset. The results demonstrated that the hybrid approach outperformed the individual
LSTM and random forest models, emphasizing the potential advantages of merging deep
learning and machine learning techniques in network intrusion detection.

Appl. Sci. 2025, 15, 1903
6 of 19
2.6. Adversarial Machine Learning in Intrusion Detection
As machine learning and deep learning techniques become increasingly common in in-
trusion detection systems, adversaries may attempt to exploit the inherent vulnerabilities of
these models [58]. Adversarial machine learning, a rapidly emerging field, investigates the
weaknesses of machine learning models when exposed to intentionally crafted adversarial
inputs. These adversarial attacks, such as evasion and poisoning attacks, aim to manipulate
the behavior of machine learning algorithms by exploiting their vulnerabilities. Evasion
attacks involve subtly altering input data to deceive a trained model into making incorrect
predictions, posing a particular threat to intrusion detection systems (IDSs), as attackers
could bypass security mechanisms undetected. Poisoning attacks, by contrast, occur during
the training phase, where malicious data is injected into the dataset to corrupt the learning
process, resulting in degraded model performance or biased decision-making [59]. Recent
research has examined the potential of adversarial machine learning to strengthen the
security of intrusion detection systems. For example, Grosse et al. [60] highlighted the
vulnerability of deep learning-based IDS to adversarial examples and proposed counter-
measures, such as adversarial training and gradient masking. This area of research is
crucial for developing more resilient and secure intrusion detection systems [61].
2.7. Research Gap
The literature review emphasizes the increasing interest in utilizing machine learning
and deep learning techniques to improve the performance of intrusion detection systems.
Although these methods have shown promising results in detecting network intrusions,
several challenges and research opportunities remain. For example, the development of
more advanced and efficient deep learning architectures specifically designed for intrusion
detection continues to be an active area of research.
Additionally, exploring hybrid approaches that combine the strengths of both deep
learning and traditional machine learning techniques may result in improved detection
accuracy and reduced false positive rates. Moreover, examining the application of machine
learning in intrusion detection systems is essential to ensure the robustness and security of
these models against potential adversarial threats.
This research project seeks to make a valuable contribution to the growing field of
cybersecurity by investigating the effectiveness of deep learning algorithms in detecting
network intrusions. As cyber threats continue to evolve, it is crucial to explore how ad-
vanced machine learning techniques, particularly deep learning, can improve the accuracy
and efficiency of intrusion detection systems. The study will not only assess the perfor-
mance of deep learning algorithms in identifying various types of intrusions but will also
compare these methods to traditional machine learning approaches that have been widely
used in the field. By conducting a thorough performance evaluation, the research aims
to identify the strengths and limitations of deep learning in this context and determine
whether it offers a significant advantage over conventional methods. Ultimately, this
project hopes to uncover new insights and approaches that can lead to the development of
more sophisticated, robust, and accurate intrusion detection systems. The findings could
provide valuable guidance for enhancing cybersecurity practices, fostering more proactive
defense strategies, and contributing to the protection of sensitive data and systems in an
increasingly connected world.
3. Methodology
This section outlines the methodology employed in researching network intrusion
detection using machine learning and deep learning algorithms. We detail the procedures

Appl. Sci. 2025, 15, 1903
7 of 19
for preprocessing the data, engineering features, and training multiple models to classify
network traffic, utilizing the CICIDS2017 dataset [62].
3.1. Data Preprocessing
The dataset utilized in this study was the CICIDS2017 dataset, which includes various
features related to network traffic. To ensure the data’s quality and consistency, the dataset
underwent preprocessing. The following preprocessing steps were applied:
•
Handling missing values: The data consists of 2,830,743 rows and 79 columns.
There were 308,381 duplicate values. We removed the duplicates using the Pan-
das drop_duplicates(inplace=True) function. We identified a total of 353 missing
values using the Pandas isna().sum() function. The missing values were handled using
mean imputation, where the mean value of the respective columns was used to fill in
the missing entries. This technique was chosen because it is simple and effective for
numerical features, and it minimizes the impact on the overall distribution of the data,
which is important for maintaining the integrity of the models being trained.
•
Removing infinity values: To identify rows with “infinity” values, we checked the
dataset for entries that were either positive or negative infinity (inf or -inf). Any rows
containing such values were removed from the dataset to avoid errors or distortions
during model training. This was necessary because machine learning algorithms often
cannot handle infinite values and could lead to model instability or incorrect learning.
•
Consolidating labels: We modified the ‘Label’ column by consolidating similar attack
types. For instance, all “Web Attack” labels were grouped under a single “Web Attack”
label, and all “DoS” labels were consolidated under a single “DoS” label. Other attack
types were left unchanged, and any remaining labels were categorized as “Other”.
This consolidation was performed to reduce the complexity of the classification task
and ensure that each category had sufficient examples for the model to learn effectively.
•
Data balancing: Upon assessing the dataset’s class distribution, we found that the
dataset was highly imbalanced, with some attack types having significantly fewer
instances than others. To address this, we employed stratified sampling during
the split of the dataset into training and testing sets, ensuring that each class was
proportionally represented in both sets. Additionally, SMOTE (synthetic minority
over-sampling technique) was applied to balance the dataset further by generating
synthetic samples for underrepresented classes. This approach was chosen because it
helps the model learn from a more diverse set of examples and improves its ability to
generalize, especially for minority class detection.
3.2. Feature Engineering and Scaling
After preprocessing the data, we performed feature engineering and scaling to prepare
the dataset for machine learning algorithms. Feature engineering involved selecting,
modifying, and creating relevant features from the raw data to improve the model’s
predictive performance. This step is essential as the quality and relevance of the features
directly impact the accuracy and efficiency of the machine learning models.
Next, we applied feature scaling to ensure that all features contributed equally to the
distance calculations used by many machine learning algorithms. Specifically, we utilized
the StandardScaler from the Scikit-learn library v1.6.1, which standardizes the features
by removing the mean and scaling them to unit variance. This transformation is critical
because it allows the algorithms to converge more quickly and enhances their performance,
especially for distance-based algorithms, such as K-nearest neighbors and support vector
machines. By standardizing the features, we ensured that the model could learn from the
data effectively, without bias toward features with larger ranges or magnitudes.

Appl. Sci. 2025, 15, 1903
8 of 19
3.3. Model Training and Evaluation
We trained and evaluated several machine learning models, including logistic regres-
sion, random forest, and support vector machines (SVMs). Each model was selected based
on its unique strengths and capabilities in handling classification tasks. Logistic regression
was chosen for its simplicity and effectiveness in binary classification problems, allowing
us to evaluate the linear relationships between features and target labels. The random
forest algorithm was selected for its robustness and ability to handle high-dimensional
datasets, offering improved accuracy through ensemble learning techniques. Additionally,
support vector machines were used for their efficiency in finding optimal hyperplanes that
separate distinct classes in the feature space.
For hyperparameter optimization, we applied random search, a technique that ran-
domly selects combinations of hyperparameters from a predefined search space, rather than
exhaustively testing all possibilities as with grid search. Random search is computationally
more efficient, especially when dealing with a large number of hyperparameters, and has
been shown to identify high-performing configurations in fewer iterations. While it may
not always find the absolute optimal solution, it typically provides competitive results at a
lower computational cost compared to more exhaustive methods.
We evaluated the performance of these models using various metrics, such as accuracy
and an F1 score, to assess their effectiveness in classifying network traffic as either normal
or malicious.
4. Result and Analysis
In this section, we present the results of the classification models applied to the network
intrusion detection dataset and evaluate their performance in terms of accuracy, F-measure,
and training time. We start by detailing the overall performance metrics achieved by each
model, offering a comprehensive overview of how well they classified network traffic as
either normal or malicious. Accuracy serves as a key metric, indicating the proportion of
correctly classified instances out of the total dataset. Specific accuracy scores for each model
will be provided, emphasizing those that performed exceptionally well and discussing any
patterns observed across the different algorithms.
F-measure, also known as the F1 score, is another critical evaluation metric that
balances precision and recall. It is especially relevant in this context, where detecting
malicious activities (true positives) while minimizing false positives is crucial. We will
compare the F-measure scores of the models to identify which ones strike the optimal
balance between precision and recall. Additionally, we will discuss the training time for
each model, an important consideration in practical applications. Longer training times
can be a significant disadvantage, particularly in environments that require real-time or
near-real-time intrusion detection.
By evaluating training times alongside accuracy and F-measure, we can gain valu-
able insights into the efficiency and feasibility of deploying each model in real-world
scenarios. This analysis aims to identify the strengths and limitations of each classification
approach, offering guidance on selecting the most appropriate model for network intrusion
detection tasks.
4.1. Data Balancing
In the dataset, we observed a significant class imbalance, which presented a major
challenge for our machine learning models. Specifically, the performance of the models for
the fifth class, “Web Attacks”, was severely impacted, resulting in an F1 score of 0. This
imbalance caused the models to be biased toward the majority classes, leading to difficulty
in recognizing patterns in the underrepresented classes. To address this issue, we utilized

Appl. Sci. 2025, 15, 1903
9 of 19
a data balancing technique known as the synthetic minority over-sampling technique
(SMOTE). SMOTE creates synthetic samples for the minority class to balance the distribu-
tion, ultimately enhancing the models’ performance on the underrepresented classes.
To mitigate the common issue of class imbalance frequently found in cybersecurity
datasets, we applied SMOTE to our dataset. Class imbalance can notably impair the
performance of machine learning models, especially in detecting underrepresented classes
like “Web Attacks”, which are often overshadowed by more frequent classes. SMOTE
works by generating synthetic samples for the minority class, resulting in a more balanced
data distribution. After applying SMOTE, we retrained our machine learning models
with the newly balanced dataset. The results revealed a significant improvement in the
detection performance of the underrepresented classes, leading to better overall model
performance. This improvement in accuracy is essential for developing a more reliable
and effective intrusion detection system capable of identifying a broader range of cyber
threats, including those that might otherwise be missed due to class imbalance. In Figure 1,
we present a visualization of the data distribution before any data balancing technique
was applied, illustrating the initial class imbalance. The plot highlights a significant
disparity in the number of instances across different classes, with some classes being
heavily overrepresented while others are notably sparse. Figure 2 provides a comparison
by showing the data distribution after the SMOTE technique was applied, demonstrating
how the dataset became more balanced, which ultimately contributed to improving the
model’s ability to detect minority class instances more effectively.
Figure 1. Data distribution before applying any data balancing mechanism.
Figure 2. Data distribution after applying SMOTE balancing mechanism.

Appl. Sci. 2025, 15, 1903
10 of 19
4.2. Feature Engineering: Correlation-Based Feature Selection
Feature engineering is a vital component of machine learning model development, as
it involves selecting the most relevant variables, creating new features from existing ones,
and transforming features to enhance model performance. One commonly used technique
in feature engineering is correlation-based feature selection, which focuses on identifying
and removing highly correlated features from the dataset. We applied a correlation-based
feature selection approach to eliminate redundant features that exhibited strong correlations
with one another.
To begin, we computed the correlation matrix for the dataset, which measures the
linear relationship between feature pairs, as shown in Figure 3. The matrix values range
from −1 to 1, where −1 represents a perfect negative correlation, 0 indicates no correlation,
and 1 indicates a perfect positive correlation. We set a threshold of 0.85 to identify feature
pairs with high correlations. If the absolute correlation value between two features exceeded
this threshold, we considered one of the features to be redundant and removed it from the
dataset. By applying this technique, we aimed to reduce the dataset’s dimensionality and
address multicollinearity issues, which ultimately improved both the performance and
interpretability of the resulting machine learning models. After applying correlation-based
feature selection, the dataset’s dimensionality was reduced, retaining only the most relevant
and non-redundant features. This refined dataset was then used for training and evaluating
the machine learning and deep learning models in the later stages of the study.
Figure 3. Correlation heatmap showing the relationships between features after feature engineering,
highlighting significant correlations among variables.
4.3. Results of Machine Learning Models
The initial phase of this study involved evaluating different machine learning models
on the given dataset and comparing their accuracy, average F1 score, and precision-recall
performance. The logistic regression model achieved an accuracy of 96.91% and an average
F1 score of 73.96%. While the model performed well for classes 0–3, it failed to classify
instances from class 4, resulting in an F1 score of 0%. The SVM model yielded results

Appl. Sci. 2025, 15, 1903
11 of 19
similar to those of logistic regression, while the naive Bayes model achieved an accuracy
of 64.59% and an average F1 score of 48.70%. Although it showed some improvement in
classifying instances from class 4 compared to logistic regression, its overall performance
for the other classes was lower.
The random forest model exhibited the best performance, with an accuracy of 99.88%
and an average F1 score of 97.46%. It successfully classified instances from all classes,
including class 4, with high precision and recall. The K-nearest neighbors (KNNs) model
recorded an accuracy of 99.36% and an average F1 score of 97.62%. This model also
performed well across all classes, although there was a slight reduction in performance for
class 3. The decision tree model obtained an accuracy of 99.83% and an average F1 score
of 97.76%. Its performance was consistently high across all classes, effectively classifying
instances from the underrepresented class 4. Overall, the random forest model was the
best performer in terms of accuracy, average F1 score, and precision-recall, achieving an
accuracy of 99.88% and an average F1 score of 97.46%. It effectively classified instances
from all classes, including the underrepresented class 4. Table 1 summarizes the results for
each machine learning model.
Table 1. Performance metrics of different ML models.
Model
Accuracy
Avg F1 Score
95% Confidence Interval
Logistic Regression
96.91%
74.00%
[96.50, 97.32]
Naive Bayes
64.59%
48.88%
[63.85, 65.33]
KNN
99.88%
97.46%
[99.75, 99.98]
Decision Tree
99.83%
97.60%
[99.70, 99.96]
SVM
97.32%
73.33%
[96.90, 97.74]
Figure 4 displays the confusion matrices for all the models we evaluated. The following
figures illustrate the confusion matrices for each individual model. Upon comparing
these matrices, it is clear that the random forest and decision tree models exhibit strong
performance in accurate classifications, with high values along the diagonal elements,
suggesting they correctly predict most instances across all classes. In contrast, the logistic
regression model shows poor performance in classifying the 5th class (web attacks), as
reflected by the low value in the corresponding diagonal element. Similarly, the naive
Bayes model shows weaker performance overall, particularly in classifying the majority
class (Class 0).
4.4. Results of Deep Learning Models
In the later stages of the experiments, we compared the performance of three deep
learning models—multilayer perceptron (MLP), convolutional neural network (CNN),
and long short-term memory (LSTM)—for network intrusion detection, in comparison to
machine learning methods. The classification report results offer a thorough understanding
of how these models performed. In Figure 5, we present the confusion matrices of the MLP,
CNN, and LSTM models. The annotations indicate that while all models perform well in
detecting the majority class, there are notable misclassifications in underrepresented attack
classes, particularly in classes 3 and 4. The CNN model demonstrates improved detection
in these classes compared to MLP, but LSTM shows the best overall balance between
precision and recall across all classes. In Figure 6, the training and validation loss curves
for the deep learning models are displayed. The updated annotations clarify that CNN
and LSTM models converge more smoothly than MLP, indicating better generalization.
Additionally, fluctuations in the validation loss for MLP suggest possible overfitting, which
can be mitigated through regularization techniques such as dropout or batch normalization.

Appl. Sci. 2025, 15, 1903
12 of 19
Figure 4. Confusion matrices showing the performance of logistic regression (LR), naive Bayes (NB),
decision trees (DTs), random forest (RF), K-nearest neighbors (KNNs), and support vector machines
(SVMs) models in classifying network intrusions.
Figure 5. Confusion matrices for MLP, CNN, and LSTM models to assess classification performance,
including true positive, true negative, false positive, and false negative rates.
Figure 6. Training and validation accuracy comparison of MLP, CNN, and LSTM models across
epochs to evaluate model performance and generalization.
The multilayer perceptron (MLP) model achieves an overall accuracy of 97%, demon-
strating high precision and recall for classes 0, 1, and 2, reflecting its effectiveness in
identifying these classes accurately. However, its performance drops slightly for class 3
and significantly for class 4. The model’s average macro F1 score is 0.82, indicating a solid
ability to distinguish between classes. Despite this, the lower F1 scores for classes 3 and 4
highlight areas for improvement in these classifications.
The convolutional neural network (CNN) model achieves an overall accuracy of 98%,
slightly outperforming the MLP model. Similar to the MLP, the CNN model displays

Appl. Sci. 2025, 15, 1903
13 of 19
high precision and recall for classes 0, 1, and 2, and shows comparable performance for
classes 3 and 4. Its macro average F1 score is 0.83, slightly higher than the MLP model,
indicating improved performance in class differentiation. However, the lower F1 scores for
classes 3 and 4 remain a concern, suggesting the need for further refinement in classifying
these categories.
The long short-term memory (LSTM) model also reaches an overall accuracy of 98%.
It maintains high precision and recall for classes 0, 1, and 2, and shows comparable
performance for classes 3 and 4 when compared to the other two models. The LSTM
model’s macro average F1 score is 0.84, the highest among the three deep learning models,
signifying its superior performance in class differentiation. Nonetheless, the lower F1
scores for classes 3 and 4 still persist, indicating that improvements are necessary for these
specific classes.
All three deep learning models exhibit strong performance in network intrusion
detection, with the LSTM model slightly outperforming the MLP and CNN models. While
they all show high accuracy and F1 scores for most classes, there is room for improvement
in the identification of classes 3 and 4. These results suggest that deep learning models,
especially the LSTM, are promising candidates for network intrusion detection and have the
potential to surpass traditional machine learning methods. By addressing the challenges in
classifying underrepresented classes, future iterations of these models could provide even
more robust results in the fight against cyber threats.
5. Discussion
In this experiment, we evaluated the performance of six machine learning models
and three deep learning models for network intrusion detection. The machine learning
models included logistic regression, Gaussian naive Bayes, random forest, KNN, SVM,
and decision tree, while the deep learning models consisted of MLP, CNN, and LSTM.
Upon reviewing the results, logistic regression achieved an accuracy of 0.97 and a weighted
average F1 score of 0.97. Gaussian naive Bayes reached an accuracy of 0.65 and a weighted
average F1 score of 0.71. Random forest demonstrated outstanding performance, with an
accuracy of 0.998 and a weighted average F1 score of 1.00. The KNN model achieved an
accuracy of 0.99 and a weighted average F1 score of 0.99. Finally, the decision tree model
showed an accuracy of 0.998 and a weighted average F1 score of 1.00.
Naive Bayes and logistic regression exhibited lower performance compared to random
forest and decision tree due to their inherent limitations in handling high-dimensional and
complex network traffic data. Naive Bayes operates under the assumption that features
are conditionally independent given the class label. However, network intrusion data
often contains highly correlated features, making this assumption unrealistic. As a result,
naive Bayes struggles to model intricate relationships within the dataset, leading to poor
classification performance, especially for minority attack classes. Logistic regression is a
linear model that performs well when data points can be separated using a linear decision
boundary. However, network intrusion detection data is inherently complex and non-
linearly separable, which limits the effectiveness of logistic regression. The model fails
to capture intricate patterns in network traffic, leading to a high misclassification rate.
Decision trees and random forests are suited well for capturing non-linear relationships in
high-dimensional datasets. Unlike logistic regression, they can model intricate decision
boundaries without requiring prior feature transformations. The ensemble nature of
random forest allows it to handle class imbalances better than naive Bayes and logistic
regression, which are more sensitive to skewed distributions.
For the deep learning models, the MLP model achieved an accuracy of 0.97 and a
weighted average F1 score of 0.98. The CNN model attained an accuracy of 0.98 and a

Appl. Sci. 2025, 15, 1903
14 of 19
weighted average F1 score of 0.98. The LSTM model showed an accuracy of 0.98 and a
weighted average F1 score of 0.98. Comparing the machine learning and deep learning
models reveals that the random forest and decision tree models exhibit the highest per-
formance, with accuracy and weighted average F1 scores nearly reaching 1.00. KNN also
performed well, with an accuracy of 0.99 and a weighted average F1 score of 0.99. The deep
learning models, MLP, CNN, and LSTM, performed similarly, with accuracy scores ranging
from 0.97 to 0.98 and weighted average F1 scores of 0.98. In conclusion, the random forest
and decision tree models were the best performers for network intrusion detection tasks in
this study. However, the deep learning models (MLP, CNN, and LSTM) also showed strong
performance, suggesting their potential for use in network intrusion detection systems. It
is important to consider that the selection of a model depends on specific application re-
quirements and constraints, such as computational resources, interpretability, and real-time
detection needs.
As network traffic increases and cyber threats grow more complex, intrusion detection
systems must be capable of efficiently processing and analyzing large-scale data streams
in real-time. Our research has highlighted the potential of deep learning-based intrusion
detection systems to address these challenges. However, optimizing the computational
efficiency and resource utilization of these models is critical for their successful deployment
in real-world scenarios. To achieve this, we explored various methods to enhance the
performance of deep learning models in intrusion detection systems. For instance, parallel
processing can take advantage of the inherent parallelism in neural networks, accelerating
training and inference tasks. Distributing the workload across multiple processing units,
such as GPUs or TPUs, can significantly reduce the time needed for training and evaluating
deep learning models.
Distributed training is another technique to improve the scalability of deep learning-
based intrusion detection systems. By partitioning the training data and model parameters
across multiple devices or nodes, we can utilize the collective computational power of these
resources to train large-scale models more effectively. Additionally, advanced algorithms
like asynchronous stochastic gradient descent and distributed batch normalization can be
incorporated to optimize synchronization and communication between the nodes.
Model compression is a key consideration for deploying deep learning models in
intrusion detection systems. Given that these models often contain many parameters, they
can be resource-intensive, which may pose challenges in resource-constrained environ-
ments. Techniques such as weight pruning, quantization, and knowledge distillation can
reduce the size and complexity of the models without significantly compromising their
performance. By compressing the models, we can achieve faster inference times and lower
memory usage, making them more suitable for real-world deployment. In addition to
these optimization techniques, we also explored the impact of data preprocessing, fea-
ture engineering, and data balancing on the performance of intrusion detection models.
Through correlation analysis, we identified and removed highly correlated features, en-
hancing the efficiency of the models. We also applied the synthetic minority over-sampling
technique (SMOTE) to address the class imbalance in the dataset, improving performance
for underrepresented classes.
Thus, our research has demonstrated the potential of deep learning-based intrusion
detection systems in effectively detecting and mitigating cyber threats in large-scale network
environments. By leveraging advanced optimization techniques and data preprocessing
strategies, we enhanced these models’ scalability, efficiency, and performance, making them
suitable for real-world deployment. As cyber threats evolve and become more sophisticated,
deep learning-based intrusion detection systems will play an increasingly important role
in safeguarding our networks and digital assets. Our study highlights the effectiveness

Appl. Sci. 2025, 15, 1903
15 of 19
of machine learning and deep learning models for network intrusion detection, which is
critical as cyber threats continue to evolve and pose significant risks to organizations. By
using advanced models like random forest and deep learning techniques such as MLP,
CNN, and LSTM, we can improve the ability to detect complex attack patterns and adapt to
new types of network threats. As cyberattacks grow in sophistication, our research suggests
that leveraging deep learning approaches will be key to building more robust, adaptable
IDS solutions capable of protecting critical infrastructure.
While this study demonstrates the effectiveness of machine learning and deep learn-
ing models for intrusion detection, several limitations must be acknowledged. One key
challenge is the dataset-specific biases present in CIC-IDS2017. Since the dataset is gen-
erated in a controlled environment, it may not fully capture the variability and evolving
nature of real-world network traffic, potentially limiting the generalizability of the models.
Additionally, certain attack categories in the dataset are underrepresented, which could
impact model performance on rare attack types. Beyond SMOTE, additional strategies
such as data augmentation, cost-sensitive learning, and advanced resampling techniques
can be explored to handle imbalanced datasets more effectively. Another significant lim-
itation is the need for real-time inference in practical deployment scenarios. Many deep
learning models, particularly LSTM and CNN, require substantial computational resources,
making real-time detection challenging in resource-constrained environments. The latency
introduced by complex models may hinder timely threat mitigation. Further research is
needed to explore model optimization techniques such as quantization and pruning to
enhance efficiency. Additionally, further research is needed to evaluate the adaptability of
these models in dynamic network conditions by testing on more diverse and continuously
updated datasets.
6. Conclusions
This study has demonstrated the potential of deep learning-based intrusion detection
systems in addressing the challenges posed by increasing network traffic volumes and
evolving cyber threats. By comparing deep learning models such as MLP, CNN, and
LSTM with traditional machine learning algorithms like logistic regression, naive Bayes,
random forest, K-nearest neighbors, and decision trees, we have shown that deep learning
models can achieve competitive accuracy and adaptability. However, the selection of an
appropriate model depends on the specific use case and system requirements. For high
interpretability and low computational overhead, random forest emerges as a strong choice
due to its explainability and effectiveness in structured intrusion detection tasks. On the
other hand, LSTM is particularly well suited for sequential network traffic analysis, making
it ideal for detecting time-dependent attack patterns. CNN can be leveraged for feature-rich
intrusion detection tasks, where spatial relationships within network data play a crucial
role. While deep learning models offer superior performance in many scenarios, they
require significant computational resources, making them more suitable for large-scale
deployments with adequate hardware support.
The application of data preprocessing, feature engineering, and data balancing tech-
niques, such as correlation analysis and SMOTE, has proven effective in enhancing the
performance of these models. Moreover, the investigation of optimization strategies, in-
cluding parallel processing, distributed training, and model compression, has highlighted
the potential for improving deep learning models’ computational efficiency and resource
utilization. The findings of this research project emphasize the suitability of deep learning-
based intrusion detection systems for large-scale network environments and their ability to
adapt to the ever-evolving landscape of cyber threats. While the random forest and decision
tree models demonstrated the best performance in this comparison, deep learning models,

Appl. Sci. 2025, 15, 1903
16 of 19
such as MLP, CNN, and LSTM, also showed promising results. As a result, these models
represent a promising solution for the ongoing challenges faced by intrusion detection
systems and can contribute to the overall security of network infrastructures.
In light of the findings from this study, future research directions could focus on the
following specific aspects:
•
Developing hybrid models that integrate the strengths of both deep learning and
traditional machine learning algorithms, which could potentially enhance performance
in detecting various types of cyber threats.
•
Exploring the use of unsupervised and semi-supervised learning techniques within
deep learning-based intrusion detection systems to mitigate the challenges posed by
the limited availability of labeled data and improve the models’ adaptability to new
and unknown threats.
•
Investigating advanced feature selection and extraction techniques, such as deep
autoencoders and graph-based methods, to more effectively capture the underlying
patterns and relationships in network traffic data.
•
Evaluating the impact of different hyperparameter tuning and model selection strate-
gies on the performance of deep learning-based intrusion detection systems to optimize
their effectiveness in real-world network settings.
•
Assessing the performance of deep learning models in adversarial conditions, such as
the presence of sophisticated and stealthy attacks designed to evade detection, as well
as the influence of noisy or incomplete data.
Author Contributions: Conceptualization, K.T., M.L.A. and S.S.; methodology, K.T., M.L.A., J.D. and
S.S.; validation, K.T., M.L.A. and S.S.; formal analysis, K.T., J.D., D.D. and S.S.; investigation, K.T.,
M.L.A. and S.S.; writing—original draft preparation, K.T., M.L.A., J.D. and D.D.; writing—review
and editing, K.T., M.L.A., J.D., D.D. and S.S.; supervision, J.D., D.D. and K.T.; project administration,
S.S. and M.L.A. All authors have read and agreed to the published version of the manuscript.
Funding: This research received no external funding.
Institutional Review Board Statement: Not applicable.
Informed Consent Statement: Not applicable.
Data Availability Statement: The original contributions presented in the study are included in the
article, further inquiries can be directed to the corresponding author.
Conflicts of Interest: The authors declare no conflicts of interest.
References
1.
Alars, E.S.A.; Kurnaz, S. Enhancing network intrusion detection systems with combined network and host traffic features using
deep learning: Deep learning and IoT perspective. Discov. Comput. 2024, 27, 39. [CrossRef]
2.
Vullam, N.; Roja, D.; Rao, N.; Vellela, S.S.; Vuyyuru, L.R.; Kumar, K.K. Enhancing Intrusion Detection Systems for Secure E-
Commerce Communication Networks. In Proceedings of the 2023 International Conference on the Confluence of Advancements
in Robotics, Vision and Interdisciplinary Technology Management (IC-RVITM), Bengaluru, India, 28–29 November 2023; pp. 1–7.
3.
Greenwood, S.; Perrin, A.; Duggan, M. Social media update 2016. Pew Res. Cent. 2016, 11, 1–18.
4.
Ali, M.L.; Thakur, K.; Atobatele, B. Challenges of cyber security and the emerging trends. In Proceedings of the 2019 ACM
International Symposium on Blockchain and Secure Critical Infrastructure, Seoul, Republic of Korea, 27–30 October 2019;
pp. 107–112.
5.
Ebert, C.; Duarte, C.H.C. Digital transformation. IEEE Softw. 2018, 35, 16–21. [CrossRef]
6.
Cheng, L.; Liu, F.; Yao, D. Enterprise data breach: Causes, challenges, prevention, and future directions. Wiley Interdiscip. Rev.
Data Min. Knowl. Discov 2017, 7, e1211. [CrossRef]
7.
Bendovschi, A. Cyber-attacks–trends, patterns and security countermeasures. Procedia Econ. Financ. 2015, 28, 24–31. [CrossRef]
8.
ALsaed, Z.; Jazzar, M. COVID-19 age: Challenges in cybersecurity and possible solution domains. J. Theor. Appl. Inf. Technol. 2021,
99, 2648–2658.

Appl. Sci. 2025, 15, 1903
17 of 19
9.
Xu, H.; Thakur, K.; Kamruzzaman, A.; Ali, M.L. Applications of cryptography in database: A review. In Proceedings of the 2021
IEEE International IOT, Electronics and Mechatronics Conference (IEMTRONICS), Virtual, 21 April 2021; pp. 1–6.
10.
Kabir, E.; Hu, J.; Wang, H.; Zhuo, G. A novel statistical technique for intrusion detection systems. Future Gener. Comput. Syst.
2018, 79, 303–318. [CrossRef]
11.
Radford, B.J.; Apolonio, L.M.; Trias, A.J.; Simpson, J.A. Network traffic anomaly detection using recurrent neural networks. arXiv
2018, arXiv:1803.10769.
12.
Luh, R.; Janicke, H.; Schrittwieser, S. AIDIS: Detecting and classifying anomalous behavior in ubiquitous kernel processes. Comput.
Secur. 2019, 84, 120–147. [CrossRef]
13.
Croft, R.; Newlands, D.; Chen, Z.; Babar, M.A. An empirical study of rule-based and learning-based approaches for static
application security testing. In Proceedings of the 15th ACM/IEEE International Symposium on Empirical Software Engineering
and Measurement (ESEM), Virtual, 11–15 October 2021; pp. 1–12.
14.
Chen, C.; Huang, Y.P.; Lam, W.H.; Pan, T.L.; Hsu, S.C.; Sumalee, A.; Zhong, R.X. Data efficient reinforcement learning and
adaptive optimal perimeter control of network traffic dynamics. Transp. Res. Part C Emerg. Technol. 2022, 142, 103759. [CrossRef]
15.
Fransen, F.; Smulders, A.; Kerkdijk, R. Cyber security information exchange to gain insight into the effects of cyber threats and
incidents. Elektrotech. Informationstechnik 2015, 132, 106–112. [CrossRef]
16.
Halimaa, A.; Sundarakantham, K. Machine learning based intrusion detection system. In Proceedings of the 2019 3rd International
Conference on Trends in Electronics and Informatics (ICOEI), Tirupati, India, 11–13 April 2019; pp. 916–920.
17.
Kus, D.; Wagner, E.; Pennekamp, J.; Wolsing, K.; Fink, I.B.; Dahlmanns, M.; Wehrle, K.; Henze, M.M. A false sense of security?
Revisiting the state of machine learning-based industrial intrusion detection. In Proceedings of the 8th ACM on Cyber-Physical
System Security Workshop, San Antonio, TX, USA, 19 May 2022; pp. 73–84.
18.
Heaton, J. An empirical analysis of feature engineering for predictive modeling. arXiv 2017, arXiv:1701.07852.
19.
Wang, H.; Chen, S.; Xu, F.; Jin, Y.-Q. Application of deep-learning algorithms to MSTAR data. In Proceedings of the 2015 IEEE
International Geoscience and Remote Sensing Symposium (IGARSS), Milan, Italy, 26–31 July 2015; pp. 3743–3745.
20.
Borys, A.; Kamruzzaman, A.; Thakur, H.N.; Brickley, J.C.; Ali, M.L.; Thakur, K. An evaluation of IoT DDoS cryptojacking malware
and Mirai Botnet. In Proceedings of the 2022 IEEE World AI IoT Congress (AIIoT), Seattle, WA, USA, 6–9 June 2022; pp. 725–729.
21.
Janiesch, C.; Zschech, P.; Heinrich, K. Machine learning and deep learning. Electron. Mark. 2021, 31, 685–695. [CrossRef]
22.
Najafabadi, M.M.; Villanustre, F.; Khoshgoftaar, T.M.; Seliya, N.; Wald, R.; Muharemagic, E. Deep learning applications and
challenges in big data analytics. J. Big Data 2015, 2, 1–21. [CrossRef]
23.
Arafah, M.; Phillips, I.; Adnane, A.; Hadi, W.; Alauthman, M.; Al-Banna, A.K. Anomaly-based network intrusion detection using
denoising autoencoder and Wasserstein GAN synthetic attacks. Appl. Soft Comput. 2025, 168, 112455. [CrossRef]
24.
Ali, M.L.; Monaco, J.V.; Tappert, C.C.; Qiu, M. Keystroke biometric systems for user authentication. J. Signal Process. Syst. 2017, 86,
175–190. [CrossRef]
25.
Kamath, C.N.; Bukhari, S.S.; Dengel, A. Comparative study between traditional machine learning and deep learning approaches
for text classification. In Proceedings of the ACM Symposium on Document Engineering, Halifax, NS, Canada, 28–31 August
2018; pp. 1–11.
26.
Panda, M.; Abraham, A.; Patra, M.R. Hybrid intelligent systems for detecting network intrusions. Secur. Commun. Netw. 2015, 8,
2741–2749. [CrossRef]
27.
Shrestha, A.; Mahmood, A. Review of deep learning algorithms and architectures. IEEE Access 2019, 7, 53040–53065. [CrossRef]
28.
Thakur, K.; Ali, M.L.; Obaidat, M.A.; Kamruzzaman, A. A systematic review on deep-learning-based phishing email detection.
Electronics 2023, 12, 4545. [CrossRef]
29.
Aslan, Ö.A.; Samet, R. A comprehensive review on malware detection approaches. IEEE Access 2020, 8, 6249–6271. [CrossRef]
30.
Membele, G.M.; Naidu, M.; Mutanga, O. Examining flood vulnerability mapping approaches in developing countries: A scoping
review. Int. J. Disaster Risk Reduct. 2022, 69, 102766. [CrossRef]
31.
Shaukat, K.; Luo, S.; Varadharajan, V.; Hameed, I.A.; Xu, M. A survey on machine learning techniques for cyber security in the
last decade. IEEE Access 2020, 8, 222310–222354. [CrossRef]
32.
Mighan, S.N.; Kahani, M. A novel scalable intrusion detection system based on deep learning. Int. J. Inf. Secur. 2021, 20, 387–403.
[CrossRef]
33.
Lansky, J.; Ali, S.; Mohammadi, M.; Majeed, M.K.; Karim, S.H.T.; Rashidi, S.; Hosseinzadeh, M.; Rahmani, A.M. Deep learning-
based intrusion detection systems: A systematic review. IEEE Access 2021, 9, 101574–101599. [CrossRef]
34.
Thakur, H.N.; Al Hayajneh, A.; Thakur, K.; Kamruzzaman, A.; Ali, M.L. A Comprehensive Review of Wireless Security
Protocols and Encryption Applications. In Proceedings of the 2023 IEEE World AI IoT Congress (AIIoT), Virtual, 7–10 June 2023;
pp. 373–379.
35.
Ljung, L. Black-box models from input-output measurements. In Proceedings of the 18th IEEE Instrumentation and Measurement
Technology Conference. Rediscovering Measurement in the Age of Informatics (Cat. No. 01CH 37188), Budapest, Hungary,
21 May 2001; pp. 138–146.

Appl. Sci. 2025, 15, 1903
18 of 19
36.
Mahdavifar, S.; Ghorbani, A.A. Application of deep learning to cybersecurity: A survey. Neurocomputing 2019, 347, 149–176.
[CrossRef]
37.
Garcia-Teodoro, P.; Diaz-Verdejo, J.; Maciá-Fernández, G.; Vázquez, E. Anomaly-based network intrusion detection: Techniques,
systems and challenges. Comput. Secur. 2009, 28, 18–28. [CrossRef]
38.
Thakur, K.; Tao, L.; Wang, T.; Ali, M.L. Cloud computing and its security issues. Appl. Theory Comput. Technol. 2017, 2, 1–10.
[CrossRef]
39.
Chiba, Z.; Abghour, N.; Moussaid, K.; Rida, M. Intelligent approach to build a Deep Neural Network based IDS for cloud
environment using combination of machine learning algorithms. Comput. Secur. 2019, 86, 291–317. [CrossRef]
40.
Ali, M.L.; Ismat, S.; Thakur, K.; Kamruzzaman, A.; Lue, Z.; Thakur, H.N. Network packet sniffing and defense. In Proceedings
of the 2023 IEEE 13th Annual Computing and Communication Workshop and Conference (CCWC), Las Vegas, NV, USA,
8–11 March 2023; pp. 499–503.
41.
Ertu˘grul, Ö.F.; Ta˘gluk, M.E. A novel version of k nearest neighbor: Dependent nearest neighbor. Appl. Soft Comput. 2017, 55,
480–490. [CrossRef]
42.
Pisner, D.A.; Schnyer, D.M. Support vector machine. In Machine Learning; Elsevier: Amsterdam, The Netherlands, 2020;
pp. 101–121.
43.
Karatas, G.; Demir, O.; Sahingoz, O.K. Increasing the performance of machine learning-based IDSs on an imbalanced and
up-to-date dataset. IEEE Access 2020, 8, 32150–32162. [CrossRef]
44.
Thakur, K.; Qiu, M.; Gai, K.; Ali, M.L. An investigation on cyber security threats and security models. In Proceedings of the 2015
IEEE 2nd international conference on cyber security and cloud computing, New York, NY, USA, 3–5 November 2015; pp. 307–311.
45.
Yin, C.; Zhu, Y.; Fei, J.; He, X. A deep learning approach for intrusion detection using recurrent neural networks. IEEE Access 2017,
5, 21954–21961. [CrossRef]
46.
Gu, J.; Wang, Z.; Kuen, J.; Ma, L.; Shahroudy, A.; Shuai, B.; Liu, T.; Wang, X.; Wang, G.; Cai, J.; et al. Recent advances in
convolutional neural networks. Pattern Recognit. 2018, 77, 354–377. [CrossRef]
47.
Kamruzzaman, A.; Thakur, K.; Ismat, S.; Ali, M.L.; Huang, K.; Thakur, H.N. Social engineering incidents and preventions.
In Proceedings of the 2023 IEEE 13th Annual Computing and Communication Workshop and Conference (CCWC), Virtual,
8–11 March 2023; pp. 494–498.
48.
Kevric, J.; Jukic, S.; Subasi, A. An effective combining classifier approach using tree algorithms for network intrusion de-tection.
Neural Comput. Appl. 2017, 28 (Suppl. S1), 1051–1058. [CrossRef]
49.
Javaid, A.; Niyaz, Q.; Sun, W.; Alam, M. A deep learning approach for network intrusion detection system. In Proceedings of
the 9th EAI International Conference on Bio-Inspired Information and Communications Technologies (Formerly BI-ONETICS),
New York, NY, USA, 3–5 December 2015; pp. 21–26.
50.
Kim, T.; Kang, B.; Rho, M.; Sezer, S.; Im, E.G. A multimodal deep learning method for android malware detection using various
features. IEEE Trans. Inf. Forensics Secur. 2018, 14, 773–788. [CrossRef]
51.
Han, J.; Zhang, D.; Cheng, G.; Liu, N.; Xu, D. Advanced deep-learning techniques for salient and category-specific object detection:
A survey. IEEE Signal Process. Mag. 2018, 35, 84–100. [CrossRef]
52.
Sherstinsky, A. Fundamentals of recurrent neural network (RNN) and long short-term memory (LSTM) network. Phys. Nonlinear
Phenom. 2020, 404, 132306. [CrossRef]
53.
Dey, R.; Salem, F.M. Gate-variants of gated recurrent unit (GRU) neural networks. In Proceedings of the 2017 IEEE 60th
International Midwest Symposium on Circuits and Systems (MWSCAS), Boston, MA, USA, 6–9 August 2017; pp. 1597–1600.
54.
Vinayakumar, R.; Alazab, M.; Soman, K.P.; Poornachandran, P.; Al-Nemrat, A.; Venkatraman, S. Deep learning approach for
intelligent intrusion detection system. IEEE Access 2019, 7, 41525–41550. [CrossRef]
55.
Ali, M.L.; Thakur, K.; Obaidat, M.A. A hybrid method for keystroke biometric user identification. Electronics 2022, 11, 2782.
[CrossRef]
56.
Wang, W.; Zhao, M.; Wang, J. Effective android malware detection with a hybrid model based on deep autoencoder and
convolutional neural network. J. Ambient Intell. Humaniz. Comput. 2019, 10, 3035–3043. [CrossRef]
57.
Zhang, P.; Yin, Z.-Y.; Jin, Y.-F.; Chan, T.H. A novel hybrid surrogate intelligent model for creep index prediction based on particle
swarm optimisation and random forest. Eng. Geol. 2020, 265, 105328. [CrossRef]
58.
Papernot, N.; McDaniel, P.; Wu, X.; Jha, S.; Swami, A. Distillation as a defense to adversarial perturbations against deep neural
networks. In Proceedings of the 2016 IEEE Symposium on Security and Privacy (S.P.), San Jose, CA, USA, 22–26 May 2016;
pp. 582–597.
59.
Tian, Z.; Cui, L.; Liang, J.; Yum, S. A comprehensive survey on poisoning attacks and countermeasures in machine learning. ACM
Comput. Surv. 2022, 55, 1–35. [CrossRef]
60.
Grosse, K.; Papernot, N.; Manoharan, P.; Backes, M.; McDaniel, P. Adversarial examples for malware detection. In Proceedings
of the Computer Security–ESORICS 2017: 22nd European Symposium on Research in Computer Security, Oslo, Norway,
11–15 September 2017; pp. 62–79.

Appl. Sci. 2025, 15, 1903
19 of 19
61.
Selvam, R.; Velliangiri, S. An Improving Intrusion Detection Model Based on Novel CNN Technique Using Recent CIC-IDS
Datasets. In Proceedings of the 2024 International Conference on Distributed Computing and Optimization Techniques (ICDCOT),
Bengaluru, India, 15–16 March 2024; pp. 1–6.
62.
Sharafaldin, I.; Lashkari, A.H.; Ghorbani, A.A. CIC-IDS2017 [Data Set]. Kaggle. 2022. Available online: https://www.kaggle.
com/datasets/dhoogla/cicids2017 (accessed on 5 February 2025).
Disclaimer/Publisher’s Note: The statements, opinions and data contained in all publications are solely those of the individual
author(s) and contributor(s) and not of MDPI and/or the editor(s). MDPI and/or the editor(s) disclaim responsibility for any injury to
people or property resulting from any ideas, methods, instructions or products referred to in the content.