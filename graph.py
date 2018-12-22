from graphviz import Digraph, Graph
import graphviz
import base64
import numpy as np

graphviz_engine = 'dot'

def to_base64_png(b):
    return 'data:image/png;base64,' + str(base64.b64encode(b))[2:-1]

def is_simple(M): return all([m == 0 for m in np.diagonal(M)]) and is_binary(M)
def is_binary(M): return all([M[i,j] == 0 or M[i,j] == 1 for j in range(M.shape[1]) for i in range(M.shape[0])])
def is_symmetric(M): return M == M.T

def is_directed(M): return not is_symmetric(M)
def is_weighted(M): return not is_binary(M)

def degree_matrix(G): return np.sum(np.vectorize(not_zero)(G), axis=0) * np.eye(G.shape[0])
def not_zero(x): return 1 if x != 0 else 0

def complement(G):
    if not is_simple(G):
        raise ValueError('G must be a simple graph.')
    return np.ones(G.shape[0]) - G - np.eye(G.shape[0])

def Kn(n): return np.ones(n) - np.eye(n)

def ring(n): 
    A = np.roll(np.eye(n), 1, axis=1)
    return A + A.T

def uring(n): 
    A = np.roll(np.eye(n), 1, axis=1)
    return A

def plot(G):
    if is_symmetric(G).all(): return plot_graph(G)
    else: return plot_digraph(G)

def plot_graph(G):
    dot = Graph(comment="Matrix graph", engine=graphviz_engine, format='png')
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
    dot = Digraph(comment="Matrix graph", engine=graphviz_engine, format='png')
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

def plot_mst(G, MST):
    dot = Graph(comment="Matrix graph", engine=graphviz_engine, format='png')
    dot.attr(size='6,6')
    #dot.attr(overlap='false')
    #dot.attr(fontsize='12')
    is_bin = is_binary(G)
    for i in range(G.shape[0]):
        dot.node(str(i), str(i))
        for j in range(i, G.shape[1]):
            if G[i,j] != 0:
                if is_bin: dot.edge(str(i), str(j), color='red' if MST[i, j] != 0 else 'black')
                else: dot.edge(str(i), str(j), str(G[i,j]), color='red' if MST[i, j] != 0 else 'black')
    return dot

def mst(G, minimum=True):
    if not is_symmetric(G):
        raise ValueError('G must be undirected.')
    n = G.shape[0]
    V = list(range(G.shape[0]))
    D = {(x,y):G[x,y] for x in range(G.shape[0]) for y in range(G.shape[1]) if G[x,y] != 0}
    D = sorted(D.items(), key=lambda kv: kv[1], reverse=minimum)
    MST = np.reshape(np.zeros(n*n), (n,n))
    weight = 0

    while len(D) > 0:
        k, d = D.pop(); x, y = k
        if V[x] != V[y]:
            mi, ma = min(V[x], V[y]), max(V[x], V[y])
            V[x] = V[y] = mi
            MST[x,y] = d; MST[y,x] = d
            weight += d
            for i in range(len(V)):
                if V[i] == ma: V[i] = mi

    return MST, weight

def generate_undirect_graph(n):
    G = np.array([ np.floor(np.random.random(n)*10) for _ in range(n)])
    G = G - np.diagonal(G) * np.eye(n)
    return G * G.T