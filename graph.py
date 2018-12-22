from graphviz import Digraph, Graph
import graphviz
import base64
import numpy as np

def to_base64_png(b):
    return 'data:image/png;base64,' + str(base64.b64encode(b))[2:-1]

def is_binary(M): return all([M[i,j] == 0 or M[i,j] == 1 for j in range(M.shape[1]) for i in range(M.shape[0])])

def is_symmetric(M): return M == M.T

def Kn(n): return np.ones(n) - np.eye(n)

def ring(n): 
    A = np.roll(np.eye(n), 1, axis=1)
    return A + A.T

def uring(n): 
    A = np.roll(np.eye(n), 1, axis=1)
    return A

def plot(G):
    print('is symmetric: {}'.format(is_symmetric(G)))
    if is_symmetric(G).all(): return plot_graph(G)
    else: return plot_digraph(G)

def plot_graph(G):
    dot = Graph(comment="Matrix graph", engine='sfdp', format='png')
    dot.attr(size='6,6')
    dot.attr(overlap='false')
    dot.attr(fontsize='12')
    is_bin = is_binary(G)
    for i in range(G.shape[0]):
        dot.node(str(i), str(i))
        for j in range(i, G.shape[1]):
            if G[i,j] != 0:
                if is_bin: dot.edge(str(i), str(j))
                else: dot.edge(str(i), str(j), str(G[i,j]))
        
    return dot

def plot_digraph(G):
    dot = Digraph(comment="Matrix graph", engine='sfdp', format='png')
    dot.attr(size='6,6')
    dot.attr(overlap='false')
    dot.attr(fontsize='12')
    is_bin = is_binary(G)
    for i in range(G.shape[0]):
        dot.node(str(i), str(i))
        for j in range(G.shape[1]):
            if G[i,j] != 0:
                if is_bin: dot.edge(str(i), str(j))
                else: dot.edge(str(i), str(j), str(G[i,j]))
        
    return dot