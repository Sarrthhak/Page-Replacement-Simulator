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

def run_algorithm(algorithm, pages, frames):
    if algorithm == "FIFO":
        return fifo(pages, frames)
    elif algorithm == "LRU":
        return lru(pages, frames)
    elif algorithm == "Optimal":
        return optimal(pages, frames)

# UI Configuration
st.set_page_config(layout="centered")

# Custom CSS for styling
st.markdown("""
<style>
    .header {
        font-size: 24px !important;
        font-weight: bold !important;
        margin-bottom: 20px !important;
    }
    .metric-box {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid #e0e0e0;
    }
    .ratio-container {
        display: flex;
        gap: 10px;
        margin: 15px 0;
    }
    .ratio-bar {
        flex: 1;
        height: 30px;
        background-color: #e9ecef;
        border-radius: 15px;
        overflow: hidden;
        position: relative;
    }
    .ratio-fill {
        height: 100%;
        display: flex;
        align-items: center;
        min-width: fit-content;
    }
    .hit-fill {
        background-color: #28a745;
        justify-content: flex-end;
        padding-right: 8px;
    }
    .miss-fill {
        background-color: #dc3545;
        padding-left: 8px;
    }
    .ratio-label {
        position: absolute;
        width: 100%;
        text-align: center;
        color: white;
        font-weight: bold;
        z-index: 2;
    }
    .insight-card {
        background-color: #f8f9fa;
        border-left: 4px solid #6c757d;
        border-radius: 0 8px 8px 0;
        padding: 15px;
        margin: 15px 0;
    }
    .insight-title {
        color: #343a40;
        font-weight: bold;
        margin-top: 0;
        font-size: 18px;
    }
    .insight-content {
        color: #495057;
        margin-bottom: 0;
        font-size: 15px;
    }
    .dataframe {
        width: 100%;
    }
    .footer {
        font-size: 12px;
        color: #666;
        margin-top: 30px;
        text-align: center;
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

# Computation Outline
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
    
    # Metrics
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <h3>Page Faults</h3>
            <h1>{page_faults}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <h3>Hits</h3>
            <h1>{hit_count}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    # Hit/Miss Ratio
    st.write("**Hit/Miss Ratio:**")
    st.markdown(f"""
    <div class="ratio-container">
        <div class="ratio-bar">
            <div class="ratio-fill hit-fill" style="width: {max(20, hit_rate)}%">
                <span class="ratio-label">{hit_rate:.1f}% Hits ({hit_count})</span>
            </div>
        </div>
        <div class="ratio-bar">
            <div class="ratio-fill miss-fill" style="width: {max(20, miss_rate)}%">
                <span class="ratio-label">{miss_rate:.1f}% Misses ({page_faults})</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

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

    # Algorithm Comparison
    st.subheader("Algorithm Comparison")
    fig, ax = plt.subplots(figsize=(8, 4))
    algorithms_all = ["FIFO", "LRU", "Optimal"]
    faults = [
        fifo(pages, frames)[0],
        lru(pages, frames)[0],
        optimal(pages, frames)[0],
    ]
    colors = ["#4C72B0", "#55A868", "#C44E52"]
    bars = ax.bar(algorithms_all, faults, color=colors, width=0.6)
    ax.set_ylabel("Page Faults")
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom')
    plt.tight_layout()
    st.pyplot(fig)

    # Insights Section
    st.markdown("---")
    st.subheader("Algorithm Insights")
    min_fault = min(faults)
    
    if faults[0] == min_fault:
        st.markdown("""
        <div class="insight-card">
            <h4 class="insight-title">FIFO Performed Best</h4>
            <p class="insight-content">
            FIFO works well when page references are evenly distributed without clustering. 
            It's simple but may suffer from Belady's anomaly where increasing frames 
            can actually increase page faults.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    if faults[1] == min_fault:
        st.markdown("""
        <div class="insight-card">
            <h4 class="insight-title">LRU Performed Best</h4>
            <p class="insight-content">
            LRU excels when recently used pages are likely to be used again soon. 
            It approximates optimal behavior but requires tracking usage history, 
            which adds overhead.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    if faults[2] == min_fault:
        st.markdown("""
        <div class="insight-card">
            <h4 class="insight-title">Optimal Performed Best</h4>
            <p class="insight-content">
            Optimal provides the theoretical minimum page faults by replacing the page 
            that won't be used for the longest time. While impossible to implement 
            in practice, it serves as a useful benchmark.
            </p>
        </div>
        """, unsafe_allow_html=True)

# Reset functionality
if reset_btn:
    st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown('<div class="footer">Page Replacement Algorithm Simulator © 2023</div>', unsafe_allow_html=True)
