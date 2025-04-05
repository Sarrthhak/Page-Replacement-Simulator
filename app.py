import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Page Replacement Algorithms
def fifo(pages, frames):
    memory, page_faults = [], 0
    memory_states = []
    decisions = []
    for page in pages:
        fault = False
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                memory.pop(0)
                memory.append(page)
            page_faults += 1
            fault = True
        memory_states.append(memory.copy())
        decisions.append("✔️" if fault else "➖")
    return page_faults, memory_states, decisions

def lru(pages, frames):
    memory, page_faults = [], 0
    memory_states = []
    decisions = []
    page_indices = {}
    for i, page in enumerate(pages):
        fault = False
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                lru_page = min(memory, key=lambda p: page_indices.get(p, -1))
                memory.remove(lru_page)
                memory.append(page)
            page_faults += 1
            fault = True
        page_indices[page] = i
        memory_states.append(memory.copy())
        decisions.append("✔️" if fault else "➖")
    return page_faults, memory_states, decisions

def optimal(pages, frames):
    memory, page_faults = [], 0
    memory_states = []
    decisions = []
    for i, page in enumerate(pages):
        fault = False
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                future_indices = []
                for mem_page in memory:
                    if mem_page in pages[i+1:]:
                        future_indices.append(pages[i+1:].index(mem_page))
                    else:
                        future_indices.append(float('inf'))
                replace_index = future_indices.index(max(future_indices))
                memory[replace_index] = page
            page_faults += 1
            fault = True
        memory_states.append(memory.copy())
        decisions.append("✔️" if fault else "➖")
    return page_faults, memory_states, decisions

# UI Configuration
st.set_page_config(layout="centered")
st.title("📄 Page Replacement Algorithm Simulator")

algorithm = st.selectbox("Select Algorithm", ["FIFO", "LRU", "Optimal"])
frames = st.number_input("Enter number of frames", min_value=1, max_value=10, value=3)
ref_string = st.text_input("Enter reference string (separated by spaces)", "6 7 8 9 6 7 1 6 7 8 9 1")

if st.button("Generate"):
    pages = list(map(int, ref_string.split()))

    # Display Computation Outline
    st.markdown("---")
    st.subheader("🧾 Computation Outline")
    st.write(f"**Algorithm:** {algorithm}")
    st.write(f"**Number of Frames:** {frames}")
    st.write(f"**Reference String Length:** {len(pages)}")
    st.write(f"**Reference String:** {' '.join(map(str, pages))}")

    # Run selected algorithm
    if algorithm == "FIFO":
        page_faults, memory_states, decisions = fifo(pages, frames)
    elif algorithm == "LRU":
        page_faults, memory_states, decisions = lru(pages, frames)
    else:
        page_faults, memory_states, decisions = optimal(pages, frames)

    # Results
    st.markdown("---")
    st.subheader("📊 Results")
    hit_count = len(pages) - page_faults
    miss_rate = (page_faults / len(pages)) * 100
    hit_rate = (hit_count / len(pages)) * 100

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Page Faults", page_faults)
    with col2:
        st.metric("Hits", hit_count)

    st.subheader("📈 Hit/Miss Visualization")
    st.markdown(
        f"""
        <div style="width: 100%; height: 30px; background-color: #eee; border-radius: 8px; display: flex; overflow: hidden; margin-top: 10px;">
            <div style="width: {miss_rate}%; background-color: #e74c3c;"></div>
            <div style="width: {hit_rate}%; background-color: #2ecc71;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 14px; margin-top: 5px;">
            <span>🔴 Miss Rate ({miss_rate:.1f}%)</span>
            <span>🟢 Hit Rate ({hit_rate:.1f}%)</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Memory State Table
    st.markdown("---")
    st.subheader("🧠 Memory State Changes")

    table_data = []
    for i in range(len(pages)):
        row = {"Step": i + 1, "Page": pages[i]}
        for f in range(frames):
            row[f"Frame {f + 1}"] = memory_states[i][f] if f < len(memory_states[i]) else "-"
        row["Page Fault"] = decisions[i]
        table_data.append(row)

    df = pd.DataFrame(table_data)
    df = df.astype(str)
    st.dataframe(df.style.set_properties(**{
        'text-align': 'center'
    }).set_table_styles([{
        'selector': 'th',
        'props': [('text-align', 'center')]
    }]), use_container_width=True)

    # Comparison Chart
    st.markdown("---")
    st.subheader("📊 Algorithm Comparison")
    fig, ax = plt.subplots(figsize=(8, 4))
    algos = ["FIFO", "LRU", "Optimal"]
    faults = [fifo(pages, frames)[0], lru(pages, frames)[0], optimal(pages, frames)[0]]
    ax.bar(algos, faults, color=["#4C72B0", "#55A868", "#C44E52"])
    ax.set_ylabel("Page Faults")
    ax.set_title("Page Faults by Algorithm")
    ax.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig)

    # Insights
    st.markdown("---")
    st.subheader("💡 Insights")
    if algorithm == "Optimal":
        st.info("Optimal provides the theoretical minimum page faults by replacing the page that won’t be used for the longest time.")
    elif algorithm == "LRU":
        st.info("LRU uses recent history to decide what to replace. It works well in programs with temporal locality.")
    else:
        st.info("FIFO is simple and easy to implement, but may suffer from Belady’s anomaly in some cases.")

st.markdown("---")
st.caption("Made with ❤️ by Sarthak Pipladiya")
