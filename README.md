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


<img width="1001" height="263" alt="image" src="https://github.com/user-attachments/assets/7a60260d-ef74-4c1b-85a3-e3314a1c3519" />





Smart Query Reformulation: Automatically strips conversational fillers and extracts core technical keywords to optimize the arXiv API search.

Semantic Search & Reranking: Computes text embeddings using BAAI/bge-large-en-v1.5 to calculate cosine similarity scores, ensuring the top  most contextually relevant papers are selected.

 <img width="464" height="259" alt="image" src="https://github.com/user-attachments/assets/dfe9a91e-f8b5-455c-ad3a-3267280c101b" />


Automated Critique Generation: An LLM reviews the retrieved papers to deliver a final verdict on whether the literature generally supports or contradicts the original thesis.

 <img width="540" height="332" alt="image" src="https://github.com/user-attachments/assets/7153968b-58d1-4a4d-aada-2f3df5f7f3b7" />


Consine Scores 

<img width="484" height="121" alt="image" src="https://github.com/user-attachments/assets/42040860-835e-4c2c-ad69-d23ffacb789c" />



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

There is fall back code in case keywords did not render results so to get a better picture of performance. You can add code that print out whether the cleaned keywords were used.  
if not live_papers:
        # Secondary attempt: Use analyzed thesis if the LLM's keywords were too restrictive
        live_papers = fetch_real_arxiv_papers(search_thesis_for_query)
        if not live_papers:
            return f" Strategy: {reasoning_part}", f" No matches found for: {api_ready_query}", "Aborted.", f"Sentiment: {sentiment}, Stance: {stance}"




 
To further test the LLM, you can add a sentiment model to compare with the LLM's sentiment results. 
<img width="604" height="134" alt="image" src="https://github.com/user-attachments/assets/a4fd9de9-bee9-4273-a1ab-794355d1363e" />



You can also  add Export Feature to CVS.  
<img width="678" height="74" alt="image" src="https://github.com/user-attachments/assets/a32dc41f-1bf3-4b41-957b-ce0be0915342" />





How much energy is actually being used? Currently, the only feedback from a black-box model is token usage, which you can try to compute against CPU and GPU consumption. While this serves as a great social hedge, in reality, the model doesn't show the true environmental impact. The only way to truly know is to measure how energy is consumed via analogous methods. It really requires a separate supply of water and energy while actively managing its own waste. Setting this within an ecosystem without disrupting the natural cycle requires a very different kind of business setup, but it can be done and can function effectively. 

This setup seems to be using less energy. 


Solution  

Looking at my results, I can see that the best outcomes come from deterministic code; the summary section acts as an extra layer. The best approach is to either teach a person how to break down a paper or to provide extra metadata specifically designed for search, such as an abstract tailored for search engines.  



Happy Coding!!!!!


 
