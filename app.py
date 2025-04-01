import streamlit as st
import matplotlib.pyplot as plt

# FIFO Algorithm
def fifo(pages, frames):
    memory, page_faults = [], 0
    memory_states = []
    
    for page in pages:
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                memory.pop(0)  # Remove the oldest page
                memory.append(page)
            page_faults += 1
        memory_states.append(memory.copy())
    
    return page_faults, memory_states

# LRU Algorithm
def lru(pages, frames):
    memory, page_faults = [], 0
    memory_states = []
    page_indices = {}  # Dictionary to track the last usage of each page
    
    for i, page in enumerate(pages):
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                # Find the least recently used page and replace it
                lru_page = min(memory, key=lambda p: page_indices.get(p, -1))
                memory.remove(lru_page)
                memory.append(page)
            page_faults += 1
        page_indices[page] = i  # Update the last used index for the page
        memory_states.append(memory.copy())
    
    return page_faults, memory_states

# Optimal Algorithm
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

def run_algorithm(algorithm, pages, frames):
    if algorithm == "FIFO":
        return fifo(pages, frames)
    elif algorithm == "LRU":
        return lru(pages, frames)
    elif algorithm == "Optimal":
        return optimal(pages, frames)

# UI Configuration
st.set_page_config(layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
    .header {
        font-size: 24px !important;
        font-weight: bold !important;
        margin-bottom: 20px !important;
    }
    .result-box {
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 20px;
        background-color: #f9f9f9;
    }
    .metric-box {
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        padding: 10px;
        margin: 5px;
        background-color: white;
    }
    .footer {
        font-size: 12px;
        color: #666;
        margin-top: 30px;
    }
    .highlight {
        background-color: #f0f2f6;
        padding: 2px 5px;
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="header">Page Replacement Algorithm Simulator</div>', unsafe_allow_html=True)

# Input Section
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        algorithm = st.selectbox("Select algorithm", ["FIFO", "LRU", "Optimal"])
    
    with col2:
        frames = st.number_input("Enter number of frames", min_value=1, max_value=10, value=3, step=1)

    ref_string = st.text_input("Enter reference string (separated by spaces)", 
                             value="6 7 8 9 6 7 1 6 7 8 9 1")

# Buttons
col1, col2, _ = st.columns([1, 1, 5])
with col1:
    generate_btn = st.button("Generate", type="primary")
with col2:
    reset_btn = st.button("Reset")

# Computation Outline Section
if generate_btn and ref_string:
    st.markdown("---")
    st.subheader("Computation Outline")
    
    pages = list(map(int, ref_string.split()))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**Algorithm:** {algorithm}")
    with col2:
        st.write(f"**Frames:** {frames}")
    with col3:
        st.write(f"**Reference Length:** {len(pages)}")
    
    st.write(f"**Reference String:** {' '.join(map(str, pages))}")

# Results Section
if generate_btn and ref_string:
    st.markdown("---")
    st.subheader("Results")
    
    page_faults, memory_states = run_algorithm(algorithm, pages, frames)
    hit_count = len(pages) - page_faults
    hit_rate = (hit_count / len(pages)) * 100
    miss_rate = 100 - hit_rate
    
    # Results Metrics
    with st.container():
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.metric("PAGE FAULTS", page_faults)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.metric("HIT RATE", f"{hit_rate:.2f}% [{hit_count}]")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.metric("MISS RATE", f"{miss_rate:.2f}% [{page_faults}]")
            st.markdown('</div>', unsafe_allow_html=True)

    # Memory States Table
    st.subheader("Memory State Changes")
    state_table = []
    for i, state in enumerate(memory_states):
        state_table.append({
            "Step": i+1,
            "Frame 1": state[0] if len(state) > 0 else "-",
            "Frame 2": state[1] if len(state) > 1 else "-",
            "Frame 3": state[2] if len(state) > 2 else "-",
            "Page Fault": "✔️" if pages[i] not in (memory_states[i-1] if i > 0 else []) else "➖"
        })
    
    st.dataframe(state_table, use_container_width=True, height=400)

    # Algorithm Comparison Chart
    st.subheader("Algorithm Comparison")
    fig, ax = plt.subplots(figsize=(10, 5))
    algorithms = ["FIFO", "LRU", "Optimal"]
    faults = [
        fifo(pages, frames)[0],
        lru(pages, frames)[0],
        optimal(pages, frames)[0],
    ]
    
    colors = ["#4C72B0", "#55A868", "#C44E52"]
    bars = ax.bar(algorithms, faults, color=colors)
    ax.set_ylabel("Page Faults")
    ax.set_title("Page Faults Comparison Across Algorithms")
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom')
    
    st.pyplot(fig)

    # Algorithm Insights
    st.subheader("Algorithm Insights")
    min_fault = min(faults)
    max_fault = max(faults)
    
    if faults[0] == min_fault:
        st.markdown("""
        <div class="highlight">
        <b>FIFO performed best:</b> FIFO works well when the page reference pattern has fewer repeated pages 
        and the order of page usage is predictable. However, it may cause Belady's anomaly.
        </div>
        """, unsafe_allow_html=True)
    
    if faults[1] == min_fault:
        st.markdown("""
        <div class="highlight">
        <b>LRU performed best:</b> LRU performs well when the most recently used pages are likely to be used again soon.
        It's more efficient for workloads where recent usage predicts future usage.
        </div>
        """, unsafe_allow_html=True)
    
    if faults[2] == min_fault:
        st.markdown("""
        <div class="highlight">
        <b>Optimal performed best:</b> Optimal provides the theoretical minimum number of page faults 
        by replacing the page that won't be used for the longest period. This is unrealistic in practice.
        </div>
        """, unsafe_allow_html=True)

# Reset functionality
if reset_btn:
    st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown('<div class="footer">Page Replacement Algorithm Simulator © 2023</div>', unsafe_allow_html=True)
