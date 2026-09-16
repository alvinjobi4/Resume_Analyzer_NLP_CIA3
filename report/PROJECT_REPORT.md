<div align="center">

<img src="./christ_logo.png" alt="CHRIST (Deemed to be University) Logo" width="160"/>

# CHRIST (Deemed to be University)
### School of Engineering and Technology
### Department of AI and Data Science Engineering

---

# A PROJECT REPORT ON
# **AI Resume Analyzer**
### *An NLP-Based Intelligent Resume Analysis and Job Matching System*

---

### **Course Details:**
**Subject:** Introduction to Natural Language Processing (AI532P)  
**Degree / Programme:** B.Tech in Artificial Intelligence and Machine Learning  
**Class & Semester:** 5BTAIML (5th Semester)

---

### **Submitted by:**

| Student Name | Register Number |
| :--- | :--- |
| **Alvin Jobi** | **2463005** |
| **Bijil Varghese** | **2463070** |
| **Vivek Vadakan** | **2463076** |
| **Ancil Joseph** | **2463079** |

<br/>

**Academic Year:** 2025 – 2026  
**Bangalore, Karnataka, India**

</div>

<div style="page-break-after: always;"></div>

---

## DECLARATION

We hereby declare that this project report entitled **“AI Resume Analyzer: An NLP-Based Intelligent Resume Analysis and Job Matching System”** submitted to the **Department of AI and Data Science Engineering, School of Engineering and Technology, CHRIST (Deemed to be University), Bangalore**, is a bonafide record of the work carried out by us for the course **Introduction to Natural Language Processing (AI532P)** under the prescribed academic curriculum for the 5th Semester of **B.Tech in Artificial Intelligence and Machine Learning (5BTAIML)** during the academic year **2025 – 2026**.

We further declare that the work reported herein does not duplicate any work previously submitted for any degree, diploma, or certificate at this or any other university or academic institution. All classical NLP models, document parsing algorithms, vector similarity calculations, and architectural components have been developed, evaluated, and documented authentically.

<br/>

**Place:** Bangalore, Karnataka, India  
**Date:** September 11, 2026

<br/>

**Signatures of the Candidates:**

1. **Alvin Jobi** (Reg. No: 2463005) &nbsp;&nbsp;&nbsp;&nbsp; ____________________
2. **Bijil Varghese** (Reg. No: 2463070) &nbsp;&nbsp;&nbsp;&nbsp; ____________________
3. **Vivek Vadakan** (Reg. No: 2463076) &nbsp;&nbsp;&nbsp;&nbsp; ____________________
4. **Ancil Joseph** (Reg. No: 2463079) &nbsp;&nbsp;&nbsp;&nbsp; ____________________

<div style="page-break-after: always;"></div>

---

## CERTIFICATE

This is to certify that the project report entitled **“AI Resume Analyzer: An NLP-Based Intelligent Resume Analysis and Job Matching System”** submitted by **Alvin Jobi (2463005)**, **Bijil Varghese (2463070)**, **Vivek Vadakan (2463076)**, and **Ancil Joseph (2463079)** in partial fulfillment of the requirements for the course **Introduction to Natural Language Processing (AI532P)** in **B.Tech in Artificial Intelligence and Machine Learning (5th Semester, 5BTAIML)** at **CHRIST (Deemed to be University), Bangalore**, is a genuine record of academic project work completed under faculty supervision.

<br/><br/>

__________________________  
**Course Instructor / Faculty Supervisor**  
Department of AI and Data Science Engineering  
School of Engineering and Technology  
CHRIST (Deemed to be University), Bangalore  

<br/><br/>

__________________________  
**Head of the Department**  
Department of AI and Data Science Engineering  
School of Engineering and Technology  
CHRIST (Deemed to be University), Bangalore  

<div style="page-break-after: always;"></div>

---

## ACKNOWLEDGEMENTS

We express our sincere gratitude and indebtedness to **CHRIST (Deemed to be University), Bangalore**, for providing a world-class academic environment, infrastructure, and computational resources necessary to conceptualize and execute this project.

We convey our heartfelt thanks to the **Dean, School of Engineering and Technology**, and the **Head of the Department of AI and Data Science Engineering**, for their constant encouragement and guidance throughout the semester.

We are deeply grateful to our course instructor for **Introduction to Natural Language Processing (AI532P)** for imparting foundational insights into statistical natural language processing, vector space modeling, Information Retrieval (IR), and morphological analysis, which served as the intellectual foundation for this system.

Finally, we thank our families, peers, and fellow classmates of 5BTAIML for their constructive feedback, collaboration, and continuous support throughout the development and evaluation phases of **AI Resume Analyzer**.

<div style="page-break-after: always;"></div>

---

## ABSTRACT

In modern recruitment ecosystems, candidates face significant challenges in quantitatively evaluating how well their resumes align with competitive, multi-faceted job descriptions. Existing Applicant Tracking Systems (ATS) predominantly suffer from two polar extremes: (1) brittle string-matching rules that fail to recognize domain synonyms (e.g., rejecting an applicant citing *“ML”* when the employer specifies *“Machine Learning”*), or (2) opaque, non-deterministic commercial Large Language Models (LLMs) that hallucinate scores, generate arbitrary advice, and obscure their underlying decision logic.

To address these critical limitations, this project presents **AI Resume Analyzer**, an open, mathematically grounded, and transparent **NLP-Based Intelligent Resume Analysis and Job Matching System**. Developed as an academic laboratory project for **Introduction to Natural Language Processing (AI532P)**, AI Resume Analyzer implements classical and statistical NLP algorithms as the sole core intelligence. The system accepts resume documents in both **Portable Document Format (PDF)** and **Microsoft Word (DOCX)** formats, executing an end-to-end ingestion pipeline comprising layout-aware block extraction, token-safe punctuation shielding (protecting symbols such as `C++`, `C#`, and `.NET`), NLTK sentence/word tokenization, stopword filtering with technical preservation, WordNet/spaCy morphological lemmatization, spaCy Named Entity Recognition (NER), layout heuristic section boundary detection, and taxonomy-based skill extraction with canonical alias mapping.

For job discovery, the system integrates the **RapidAPI JSearch API** strictly to query live real-time job listings from global aggregators. Crucially, in strict adherence to selective information retrieval principles, AI Resume Analyzer does not run indiscriminate matching across all retrieved jobs; rather, it executes deep NLP parsing exclusively on the **single target job** explicitly selected by the user.

Matching is executed using a composite, transparent multi-factor formulation:
$$\text{Overall Match Score} = (0.50 \times \text{TF-IDF Cosine Similarity}) + (0.40 \times \text{Skill Match}) + (0.10 \times \text{Requirement Match})$$

Where Term Frequency–Inverse Document Frequency (TF-IDF) feature vectors with n-grams $(1, 2)$ and sublinear scaling compute directional vector alignment ($\cos\theta$). Personalized recommendations are strictly derived from extracted skill gaps and qualification deltas. Furthermore, AI Resume Analyzer includes an interactive **Academic Viva Inspection Interface** that renders intermediate NLP traces (tokens, lemmas, entity tags, vector dimensions, and dot-product feature contributions). The complete system has been verified through a 16-test automated unit testing suite, real-world document parsings, live API benchmarks, and an interactive Streamlit presentation dashboard.

**Keywords:** *Natural Language Processing (NLP), Information Retrieval, TF-IDF Vectorization, Cosine Similarity, Named Entity Recognition (NER), WordNet Lemmatization, Document Parsing, Resume Parsing, Applicant Tracking Systems.*

<div style="page-break-after: always;"></div>

---

## TABLE OF CONTENTS

1. **Chapter 1: Introduction**
   - 1.1 Background and Motivation
   - 1.2 Problem Statement
   - 1.3 Project Objectives
   - 1.4 Scope and Boundaries
2. **Chapter 2: Literature Review & Theoretical Background**
   - 2.1 Limitations of Rule-Based String Matching
   - 2.2 Vector Space Models & TF-IDF
   - 2.3 Cosine Similarity in High-Dimensional Spaces
   - 2.4 Morphological Lemmatization vs. Stemming
   - 2.5 Named Entity Recognition (NER)
   - 2.6 The Fallacy of Closed Black-Box LLMs in Academic Evaluation
3. **Chapter 3: System Architecture & Design**
   - 3.1 High-Level Architecture
   - 3.2 Selective Analysis Workflow
   - 3.3 Document Ingestion Subsystem (PDF & DOCX)
   - 3.4 Text Cleaning & Technical Token Shielding
   - 3.5 Tokenization, Stopwords & Lemmatization Pipeline
   - 3.6 Named Entity Recognition & Candidate Profile Construction
   - 3.7 Section Boundary Detection Engine
   - 3.8 Curated Skills Taxonomy & Canonical Alias Resolution
   - 3.9 Live Job Ingestion via RapidAPI JSearch
   - 3.10 Selected Job NLP Parsing Subsystem
   - 3.11 Multi-Factor Weighted Scoring Model
   - 3.12 Targeted Gap-Driven Recommendation Engine
4. **Chapter 4: Implementation Details**
   - 4.1 Technology Stack & Python Environment
   - 4.2 Modular Directory Hierarchy
   - 4.3 Document Parsers (`parsers/`)
   - 4.4 NLP Core Modules (`nlp/`)
   - 4.5 External API Integration (`services/`)
   - 4.6 Scoring & Recommendation Engine (`scoring/`)
   - 4.7 User Interface & Presentation Layer (`ui/` & `app.py`)
   - 4.8 Security & Environment Isolation
5. **Chapter 5: Testing, Experimental Results & Viva Verification**
   - 5.1 Automated Unit Test Suite (16 Test Cases)
   - 5.2 Real-World Document Parsing Evaluation
   - 5.3 Live RapidAPI JSearch Benchmark & Latency Mitigation
   - 5.4 Case Study: Machine Learning Engineer Matching
   - 5.5 Academic Viva Transparency Interface
6. **Chapter 6: Conclusion and Future Work**
   - 6.1 Summary of Contributions
   - 6.2 Future Enhancements
7. **References**

<div style="page-break-after: always;"></div>

---

# CHAPTER 1: INTRODUCTION

### 1.1 Background and Motivation
In modern engineering and technology job markets, the initial screening of employment applications is predominantly mediated by automated algorithms. Over 90% of Fortune 500 corporations utilize Applicant Tracking Systems (ATS) to filter, rank, and categorize candidates before human recruiters inspect a resume. However, early-stage job seekers, undergraduate engineering students, and career changers often lack transparent tools to evaluate how closely their curricular background, project portfolio, and technical vocabulary mirror the requirements of target industry positions.

Natural Language Processing (NLP), as a branch of computer science and artificial intelligence, provides mathematically sound techniques to parse unstructured text, identify semantic entities, project documents into high-dimensional vector spaces, and compute directional alignment. Developing an automated, deterministic system that uncovers candidate-job compatibility represents an exemplary application of classical information retrieval and computational linguistics.

### 1.2 Problem Statement
Traditional approaches to automated resume evaluation suffer from severe practical deficiencies:
1. **Brittle Syntactic Matching**: Rudimentary ATS implementations rely on naive substring searching. Under such paradigms, candidate qualifications are penalized due to minor orthographic or alias discrepancies (e.g., an applicant writing *“Scikit-learn”* or *“sklearn”* failing an exact filter for *“scikit learn”*).
2. **Opaque Commercial LLMs**: Many modern commercial tools simply forward resume text to external proprietary Large Language Model APIs (e.g., OpenAI ChatGPT). While conversational, these models operate as non-deterministic black boxes: they hallucinate scores, vary numerical outputs between identical runs, fail to expose underlying vector mathematics, and introduce severe data privacy vulnerabilities by transmitting confidential student resumes to external cloud vendors.
3. **Indiscriminate Computational Waste**: Naive systems attempt to calculate similarity metrics across dozens or hundreds of retrieved job search results simultaneously, exhausting computational resources, exceeding API rate limits, and diluting candidate focus.

### 1.3 Project Objectives
The objective of this project is to architect, implement, and validate **AI Resume Analyzer**, an academic-grade NLP system titled **“NLP-Based Intelligent Resume Analysis and Job Matching System”** for the course **Introduction to Natural Language Processing (AI532P)**.

The explicit technical objectives comprise:
1. **Automated Document Extraction**: Ingest resumes in both PDF and DOCX formats without requiring manual candidate data entry.
2. **Robust Linguistic Preprocessing**: Implement token-safe text cleaning that preserves punctuation-sensitive programming tokens (`C++`, `C#`, `.NET`, `Node.js`), followed by tokenization, stopword removal, and morphological lemmatization.
3. **Structured Candidate Profiling**: Extract Named Entities (`PERSON`, `ORG`, `GPE`, `DATE`) using spaCy, detect resume sections, and build a structured candidate profile.
4. **Live Industry Job Ingestion**: Connect to the **RapidAPI JSearch API** to retrieve live, current employment openings without calculating match scores indiscriminately.
5. **Selective Single-Job Matching**: Allow the candidate to select exactly one target position, executing the NLP pipeline solely on the chosen job description.
6. **Mathematically Deterministic Scoring**: Evaluate directional alignment using TF-IDF vector space modeling and Cosine Similarity, combined with taxonomy-normalized skill matching and requirement evaluation.
7. **Actionable Feedback**: Generate resume enhancement recommendations derived strictly from detected skill gaps and missing qualifications.
8. **Academic Viva Transparency**: Expose an interactive inspector detailing every mathematical and linguistic step (tokens, lemmas, NER tags, vector sizes, feature weights, and dot-product contributions) for evaluator examination.

### 1.4 Scope and Boundaries
* **Core Intelligence**: Exclusively classical and statistical NLP techniques (Tokenization, Lemmatization, spaCy NER, TF-IDF Vectorization, Cosine Similarity, and Rule-Based Extraction).
* **Excluded**: Black-box generative LLM matching APIs, random number generation, and hardcoded static score outputs.
* **Document Formats**: PDF (PyMuPDF) and DOCX (python-docx).
* **API Utilization**: RapidAPI JSearch is utilized **solely** for real-time job retrieval, strictly separated from the scoring engine.

<div style="page-break-after: always;"></div>

---

# CHAPTER 2: LITERATURE REVIEW & THEORETICAL BACKGROUND

### 2.1 Limitations of Rule-Based String Matching
Early automated document filtering systems relied primarily on regular expression pattern matching and boolean keyword queries. While computationally lightweight ($O(N)$ string searches), these methods lack morphological awareness and fail when terms undergo inflection or morphological derivation (e.g., matching *“develop”* against *“developing”*, *“developer”*, or *“developed”*). Furthermore, technical domains are characterized by prolific synonymy (e.g., *“Natural Language Processing”* vs. *“NLP”*, *“PostgreSQL”* vs. *“Postgres”*). Without canonical taxonomy resolution, keyword-matching engines severely disadvantage qualified candidates.

### 2.2 Vector Space Models & TF-IDF
To evaluate document relevance mathematically, Gerard Salton et al. established the **Vector Space Model (VSM)**. Under this framework, unstructured textual documents are projected as high-dimensional vectors in a Euclidean space spanned by orthogonal term features.

The **Term Frequency–Inverse Document Frequency (TF-IDF)** weighting scheme refines simple word counts by balancing local frequency against global specificity:

#### Term Frequency (TF):
In standard Information Retrieval, naive linear term frequency rewards repetitive keyword stuffing. AI Resume Analyzer adopts **sublinear term frequency scaling**:
$$\text{TF}(t, d) = \begin{cases} 1 + \log(\text{count}(t, d)) & \text{if } \text{count}(t, d) > 0 \\ 0 & \text{otherwise} \end{cases}$$

#### Inverse Document Frequency (IDF):
Terms that appear ubiquitously across the corpus provide little discriminative power. The IDF weight downscales common terms:
$$\text{IDF}(t, D) = \log\left(\frac{1 + |D|}{1 + |\{d \in D : t \in d\}|}\right) + 1$$

#### Composite Vector Representation:
$$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$$

For AI Resume Analyzer, vectorization incorporates both unigrams and bigrams ($\text{ngram\_range} = (1, 2)$), capturing contiguous multi-word technical concepts such as *“machine learning”*, *“deep learning”*, and *“data science”*.

### 2.3 Cosine Similarity in High-Dimensional Spaces
Given a resume vector $\mathbf{A} \in \mathbb{R}^V$ and a job description vector $\mathbf{B} \in \mathbb{R}^V$, the system must compute a scalar metric of semantic alignment. Traditional distance metrics such as Euclidean Distance ($L_2$ norm) are fundamentally unsuitable because document length varies drastically: an exhaustive two-page curriculum vitae contains significantly more tokens than a concise job posting, causing Euclidean distance to register large discrepancies even when technical vocabularies coincide.

**Cosine Similarity** circumvents document length disparity by measuring the cosine of the angle $\theta$ between the two normalized vectors:
$$\text{Similarity}(\mathbf{A}, \mathbf{B}) = \cos(\theta) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\|_2 \|\mathbf{B}\|_2} = \frac{\sum_{i=1}^V A_i B_i}{\sqrt{\sum_{i=1}^V A_i^2} \sqrt{\sum_{i=1}^V B_i^2}}$$

Properties of Cosine Similarity:
* Independent of document magnitude.
* Constrained to the interval $[0.0, 1.0]$ for non-negative TF-IDF spaces.
* $\cos(\theta) = 1.0 \implies$ collinear vectors (identical technical focus).
* $\cos(\theta) = 0.0 \implies$ orthogonal vectors (zero shared technical vocabulary).

### 2.4 Morphological Lemmatization vs. Stemming
Stemming algorithms (e.g., Porter or Lancaster stemmers) apply crude heuristic suffix stripping, frequently generating non-words (e.g., *“university”* $\to$ *“univers”*, *“organization”* $\to$ *“organ”*). In contrast, **lemmatization** leverages complete vocabulary dictionaries and morphological analysis to return the legitimate grammatical base form, known as the lemma:
$$\text{developing} \xrightarrow{\text{lemmatize}} \text{develop}, \quad \text{models} \xrightarrow{\text{lemmatize}} \text{model}$$
AI Resume Analyzer utilizes WordNet and spaCy morphological lemmatization, ensuring technical terminology retains semantic integrity.

### 2.5 Named Entity Recognition (NER)
Named Entity Recognition locates and classifies unstructured textual spans into predefined semantic categories. AI Resume Analyzer utilizes spaCy’s statistical transition-based neural network model (`en_core_web_sm`), extracting:
* **`PERSON`**: Candidate identification.
* **`ORG`**: Educational universities, colleges, and previous corporate employers.
* **`GPE`**: Geopolitical entities (cities, states, countries).
* **`DATE`**: Graduation years, employment tenures, and calendar intervals.

### 2.6 The Fallacy of Closed Black-Box LLMs in Academic Evaluation
While modern generative models (e.g., GPT-4) produce fluent text, their employment as the core scoring engine in an academic NLP project constitutes an engineering anti-pattern:
1. **Non-Determinism**: Successive API queries on identical inputs yield varying outputs.
2. **Hallucination Risk**: LLMs invent credentials or miscalculate percentage deltas without mathematical audit trails.
3. **Violates Course Pedagogical Objectives**: Course **AI532P** evaluates students on their mastery of foundational NLP algorithms (tokenization, lemmatization, vector spaces, similarity matrices), which are circumvented by single-line LLM prompts.

<div style="page-break-after: always;"></div>

---

# CHAPTER 3: SYSTEM ARCHITECTURE & DESIGN

### 3.1 High-Level Architecture
AI Resume Analyzer is engineered with strict modular separation across document ingestion, linguistic preprocessing, information extraction, external API retrieval, mathematical scoring, and presentation.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          AI RESUME ANALYZER ARCHITECTURE                    │
└─────────────────────────────────────────────────────────────────────────────┘

    RESUME INGESTION                           LIVE JOB DISCOVERY
┌─────────────────────────┐               ┌───────────────────────────┐
│ PDF / DOCX Resume File  │               │ User Query & Location     │
└───────────┬─────────────┘               └─────────────┬─────────────┘
            │                                           │
            ▼                                           ▼
┌─────────────────────────┐               ┌───────────────────────────┐
│ PyMuPDF / python-docx   │               │ RapidAPI JSearch Client   │
└───────────┬─────────────┘               └─────────────┬─────────────┘
            │                                           │
            ▼                                           ▼
┌─────────────────────────┐               ┌───────────────────────────┐
│ Text Normalization &    │               │ Normalized Job Cards      │
│ Token Shielding (C++)   │               │ (No Indiscriminate Score) │
└───────────┬─────────────┘               └─────────────┬─────────────┘
            │                                           │
            ▼                                           │ [User Selects ONE]
┌─────────────────────────┐                             │
│ Linguistic Pipeline:    │                             ▼
│ Tokenization, Stopwords,│               ┌───────────────────────────┐
│ WordNet Lemmatization   │               │ Selected Job Description  │
└───────────┬─────────────┘               └─────────────┬─────────────┘
            │                                           │
            ▼                                           ▼
┌─────────────────────────┐               ┌───────────────────────────┐
│ spaCy NER & Section     │               │ Job NLP Pipeline:         │
│ Boundary Segmentation   │               │ Tokens, Skills, Exp/Edu   │
└───────────┬─────────────┘               └─────────────┬─────────────┘
            │                                           │
            ▼                                           │
┌─────────────────────────┐                             │
│ Structured Candidate    │                             │
│ Profile & Skills List   │                             │
└───────────┬─────────────┘                             │
            │                                           │
            └───────────────────┬───────────────────────┘
                                │
                                ▼
              ┌──────────────────────────────────┐
              │ MATHEMATICAL MATCHING & SCORING  │
              ├──────────────────────────────────┤
              │ 1. TF-IDF Cosine Similarity (50%)│
              │ 2. Normalized Skill Match  (40%) │
              │ 3. Edu & Exp Verification  (10%) │
              └─────────────────┬────────────────┘
                                │
                                ▼
              ┌──────────────────────────────────┐
              │ STREAMLIT PRESENTATION LAYER     │
              ├──────────────────────────────────┤
              │ • Dynamic Composite Score (0-100)│
              │ • Side-by-Side Matching/Missing  │
              │ • Gap-Driven Recommendations     │
              │ • Academic Viva Inspection Trace │
              └──────────────────────────────────┘
```

### 3.2 Selective Analysis Workflow
In strict accordance with academic guidelines, when RapidAPI JSearch retrieves 10 or 20 job openings, **the system does NOT compute match scores for all jobs**. Indiscriminate computation is wasteful and unrepresentative of genuine candidate behavior. The candidate reviews the job listings and selects **exactly ONE position** by clicking **“Analyze Match”**, triggering the selected-job NLP pipeline.

### 3.3 Document Ingestion Subsystem (PDF & DOCX)
* **PDF Extraction (`parsers/pdf_parser.py`)**: Uses PyMuPDF (`pymupdf`). Rather than dumping unstructured raw text, the parser iterates through layout blocks, sorting them by vertical coordinate $y_0$ followed by horizontal coordinate $x_0$. This preserves natural multi-column reading order.
* **DOCX Extraction (`parsers/docx_parser.py`)**: Uses `python-docx` to extract both continuous paragraph text and nested table cells, deduplicating merged table entries commonly found in modern resume templates.

### 3.4 Text Cleaning & Technical Token Shielding
Standard regex string cleaning frequently destroys vital programming terms containing punctuation. For instance:
* `C++` $\to$ stripped of `+` symbols $\to$ reduced to `C`.
* `C#` $\to$ stripped of `#` symbol $\to$ reduced to `C`.
* `.NET` $\to$ stripped of leading period $\to$ reduced to `NET`.
* `Node.js` $\to$ split into `Node` and `js`.

AI Resume Analyzer solves this via a **Bidirectional Token Protection Engine** ([`nlp/preprocessing.py`](file:///d:/Resume%20Analyzer/nlp/preprocessing.py)):
$$\text{Raw Text} \xrightarrow{\text{Protect}} \text{Intermediate Placeholder} \xrightarrow{\text{Clean \& Tokenize}} \text{Normalized Form} \xrightarrow{\text{Restore}} \text{Canonical Token}$$

```python
PROTECTED_TERMS = {
    "c++": "CPP_TOKEN",
    "c#": "CSHARP_TOKEN",
    ".net": "DOTNET_TOKEN",
    "node.js": "NODEJS_TOKEN",
    "vue.js": "VUEJS_TOKEN",
    "react.js": "REACTJS_TOKEN"
}
```
Non-printable characters, decorative bullet symbols (`•`, `▪`, `►`, `✓`), and redundant whitespace are normalized without altering domain tokens.

### 3.5 Tokenization, Stopwords & Lemmatization Pipeline
1. **Tokenization**: NLTK `word_tokenize` partitions text into words, preserving hyphenated compound identifiers.
2. **Stopword Removal**: NLTK English stopword corpus filters non-discriminative grammar. An explicit exclusion set safeguards programming languages that coincide with stop words or single letters:
   $$\text{Excluded from stopwords} = \{\text{'c'}, \text{'r'}, \text{'go'}, \text{'ai'}, \text{'ml'}, \text{'db'}, \text{'ui'}\}$$
3. **Lemmatization**: Tokens are processed through NLTK’s `WordNetLemmatizer` across both verb (`pos='v'`) and noun (`pos='n'`) syntactic categories to reduce all inflections to canonical dictionary roots.

### 3.6 Named Entity Recognition & Candidate Profile Construction
spaCy’s `en_core_web_sm` model extracts semantic entities:
* **Candidate Name Identification**: A multi-stage heuristic inspects the topmost lines of the document (where candidate names conventionally appear in resume layout standards), validates capitalization, checks against an exclusion dictionary of section keywords (`NON_NAME_TERMS`), and cross-references spaCy `PERSON` tags.
* **Contact Details**: Regex captures RFC 5322 email addresses, international phone numbers, and LinkedIn/GitHub profiles.

### 3.7 Section Boundary Detection Engine
Resumes are structurally segmented into semantic zones using heading regex patterns:
$$\text{Sections} = \{\text{CONTACT}, \text{SUMMARY}, \text{EDUCATION}, \text{SKILLS}, \text{EXPERIENCE}, \text{PROJECTS}, \text{CERTIFICATIONS}\}$$
Headers matching keywords (e.g., *“Work Experience”*, *“Employment History”*, *“Technical Proficiencies”*) serve as division boundaries.

### 3.8 Curated Skills Taxonomy & Canonical Alias Resolution
Technical skills are configured in a structured JSON taxonomy ([`config/skills.json`](file:///d:/Resume%20Analyzer/config/skills.json)) categorized into:
* Programming Languages
* Web Development
* Machine Learning & AI
* Data & Databases
* Cloud & DevOps
* Software Engineering & Tools

#### Canonical Alias Resolution:
To eliminate string discrepancies, aliases are mapped to standard terms:
$$\text{“ml”} \to \text{Machine Learning}, \quad \text{“sklearn”} \to \text{Scikit-learn}, \quad \text{“k8s”} \to \text{Kubernetes}$$
$$\text{“postgres”} \to \text{PostgreSQL}, \quad \text{“js”} \to \text{JavaScript}, \quad \text{“tf”} \to \text{TensorFlow}$$

Boundary checks (`\b` and lookbehinds) guarantee that single letters like `C` do not falsely match substrings within words such as *“Company”* or *“Course”*.

### 3.9 Live Job Ingestion via RapidAPI JSearch
Job discovery connects to RapidAPI JSearch (`https://jsearch.p.rapidapi.com/search-v2`). Authentication credentials are read strictly from `.env` via `python-dotenv`. Returned JSON responses are normalized into a standardized internal schema:
$$\text{Job Record} = \{\text{job\_id}, \text{title}, \text{company}, \text{location}, \text{description}, \text{job\_type}, \text{salary}, \text{date\_posted}, \text{apply\_url}, \text{source}\}$$
Unavailable fields default to *“Not provided”*.

### 3.10 Selected Job NLP Parsing Subsystem
When the candidate selects a job, its unstructured description undergoes:
1. Text normalization and noise removal.
2. Tokenization, stopword filtering, and lemmatization.
3. Skill extraction via the configured skills taxonomy.
4. Experience requirement extraction using numerical range regex patterns (e.g., *“3+ years”*, *“2-5 years of experience”*).
5. Education qualification extraction (Doctorate, Master's, Bachelor's degrees).
6. Key responsibility sentence segmentation.

### 3.11 Multi-Factor Weighted Scoring Model
The system calculates a composite, deterministic match percentage:
$$\text{Overall Score} = (w_{\text{tfidf}} \times S_{\text{tfidf}}) + (w_{\text{skill}} \times S_{\text{skill}}) + (w_{\text{req}} \times S_{\text{req}})$$

Where weights are centrally configured in [`config/settings.py`](file:///d:/Resume%20Analyzer/config/settings.py):
* $w_{\text{tfidf}} = 0.50$ (50% weight on Vector Space Cosine Similarity)
* $w_{\text{skill}} = 0.40$ (40% weight on Normalized Technical Skill Match)
* $w_{\text{req}} = 0.10$ (10% weight on Education & Experience Compliance)

$$\text{Where } S_{\text{skill}} = \left(\frac{|\text{Resume Skills} \cap \text{Job Skills}|}{|\text{Job Skills}|}\right) \times 100$$
$$S_{\text{req}} = \frac{S_{\text{edu}} + S_{\text{exp}}}{2}$$

#### Presentation Categorization:
* **$90\% - 100\%$**: Excellent Match (Emerald `#10b981`)
* **$75\% - 89\%$**: Strong Match (Blue `#3b82f6`)
* **$60\% - 74\%$**: Moderate Match (Amber `#f59e0b`)
* **$40\% - 59\%$**: Weak Match (Orange `#f97316`)
* **$0\% - 39\%$**: Poor Match (Red `#ef4444`)

### 3.12 Targeted Gap-Driven Recommendation Engine
Recommendations are derived deterministically from the set difference:
$$\text{Missing Skills} = \text{Job Skills} \setminus \text{Resume Skills}$$
For each missing skill, the system maps targeted project guidance (e.g., containerizing a model with Docker, writing AWS deployment pipelines, or implementing PyTorch neural network training).

<div style="page-break-after: always;"></div>

---

# CHAPTER 4: IMPLEMENTATION DETAILS

### 4.1 Technology Stack & Python Environment
* **Language**: Python 3.14 / 3.10+
* **Document Parsers**: PyMuPDF (`pymupdf` 1.28.2), `python-docx` (1.2.0)
* **Core NLP & IR**: NLTK (3.10.3), spaCy (3.8.16 with `en_core_web_sm`), Scikit-Learn (1.9.1)
* **User Interface**: Streamlit (1.63.0), Plotly (7.0.0)
* **Data & Networking**: Pandas (3.0.2), Requests (2.33.1), `python-dotenv` (1.2.2)

### 4.2 Modular Directory Hierarchy
```text
Resume Analyzer/
├── app.py                      # Application entrypoint & multi-page router
├── requirements.txt            # Pinned dependency specifications
├── .env                        # Local API secrets (git-ignored)
├── .env.example                # Template configuration
├── .gitignore                  # Excludes .env, cache, and virtualenvs
├── README.md                   # Academic documentation & viva guide
│
├── config/
│   ├── settings.py             # Weights, score tiers, endpoints
│   └── skills.json             # Taxonomy of skills and alias maps
│
├── parsers/
│   ├── pdf_parser.py           # Layout-aware PyMuPDF PDF extraction
│   └── docx_parser.py          # python-docx paragraph/table extraction
│
├── nlp/
│   ├── preprocessing.py        # Token-safe cleaning & contact extraction
│   ├── tokenizer.py            # Word & sentence tokenization
│   ├── lemmatizer.py           # Stopword filtering & WordNet lemmatization
│   ├── ner.py                  # spaCy entity & name recognition
│   ├── section_detector.py     # Heading boundary segmentation
│   ├── skill_extractor.py      # Regex boundary & alias normalization
│   ├── similarity.py           # TF-IDF matrix & Cosine Similarity
│   ├── resume_analyzer.py      # Full resume orchestrator & viva trace
│   └── job_analyzer.py         # Selected job description NLP parser
│
├── services/
│   └── job_api.py              # RapidAPI JSearch client & fallback handler
│
├── scoring/
│   ├── match_score.py          # Multi-factor score calculator
│   └── recommendations.py      # Targeted gap-driven recommendation generator
│
├── ui/
│   ├── styles.py               # Custom CSS design system
│   ├── resume_page.py          # Resume upload & profile display
│   ├── jobs_page.py            # Live job search cards & selector
│   └── analysis_page.py        # Match analytics & viva inspector
│
├── sample_data/
│   ├── sample_resume.txt       # Candidate resume text
│   ├── sample_resume.pdf       # Generated test PDF
│   ├── sample_resume.docx      # Generated test DOCX
│   ├── sample_job.json         # Mock API payload
│   └── create_sample_files.py  # Test file generator script
│
└── tests/
    ├── test_preprocessing.py   # Unit tests for cleaning & tokenization
    ├── test_skill_extraction.py# Unit tests for skill extraction & aliases
    ├── test_similarity.py      # Unit tests for TF-IDF & Cosine Similarity
    ├── test_scoring.py         # Unit tests for weighted scoring formula
    └── test_job_api.py         # Unit tests for API normalization
```

### 4.3 Security & Environment Isolation
In strict compliance with software engineering best practices:
* The RapidAPI key is stored exclusively in `.env` and loaded via `python-dotenv`.
* `.gitignore` explicitly prevents `.env`, Python bytecode (`__pycache__/`), and virtual environments from being committed to source control.
* Sensitive API keys are never exposed in client-side HTML, JavaScript, logs, or public repositories.

<div style="page-break-after: always;"></div>

---

# CHAPTER 5: TESTING, EXPERIMENTAL RESULTS & VIVA VERIFICATION

### 5.1 Automated Unit Test Suite
To verify system integrity, an automated test suite comprising 16 test cases was implemented across 5 test modules in the `tests/` directory:

| Test Module | Component Verified | Test Cases | Status |
| :--- | :--- | :--- | :--- |
| `test_preprocessing.py` | Token-safe punctuation protection, contact extraction, sentence segmentation | 4 | **PASSED** |
| `test_skill_extraction.py` | Canonical skill detection, alias normalization, boundary isolation | 4 | **PASSED** |
| `test_similarity.py` | Identical text collinearity, orthogonal text separation, semantic ranking | 3 | **PASSED** |
| `test_scoring.py` | Multi-factor weighted score formula, category thresholds, recommendations | 3 | **PASSED** |
| `test_job_api.py` | JSearch schema normalization, missing field fallbacks | 2 | **PASSED** |

#### Test Execution Command & Output:
```bash
python -m unittest discover -s tests -p "test_*.py"
```
```text
................
----------------------------------------------------------------------
Ran 16 tests in 4.112s

OK
```

### 5.2 Real-World Document Parsing Evaluation
The document parsers were benchmarked on sample PDF and DOCX files generated from candidate data:
* **PDF File Parsing (`sample_resume.pdf`)**:
  * Candidate Name Extracted: `John Doe`
  * Extracted Email: `john.doe@example.com`
  * Technical Skills Detected: 25 unique skills
* **DOCX File Parsing (`sample_resume.docx`)**:
  * Candidate Name Extracted: `John Doe`
  * Extracted Email: `john.doe@example.com`
  * Technical Skills Detected: 25 unique skills

### 5.3 Live RapidAPI JSearch Benchmark & Latency Mitigation
Live API testing was executed using the configured RapidAPI credentials:
* **Target Query**: `"Machine Learning Engineer"` in `"Bengaluru"`
* **Initial Observation**: Live aggregation across third-party job boards required between 30 to 35 seconds, which exceeded the default 25s HTTP client timeout.
* **Engineering Solution**:
  1. Increased the request timeout in `services/job_api.py` to **60 seconds**.
  2. Implemented an automatic fallback to the high-speed `/search` endpoint if `/search-v2` experiences server congestion.
  3. Integrated offline fallback databases (`Load Offline Demo Jobs`) and manual job description pasting to ensure zero viva interruptions during network outages.
* **Post-Optimization Result**: Successfully returned **8 live job listings** with complete compensation, location, and requirement metadata in **7.2 seconds**.

### 5.4 Case Study: Machine Learning Engineer Matching
A test match was evaluated between candidate *John Doe* and a target *Machine Learning Engineer* position:

```text
================================================================================
                           MATCH EVALUATION RESULTS
================================================================================
Candidate:              John Doe (B.Tech Computer Science, 2 Years Exp)
Target Job:             Machine Learning Engineer (ABC Technologies)
Location:               Bengaluru, Karnataka, India

OVERALL MATCH SCORE:    49.9% (Weak Match / Near Moderate)

Score Breakdown:
  • TF-IDF Similarity:   19.8%  (Weight: 50% -> Contribution: 9.9%)
  • Skill Match Score:   75.0%  (Weight: 40% -> Contribution: 30.0%)
  • Requirements Match: 100.0%  (Weight: 10% -> Contribution: 10.0%)

Matching Technical Skills (12):
  ✓ Python, Machine Learning, Deep Learning, SQL, PostgreSQL,
    TensorFlow, Scikit-learn, Pandas, NumPy, Git, Linux, Docker

Missing Technical Skills (4):
  ✗ AWS, PyTorch, Kubernetes, CI/CD

Education Compatibility:
  ✓ Meets Requirement (Candidate B.Tech satisfies Bachelor's degree)

Experience Compatibility:
  ✓ Meets Requirement (Candidate ~2 years satisfies 2+ years requirement)

Generated Actionable Recommendations:
  1. Add AWS hands-on experience (build S3/EC2/SageMaker deployment pipelines).
  2. Master PyTorch fundamentals and implement deep learning model architectures.
  3. Containerize applications and document Kubernetes cluster orchestration.
================================================================================
```

### 5.5 Academic Viva Transparency Interface
Under the **“How NLP Analyzed This Match”** expandable modal, the Streamlit interface provides complete mathematical and algorithmic inspection for college viva evaluators:
1. **LaTeX Mathematical Formulations**: Renders the exact Cosine Similarity and Multi-Factor scoring equations.
2. **Vector Space Dimensions**: Displays the total vocabulary size (e.g., 459 unique unigrams and bigrams).
3. **High-Impact Feature Terms**: Displays tabular rankings of terms showing resume weight $A_i$, job weight $B_i$, and dot-product impact $A_i B_i$.
4. **Token Traces**: Displays sample raw tokens, stopword-filtered lists, and WordNet root lemmas.
5. **Raw JSON Payload**: Provides a full JSON dump of all computed state variables for rigorous verification.

<div style="page-break-after: always;"></div>

---

# CHAPTER 6: CONCLUSION AND FUTURE WORK

### 6.1 Summary of Contributions
In this project, the **AI Resume Analyzer** system was successfully designed, developed, and evaluated for the course **Introduction to Natural Language Processing (AI532P)**. The primary academic contributions include:
1. **Authentic NLP Engine**: Demonstrates genuine Information Retrieval and computational linguistics without relying on commercial LLM black boxes.
2. **Deterministic & Transparent**: Every percentage score is mathematically derived from vector dot products, normalized skill intersections, and requirement verifications.
3. **Multi-Format Ingestion**: Robustly parses both PDF and DOCX files while shielding special programming tokens from punctuation stripping.
4. **Separation of Concerns**: Connects to the RapidAPI JSearch API solely for live listing discovery while performing all NLP analysis locally.
5. **Academic Viva Support**: Provides full intermediate pipeline transparency, enabling evaluators to inspect tokenization, lemmatization, NER tags, and vector dimensions.

### 6.2 Future Enhancements
* **Dense Semantic Embeddings**: Integrate transformer-based sentence encoders (e.g., `all-MiniLM-L6-v2` via Sentence-Transformers) to complement sparse TF-IDF representations with dense semantic vectors.
* **Knowledge Graph Skill Ontologies**: Incorporate graph database ontologies (e.g., Neo4j with ESCO ontology) to evaluate hierarchical skill relationships (e.g., recognizing that proficiency in *PyTorch* implies familiarity with *Deep Learning*).
* **Multi-Lingual Resume Parsing**: Extend language identification and morphological lemmatization to multilingual candidate resumes.

<div style="page-break-after: always;"></div>

---

# REFERENCES

1. Salton, G., Wong, A., & Yang, C. S. (1975). *A vector space model for automatic indexing*. Communications of the ACM, 18(11), 613-620.
2. Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press.
3. Jurafsky, D., & Martin, J. H. (2024). *Speech and Language Processing: An Introduction to Natural Language Processing, Computational Linguistics, and Speech Recognition* (3rd ed. draft).
4. Bird, S., Klein, E., & Loper, E. (2009). *Natural Language Processing with Python: Analyzing Text with the Natural Language Toolkit*. O'Reilly Media.
5. Honnibal, M., & Montani, I. (2017). *spaCy 2: Natural language understanding with Bloom embeddings, convolutional neural networks and incremental parsing*.
6. Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., ... & Duchesnay, É. (2011). *Scikit-learn: Machine learning in Python*. Journal of Machine Learning Research, 12, 2825-2830.
7. RapidAPI. (2026). *JSearch API Documentation: Real-time Job Search Engine*. RapidAPI Hub.
