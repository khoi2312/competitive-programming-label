import os
from pathlib import Path
import logging
import pandas as pd
from tqdm import tqdm
from collections import namedtuple

import networkx as nx
from tree_sitter import Parser, Node

from common import draw_graph, initialize_cpp_tree_sitter, add_string_literal

from torch_geometric.data import Data
from torch_geometric.utils.convert import from_networkx


StringLiteral = namedtuple('StringLiteral', ['value'])
DATA_PATH = "../data/cpreprocess/"
FILE_NAMES = os.listdir(DATA_PATH)

print(len(FILE_NAMES))

EdgeColors = {
    "Child" : "black",
    "ReturnTo" : "yellow",
    "LastLexicalUsed" : "orange",
    "LastUse" : "red",
    "ComputedFrom" : "purple",
    "NextToken" : "blue",
    "LastWrite" : "green"
}

CPP_LANGUAGE = initialize_cpp_tree_sitter()
# CPP Parser
parser = Parser()
parser.set_language(CPP_LANGUAGE)
    
def add_self_loop(G : nx.DiGraph, node : Node, edge_attr : str, color : str):
    G.add_edge(node, node, type = edge_attr, color = color)
    return G

def make_edge_attribute(G : nx.DiGraph, f_node : Node, s_node: Node, edge_attr : str, color : str):
    G.add_edge(f_node, s_node, type = edge_attr, color = color)
    return G
    
def tree_to_graph(root):
    G = nx.Graph()
    
    todo = [root]
    NextTokenNodes = []
    LastReadNodes = {"level" : 0}
    LastWriteNodes = {"level" : 0}
    LastLexicalUsedNodes = dict()
    ComputedFromNodes = []

    FunctionDefinitionId = None

    x = [[root.type, ""]]
    edge_index = [[], []]
    edge_attr = [[], []]

    # Make edges based on leaf nodes
    while todo:
        node = todo.pop()
        node_text = node.text.decode("utf-8")
        #print(node_text)

        G.add_node(node.id, label = add_string_literal(node.type))
        x.append([node.type, node_text])

        # Return To Edges
        if node.type == "function_definition":
            FunctionDefinitionId = node.id
        if node.type == "return":
            edge_attr = "ReturnTo"
            if FunctionDefinitionId is not None:
                G = make_edge_attribute(G, node.id, FunctionDefinitionId, edge_attr= edge_attr, color = EdgeColors[edge_attr])
            #edge_index[0].append(node.id)
            #edge_index[1].append(FunctionDefinitionId)

        # Leaf of AST Trees
        if node.children == []: #Last node in branch

            # Next Token nodes
            NextTokenNodes.append(node.id)
            
            
            # Get node text
            if "literal" in node.type or "identifier" in node.type or "type" in node.type:
                G.nodes[node.id]["label"] = add_string_literal(node.type + "_" + node_text)
            
            if "identifier" in node.type:
                # Last Lexical Used Nodes
                if node_text in LastLexicalUsedNodes.keys():
                    edge_attr = "LastLexicalUsed"
                    G = make_edge_attribute(G,LastLexicalUsedNodes[node_text], node.id, edge_attr= edge_attr, color = EdgeColors[edge_attr])
                    LastLexicalUsedNodes[node_text] = node.id
                else:
                    LastLexicalUsedNodes[node_text] = node.id

        else:
            for child in node.children:                
                # Make Child Edges
                edge_attr = "Child"
                G = make_edge_attribute(G, node.id, child.id, edge_attr= edge_attr, color = EdgeColors[edge_attr])

                # Add child node into process loop
                todo.append(child)
        
        # Make Computed From Edges
        if "assignment" in node.type:
            CFRoot = [node]
            while CFRoot:
                cfnode = CFRoot.pop()
                if "identifier" in cfnode.type:
                    ComputedFromNodes.append(cfnode.id)

                for child in cfnode.children:
                    CFRoot.append(child)

            ComputedFromNodes.append(node.id)

        if ComputedFromNodes != []:
            edge_attr = "ComputedFrom"
            f_node_id = ComputedFromNodes[-1]
            
            for idx in range(1,len(ComputedFromNodes)):
                s_node_id = ComputedFromNodes[-idx - 1]
                G = make_edge_attribute(G, f_node_id, s_node_id , edge_attr= edge_attr, color = EdgeColors[edge_attr])


            ComputedFromNodes = []
            
    # Make Next Token Edges
    edge_attr = "NextToken"
    for idx in range(len(NextTokenNodes) - 1):
        G = make_edge_attribute(G, NextTokenNodes[-idx], NextTokenNodes[-idx -1], edge_attr= edge_attr, color = EdgeColors[edge_attr])
    
    return G


def ast_transform(source_code : str):
    tree = parser.parse(bytes(source_code, "utf-8"))
    root = tree.root_node
    
    ast = tree_to_graph(root)
    
    return ast

def pyg_graph_transform(source_code : str):
    logfile = open("log.txt", "a")
    try:
        ast = ast_transform(source_code)
    except:
        #logfile.write(str(source_code) + "\n")
        #logfile.write("______________")
        ast = None


    #pyg_data = from_networkx(ast)
    
    #print(pyg_data.edge_index)
    #print(pyg_data.num_nodes)
    #print(pyg_data.type)

    return ast

def main():
    er_contest = []
    for fn in tqdm(FILE_NAMES[:]):
        
        df = pd.read_csv(open(DATA_PATH + fn, 'r'), encoding='utf-8', engine='c')
        
        df["graph"] = df["source_code"].apply(lambda x : pyg_graph_transform(x))

        #with open("sample.cpp", "r") as infile:
        #    source_code = infile.read()
        
        #src_code_graph = pyg_graph_transform(source_code)
        #draw_graph(src_code_graph, "type")
        #nx.drawing.nx_pydot.write_dot(src_code_graph, "sample.dot")
        #break

if __name__ == "main":
    main()

