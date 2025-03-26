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
                memory.pop(0)
                memory.append(page)
            page_faults += 1
        memory_states.append(memory[:])
    
    return page_faults, memory_states

# LRU Algorithm
def lru(pages, frames):
    memory, page_faults = [], 0
    memory_states = []
    page_indices = {}
    
    for i, page in enumerate(pages):
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                lru_page = min(memory, key=lambda p: page_indices[p])
                memory.remove(lru_page)
                memory.append(page)
            page_faults += 1
        page_indices[page] = i
        memory_states.append(memory[:])
    
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
        memory_states.append(memory[:])
    
    return page_faults, memory_states

# Run the selected algorithm
def run_algorithm(algorithm, pages, frames):
    if algorithm == "FIFO":
        return fifo(pages, frames)
    elif algorithm == "LRU":
        return lru(pages, frames)
    elif algorithm == "Optimal":
        return optimal(pages, frames)

# Streamlit interface
st.title("Page Replacement Algorithm Simulator")
st.write("Simulate and compare FIFO, LRU, and Optimal page replacement algorithms.")

# Input for page reference string and number of frames
pages_input = st.text_input("Enter page reference string (comma-separated):")
frames = st.number_input("Enter number of frames:", min_value=1, max_value=10, value=3)

# Algorithm selection
algorithm = st.selectbox("Select Algorithm", ["FIFO", "LRU", "Optimal"])

# Run the simulation when the button is pressed
if st.button("Run Simulation"):
    if pages_input:
        pages = list(map(int, pages_input.split(",")))
        page_faults, memory_states = run_algorithm(algorithm, pages, frames)

        st.write(f"**Number of Page Faults:** {page_faults}")
        st.write("**Memory State Changes:**")

        # Split the states into columns to display them side by side
        columns = st.columns(4)  # 4 columns for better layout
        for i, state in enumerate(memory_states):
            with columns[i % 4]:  # Distribute memory states into columns
                st.write(f"Step {i+1}: {state}")

                # Bar graph to compare page faults
        fig, ax = plt.subplots(figsize=(8, 6))  # Increased figure size
        algorithms = ["FIFO", "LRU", "Optimal"]
        faults = [
            fifo(pages, frames)[0],
            lru(pages, frames)[0],
            optimal(pages, frames)[0],
        ]
        colors = ["#4C72B0", "#55A868", "#C44E52"]  # Professional color palette
        ax.bar(algorithms, faults, color=colors, width=0.6, edgecolor="black")

        ax.set_ylabel("Page Faults", fontsize=12, fontweight="bold")
        ax.set_xlabel("Algorithm", fontsize=12, fontweight="bold")
        ax.set_title("Comparison of Page Faults Across Algorithms", fontsize=14, fontweight="bold")
        ax.grid(axis="y", linestyle="--", alpha=0.7)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        st.pyplot(fig)


    else:
        st.warning("Please enter a valid page reference string!")
