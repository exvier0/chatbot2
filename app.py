import streamlit as st
import time
from graphviz import Digraph

st.set_page_config(
    page_title="Simulasi Evakuasi DFA",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 Simulasi Jalur Evakuasi Korban Menggunakan DFA")

st.markdown("""
Aplikasi ini mensimulasikan proses evakuasi korban bencana menggunakan
**Deterministic Finite Automata (DFA)**.
""")

# DFA
transitions = {
    'q0': {
        'a': 'q1',
        'b': 'q5'
    },
    'q1': {
        'a': 'q2',
        'd': 'q3',
        'b': 'q5'
    },
    'q2': {
        'c': 'q4',
        'b': 'q5'
    },
    'q3': {
        'c': 'q4',
        'b': 'q5'
    },
    'q4': {},
    'q5': {}
}

state_names = {
    'q0': '🏠 Rumah',
    'q1': '🛣 Jalan Utama',
    'q2': '⛺ Posko Evakuasi 1',
    'q3': '🚑 Posko Evakuasi 2',
    'q4': '🟢 Zona Aman',
    'q5': '🌊 Area Banjir'
}

accept_state = 'q4'

# Input
input_string = st.text_input(
    "Masukkan jalur (contoh: aac)",
    value="aac"
)

run = st.button("▶ Jalankan Simulasi")

def draw_graph(active_state=None):

    dot = Digraph()

    states = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5']

    for s in states:

        color = "lightblue"

        if s == active_state:
            color = "green"

        if s == accept_state:
            color = "lightgreen"

        if s == 'q5':
            color = "red"

        dot.node(
            s,
            state_names[s],
            style="filled",
            fillcolor=color
        )

    dot.edge('q0', 'q5', label='b')
    dot.edge('q0', 'q1', label='a')


    dot.edge('q1', 'q2', label='a')
    dot.edge('q1', 'q3', label='d')
    dot.edge('q1', 'q5', label='b')

    dot.edge('q2', 'q4', label='c')
    dot.edge('q2', 'q5', label='b')

    dot.edge('q3', 'q4', label='c')
    dot.edge('q3', 'q5', label='b')

    return dot

graph_placeholder = st.empty()
graph_placeholder.graphviz_chart(draw_graph())

if run:

    current_state = 'q0'

    log_box = st.empty()
    graph_area = st.empty()

    logs = []

    logs.append(
        f"Start dari {state_names[current_state]}"
    )

    graph_area.graphviz_chart(
        draw_graph(current_state)
    )

    time.sleep(1)

    valid = True

    for symbol in input_string:

        if symbol not in transitions[current_state]:

            valid = False
            break

        next_state = transitions[current_state][symbol]

        logs.append(
            f"Input '{symbol}' ➜ {state_names[next_state]}"
        )

        current_state = next_state

        graph_area.graphviz_chart(
            draw_graph(current_state)
        )

        log_box.info("\n".join(logs))

        time.sleep(1)

    st.divider()

    if valid and current_state == accept_state:

        st.success(
            "✅ Evakuasi Berhasil! Korban mencapai Zona Aman."
        )

        st.balloons()

    else:

        st.error(
            "❌ Evakuasi Gagal! Korban tidak mencapai Zona Aman."
        )