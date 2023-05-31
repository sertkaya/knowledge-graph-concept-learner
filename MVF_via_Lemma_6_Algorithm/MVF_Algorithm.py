# Importing the libraries
from collections import defaultdict
from typing import Dict, List, Tuple

'''
The below code is a python script for Computing MVF algorithm via Lemma 6.
The following steps are implemented in this python script:
    Input to be given: A description graph G = (V,E,L) and a vertex v ∈ V
    Expected Output: The MVF of v in G, i.e., mvf(G, v)
        1. V^* ← SCC(G)
        2. E^* ← condense(G, V^*)
        3. G^*   (V^*, E^*)
        4. for V^' ← V^* do
        5.	 wgt[V^']  ← null
        6. return maxWeight(G^*,scc(G,v), wgt)
        // Auxiliary Function
        7. Function maxWeight(G^*, V^',wgt):
        8.  current  ← 0
        9.  for W^' ∈ {U^'∈V^* | (V^',U^' )∈ E^*} do
        10.     if wgt[W^'] = null then
        11.         current  ← max(current, maxWeight(G^*, W^',wgt))
        12.     else
        13.         current  ← wgt[W^']
        14.     wgt[V^']   current + |V^' |
        15. return wgt[V^']

'''

# Read the file and assign the values to variable G
file_path = 'C:/Users/prana/Desktop/Masters Thesis/MVF_via_Lemma_6_Algorithm/examples/example-product-1.txt'

with open(file_path, 'r') as file:
    G = eval(file.read())


def SCC(G: Dict[str, List[str]]) -> List[List[str]]:
    """
    Finds the strongly connected components in a graph using Tarjan's algorithm.

    Args:
        G: The input graph.

    Returns:
        A list of lists, where each inner list is a strongly connected component.
    """
    index = {}
    lowlink = {}
    stack = []
    result = []
    idx = [0]

    def visit(v):
        index[v] = idx[0]
        lowlink[v] = idx[0]
        idx[0] += 1
        stack.append(v)

        for w in G.get(v, []):
            if w not in index:
                visit(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in stack:
                lowlink[v] = min(lowlink[v], index[w])

        if lowlink[v] == index[v]:
            scc = []
            while True:
                w = stack.pop()
                scc.append(w)
                if w == v:
                    break
            result.append(scc)

    for v in G.keys():
        if v not in index:
            visit(v)

    return result


def condense(G: Dict[str, List[str]], sccs: List[List[str]]) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    """
    Condenses a graph by collapsing strongly connected components into a single vertex.

    Args:
        G: The input graph.
        sccs: The strongly connected components of the graph.

    Returns:
        A tuple containing the condensed graph and the mapping from original vertices to the new vertices.
    """
    cmap = {v: i for i, scc in enumerate(sccs) for v in scc}
    cond = defaultdict(list)
    for v, edges in G.items():
        for w in edges:
            if cmap[v] != cmap[w]:
                cond[cmap[v]].append(cmap[w])
    return dict(cond), cmap


def maxWeight(G: Dict[str, List[str]], v: str, wgt: Dict[str, int]) -> int:
    """
    Finds the maximum weight of a vertex in a directed graph.

    Args:
        G: The input graph.
        v: The starting vertex.
        wgt: A dictionary mapping vertices to their weights.

    Returns:
        The maximum weight of a vertex in the graph.
    """
    if wgt[v] is not None:
        return wgt[v]
    current = 0
    for w in G.get(v, []):
        if wgt[w] is None:
            current = max(current, maxWeight(G, w, wgt))
        else:
            current = max(current, wgt[w])
    wgt[v] = current + len(G[v])
    return wgt[v]


# Algorithm implementation
sccs = SCC(G)
cond, cmap = condense(G, sccs)
G_condensed = {i: [] for i in range(len(sccs))}
for v, edges in cond.items():
    for w in edges:
        G_condensed[v].append(w)

wgt = {i: None for i in range(len(sccs))}


v_scc1 = cmap['ex:x1']
v_scc2 = cmap['ex:y1']
v_scc3 = cmap['ex:z1']
v_scc4 = cmap['ex:x2']
v_scc5 = cmap['ex:y2']
v_scc6 = cmap['ex:z2']

mvf1 = maxWeight(G_condensed, v_scc1, wgt)
mvf2 = maxWeight(G_condensed, v_scc2, wgt)
mvf3 = maxWeight(G_condensed, v_scc3, wgt)
mvf4 = maxWeight(G_condensed, v_scc4, wgt)
mvf5 = maxWeight(G_condensed, v_scc5, wgt)
mvf6 = maxWeight(G_condensed, v_scc6, wgt)

print(f"The MVF of 'ex:x1' in G is {mvf1}")  # Output is 3
print(f"The MVF of 'ex:y1' in G is {mvf2}")
print(f"The MVF of 'ex:z1' in G is {mvf3}")
print(f"The MVF of 'ex:x2' in G is {mvf4}")
print(f"The MVF of 'ex:y2' in G is {mvf5}")
print(f"The MVF of 'ex:z2' in G is {mvf6}")

'''
1. Explanation of why The MVF of 'ex:x1' in G is 3?

In the given graph G, the MVF of 'ex:x1' is 3, as it has three edges connected to it 
(i.e., 'rdf:type', 'ex:r1', and 'ex:r2').

2. Explanation of why The MVF of 'ex:y1'/'ex:z1' in G is 1?

In the given graph, the maximum vertex frequency of 'ex:y1' and 'ex:z1' would be 1, 
as they are only referenced once as the object of the 'ex:r1' and 'ex:r2' properties of the vertex 'ex:x1'.
'''
