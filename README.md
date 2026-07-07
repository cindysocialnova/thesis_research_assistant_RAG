Thesis-Driven Paper RAG Agent

Model 
model="llama-3.1-8b-instant",
Feel free to chnage.  
Current Setting
            temperature=0.3,  
            max_tokens=1024,

This application is an advanced Retrieval-Augmented Generation (RAG) tool designed to validate or critique academic thesis statements. By fetching live papers from the arXiv API, the agent analyzes the alignment, sentiment, and stance of academic literature against a user's initial thesis—even accounting for whether a thesis is framed to be supported or disproven.


Features
Stance & Sentiment Analysis: Evaluates the user's thesis to determine if it is framed positively, negatively, or neutrally, and checks whether the stance is to "Support" or "Disprove".


<img width="1038" height="248" alt="image" src="https://github.com/user-attachments/assets/c5dbc4aa-5bec-47e5-a72f-1210e7d33cf6" />





Smart Query Reformulation: Automatically strips conversational fillers and extracts core technical keywords to optimize the arXiv API search.

Semantic Search & Reranking: Computes text embeddings using BAAI/bge-large-en-v1.5 to calculate cosine similarity scores, ensuring the top  most contextually relevant papers are selected.

<img width="483" height="113" alt="image" src="https://github.com/user-attachments/assets/34ee5d3f-1405-4ba2-b69d-7ef8ea6ec271" />


Automated Critique Generation: An LLM reviews the retrieved papers to deliver a final verdict on whether the literature generally supports or contradicts the original thesis.

<img width="451" height="114" alt="image" src="https://github.com/user-attachments/assets/3643e726-d91a-4836-8dc9-13ef4cbc68cd" />


Consine Scores 

<img width="456" height="84" alt="image" src="https://github.com/user-attachments/assets/7e2dee9f-c49f-4250-81e2-948ab5997ce0" />


 

 Key Technical Notes & Insights
If you are experimenting with or altering this RAG pipeline, please keep the following system constraints and behavioral notes in mind:
1. API Parameter Constraints
During development, attempts to introduce custom relevance parameters directly into the API fetching layer caused errors. The arXiv API integration is structurally pre-coded to sort heavily by sortBy: "relevance". Overriding this behavior requires modifying the internal payload structure, not just appending parameters.
2. Black-Box Behavioral Traps
The underlying LLM utilizes its own internal logic during the query expansion phase. Because these mechanisms occur "behind the box," directly manipulating or altering the precise search outputs from outside the prompt schema can be difficult.
3. Boolean Operator Limitations (Context)
Do not rely on Boolean logic for query refinement. Testing indicates that adding explicit AND or OR operators to the search strings does not improve the retrieval performance or precision of the arXiv API in this architecture.
4. Production Cleanliness Recommendations
For a public-facing deployment, it is highly recommended to strip out the Reasoning Chain-of-Thought (CoT) output and the raw Cosine Similarity Scores from the final user view. These metrics are vital for model analysts calibrating the pipeline but clutter the user experience.
 
