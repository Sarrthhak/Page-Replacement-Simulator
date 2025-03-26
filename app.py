import streamlit as st
import matplotlib.pyplot as plt

# Page Replacement Algorithms
def fifo(pages, frames):
    memory = []
    page_faults = 0
    for page in pages:
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                memory.pop(0)
                memory.append(page)
            page_faults += 1
    return page_faults

def lru(pages, frames):
    memory = []
    page_faults = 0
    page_index = {}
    for i, page in enumerate(pages):
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                lru_page = min(page_index, key=page_index.get)
                memory.remove(lru_page)
                memory.append(page)
            page_faults += 1
        page_index[page] = i
    return page_faults

def optimal(pages, frames):
    memory = []
    page_faults = 0
    for i, page in enumerate(pages):
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                future_use = {}
                for mem_page in memory:
                    if mem_page in pages[i:]:
                        future_use[mem_page] = pages[i:].index(mem_page)
                    else:
                        future_use[mem_page] = float('inf')
                farthest_page = max(future_use, key=future_use.get)
                memory.remove(farthest_page)
                memory.append(page)
            page_faults += 1
    return page_faults

# Plot Results with Professional-Looking Graphs
def plot_results(fifo_faults, lru_faults, opt_faults):
    algorithms = ["FIFO", "LRU", "Optimal"]
    faults = [fifo_faults, lru_faults, opt_faults]
    
    plt.figure(figsize=(8, 6))
    bar_colors = ["#4C72B0", "#55A868", "#C44E52"]
    bars = plt.bar(algorithms, faults, color=bar_colors)
    
    # Add labels on top of each bar with padding
    for bar in bars:
        yval = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2, 
            yval - 0.1 if yval == max(faults) else yval + 0.1,  # Adjust for highest bar
            f"{int(yval)}", 
            ha="center", 
            va="bottom", 
            fontsize=12, 
            fontweight="bold"
        )
    
    # Add extra space on top to prevent text overflow
    plt.ylim(0, max(faults) + 2)
    
    plt.title("Page Faults Comparison", fontsize=14, fontweight="bold")
    plt.xlabel("Algorithm", fontsize=12, fontweight="bold")
    plt.ylabel("Number of Page Faults", fontsize=12, fontweight="bold")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    st.pyplot(plt)

# Streamlit UI
st.title("Page Replacement Algorithm Simulator")
st.write(
    "This application simulates and compares the performance of different page replacement algorithms: "
    "FIFO, LRU, and Optimal. Enter the page reference string and number of frames to visualize the results."
)

# User Inputs
pages_input = st.text_input("Enter Page Reference String (comma-separated)", "7, 0, 1, 2, 0, 3, 4, 2, 3, 0, 3, 2")
frames_input = st.number_input("Enter Number of Frames", min_value=1, max_value=10, value=3)

# Process Input
if st.button("Run Simulation"):
    try:
        pages = list(map(int, pages_input.split(",")))
        frames = int(frames_input)
        
        # Run all algorithms
        fifo_faults = fifo(pages, frames)
        lru_faults = lru(pages, frames)
        opt_faults = optimal(pages, frames)
        
        # Display results
        st.write(f"**FIFO Algorithm:** {fifo_faults} page faults")
        st.write(f"**LRU Algorithm:** {lru_faults} page faults")
        st.write(f"**Optimal Algorithm:** {opt_faults} page faults")
        
        # Plot the results
        plot_results(fifo_faults, lru_faults, opt_faults)

    except ValueError:
        st.error("Please enter a valid comma-separated sequence of integers for the page reference string.")
