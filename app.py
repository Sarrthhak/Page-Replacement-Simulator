import streamlit as st
import matplotlib.pyplot as plt

# Algorithm Implementations
def fifo(pages, frames):
    memory, page_faults = [], 0
    memory_states = []
    for page in pages:
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                memory.pop(0)
                memory.append(page)
            page_faults += 1
        memory_states.append(memory.copy())
    return page_faults, memory_states

def lru(pages, frames):
    memory, page_faults = [], 0
    memory_states = []
    page_indices = {}
    for i, page in enumerate(pages):
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                lru_page = min(memory, key=lambda p: page_indices.get(p, -1))
                memory.remove(lru_page)
                memory.append(page)
            page_faults += 1
        page_indices[page] = i
        memory_states.append(memory.copy())
    return page_faults, memory_states

def optimal(pages, frames):
    memory, page_faults = [], 0
    memory_states = []
    for i, page in enumerate(pages):
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                future_indices = []
                for mem_page in memory:
                    if mem_page in pages[i:]:
                        future_indices.append(pages[i:].index(mem_page))
                    else:
                        future_indices.append(float('inf'))
                replace_index = future_indices.index(max(future_indices))
                memory[replace_index] = page
            page_faults += 1
        memory_states.append(memory.copy())
    return page_faults, memory_states

# UI Configuration
st.set_page_config(layout="centered")

# Input Section
st.title("Page Replacement Algorithm Simulator")

algorithm = st.selectbox("Select algorithm", ["FIFO", "LRU", "Optimal"])
frames = st.number_input("Enter number of frames", min_value=1, max_value=10, value=3)
ref_string = st.text_input("Enter reference string (separated by spaces)", "6 7 8 9 6 7 1 6 7 8 9 1")

if st.button("Generate"):
    pages = list(map(int, ref_string.split()))
    
    # Computation Outline
    st.markdown("---")
    st.header("Computation Outline")
    st.write(f"**Algorithm:** {algorithm}")
    st.write(f"**Frames:** {frames}")
    st.write(f"**Reference Length:** {len(pages)}")
    st.write(f"**Reference String:** {' '.join(map(str, pages))}")
    
    # Run selected algorithm
    if algorithm == "FIFO":
        page_faults, memory_states = fifo(pages, frames)
    elif algorithm == "LRU":
        page_faults, memory_states = lru(pages, frames)
    else:
        page_faults, memory_states = optimal(pages, frames)
    
    # Results
    st.markdown("---")
    st.header("Results")
    
    hit_count = len(pages) - page_faults
    miss_rate = (page_faults / len(pages)) * 100
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Page Faults", page_faults)
    with col2:
        st.metric("Hits", hit_count)
    
    # Battery-style Hit/Miss Ratio Visualization
    st.markdown("---")
    st.header("Hit/Miss Ratio Visualization")
    
    fig, ax = plt.subplots(figsize=(6, 1.2))
    ax.barh(["Hit Ratio", "Miss Ratio"], [hit_count, page_faults], color=["#4CAF50", "#F44336"], height=0.5)
    ax.set_xlim(0, len(pages))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    
    # Display text inside bars
    ax.text(hit_count / 2, 0, f"Hits: {hit_count} ({100 - miss_rate:.1f}%)", color="white", ha="center", va="center", fontsize=12)
    ax.text(page_faults / 2, 1, f"Misses: {page_faults} ({miss_rate:.1f}%)", color="white", ha="center", va="center", fontsize=12)
    
    st.pyplot(fig)
    
    # Memory States Table
    st.markdown("---")
    st.header("Memory State Changes")
    state_data = []
    for i, state in enumerate(memory_states):
        fault = "✔️" if pages[i] not in (memory_states[i-1] if i > 0 else []) else "➖"
        row = {
            "Step": i+1,
            "Frame 1": state[0] if len(state) > 0 else "-",
            "Frame 2": state[1] if len(state) > 1 else "-",
            "Frame 3": state[2] if len(state) > 2 else "-",
            "Page Fault": fault
        }
        state_data.append(row)
    st.table(state_data)
    
    # Algorithm Comparison
    st.markdown("---")
    st.header("Algorithm Comparison")
    fig, ax = plt.subplots(figsize=(8, 4))
    algorithms = ["FIFO", "LRU", "Optimal"]
    faults = [fifo(pages, frames)[0], lru(pages, frames)[0], optimal(pages, frames)[0]]
    ax.bar(algorithms, faults, color=["#4C72B0", "#55A868", "#C44E52"])
    ax.set_ylabel("Page Faults")
    st.pyplot(fig)
    
    # Insights
    st.markdown("---")
    st.header("Algorithm Insights")
    if algorithm == "Optimal":
        st.info("""
        Optimal provides the theoretical minimum page faults by replacing the page that won't be used for the longest time. 
        While impossible to implement in practice, it serves as a useful benchmark.
        """)
    elif algorithm == "LRU":
        st.info("""
        LRU performs well when recently used pages are likely to be used again soon.
        It approximates optimal behavior but requires tracking usage history.
        """)
    else:
        st.info("""
        FIFO works well when page references are evenly distributed without clustering.
        It's simple but may suffer from Belady's anomaly where increasing frames can increase page faults.
        """)

st.markdown("---")
st.caption("Made by Sarthak Pipladiya, Abhishek Kumar, Himanshu Gobari")
