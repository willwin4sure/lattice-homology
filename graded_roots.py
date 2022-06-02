import os
import math
import networkx as nx
import matplotlib.pyplot as plt
from networkx.classes.function import subgraph
from regex import F

import tau_extrema_sequence

def draw_lattice_homology(tau_extrema, cutoff=100, name=None, save_dir='.'):
    '''
    Args:
        tau_extrema (list[int]): list of local extrema of a tau sequence,
            output of tau_extrema_sequence.extrema_sequence
            (tend to be negative numbers for grading; 
            we pick convention of lattice homology being drawn downwards, 
            with infinite stem extending upwards)

        cutoff (int): an optional argument to specify how many layers 
            from the bottom of the lattice homology upward to draw;
            used when the lattice homology is too large,
            as the bottom is what has topological importance

        name (str): an optional argument to specify a name for the saved .png file
        save_dir (str): an optional argument to specify a directory to save the .png file; defaults to current directory

    Returns (None): nothing is returned; it saves a .png file of the lattice homology to the current working directory
    '''
    # store the number of nodes on each layer/grading for plotting purposes, initialize with small stem above max
    counts = {i: 1 for i in range(0, int(round(max(tau_extrema)))+2)}
    counts[0] = 2

    length = (len(tau_extrema)-1)//2
    for i in range(1, length):
        # tau sequence alternates between maxima and minima, extract these
        max_val = int(round(tau_extrema[2*i-1])) 
        min_val = int(round(tau_extrema[2*i]))

        # each max_val -> min_val adds nodes to the layers between
        for j in range(min_val, max_val):
            if j in counts.keys():
                counts[j] = counts[j] + 1
            else:
                counts[j] = 1

    # size of the lattice homology, for drawing purposes
    height = len(counts.keys())
    width = max(counts.values())

    # minimum grading, for cutoff purposes
    min_grading = min(counts.keys())

    G = nx.Graph()
    subgraph_nodes = []

    # add nodes in each layer to the graph, based on the counts
    for layer, number in counts.items():
        for i in range(number):
            G.add_node(f'{layer}, {i}')
            # only add nodes to the subgraph if they are below the cutoff
            if (layer < min_grading + cutoff):
                subgraph_nodes.append(f'{layer}, {i}')

    # add edges between nodes in the graph; to do so, we define a pointer for each layer
    # that moves left to right along the nodes on that layer
    # then we traverse the graph as the tau sequence dictates, advancing the pointers accordingly
    pointers = {layer: 0 for layer in counts.keys()}

    for i in range(len(tau_extrema)):
        if i == 0:
            start = int(round(max(tau_extrema)))+2
            end = int(round(tau_extrema[i]))
            for j in range(end, start-1):
                G.add_edge(f'{j}, {pointers[j]}', f'{j+1}, {pointers[j+1]}')

        # if the current node is a maxima, we add edges downwards to next nodes until we hit the next minima
        elif i % 2 == 0:
            start = int(round(tau_extrema[i-1]))
            end = int(round(tau_extrema[i]))
            for j in range(end, start):
                G.add_edge(f'{j}, {pointers[j]}', f'{j+1}, {pointers[j+1]}')
        
        # if the current node is a minima, we go back up to the next maxima, advancing pointers along the way
        else:
            start = int(round(tau_extrema[i-1]))
            end = int(round(tau_extrema[i]))
            for j in range(start, end):
                pointers[j] += 1

    # tell nx where to place the vertices in our diagram
    positions = {}
    for layer,number in counts.items():
        for i in range(number):
            positions[f'{layer}, {i}'] = (i - (number - 1)/2, layer)

    # create the figure and plot the graph
    plt.figure(figsize=(width, min(height, cutoff-1)))
    nx.draw_networkx(G.subgraph(subgraph_nodes), pos = positions)

    # save the graph to the correct directory + file name
    if (name is None):
        plt.savefig('lattice_homology.png')
    else:
        plt.savefig(os.path.join(save_dir, f'lattice_homology_for_{name}.png'))
    
class Node:
    '''
    Class which represents nodes in the lattice homology

    Attributes:
        layer (int): the layer of the node
        index (int): the index of the node in the layer
        parent (Node): the parent node of the node
        children (list[Node]): the children nodes of the node
        is_stem (bool): whether the node is on the central stem
    '''
    def __init__(self, layer, index, parent=None):
        self.layer = layer
        self.index = index
        self.parent = parent
        self.children = []
        self.is_stem = False

    def __str__(self):
        if self.parent is None:
            return f'{self.layer}, {self.index}, no parent'
        else:
            return f'{self.layer}, {self.index}, {self.parent.layer}, {self.parent.index}'

class Graph:
    '''
    Class which represents the lattice homology

    Attributes:
        
    '''
    def __init__(self, root, stem_end, dir, counts):
        self.root = root
        self.stem_end = stem_end
        self.dir = dir
        self.counts = counts

def build_graph(tau_extrema):
    # top is one layer above the top node
    top = int(round(max(tau_extrema)))+2
    counts = {i: 1 for i in range(0, top)} 
    counts[0] = 2

    length = (len(tau_extrema)-1)//2

    for i in range(1, length):
        min_val = int(round(tau_extrema[2*i]))
        max_val = int(round(tau_extrema[2*i-1])) 
        for j in range(min_val, max_val):
            if j in counts.keys():
                counts[j] = counts[j] + 1
            else:
                counts[j] = 1

    #print(counts)

    dir = {}

    for layer,num_nodes in counts.items():
        #print(layer,number)
        for i in range(num_nodes):
            #print(i)
            node = Node(layer, i)
            dir[(layer, i)] = node

    pointers = {layer: 0 for layer in counts.keys()}

    for i in range(len(tau_extrema)):
        if i == 0:
            start = int(round(max(tau_extrema)))+2
            end = int(round(tau_extrema[i]))
            for j in range(end, start-1):
                dir[(j, pointers[j])].parent = dir[(j+1, pointers[j+1])]
                dir[(j+1, pointers[j+1])].children.append(dir[(j, pointers[j])])

        elif i % 2 == 0:
            start = int(round(tau_extrema[i-1]))
            end = int(round(tau_extrema[i]))
            for j in range(end, start):
                dir[(j, pointers[j])].parent = dir[(j+1, pointers[j+1])]
                dir[(j+1, pointers[j+1])].children.append(dir[(j, pointers[j])])
        
        else:
            start = int(round(tau_extrema[i-1]))
            end = int(round(tau_extrema[i]))
            for j in range(start, end):
                pointers[j] += 1

    #for k, node in dir.items():
    #    print(f'{k}, {node}')

    #default value
    last_stem_layer = min(counts.keys())

    for layer,value in sorted(counts.items(), reverse=True):
        if value % 2 == 0:
            last_stem_layer = layer + 1
            break

    for layer in range(last_stem_layer, top):
        dir[(layer, (counts[layer] - 1)/2)].is_stem = True

    last_stem_node = dir[(last_stem_layer,(counts[last_stem_layer]-1)/2)]
    
    return Graph(dir[(top-1, 0)], last_stem_node, dir, counts)

def maximal_monotone_subroot(tau_extrema):
    graph = build_graph(tau_extrema)

    #bfs to calculate max branch depths, which are absolute layer numbers
    max_branch_depths = {}

    for layer in range(graph.stem_end.layer, graph.root.layer + 1):
        current = graph.dir[layer, (graph.counts[layer]-1)/2]
        queue = [current]

        min_depth = layer

        while len(queue) > 0:
            current = queue.pop(0)
            if current.layer < min_depth:
                min_depth = current.layer

            for child in current.children:
                if not child.is_stem:
                    queue.append(child)

        max_branch_depths[layer] = min_depth

    #print(max_branch_depths)

    monotone_subroot = {graph.stem_end.layer: max_branch_depths[graph.stem_end.layer]}
    current_min_depth = max_branch_depths[graph.stem_end.layer]

    for layer in range(graph.stem_end.layer + 1, graph.root.layer + 1):
        if (max_branch_depths[layer] < current_min_depth):
            current_min_depth = max_branch_depths[layer]
            monotone_subroot[layer] = max_branch_depths[layer]
        
        else:
            monotone_subroot[layer] = layer

    return monotone_subroot

def draw_monotone_subroot(monotone_subroot, cutoff, name=None, save_dir='new_project'):
    G=nx.Graph()

    positions = {}

    topHeight = max(monotone_subroot.keys())
    bottomHeight = min(monotone_subroot.values())
    max_height = topHeight - bottomHeight

    max_width = 2 * max(k-v for k,v in monotone_subroot.items())

    if max_height < 1:
        max_height = 1

    if max_width < 1:
        max_width = 1

    subgraph_nodes = []

    for layer,depth in monotone_subroot.items():
        G.add_node(f'stem {layer}')
        positions[f'stem {layer}'] = (0, layer)
        if (layer < bottomHeight + cutoff):
            subgraph_nodes.append(f'stem {layer}')
        for i in range(depth, layer):
            G.add_node(f'{layer}, {i}, left')
            G.add_node(f'{layer}, {i}, right')
            if (layer < bottomHeight + cutoff):
                subgraph_nodes.append(f'{layer}, {i}, left')
                subgraph_nodes.append(f'{layer}, {i}, right')
            positions[f'{layer}, {i}, left'] = (i - layer, i)
            positions[f'{layer}, {i}, right'] = (layer - i, i)

        for i in range(depth, layer-1):
            G.add_edge(f'{layer}, {i}, left', f'{layer}, {i+1}, left')
            G.add_edge(f'{layer}, {i}, right', f'{layer}, {i+1}, right')

        if (depth < layer):
            G.add_edge(f'stem {layer}', f'{layer}, {layer-1}, left')
            G.add_edge(f'stem {layer}', f'{layer}, {layer-1}, right')

    for layer in monotone_subroot.keys():
        if (layer != topHeight):
            G.add_edge(f'stem {layer}', f'stem {layer+1}')
        

    # plt.figure(figsize=(max_width,max_height))
    plt.figure(figsize=(10,50))

    nx.draw_networkx(G.subgraph(subgraph_nodes), pos = positions)
    if (name is None):
        plt.savefig('monotone_subroot.png')
    else:
        plt.savefig(os.path.join(save_dir, f'monotone_subroot_for_{name}.png'))
    plt.close()

def check_trivial(monotone_subroot):
    for k,v in monotone_subroot.items():
        if k != v:
            return False
        
    return True

def check_monotone_equivalence(ms1, ms2):
    '''
    Args:
        ms1 (dict[int, int]), ms2 (dict[int, int]): dicts with layers to layer that branches end at. Format of the output of maximal_monotone_subroot
     
    Returns (bool): True if ms1 and ms2 have the same structure (ignores grading shift i.e. length of stem above first branch)
    '''

    # trivial1 = check_trivial(ms1)
    # trivial2 = check_trivial(ms2)

    # if trivial1 and trivial2:
    #     return True
    # elif trivial1:
    #     return False
    # elif trivial2:
    #     return False

    # layer num of the highest layer with a branch
    ms1_top = max([key for key in ms1.keys() if ms1[key] != key], default=min(ms1.keys()))
    ms2_top = max([key for key in ms2.keys() if ms2[key] != key], default=min(ms2.keys()))

    # delete everything above to ignore grading shifts, recentering top to 0
    ms1_new = {key-ms1_top: value-ms1_top for key,value in ms1.items() if key-ms1_top <= 0}
    ms2_new = {key-ms2_top: value-ms2_top for key,value in ms2.items() if key-ms2_top <= 0}

    # compare the resulting dictionaries
    return ms1_new == ms2_new



def draw_monotone_short(a, b, c, cutoff, shift=False, save_dir=''):
    if not shift:
        draw_monotone_subroot(maximal_monotone_subroot(tau_extrema_sequence.extrema_sequence(a,b,c)), cutoff, name=f'{a}, {b}, {c}', save_dir=save_dir)
    else:
        draw_monotone_subroot(maximal_monotone_subroot(tau_extrema_sequence.extrema_sequence(a,b,c+a*b)), cutoff, name=f'{a}, {b}, {c}+shift', save_dir=save_dir)

def main():
    co = 100
    a = 12
    N = 50

    with open(f'conjecture_log_{a}.txt', 'w') as f:
        for b in range(a+1,N):
            if math.gcd(a,b) == 1:
                for c in range(2, a*b+1):
                    if math.gcd(a,c) == 1 and math.gcd(b,c) == 1:
                        if set([a,b,c]) != set([2,3,5]):
                            ms1 = maximal_monotone_subroot(tau_extrema_sequence.extrema_sequence(a,b,c))
                            ms2 = maximal_monotone_subroot(tau_extrema_sequence.extrema_sequence(a,b,c+a*b))

                            if set([a,b,2*a*b-c]) != set([2,3,5]):
                                ms3 = maximal_monotone_subroot(tau_extrema_sequence.extrema_sequence(a,b,2*a*b-c))
                                ms4 = maximal_monotone_subroot(tau_extrema_sequence.extrema_sequence(a,b,3*a*b-c))

                                conj = check_monotone_equivalence(ms1, ms2) == check_monotone_equivalence(ms3, ms4)

                                
                                f.write(f'{a}, {b}, {c}, {conj}\n')
                                print(f'{a}, {b}, {c}', conj)
                                if not conj:
                                    f.write(f'OHHHH NOOOO: {a}, {b}, {c}')
                                    print(f'OHHHH NOOOO: {a}, {b}, {c}')
                                    break
                            

if __name__ == '__main__':
    main()