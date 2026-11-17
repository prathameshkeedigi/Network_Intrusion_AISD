# 11_Zaim_2025_Appl_Sci_FPE_Transformer

_Source PDF, 25 pages. Auto-converted._

Academic Editor: Luis Javier Garcia
Villalba
Received: 23 December 2024
Revised: 18 January 2025
Accepted: 23 January 2025
Published: 26 January 2025
Citation: Çav¸si Zaim, H.; Yolaçan,
E.N. FPE–Transformer: A Feature
Positional Encoding-Based
Transformer Model for Attack
Detection. Appl. Sci. 2025, 15, 1252.
https://doi.org/10.3390/
app15031252
Copyright: © 2025 by the authors.
Licensee MDPI, Basel, Switzerland.
This article is an open access article
distributed under the terms and
conditions of the Creative Commons
Attribution (CC BY) license
(https://creativecommons.org/
licenses/by/4.0/).
Article
FPE–Transformer: A Feature Positional Encoding-Based
Transformer Model for Attack Detection
Hande Çav¸si Zaim
and Esra Nergis Yolaçan *
Department of Computer Engineering, Eskisehir Osmangazi University, Eskisehir 26040, Türkiye;
handecavsi@gmail.com
* Correspondence: yolacan@ogu.edu.tr
Abstract: The increase in cybersecurity threats has made attack detection systems critically
important. Traditional deep learning methods often require large amounts of data and
struggle to understand relationships between features effectively. With their self-attention
mechanism, Transformers excel in modeling complex relationships and long-term depen-
dencies. They are also adaptable to various data types and sources, making them advanta-
geous in large-scale attack detection scenarios. This paper introduces the FPE–Transformer
framework, leveraging the strengths of the Transformer architecture. FPE–Transformer
incorporates an innovative feature positional encoding mechanism that encodes the posi-
tional information of each feature separately, enabling a deeper understanding of feature
relationships and more precise attack detection. Additionally, the model includes a Classi-
ficationHead for enhanced accuracy and complex pattern recognition. The framework’s
performance was validated using the NSL-KDD and CIC-IDS2017 datasets, demonstrating
its superiority over traditional methods in detecting diverse attack types and improving
overall performance. This study highlights FPE–Transformer’s innovative approach and
ability to address key limitations of traditional deep learning methods, establishing it as a
robust solution for modern attack detection challenges.
Keywords: Transformer models; attack detection; cybersecurity; deep learning; FPE–
Transformer
1. Introduction
As the reliance on interconnected systems grows across various sectors, the need for
robust cybersecurity mechanisms has become increasingly critical. Modern systems, inte-
grated with complex networks and control architectures, are highly vulnerable to diverse
cyberattacks. Such attacks can hinder operations, jeopardize data integrity, and result in
substantial financial losses, reputational harm, and potential threats to public safety in criti-
cal settings. Effective attack detection systems are essential to prevent unauthorized access,
mitigate data breaches, and safeguard the functionality of systems against manipulations
that could compromise their operations. Addressing these cybersecurity challenges is vital
for ensuring the reliability and resilience of today’s interconnected infrastructures.
Deep learning (DL) models have gained popularity by providing successful results in
attack detection tasks [1]. DL models are more suitable for processing high-dimensional
and complex features than classical machine learning (ML) models [2]. DL models such as
Long Short-Term Memory (LSTM), Recurrent Neural Networks (RNNs), Convolutional
Neural Networks (CNNs), Bi-Directional-LSTM (Bi-LSTM), and Generative Adversarial
Networks (GANs) are widely used in attack detection tasks. In [3], the LSTM model was
used to detect replay and amplitude shift attacks, while in [4], it was used to detect false
Appl. Sci. 2025, 15, 1252
https://doi.org/10.3390/app15031252

Appl. Sci. 2025, 15, 1252
2 of 25
data injection attacks. Similarly, Muhiri et al. applied an LSTM-RNN hybrid model for
attack classification on the NSL-KDD dataset, achieving improved accuracy in binary and
multi-class classification tasks [5]. Hwang et al. developed an approach for real-time
classification using an innovative word embedding mechanism and LSTM model at the
packet level to achieve faster attack detection results [6]. Another study utilized a CNN-
LSTM hybrid model to detect BotNet attacks [7]. In addition, the CNN–Gated Recurrent
Unit (GRU) hybrid model was proposed to improve the classification accuracy and class
imbalance problem, and high accuracy rates were achieved on various datasets [8]. In
another study on CNN-based attack detection, the performance of CNN and CNN-LSTM
models for multi-class categorization of network attacks is discussed [9]. The effectiveness
of these models is tested on the NSL-KDD dataset. The Bi-LSTM model, with its iterative
learning capability, has been effectively used for tasks such as malware detection, VPN
encapsulation recognition, and Trojan classification [10]. Additionally, the GAN model,
which addresses the challenge of low attack detection accuracy due to limited labeled data,
expands the training dataset by continuously generating samples, thereby significantly
improving accuracy [11].
LSTMs and RNNs perform well in time series data by leveraging historical informa-
tion; however, they may struggle to capture long-term dependencies and often encounter
issues like gradient vanishing during training. While CNNs can extract spatial features
effectively, they may be limited when dealing with time series or sequence-based data.
Bi-LSTMs improve analysis by capturing both forward and backward dependencies, yet
their high computational cost can impact performance, especially with long sequences.
GANs are valuable for attack simulation and data generation, but their training process
can be challenging to maintain, and they may lead to high false positive rates. In contrast,
Transformer models excel at learning both short-term and long-term patterns by effectively
capturing long-term dependencies through their self-attention mechanism [12]. Their
parallel processing capabilities make them faster and more scalable for large datasets. By
analyzing the entire sequence regardless of input size, Transformers avoid issues like gradi-
ent vanishing in sequence data, offering enhanced accuracy, scalability, and flexibility for
detecting cyberattacks. The Finformer model provides higher accuracy and efficiency in fi-
nancial attack detection using the Transformer architecture compared to traditional models,
validating the advantages of Transformers in the capture of complex attack patterns [13]. A
Transformer model named FCNN-SE has achieved successful results in multi-dimensional
traffic data to improve complex feature extraction processes [14].
This study introduces a novel Transformer-based feature positional encoding (FPE)
Transformer model for attack detection. Unlike existing Transformer-based approaches,
FPE–Transformer only uses encoders, and it includes an optimized classification head that
follows these encoders. In addition, instead of traditional positional encoding adapted to
text, it uses feature positional encoding. Feature positional encoding can better capture the
relationships and temporal patterns among features, enabling more precise attack detection.
Experimental results show that the FPE–Transformer model is successful in attack detection.
The primary contributions of our work can be summarized as follows:
•
We reviewed existing Transformer models in the literature.
•
We introduced a novel feature positional encoding method, which uniquely calculates
separate positional encodings for each feature in a dataset.
•
We introduced the novel FPE–Transformer attack detection framework, which
combines temporal analysis with the feature positional encoding technique in a
Transformer-based model. Our FPE–Transformer framework is a Transformer-based
attack detection model that applies feature positional encoding to capture complex

Appl. Sci. 2025, 15, 1252
3 of 25
temporal patterns of individual features. By improving the ability to distinguish attack
behaviors, this approach increases detection accuracy in network security applications.
•
We compared the performance of the classification results for Transformer models
with various positional encodings.
Section 2 examines Transformer models in the literature and their application for
attack detection. Section 3 includes the FPE–Transformer model. Section 4 outlines the
experimental findings. Section 5 presents recommendations for future research.
2. Literature Review
In recent years, Transformer models have revolutionized the landscape of natural
language processing and machine learning, demonstrating remarkable performance across
various tasks. Understanding the architecture and mechanisms of these models is essential
for grasping their efficacy in detecting and mitigating security threats. This section examines
large language model (LLM)-based Transformer models and attack detection. While
Background of Transformer Models examines various LLM-based Transformer models,
the Transformer Models for Attack Detection section examines Transformer models in the
context of attack detection applications.
2.1. Background of Transformer Models
The Transformer model was first described in 2017 as a simple and innovative network
architecture that eliminates recurrent and convolutional networks and relies solely on
attention mechanisms [15]. These architectures are highly effective in natural language
processing (NLP) tasks because they can capture long-range dependencies and relation-
ships between elements in sequences without needing prior domain knowledge or feature
engineering. Vaswani’s essential Transformer model includes both encoder and decoder
modules. The encoder processes the input sequence to create representations, and the
decoder generates the output sequence based on these representations. This dual structure
effectively allows the model to handle various tasks, from translation to text generation.
The outstanding success of the Transformer model in NLP tasks has led to the emergence
of various versions of this modeling, which have increased its applicability to different
tasks. These LLM-based models can be classified as auto-encoding, encoder–decoder, and
autoregressive according to the differences in their pre-training architectures [16].
The pre-training architecture of auto-encoding Transformers consists of encoders only.
These models effectively capture contextual information and learn rich representations
of input data by reconstructing missing or masked portions. This allows them to excel
in tasks like text classification, sentiment analysis, and other downstream tasks where
understanding the full context of the input is crucial. The Bidirectional Encoding Represen-
tation Transformer (BERT) is one of the automatic encoding Transformer models [17]. BERT
stands out with its ability to train language models bidirectionally. Unlike the one-way
models developed in the OpenAI technical report [18], BERT extracts information from
both aspects of the context around words using Masked Language Modeling (MLM). Then,
it performs the sentence-matching task with Next Sentence Prediction (NSP). This bidirec-
tional pre-training approach makes language representations richer and more meaningful
because the left and right contexts are evaluated together. Thus, unlike unidirectional
models such as OpenAI GPT, BERT improves the task-specific fine-tuning phase by per-
forming bidirectional pre-training. BioBERT is the first BERT-based pre-trained model for
biomedical data [19]. The pre-training phase starts with weights taken from BERT and
improves performance on named entity recognition (NER), relation extraction (RE), and
question–answer (QA) tasks. RoBERTa is a retrained BERT version with more data and
computational power. It removes the NSP task and uses dynamic masking [20]. ALBERT

Appl. Sci. 2025, 15, 1252
4 of 25
uses factorial embedding and cross-layer parameter sharing to reduce the parameters in
BERT [21]. This way, it has 18 times fewer parameters than BERT and trains 1.7 times faster
while showing similar performance [22]. DeBERTa improves on previous models with
disaggregated attention and an enhanced mask decoder [23]. Instead of combining word
and location information as in BERT, decoupled attention encodes content and location
separately for each input token. This way, the model can calculate attention weights based
on the token’s content and location. The improved mask decoder allows the use of absolute
locations of markers when making MLM predictions, together with location-based atten-
tion. ELECTRA is another auto-encoding model that uses alternative tokens produced by a
generator to replace tokens in a sequence [24]. This model has a discriminative model that
predicts whether the generator has modified each token in the corrupted input.
The pre-training architecture of autoregressive Transformers consists of decoders only.
These models effectively generate data sequences by predicting the next element in a se-
quence based on the previously generated elements, making them particularly suitable
for tasks like language modeling, text generation, and dialogue systems, where producing
coherent and contextually relevant outputs is essential. OpenAI GPT is one of the autore-
gressive Transformer models, and its pre-training architecture consists of decoders [25]. The
model training goal is to predict the following words, given all previous words in the text.
The various versions of GPT differ primarily in the number of decoder layers used [26].
GPT-1 uses 12 decoders, GPT-2 uses 48 decoders, and GPT-3 uses 96 decoders. These
increases in decoder layers allow the model to produce more consistent and contextually
rich text output.
The pre-training architecture of encoder–decoder Transformers includes both encoders
and decoders. This architecture allows the learning of both input data (encoder) and output
sequences (decoder). The encoder analyzes the input’s complex language structure and con-
text, while the decoder uses this information to produce a new text sequence. These models
are particularly good at language translation, summarization, text completion, and error
correction tasks. Encoder–decoder models perform strongly in tasks requiring sequential
data processing because they generate the output by considering the entire input. The Text-
To-Text Transfer Transformer (T5) encoder–decoder model aims to formulate all tasks as a
text-to-text transformation problem by addressing language processing tasks in a unifying
framework [27]. It becomes usable in various NLP tasks by always presenting input and
output as text strings. The T5 model aims to provide a flexible structure for different tasks
(e.g., language modeling, translation, summarization, classification, Q&A). During T5’s
pre-training, some distortions are applied to the input text strings. The T5 model is trained
by correcting these distortions. In this way, the model improves its understanding of the
broader structure and context of the language. The T5 has been used for translation, text
summarization, text classification, question-and-answer, and other language processing
tasks and has demonstrated high performance in many NLP benchmarks [28]. Code-T5 is
introduced as an optimized version of T5 [29]. It focuses on understanding and generating
software code, specifically for programming languages’ tasks such as code completion,
error detection, and comment generation. Another encoder–decoder Transformer model,
the Bidirectional and Autoregressive Transformer (BART), offers a more powerful and
flexible structure by combining forward and backward information flow [30]. BART is
mainly used in text corruption and reconstruction tasks, meaning that it learns to recon-
struct the input text by corrupting it (for example, by removing words or changing the
order of sentences). Therefore, BART is preferred in tasks such as text enhancement, text
summarization, translation, and Q&A. Multilingual BART (mBART) is derived from the
BART model and focuses on multilingual NLP tasks [31]. While the BART model is trained
only in a single language, mBART offers a structure trained on parallel data in multiple lan-

Appl. Sci. 2025, 15, 1252
5 of 25
guages and supports cross-language transfer. The critical difference between mBART and
BART is that mBART can overcome language barriers and learn patterns in multilingual
texts, thus enabling cross-language transfer learning. mBART combines text decomposition
and reconstruction capabilities with multi-language support, demonstrating high perfor-
mance in language pair conversions, multi-language summarization, and multi-language
translation tasks. Programming Language BART (PLBART) is a version of the BART model
adapted to programming languages and is designed to understand and generate software
code [32]. While BART is optimized for general NLP tasks, PLBART is explicitly used for
code completion, error detection, code commenting, and natural language generation from
code. It bridges the gap between natural language and programming language. PLBART
uses BART’s encoder–decoder architecture to process natural and programming language
text. Another encoder–decoder Transformer model, BERT2GPT, combines BERT’s powerful
language understanding capabilities with GPT’s language generation capabilities [33]. This
model succeeds in text understanding tasks with the bidirectional encoder structure of
BERT and generates text effectively with the autoregressive decoder structure of GPT.
BERT2GPT is mainly introduced in tasks where complex language understanding and
production processes are integrated. It aims to bridge the gap between natural language
understanding (NLU) and natural language generation (NLG). The model excels in tasks
such as text completion, Q&A systems, dialogue generation, and text summarization.
Consequently, the evolution of Transformer models has significantly propelled ad-
vancements in natural language processing and has facilitated the creation of various
architectures designed for specific tasks. Table 1 compares the various Transformer models
examined according to their types and preferred application areas.
Table 1. Comparison of Transformer models.
Model
Type
Pre-Training
Architecture
Applications
BERT
Auto-encoding
Encoders
Text classification,
sentiment
analysis, NER
BioBERT
Auto-encoding
Encoders
RE, Q&A, NER
RoBERTa
Auto-encoding
Encoders
Text classification,
sentiment analysis
ALBERT
Auto-encoding
Encoders
Text classification,
NLP tasks
DeBERTa
Auto-encoding
Encoders
Text classification,
dialogue systems
ELECTRA
Auto-encoding
Encoders
Text classification,
NLP tasks
GPT-1
Autoregressive
12 Decoders
Text generation,
dialogue systems
GPT-2
Autoregressive
48 Decoders
Text generation,
dialogue systems
GPT-3
Autoregressive
96 Decoders
Text generation,
dialogue systems
T5
Encoder–Decoder
Encoders and
Decoders
Language modeling,
translation,
summarization,
classification, Q&A

Appl. Sci. 2025, 15, 1252
6 of 25
Table 1. Cont.
Model
Type
Pre-Training
Architecture
Applications
Code-T5
Encoder–Decoder
Encoders and
Decoders
Generating software
code, code completion,
error detection,
comment generation
BART
Encoder–Decoder
Encoders and
Decoders
Text enhancement,
text summarization,
translation, Q&A
mBART
Encoder–Decoder
Encoders and
Decoders
Pair conversions,
multi-language
summarization,
multi-language
translation
PLBART
Encoder–Decoder
Encoders and
Decoders
Code completion,
error detection, code
commenting, natural
language generation
BERT2GPT
Encoder–Decoder
Encoders and
Decoders
Text completion, Q&A,
dialogue generation,
text summarization
Auto-encoding Transformers, such as BERT and its derivatives, leverage bidirectional
training approaches to capture contextual nuances effectively, making them suitable for
various applications, including text classification and named entity recognition. In contrast,
autoregressive Transformers, exemplified by the GPT series, focus on sequential text
generation, enabling coherent and contextually relevant output. The ongoing enhancements
in these models, such as dynamic masking in RoBERTa and decoupled attention in DeBERTa,
highlight the continuous quest for optimizing performance while reducing computational
requirements. Encoder–decoder Transformer models are architectures that can establish
complex relationships between input and output sequences. Models such as T5, BART, and
mBART use a powerful encoder to understand input sequences and work with a decoder to
produce consistent outputs using this information. This architecture is particularly effective
in machine translation, text summarization, and Q&A. In addition, models such as PLBART
and Code-T5 offer practical solutions for software development processes by processing
natural language and programming languages in the same structure. Developments made
in encoder–decoder models provide versatile use by optimizing both understanding and
production processes, unlike models such as BERT and GPT, which focus solely on encoders
or decoders.
2.2. Transformer Models for Attack Detection
With significant advancements in NLP and LLMs, Transformers have expanded their
reach into many research areas due to its advanced text generation and user interaction
capabilities. One area that has significantly benefited from these advancements is cyberse-
curity [34]. Transformer models have emerged as powerful tools in attack detection thanks
to their ability to capture complex patterns and relationships in data through attention
mechanisms. These models can learn benign patterns found in sequential sequences, such
as network traffic, and can successfully detect changes in network traffic patterns even
when the number of attacks is small [35].
In an attack detection study that utilizes the attention mechanism, CNN and GRU
were combined with an attention mechanism to avoid SQL injection and cross-site scripting

Appl. Sci. 2025, 15, 1252
7 of 25
(XSS) attacks [36]. The proposed approach leveraged an attention mechanism to attain
high accuracy, minimize the need for extensive training data, and shorten the training
duration. Barut et al. [37] proposed the Residual 1-D Image Transformer (R1DIT) model
to tackle challenges related to privacy and generalization in malware traffic classification.
The proposed model parses network headers while preserving sensitive data and uses
DL and Multi-Head Attention (MHA) mechanisms to distinguish between malware and
benign traffic. Nguyen et al. [38] introduced a Transformer-based attention network (TAN)
as a multi-class intrusion detection system for the in-car Control Area Network (CAN)
bus protocol. The proposed model eliminates the limitations of RNN-based methods
and can classify attacks without needing message labeling using sequential CAN ID
data. In another study based on the Transformer attention mechanism, the proposed
Transformer-based model was compared with Tree-based models, and it was observed that
the Transformer-based intrusion detection model performed better [39]. One approach to
address Deep Neural Network (DNN) limitations combined feature embedding and self-
attention modules of the Transformer model with fully connected layers [40]. The proposed
model gave better results compared to the Decision Tree (DT) algorithm. Another study
introduced an MHA-based Transformer that enhanced intrusion detection robustness
compared to LSTM and RNN models [41]. Hou et al. [42] introduced a Denseformer
model that integrates the self-attention mechanism with the cross-attention mechanism
and includes encoders and decoders. Due to the Denseformer’s cross-fusion structure,
feature correlations were identified more effectively. Finformer, on the other hand, identifies
attacks in financial data by integrating the Transformer architecture with a cluster-attention
mechanism [13].
In addition to the attention mechanism provided by Transformer models, the CNN–
Transformer hybrid model has also emerged as a powerful tool in intrusion detection.
Leveraging CNNs’ ability to extract local features enables rapid and effective pattern
identification, especially in large, complex datasets like network traffic. Yao et al. [43]
proposed a CNN–Transformer model to capture spatial relationships and patterns in
more detail, enhancing feature representation across different data domains. Similarly, a
CNN–Transformer hybrid model, combining dense CNNs and Transformers, has been
applied for feature fusion and time series extraction [44]. Another study utilized this
model to address RNNs’ challenges with information loss, computational complexity,
and detection performance [45]. Observing the model’s strength in capturing spatial and
local features, researchers experimented with adding LSTM layers or replacing CNN with
LSTM to improve temporal relationship modeling, facilitating deep analysis and sequential
dependencies in time series data. Wang and Li [46] introduced a hybrid DdosTC network,
combining Transformer and CNN architectures to detect Distributed Denial of Service
(DDoS) attacks. Similarly, the XTM model, a Transformer-based approach, was developed
for real-time data breach detection, achieving high performance on the IEEE-14 bus system
and advancing smart grid security [47]. Ding et al. [48] proposed an attack detection model
that leverages multi-frequency LSTM and Transformer modules to analyze temporal details
across high- and low-frequency data, enhancing detection precision.
Vision Transformer (ViT) models have significantly contributed to attack detection
applications. Unlike CNNs, which analyze images hierarchically by focusing on local
features, ViTs process images as patch arrays and leverage self-attention to capture global
relationships. While ViTs require larger datasets and more computational resources than
CNNs, they excel in capturing global context. Ref. [49] highlights the advantages of ViT
models on visual data compared to traditional data. Li et al. [50] proposed an architecture
integrating a feature fusion network with ViT, improving the model’s capability to manage
imbalanced datasets and decreasing the required training sample size. In another study,

Appl. Sci. 2025, 15, 1252
8 of 25
network data streams were transformed into images by mapping them to RGB values [51].
After initial analysis with a decision tree algorithm, these images were categorized using a
ViT classifier. Similarly, another approach converted network traffic data from packet cap-
ture (PCAP) files into grayscale images for malware classification using ViT techniques [52].
The effectiveness of ViT was evaluated by comparing its performance with that of CNNs,
highlighting the strengths of ViT in this context.
Classification performance in attack detection suffers due to imbalanced training data
and limited feature extraction. To increase minority class examples and address the imbal-
ance problem in attack data, a new method for multi-class attack detection that combines a
conditional generative adversarial network (CGAN) and a pre-trained language model,
BERT, was presented in [53]. BERT is integrated with CGAN to improve the relationship be-
tween input and output for robust feature extraction. Similarly, Wang et al. [54] integrated
CGAN with ViT to enhance detection accuracy in imbalanced network flow data.
In addition to the hybrid models examined, the authors have proposed new
Transformer-based attack detection frameworks by changing the components of the Trans-
former architecture. Wu et al. [55] introduced the Robust Transformer-based Intrusion
Detection System (RTIDS), designed to reconstruct feature representations, achieving a
balance between dimensionality reduction and feature preservation in imbalanced datasets.
Seyyar et al. [56] proposed a model combining BERT and deep learning techniques to detect
HTTP attacks. Ghourabi [57] developed an attack detection model based on LightGBM and
Transformers to enhance system security in the healthcare domain. Additionally, Liu and
Wu [58] presented an improved Transformer-based attack detection model that addresses
challenges such as long training times, inaccurate detection of overlapping classes, and low
multi-class classification performance in existing models. By updating the Transformer’s
positional encoding module, their model achieved higher accuracy than CNN–Transformer
models. Ullah et al. [59] proposed the IDS-INT system, a Transformer-based transfer learn-
ing model, to tackle the complexities of network traffic features and imbalanced datasets.
Table 2 summarizes these Transformer models applied in attack detection.
Transformer-based attack detection methods offer various advantages by combining
the strengths of different models. CNN–Transformer models combine CNNs’ local feature
extraction capabilities with the Transformer’s capacity to understand the global context.
They are particularly effective on large, complex datasets. However, LSTM–Transformer
models are preferred for cases where CNNs may cause information loss in time series
data. While LSTMs capture serial dependencies in time series data, Transformer analyzes
these relationships more deeply with the attention mechanism. CNN–LSTM–Transformer
models provide a broader perspective by capturing both local and time-based features, but
these models have high computational costs and training time.
GAN–Transformer models stand out to address data imbalance issues. GANs increase
minority class examples, while Transformers improve input–output relationships with an
attention mechanism. ViT models exhibit high performance in extracting global features
and processing image data in image-based analysis. However, ViT models require large
datasets and have high computational costs.
Attention-based Transformer models, on the other hand, fully utilize the power of the
attention mechanism by better capturing complex relationships and long-term dependen-
cies. In addition, other Transformer models, such as the more specialized Denseformer,
provide more optimized results in capturing data correlations.
While previous research focuses on attention mechanisms and hybrid model archi-
tectures, FPE–Transformer takes a different path from these approaches by offering an
innovative feature position encoder module.

Appl. Sci. 2025, 15, 1252
9 of 25
Table 2. Transformer models for attack detection applications.
Reference
Type
Dataset
[13]
Attention-based
Public financial transaction records,
synthetic data, anonymized data
from financial institutions
[36]
Attention-based
Kaggle SQL injection, Kaggle XSS,
DeepXSS, Cross-Site-ScriptingXSS
[37]
Attention-based
NetML, CICIDS2017, CICDDoS2019
[38]
Attention-based
Car Hacking
[39]
Attention-based
CICIDS-2017
[40]
Attention-based
CIC-IDS 2017, UNSW-NB15,
Kitsune
[41]
Attention-based
ToN_IoT
[42]
Attention-based
NSL-KDD
[43]
CNN–Transformer
KDDCup99, NSL-KDD,
CICIDS-2017
[44]
CNN–Transformer
CICIDS-2018
[45]
CNN–Transformer
CICDDoS2019, CSE CIC-IDS2018
[46]
CNN–Transformer
CICDDoS2019
[47]
LSTM–Transformer
IEEE-14 Bus System (FDI Attacks)
[48]
LSTM–Transformer
UNSW-NB15, KDDCup99,
NSL-KDD, CICIDS-2017
[50]
ViT
IDS 2017, IDS 2012
[51]
ViT
CICIDS2017, UNSW-NB15
[52]
ViT
CICIDS2017
[53]
GAN–Transformer
CSE-CIC-IDS2018, NF-ToN-IoT-V2,
NF-UNSW-NB15-v2
[54]
GAN&ViT
CICIDS-2017
[55]
RTIDS
CICIDS2017, CIC-DdoS2019
[56]
BERT&DL Techniques
FWAF, CSIC2010, HttpParams
[57]
LightGBM&Transformer
IoT, IoMT, Windows Malware
[58]
Improved Transformer
NSL-KDD, UNSW-NB15
[59]
IDS-INT
UNSW-NB15, CICIDS2017,
NSL-KDD
3. Materials and Methods
3.1. Datasets
In this study, the well-known CIC-IDS2017 and NSL-KDD datasets were used to
validate the FPE–Transformer model. CIC-IDS2017 was created by the Canadian Institute
for Cybersecurity (CIC) in Canada [60]. This dataset contains traffic recorded in a network
environment with a speed of 10Gbps for one week in 2017 (10–15 July 2017). During the
data collection process, various user profiles were created that mimic real user behavior.
The sample numbers according to the attack type of the CIC-IDS2017 dataset, which covers
various network protocols such as HTTP, HTTPS, FTP, SSH, and SMTP, and consists of a
total of 2,672,997 traffic samples, are as shown in Table 3.
The NSL-KDD dataset is an enhanced variant of the KDD-CUP-99 dataset, with redun-
dant and duplicate entries eliminated [61]. The dataset includes normal and anomalous
network traffic, organized into training and testing subsets. The training subset comprises
125,972 samples, whereas the testing subset contains 22,543 samples. The label and sample
counts of the NSL-KDD+train dataset are shown in Table 4, and Table 5 presents the com-
parative sample counts of the NSL-KDD train and test data according to attack categories.

Appl. Sci. 2025, 15, 1252
10 of 25
Table 3. CIC-IDS2017 label and total sample counts.
Label
Sample Count
Benign
2,203,723
DoS Hulk
231,073
Port Scan
158,930
DoS GoldenEye
10,293
DDoS
41,835
FTP-Patator
7938
SSH-Patator
5897
DoS slowloris
5796
DoS Slowhttptest
5499
Bot
1966
Infiltration
36
Heartbleed
11
Table 4. NSL-KDD+train label and total sample counts.
Label
Sample Count
benign
67,342
neptune
41,214
satan
3633
ipsweep
3599
portsweep
2931
smurf
2646
nmap
1493
back
956
teardrop
892
warezclient
890
pod
201
guess_passwd
53
buffer_overflow
30
warezmaster
20
land
18
imap
11
rootkit
10
loadmodule
9
ftp_write
8
multihop
7
phf
4
perl
3
spy
2
Table 5. Number of samples in training and test datasets according to attack types.
Category
Attack Types
Train Sample
Count
Test Sample Count
Normal
normal
67,342
9711
DoS
neptune, smurf,
back, teardrop, pod,
land
50,943
5780

Appl. Sci. 2025, 15, 1252
11 of 25
Table 5. Cont.
Category
Attack Types
Train Sample
Count
Test Sample Count
Probe
satan, ipsweep,
portsweep, nmap,
mscan,
snmpgetattack,
saint, snmpguess
13,764
6639
R2L
guess_passwd,
buffer_overflow,
warezmaster, imap,
rootkit,
loadmodule,
ftp_write, phf, perl
36,215
2227
U2R
multihop, spy,
sqlattack, apache2,
processtable,
httptunnel, worm,
named, ps,
sendmail, xterm,
xlock, xsnoop,
udpstorm
21,256
1551
3.2. Data Preprocessing
A balanced dataset was created to address the problem of class imbalance between
benign and attack samples of NSL-KDD. For binary classification, the dataset was split into
two subsets based on their class labels: attack samples (1) and benign samples (0). The
Borderline-SMOTE technique was applied to the attack class to mitigate the imbalance,
generating synthetic samples by focusing on borderline instances, which are critical for
classification tasks [62]. After oversampling the attack class, the k-Nearest Neighbors
(k-NN) approach was used to downsample the benign class selectively. Specifically, the
k-NN algorithm identified representative benign samples based on their proximity to the
oversampled attack instances, ensuring a balanced yet representative subset of the benign
class. The final balanced dataset was constructed by combining the oversampled attack
samples with the downsampled benign samples. The dataset was then shuffled, and indices
were reset to maintain randomness and consistency in further experiments. This prepro-
cessing strategy resulted in a balanced dataset, effectively reducing the impact of class
imbalance on model training while preserving the intrinsic characteristics of both classes.
The subsampling of the benign class with the k-NN algorithm is as in Equation (1) [63].
SB = {xi ∈CB | ∃xj ∈CA, d(xi, xj) ≤d(xi, xk), ∀xk ∈CB}
(1)
SB represents the subset of benign class examples, CB represents all examples in benign
class, CA represents the set of examples in attack class, d(xi, xj) represents the Euclidean
distance between data points xi and xj, and k = 3 represents the number of nearest neighbors
to be selected from the benign class. This formula calculates the distance of each data point
xi in the benign class to the points xj in the attack class. It then performs the downsampling
process by selecting the benign instances close to the k = 3 nearest attack class instances.

Appl. Sci. 2025, 15, 1252
12 of 25
The attack types in the train and test sections of the NSL-KDD dataset are different.
This can complicate evaluating the overall performance of models for multi-class classifica-
tion and limit the model’s ability to recognize different attack types. Therefore, the attack
types are grouped appropriately in multi-class classification scenarios for more consistent
comparison and analysis. In the NSL-KDD dataset, train and test data are grouped as “nor-
mal”, “Dos”, “R2L”, “Probing”, and “U2R” for multi-class classification. Table 5 presents
the details of these groups for train and test data. Additionally, only numeric features
of NSL-KDD were selected in the training and testing phase for binary and multi-class
classification. Feature selection for the CIC-IDS2017 dataset was performed according to
the importance weights given by the Random Forest (RF) algorithm. The “Fwd Packet
Length Max”,“Fwd Packet Length Std”, “Fwd Packet Length Mean”, and “Bwd Packet
Length Std” properties were used for binary and multi-class classification.
3.3. Attack Detection Framework
Transformer-based attack detection models proposed in previous studies have focused
on attention mechanisms and hybrid models [34]. FPE–Transformer takes a different path
from these approaches by offering an innovative feature position encoder module. As seen
in Figure 1, the FPE–Transformer model consists of feature positional encoding, encoder,
pooling, and classification head layers.
Figure 1. FPE–Transformer.

Appl. Sci. 2025, 15, 1252
13 of 25
Positional encoding adds the positional information of the input data as a fixed vector
of size dmodel through the sin and cos functions and is calculated as in Equation (2) [15].
PE(pos,2i) = sin

pos
10000
2i
dmodel
!
PE(pos,2i+1) = cos

pos
10000
2i
dmodel
!
(2)
The variable pos represents a word’s position within the text string, which varies
between 0 and the maximum string length. dmodel is the vector dimension in which each
word is expressed. i represents the index in the dmodel vector. Sin and cos functions have
complementary properties, allowing the model to distinguish between words in different
positions. The vector matrices’ indexes are expressed as 2i to clarify this distinction.
Thus, sin and cos waves become more distinguishable. The sin and cos functions have
a phase difference. The sin function starts from zero and continues increasing. The cos
function starts from a maximum and decreases. This phase difference differentiates the
i in even and odd positions. Periodicity in the sin and cos functions helps the model
learn positional information even in long sequences. 10000
2i
dmodel controls the frequency of
positional encoding and creates a different frequency scale for each dimension. Notations
of Equation (2) are as in Table 6.
Table 6. Notations of Equation (2).
Notations
Description
pos
Position index in the sequence.
2i
Index used for positional encoding matrix.
dmodel
Dimensionality of the positional encoding matrix.
PE(pos,2i)
It refers to the even-numbered indices of the positional encoding matrices
in the dimension dmodel.
PE(pos,2i+1)
It refers to the odd-numbered indices of the positional encoding matrices
in the dimension dmodel.
In summary, positional encoding represents the sequential relationships between
words in text data with sin and cos functions. Thus, it better captures semantic structures
and grammatical relationships. Liu and Wu [58] suggested that in tasks based on numerical
features, such as attack detection, using positional information could disrupt the intrinsic
structure of the data due to the independence of the features, potentially negatively impact-
ing the model’s performance. For this reason, the authors updated the positional encoding
method used in text data as in Equation (3) for numerical data.
PE(pos,2i) = sin

1
10000
2i
dmodel
!
PE(pos,2i+1) = cos

1
10000
2i
dmodel
!
(3)
This method aims to capture sequential information in numerical data more accurately
using only the features’ positional indices (i). However, a fixed positional encoding is
applied to each feature and does not consider the unique timing patterns that different
features may exhibit. Temporal pattern refers to the changes or frequency of information
that features in a dataset show over time.

Appl. Sci. 2025, 15, 1252
14 of 25
In multi-feature datasets, the timing of each feature and the relationships between
these features play a critical role in the model’s learning process [64]. For example, one
feature might exhibit rapid changes, while another might display periodic fluctuations
over time. Figure 2 analyzes a subset of the NSL-KDD dataset, revealing that the src_bytes
feature exhibits rapid changes, while the same_srv_rate feature displays periodic behavior
from 0 to 1.
Figure 2. Feature analysis of a subset of the NSL-KDD dataset, showing rapid changes in src_bytes
and periodic behavior in same_srv_rate.
Similarly, Figure 3 analyzes a subset of the CIC-IDS2017 dataset, revealing that the
Fwd Packet Length Max feature exhibits rapid changes, while the Flow AIT Std feature
exhibits periodic behavior from 0 to 4.
Encoding these differences allows the model to correctly capture the context of each
feature. Without considering timing patterns, applying the same positional encoding to all
features can lead to the loss of critical temporal relationships within the data.

Appl. Sci. 2025, 15, 1252
15 of 25
Figure 3. Feature analysis of a subset of the CIC-IDS2017 dataset, showing rapid changes in Fwd
Packet Length Max and periodic behavior in Flow AIT Std.
Our feature positional encoding removes the temporal pattern problem by inde-
pendently computing positional encodings for each feature and capturing its temporal
dynamics. To capture the temporal dynamics of each feature f, div_term f is used and
calculated as in Equation (4).
div_termf = exp

−log10 10000
dmodel
× 2i

(4)
The dmodel feature determines the size of positional encoding matrices and represents
the matrix index i. The number of div_termf is set to be the same as the number of features.
log10 10000 is used for scaling purposes in feature positional encoding. The natural expo-
nential function (exp) converts a negative value to a positive one, ensuring the resulting
value is always positive. Negative values can negatively affect the learning process of
the model in deep learning and optimization processes. Using positive values allows the
model to learn faster and more stably. Linear functions preserve the linear effects of the
data and are often suitable for simpler problems. However, changes in time series data are
often non-linear. Linear functions do not always provide accurate modeling of continuous
changes, and transitions are often irregular and sharp. Ref. [65] explains different transfor-
mation methods in time series analysis and shows how exponential functions provide more
effective results. The study provides experimental results supporting the effectiveness of
exponential functions in better modeling continuously changing data compared to other

Appl. Sci. 2025, 15, 1252
16 of 25
methods, such as linear functions. In time series data, the exponential function empha-
sizes the effect of time-varying data. Exponential functions provide smoother transitions
between data because they change continuously and smoothly, which can help the model
generalize better. Positional encoding PEf in the div_term f determined for each feature f
is calculated as in Equation (5).
PEf (pos, 2i) = sin(pos × div_termf )
PEf (pos, 2i + 1) = cos(pos × div_termf )
(5)
Here, a separate positional encoding is calculated for each feature. Pos represents
the time steps within each feature. Feature positional encoding calculates positional
information for each feature independently, allowing the model to learn the order and
context of each feature over time separately. The proposed method provides a significant
advantage when working with multi-feature data, where different features may exhibit
different timing patterns. Figure 4 visualizes the difference between feature positional
encoding and positional encoding methods customized for numeric data.
Figure 4. Feature positional encoding vs. uniform positional encoding.
An encoder is a critical component for the model to process and encode the input data
meaningfully. Input data enriched with feature positional encoding are processed in the
encoder using three essential substructures: MHA, feed-forward network, and add&norm.
MHA divides an input feature into parts called heads and performs attention calculations
for each head separately. The outputs of these heads are combined to obtain a final output.
The scale dot product is calculated for each head as in Equation (6).
Attention(Q, K, V) = softmax
 QKT
√dmodel

V
(6)
Here, Q, K, and V are vectors that calculate the attention weights obtained for each
feature. Q (Query) represents the query vector for the feature the relevant head represents.
This is used to emphasize which information is important. Key (K) represents the funda-
mental keys related to the feature the relevant head represents. Value (V) represents the
actual information values carried by the feature. A multiplication operation is performed
between the vectors Q and K, and each query vector’s relationship to the corresponding
key vectors is calculated. The multiplication result is divided by √dmodel to scale the large
values that can result from large matrix multiplications. Softmax ensures each feature
focuses on a specific value, ensuring their sum is one and obtaining attention weights.
The resulting attention weights are multiplied by the V (Value) vectors. This determines

Appl. Sci. 2025, 15, 1252
17 of 25
which information the model should pay more attention to. The results obtained from each
head are combined as in Equation (7) and then passed through a linear layer. The MHA
mechanism is visualized in Figure 5.
Multi-head Attention(Q, K, V) = Concat(head1, . . . , headn)WQ
headi = Attention(QWQ
i , KWK
i , VWV
i )
(7)
Figure 5. Multi-head attention mechanism.
The MHA mechanism identifies important features in attack detection tasks and
learns the interactions between these features. Therefore, it enables the simultaneous
capture of various input elements representing different types of cyberattacks. For
example, although the number of bytes is critical in a DoS attack, key certificate details
can be more decisive in ransomware attacks. By learning these contextual differences,
MHA increases its capacity to identify and classify different types of attacks. These
features make the MHA mechanism an effective tool for attack detection. Therefore,
various deep learning layers have been combined with the MHA mechanism, and
powerful hybrid models have been created for attack detection [38,40,41]. In addition,
the experimental results obtained with our FPE–Transformer model incorporating the
MHA mechanism on the CIC-IDS2017 and NSL-KDD datasets demonstrate that the
MHA mechanism suits the attack detection task.
The Add & Norm layer performs the normalization operations by adding the atten-
tion weights resulting from MHA to the input data. Normalization is calculated as in
Equation (8).
ˆxi =
xi −µ
√
σ2 + ϵ
(8)
Here, xi represents the ith input, µ represent the mean value, and σ represents the
variance. The feed-forward function is used for forward passing of the encoder layer.
Classification head contains one or more fully connected layers and uses learnable
weights to summarize better and classify the information in the encoder’s final output.
The encoder output is passed through one or more linear layers to extract higher-level
features. Finally, softmax is applied to these outputs to perform the final classification. This
approach allows the encoder output to gain deeper meaning.
The classification head allows the model to learn more complex features by adding
additional structures (e.g., linear layers and activation functions). Using activation functions
such as ReLu with linear layers supports the model’s learning of non-linear relationships.

Appl. Sci. 2025, 15, 1252
18 of 25
Applying softmax directly to the encoder output instead of the classification head is a
sufficient approach for simple classification. However, this method may limit the model’s
ability to learn complex features. FPE–Transformer’s ClassificationHead allows the model
to generalize to more complex data, producing more effective and meaningful classification
results. Additionally, normalization layers within ClassificationHead facilitate the learning
process by increasing the modeling stability.
4. Results
This section evaluates the FPE–Transformer model using the CIC-IDS2017 and NSL-
KDD datasets.
The experiments were conducted in the Google Colab environment,
equipped with a 2.9 GHz CPU, 12.68 GB of RAM, and 107.72 GB of disk space. Python
version 3.10.12 and the PyTorch framework were utilized throughout the experimenta-
tion process. Accuracy and loss were employed as the primary evaluation metrics, with
accuracy calculated as described in Equation (9).
Accuracy =
TP + TN
TP + TN + FP + FN
(9)
True Positive (TP) refers to attack data the model predicts as an attack. True Negative
(TN) refers to the benign data the model predicts as benign. False Positive (FP) refers
to benign data that are predicted as an attack. False Negative (FN) refers to the benign
prediction of attack data. Binary cross entropy loss is used as the loss function, as in
Equation (10).
Loss = −1
N
N
∑
i=1
h
yi log(yˆ
i) + (1 −yi) log(1 −yˆ
i)
i
(10)
N refers total sample numbers, yi represents the true label of the ith sample, and yˆ
i
represents the probability that the model predicts for the ith sample. The formula calculates
the logarithmic loss between the true label and the predicted probability for each example
and then averages these losses across all examples. This measures how close the model’s
predictions are to the true values, allowing the model to be guided to improve accuracy.
The experiments were conducted systematically to evaluate the effectiveness of dif-
ferent positional encoding methods on the CIC-IDS2017 and NSL-KDD datasets. For the
NSL-KDD dataset, three positional encoding techniques—original positional encoding
(PE) [15], uniform positional encoding (UPE) [58], and the proposed feature positional
encoding (FPE)—were compared under two classification tasks: binary classification and
multi-class classification. Similarly, for the CIC-IDS2017 dataset, the same three positional
encoding methods were tested across binary and multi-class classification scenarios. The
hyperparameters of all Transformer models with FPE, UPE, and PE were set in the same
way to produce comparable results. The models had one encoder layer (n_layer = 1) and
two attention heads (n_head = 2). To prevent over-learning, the dropout rate was set to
10% (drop_prob = 0.1), and training was performed with a batch size of 100 samples each
time (batch_size = 100). The number of epochs was set to 20. The Adam optimizer was
employed as the optimization function, configuring the learning rate to 0.001.
The comparison of NSL-KDD binary classification test accuracy and loss values for all
three positional encodings is shown in Figure 6. The red line represents FPE, the blue line
represents UPE, and the green line represents PE.

Appl. Sci. 2025, 15, 1252
19 of 25
Figure 6. The comparison of NSL-KDD binary classification test accuracy and loss values. (a) Loss
value comparison for FPE, UPE, and PE in binary classification. (b) Accuracy value comparison for
FPE, UPE, and PE in binary classification.
The comparison of NSL-KDD binary classification test accuracy and loss values for all
three positional encodings is shown in Table 7.
Table 7. NSL-KDD test accuracy and loss values for FPE, UPE, and PE in binary classification.
Positional Encoder Type
Accuracy
Loss
FPE
0.899
0.35
UPE
0.873
0.42
PE
0.870
0.46
FPE performed better than other positional encodings in the binary classification task
performed on the NSL-KDD dataset. The comparison of CIC-IDS2017 binary classification
test accuracy and loss values for all three positional encodings is shown in Figure 7. The
red line represents FPE, the blue line represents UPE, and the green line represents PE.
Figure 7. The comparison of CIC-IDS2017 binary classification test accuracy and loss values. (a) Loss
value comparison for FPE, UPE, and PE in binary classification. (b) Accuracy value comparison FPE,
UPE, and PE in binary classification.
The comparison of CIC-IDS-2017 binary classification test accuracy and loss values for
all three positional encodings is shown in Table 8.

Appl. Sci. 2025, 15, 1252
20 of 25
Table 8. CIC-IDS2017 test accuracy and loss values for FPE, UPE, and PE in binary classification.
Positional Encoder Type
Accuracy
Loss
FPE
0.917
0.18
UPE
0.876
0.19
PE
0.871
0.20
FPE performed better than other positional encodings in the binary classification
task performed on the CIC-IDS2017 dataset. The comparison of NSL-KDD multi-class
classification test accuracy and loss values for all three positional encodings is shown in
Figure 8. The red line represents FPE, the blue line represents UPE, and the green line
represents PE.
Figure 8. The comparison of NSL-KDD multi-class classification test accuracy and loss values. (a) Loss
value comparison for FPE, UPE, and PE in multi-class classification. (b) Accuracy value comparison
FPE, UPE, and PE in multi-class classification.
The comparison of NSL-KDD multi-class classification test accuracy and loss values
for all three positional encodings is shown in Table 9.
Table 9. NSL-KDD test accuracy and loss values for FPE, UPE, and PE in multi-class classification.
Positional Encoder Type
Accuracy
Loss
FPE
0.773
0.13
UPE
0.757
0.16
PE
0.758
0.15
FPE performed better than other positional encodings in the multi-class classification
task performed on the NSL-KDD dataset. The comparison of multi-class classification on
CIC-IDS2017 dataset for all three positional encodings is shown in Figure 9. The red line
represents FPE, the blue line represents UPE, and the green line represents PE.
The comparison of CIC-IDS2017 multi-class classification test accuracy and loss values
for all three positional encodings is shown in Table 10.
Table 10. CIC-IDS2017 test accuracy and loss values for FPE, UPE, and PE in multi-class classification.
Positional Encoder Type
Accuracy
Loss
FPE
0.906
0.26
UPE
0.865
0.29
PE
0.864
0.29

Appl. Sci. 2025, 15, 1252
21 of 25
Figure 9. The comparison of CIC-IDS2017 multi-class classification test accuracy and loss values.
(a) Loss value comparison for FPE, UPE, and PE in multi-class classification. (b) Accuracy value
comparison FPE, UPE, and PE in multi-class classification.
FPE performed better than other positional encodings in the multi-class classification
task performed on the CIC-IDS2017 dataset.
Experimental results show that FPE achieved higher accuracy and lower loss values
than other positional encoding methods on the CIC-IDS2017 and NSL-KDD datasets. In
binary classification, FPE can precisely learn simple patterns in the dataset. In addition,
relationships between complex classes can be effectively modeled in multi-class classifi-
cation. This is an indication of the capacity of FPE to capture contextual information. By
incorporating positional information specific to each feature into the model, FPE provides
a sensitive representation according to different data features. This was especially effective
in learning subtle differences between classes in multi-class classification in the NSL-KDD
dataset. FPE effectively encoded relationships between features or in different periods,
enabling attacks to be detected correctly. FPE produced lower loss values compared to
other methods, showing that the model was more effective in the optimization process
and performed more stable learning. Although UPE used uniformly distributed positional
information, it was less effective than FPE in modeling contextual relationships. This
became especially evident in multi-class classification. Although PE was designed for time
series and sequential data, it was not as effective as FPE in distinguishing differences at
the feature level. The fact that FPE achieves higher accuracy and lower loss values reveals
the importance of optimizing positional coding in a data-driven manner. These findings
show that FPE provides a reliable solution for critical tasks such as intrusion detection and
outperforms other methods with lower data loss and better contextual learning capacity.
5. Conclusions
This paper presents a novel Transformer-based attack detection framework. While
existing Transformer-based models used for attack detection generally focus on hybrid
structures and attention mechanisms, the FPE–Transformer model differs from these models
with a feature-based feature positional encoding and ClassificationHead structure.
This study used the known NSL-KDD and CIC-IDS2017 datasets to validate the
FPE–Transformer model. Binary and multi-class classification were performed with these
datasets, and the results of Transformer models with FPE, UPE, and PE were compared.
Experimental results show that FPE–Transformer provides higher accuracy than Trans-
former models with other positional encoding methods in various attack types. The feature
positional encoding in the FPE–Transformer model offers the advantages of feature-based
customization, better generalization ability, and computational efficiency. Using separate
positional encoding matrices for each feature, the model can independently learn each

Appl. Sci. 2025, 15, 1252
22 of 25
feature’s order and timing. This is a great advantage, especially in cases where different
features have different timing or ordering patterns, such as multi-feature time series. In
scenarios where different features may exhibit different contextual relationships or timing
patterns, applying positional encoding specific to each feature allows the model to learn
better and generalize these differences, resulting in more accurate results, especially in mul-
tivariate datasets. In addition, ClassificationHead in FPE–Transformer allows the model
to learn complex features by adding additional configurations such as linear layers and
activation functions, thus producing effective and meaningful classification results.
Future studies aim to adapt the FPE–Transformer model to robotic applications and
develop it to support the integration of information from multiple data sources. FPE–
Transformer can learn timing and contextual relationships specific to each data source
with its feature-based positional encoding approach. Developing this model with multi-
source data sources can provide higher accuracy and flexibility in attack detection and
robotic systems’ security. Additionally, the MHA mechanism can be optimized to make
it more effective for attack detection. This mechanism can customize headers to model
attack-specific behavior and, more precisely, analyze threat scenarios’ different features. For
example, the attention mechanism can be strengthened to distinguish anomalies over time
to detect anomalous data patterns earlier and more accurately. In addition, the dynamic
structures of current threats can be better understood with the information learned from
past attack patterns, which can increase the adaptability and accuracy of the model.
Author Contributions: Conceptualization and methodology, H.Ç.Z. and E.N.Y.; software, H.Ç.Z.;
validation, formal analysis, and investigation, H.Ç.Z. and E.N.Y.; data curation and writing—original
draft, H.Ç.Z.; writing—review and editing, E.N.Y.; visualization, H.Ç.Z.; supervision, E.N.Y. All
authors have read and agreed to the published version of the manuscript.
Funding: This research received no external funding.
Institutional Review Board Statement: Not applicable.
Informed Consent Statement: Not applicable.
Data Availability Statement: Publicly available datasets were analyzed in this study. The NSL-
KDD dataset can be accessed here: https://web.archive.org/web/20150205070216/http://nsl.cs.
unb.ca/NSL-KDD/, accessed on 16 December 2024 and the CIC-IDS2017 dataset can be accessed
here: https://www.unb.ca/cic/datasets/ids-2017.html, accessed on 16 December 2024.
Acknowledgments: Hande ÇAV¸S˙I ZA˙IM, one of the authors of this article, is supported by the
Council of Higher Education of the Republic of Turkey, 100/2000 PhD scholarship in Advanced
Robotic Systems and Mechatronics. The authors would also like to express their gratitude to the
editors and reviewers for their valuable comments that improved the quality of this paper.
Conflicts of Interest: The authors declare no conflicts of interest.
References
1.
Zhang, J.; Pan, L.; Han, Q.L.; Chen, C.; Wen, S.; Xiang, Y. Deep learning based attack detection for cyber-physical system
cybersecurity: A survey. IEEE/CAA J. Autom. Sin. 2021, 9, 377–391. [CrossRef]
2.
Liu, H.; Lang, B. Machine learning and deep learning methods for intrusion detection systems: A survey. Appl. Sci. 2019, 9, 4396.
[CrossRef]
3.
Khan, Z.; Chowdhury, M.; Islam, M.; Huang, C.Y.; Rahman, M. Long short-term memory neural network-based attack detection
model for in-vehicle network security. IEEE Sens. Lett. 2020, 4, 1–4. [CrossRef]
4.
Zhao, Y.; Jia, X.; An, D.; Yang, Q. LSTM-Based false data injection attack detection in smart grids. In Proceedings of the 35th
Youth Academic Annual Conference of Chinese Association of Automation (YAC), Virtual Conference, China, 24–26 October
2020; pp. 638–644.
5.
Muhuri, P.S.; Chatterjee, P.; Yuan, X.; Roy, K.; Esterline, A. Using a long short-term memory recurrent neural network (LSTM-RNN)
to classify network attacks. Information 2020, 11, 243. [CrossRef]

Appl. Sci. 2025, 15, 1252
23 of 25
6.
Hwang, R.H.; Peng, M.C.; Nguyen, V.L.; Chang, Y.L. An LSTM-based deep learning approach for classifying malicious traffic at
the packet level. Appl. Sci. 2019, 9, 3414. [CrossRef]
7.
Alkahtani, H.; Aldhyani, T.H. Botnet Attack Detection by Using CNN-LSTM Model for Internet of Things Applications. Secur.
Commun. Netw. 2021, 2021, 3806459. [CrossRef]
8.
Cao, B.; Li, C.; Song, Y.; Qin, Y.; Chen, C. Network intrusion detection model based on CNN and GRU. Appl. Sci. 2022, 12, 4184.
[CrossRef]
9.
Zainel, H.; Koçak, C. LAN intrusion detection using convolutional neural networks. Appl. Sci. 2022, 12, 6645. [CrossRef]
10.
Wang, X.; Liu, J.; Zhang, C. Network intrusion detection based on multi-domain data and ensemble-bidirectional LSTM. EURASIP
J. Inf. Secur. 2023, 2023, 5. [CrossRef]
11.
Liao, D.; Huang, S.; Tan, Y.; Bai, G. Network intrusion detection method based on gan model. In Proceedings of the 2020
International Conference on Computer Communication and Network Security (CCNS), Guilin, China, 21–23 August 2020;
pp. 153–156.
12.
Rahali, A.; Akhloufi, M.A. End-to-end transformer-based models in textual-based NLP. AI 2023, 4, 54–110. [CrossRef]
13.
An, H.; Ma, R.; Yan, Y.; Chen, T.; Zhao, Y.; Li, P.; Lv, C. Finsformer: A Novel Approach to Detecting Financial Attacks Using
Transformer and Cluster-Attention. Appl. Sci. 2024, 14, 460. [CrossRef]
14.
Chen, C.; Song, Y.; Yue, S.; Xu, X.; Zhou, L.; Lv, Q.; Yang, L. Fcnn-se: An intrusion detection model based on a fusion CNN and
stacked ensemble. Appl. Sci. 2022, 12, 8601. [CrossRef]
15.
Vaswani, A.; Shazeer, N.; Parmar, N.; Uszkoreit, J.; Jones, L.; Gomez, A.N.; Kaiser, L.; Polosukhin, I. Attention is all you need. Adv.
Neural Inf. Process. Syst. 2017, 30.
16.
Li, Z.; Gao, Z.; Tan, C.; Ren, B.; Yang, L.T.; Li, S.Z. General Point Model Pretraining with Autoencoding and Autoregressive. In
Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, Seattle, WA, USA, 16–22 June 2024;
pp. 20954–20964.
17.
Kenton, J.D.M.W.C.; Toutanova, L.K. Bert: Pre-training of deep bidirectional transformers for language understanding. In
Proceedings of the NAACL-HLT, Minneapolis, MN, USA, 2–7 June 2019; Volume 1, p. 2.
18.
Radford, A. Improving Language Understanding by Generative Pre-Training; Technical Report; OpenAI: San Francisco, CA, USA, 2018.
19.
Lee, J.; Yoon, W.; Kim, S.; Kim, D.; Kim, S.; So, C.H.; Kang, J. BioBERT: A pre-trained biomedical language representation model
for biomedical text mining. Bioinformatics 2020, 36, 1234–1240. [CrossRef]
20.
Briskilal, J.; Subalalitha, C.N. An ensemble model for classifying idioms and literal texts using BERT and RoBERTa. Inf. Process.
Manag. 2022, 59, 102756. [CrossRef]
21.
Lan, Z.Z.; Chen, M.D.; Goodman, S.; Gimpel, K.; Sharma, P.; Soricut, R. ALBERT: A lite BERT for self-supervised learning
of language representations. In Proceedings of the 8th International Conference on Learning Representations, Addis Ababa,
Ethiopia, 26–30 April 2020.
22.
Khan, P.I.; Razzak, I.; Dengel, A.; Ahmed, S. Performance comparison of transformer-based models on twitter health mention
classification. IEEE Trans. Comput. Soc. Syst. 2022, 10, 1140–1149. [CrossRef]
23.
He, P.; Liu, X.; Gao, J.; Chen, W. DeBERTa: Decoding-enhanced BERT with disentangled attention. arXiv 2020, arXiv:2006.03654.
24.
Clark, K. Electra: Pre-training text encoders as discriminators rather than generators. arXiv 2020, arXiv:2003.10555.
25.
Radford, A.; Wu, J.; Child, R.; Luan, D.; Amodei, D.; Sutskever, I. Language models are unsupervised multitask learners. OpenAI
Blog 2019, 1, 9.
26.
Wang, B.; Chen, W.; Pei, H.; Xie, C.; Kang, M.; Zhang, C.; Li, B. DecodingTrust: A Comprehensive Assessment of Trustworthiness
in GPT Models. In Proceedings of the NeurIPS, New Orleans, LA, USA, 12–14 December 2023.
27.
Raffel, C.; Shazeer, N.; Roberts, A.; Lee, K.; Narang, S.; Matena, M.; Liu, P.J. Exploring the limits of transfer learning with a unified
text-to-text transformer. J. Mach. Learn. Res. 2020, 21, 1–67.
28.
Khashabi, D.; Min, S.; Khot, T.; Sabharwal, A.; Tafjord, O.; Clark, P.; Hajishirzi, H. Electra: Unifiedqa: Crossing format boundaries
with a single qa system. arXiv 2020, arXiv:2005.00700.
29.
Wang, Y.; Wang, W.; Joty, S.; Hoi, S.C. Codet5: Identifier-aware unified pre-trained encoder-decoder models for code understand-
ing and generation. arXiv 2021, arXiv:2109.00859.
30.
Lewis, M.C. Bart: Denoising sequence-to-sequence pre-training for natural language generation, translation, and comprehension.
arXiv 2019, arXiv:1910.13461.
31.
Liu, Y. Multilingual denoising pre-training for neural machine translation. arXiv 2020, arXiv:2001.08210. [CrossRef]
32.
Ahmad, W.U.; Chakraborty, S.; Ray, B.; Chang, K.W. Unified pre-training for program understanding and generation. arXiv 2021,
arXiv:2103.06333.
33.
Chouikhi, H.; Jarray, F.; Alsuhaibani, M. ICAART; Science and Technology Publications, Ltd.: Setúbal, Portugal, 2023; pp. 117–123.
34.
Kheddar, H. Transformers and Large Language Models for Efficient Intrusion Detection Systems: A Comprehensive Survey.
arXiv 2024, arXiv:2408.07583.

Appl. Sci. 2025, 15, 1252
24 of 25
35.
Nam, M.; Park, S.; Kim, D.S. Intrusion detection method using bi-directional GPT for in-vehicle controller area networks. IEEE
Access 2021, 9, 124931–124944.
36.
Hsiao, W.C.; Wang, C.H. Detection of SQL Injection and Cross-Site Scripting Based on Multi-Model CNN Combined with
Bidirectional GRU and Multi-Head Self-Attention. In Proceedings of the 2023 5th International Conference on Computer
Communication and the Internet (ICCCI), Fujisawa, Japan, 23–25 June 2023; pp. 142–150.
37.
Barut, O.; Luo, Y.; Li, P.; Zhang, T. R1dit: Privacy-preserving malware traffic classification with attention-based neural networks.
IEEE Trans. Netw. Serv. Manag. 2022, 20, 2071–2085. [CrossRef]
38.
Nguyen, T.P.; Nam, H.; Kim, D. Transformer-based attention network for in-vehicle intrusion detection. IEEE Access 2023, 11,
55389–55403. [CrossRef]
39.
Dang, Q.V. Using Transformer Technique for Intrusion Detection. In Proceedings of the International Conference on Future Data
and Security Engineering, Singapore, 22–24 November 2023; pp. 184–196.
40.
Lan, Y.; Truong Huu, T.; Wu, J.; Teo, S.G. Cascaded multi-class network intrusion detection with decision tree and self-attentive
model. In Proceedings of the 2022 IEEE International Conference on Data Mining Workshops (ICDMW), Orlando, FL, USA,
28 November–1 December 2022; pp. 1–7.
41.
Ahmed, S.W.; Kientz, F.; Kashef, R. A modified transformer neural network (MTNN) for robust intrusion detection in IoT
networks. In Proceedings of the 2023 International Telecommunications Conference (ITC-Egypt), Alexandria, Egypt, 18–20 July
2023; pp. 663–668.
42.
Hou, H.; Liang, D.; Zhang, M. Yuan, D.A Densely Stacked Attention Method for Cyberattack Detection. J. Inf. Sci. Eng. 2023,
39, 935. [CrossRef]
43.
Yao, R.; Wang, N.; Chen, P.; Ma, D.; Sheng, X. Yuan, D. A CNN-transformer hybrid approach for an intrusion detection system in
advanced metering infrastructure. Multimed. Tools Appl. 2023, 82, 19463–19486. [CrossRef]
44.
He, G.; Lu, Q.; Yin, G.; Xiong, H. Network intrusion detection based on hybrid neural network. In Proceedings of the International
Conference on Wireless Algorithms, Systems, and Applications, Dalian, China, 24–26 November 2022; pp. 644–655.
45.
Lopes, I.O.; Zou, D.; Abdulqadder, I.H.; Akbar, S.; Li, Z.; Ruambo, F.; Pereira, W. Network intrusion detection based on the
temporal convolutional model. Comput. Secur. 2023, 135, 103465. [CrossRef]
46.
Wang, H.; Li, W. DDosTC: A transformer-based network attack detection hybrid mechanism in SDN. Sensors 2021, 21, 5047.
[CrossRef]
47.
Baul, A.; Sarker, G.C.; Sadhu, P.K.; Yanambaka, V.P.; Abdelgawad, A. XTM: A novel transformer and LSTM-based model for
detection and localization of formally verified fdi attack in smart grid. Electronics 2023, 12, 797. [CrossRef]
48.
Ding, Z.; Zhong, G.; Qin, X.; Li, Q.; Fan, Z.; Deng, Z.; Xiang, W. MF-Net: Multi-frequency intrusion detection network for Internet
traffic data. Pattern Recognit. 2024, 146, 109999. [CrossRef]
49.
Rehman, M.U.; Nizami, I.F.; Ullah, F.; Hussain, I. IQA Vision Transformed: A Survey of Transformer Architectures in Perceptual
Image Quality Assessment. IEEE Access 2024, 12, 183369–183393. [CrossRef]
50.
Li, M.; Han, D.; Li, D.; Liu, H.; Chang, C.C. MFVT: An anomaly traffic detection method merging feature fusion network and
vision transformer architecture. EURASIP J. Wirel. Commun. Netw. 2022, 2022, 39. [CrossRef]
51.
Ho, C.M.K.; Yow, K.C.; Zhu, Z.; Aravamuthan, S. Network intrusion detection via flow-to-image conversion and vision
transformer classification. IEEE Access 2022, 10, 97780–97793. [CrossRef]
52.
Agrafiotis, G.; Makri, E.; Flionis, I.; Lalas, A.; Votis, K.; Tzovaras, D. Image-based neural network models for malware traffic
classification using pcap to picture conversion. In Proceedings of the 17th International Conference on Availability, Reliability
and Security, Vienna, Austria, 23–26 August 2022; pp. 1–7.
53.
Li, F.; Shen, H.; Mai, J.; Wang, T.; Dai, Y.; Miao, X. Pre-trained language model-enhanced conditional generative adversarial
networks for intrusion detection. Peer-to-Peer Netw. Appl. 2024, 17, 227–245. [CrossRef]
54.
Wang, Z.; Zhou, J.; Wang, Z.; Hei, X. Research on Network Traffic Anomaly Detection for Class Imbalance. In Proceedings of the
China Intelligent Robotics Annual Conference, Xi’an, China, 16–18 December 2022; pp. 135–144.
55.
Wu, Z.; Zhang, H.; Wang, P.; Sun, Z. RTIDS: A robust transformer-based approach for intrusion detection system. IEEE Access
2022, 10, 64375–64387. [CrossRef]
56.
Seyyar, Y.E.; Yavuz, A.G.; Ünver, H.M. An attack detection framework based on BERT and deep learning. IEEE Access 2022,
10, 68633–68644. [CrossRef]
57.
Ghourabi, A. A security model based on lightgbm and transformer to protect healthcare systems from cyberattacks. IEEE Access
2022, 10, 48890–48903. [CrossRef]
58.
Liu, Y.; Wu, L. Intrusion detection model based on improved transformer. Appl. Sci. 2023, 13, 6251. [CrossRef]
59.
Ullah, F.; Ullah, S.; Srivastava, G.; Lin, J.C.W. IDS-INT: Intrusion detection system using transformer-based transfer learning for
imbalanced network traffic. Digit. Commun. Netw. 2024, 10, 190–204. [CrossRef]

Appl. Sci. 2025, 15, 1252
25 of 25
60.
Sharafaldin, I.; Lashkari, A.H.; Ghorbani, A.A. Toward generating a new intrusion detection dataset and intrusion traffic
characterization. In Proceedings of the 4th International Conference on Information Systems Security and Privacy (ICISSP 2018),
Funchal, Portugal, 22–24 January 2018; pp. 108–116.
61.
Archibe, U.K. NSL Data. 2006. Available online: https://web.archive.org/web/20150205070216/http://nsl.cs.unb.ca/NSL-
KDD/ (accessed on 28 December 2024).
62.
Han, H.; Wang, W.Y.; Mao, B.H. Borderline-SMOTE: A new over-sampling method in imbalanced data sets learning. In Proceed-
ings of the International Conference on Intelligent Computing, Hefei, China, 23–26 August 2005; Springer: Berlin/Heidelberg,
Germany, 2005; pp. 878–887.
63.
Kubat, M.; Matwin, S. Addressing the curse of imbalanced training sets: One-sided selection. In Proceedings of the of the 14th
International Conference on Machine Learning, Nashville, TN, USA, 8–12 July 1997; pp. 179–186.
64.
Batal, I.; Fradkin, D.; Harrison, J.; Moerchen, F.; Hauskrecht, M. Mining recent temporal patterns for event detection in multivariate
time series data. In Proceedings of the 18th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining,
Beijing, China, 12–16 August 2012; pp. 280–288.
65.
Faraway, J.; Chatfield, C. Time series forecasting with neural networks: A comparative study using the air line data. J. R. Stat. Soc.
Ser. C Appl. Stat. 1998, 47, 231–250. [CrossRef]
Disclaimer/Publisher’s Note: The statements, opinions and data contained in all publications are solely those of the individual
author(s) and contributor(s) and not of MDPI and/or the editor(s). MDPI and/or the editor(s) disclaim responsibility for any injury to
people or property resulting from any ideas, methods, instructions or products referred to in the content.