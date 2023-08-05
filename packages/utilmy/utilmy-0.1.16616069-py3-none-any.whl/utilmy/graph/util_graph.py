""" Network DAG Processing

Docs::

  https://www.timlrx.com/blog/benchmark-of-popular-graph-network-packages

  The benchmark was carried out using a Google Compute n1-standard-16 instance (16vCPU Haswell 2.3GHz, 60 GB memory). I compare 5 different packages:

  graph-tool
  igraph
  networkit
  networkx
  snap

  Full results can be seen from the table below:


  dataset	Algorithm	graph-tool	igraph	networkit	networkx	snap
  Google	connected components	0.32	2.23	0.65	21.71	2.02
  Google	k-core	0.57	1.68	0.06	153.21	1.57
  Google	loading	67.27	5.51	17.94	39.69	9.03
  Google	page rank	0.76	5.24	0.12	106.49	4.16
  Google	shortest path	0.20	0.69	0.98	12.33	0.30

  Pokec	connected components	1.35	17.75	4.69	108.07	15.28
  Pokec	k-core	5.73	10.87	0.34	649.81	8.87
  Pokec	loading	119.57	34.53	157.61	237.72	59.75
  Pokec	page rank	1.74	59.55	0.20	611.24	19.52
  Pokec	shortest path	0.86	0.87	6.87	67.15	3.09

https://networkit.github.io/


"""
import os, glob, sys, math, time, json, functools, random, yaml, gc, copy, pandas as pd, numpy as np
import datetime
from box import Box
from typing import Union
import warnings ;warnings.filterwarnings("ignore")
from warnings import simplefilter  ; simplefilter(action='ignore', category=FutureWarning)
with warnings.catch_warnings():
    pass


from utilmy import pd_read_file, os_makedirs, pd_to_file, glob_glob


#############################################################################################
from utilmy import log, log2, os_module_name

def help():
    """function help        """
    from utilmy import help_create
    print( help_create(__file__) )



#############################################################################################
def test_all() -> None:
    """ python  $utilmy/deeplearning/util_topk.py test_all         """
    log(os_module_name(__file__))
    test1()


def test1():
    pass


############################################################################################################################
def dag_create_network(df_or_file: Union[str,pd.DataFrame], cola, colb, colvertex=""):
    """Convert a panadas dataframe into a NetworKit graph
    Docs::
                     df   :    dataframe[[ cola, colb, colvertex ]]
        cola='col_node1'  :  column name of node1
        colb='col_node2'  :  column name of node2
        colvertex=""      :  weight

    """
    import networkit as nk, gc

    if isinstance(df_or_file, str):
        df = pd_read_file(df_or_file)
    else :
        df = df_or_file

    #### not clear ?
    arr = np.unique(df[[cola, colb]].values)
    arr+= 1
    graph = nk.Graph(max(arr), edgesIndexed=False)
    del arr ; gc.collect()   ### save memory

    df = df[[cola, colb]].values
    for i in range(len(df)):
        graph.addEdge( df[i, 0], df[i, 0])
    return graph




def dag_pagerank(net):
   pass




def dag_save(net, dirout):
   pass



def dag_load(dirin=""):
   pass





############################################################################################################################
def pd_plot_network(df:pd.DataFrame, cola: str='col_node1', 
                    colb: str='col_node2', coledge: str='col_edge',
                    colweight: str="weight",html_code:bool = True):
    """  Function to plot network https://pyviz.org/tools.html
    Docs::

            df                :        dataframe with nodes and edges
            cola='col_node1'  :        column name of node1
            colb='col_node2'  :        column name of node2
            coledge='col_edge':        column name of edge
            colweight="weight":        column name of weight
            html_code=True    :        if True, return html code
    """

    def convert_to_networkx(df:pd.DataFrame, cola: str="", colb: str="", colweight: str=None):
        """
        Convert a panadas dataframe into a networkx graph
        and return a networkx graph
        Docs::

                df                :        dataframe with nodes and edges
        """
        import networkx as nx
        import pandas as pd
        g = nx.Graph()
        for index, row in df.iterrows():
            g.add_edge(row[cola], row[colb], weight=row[colweight],)

        nx.draw(g, with_labels=True)
        return g


    def draw_graph(networkx_graph, notebook:bool =False, output_filename='graph.html',
                   show_buttons:bool =True, only_physics_buttons:bool =False,html_code:bool  = True):
        """  This function accepts a networkx graph object, converts it to a pyvis network object preserving
        its node and edge attributes,
        and both returns and saves a dynamic network visualization.
        Valid node attributes include:
            "size", "value", "title", "x", "y", "label", "color".
            (For more info: https://pyvis.readthedocs.io/en/latest/documentation.html#pyvis.network.Network.add_node)

        Docs::

                networkx_graph: The graph to convert and display
                notebook: Display in Jupyter?
                output_filename: Where to save the converted network
                show_buttons: Show buttons in saved version of network?
                only_physics_buttons: Show only buttons controlling physics of network?
        """
        from pyvis import network as net
        import re
        # make a pyvis network
        pyvis_graph = net.Network(notebook=notebook)

        # for each node and its attributes in the networkx graph
        for node, node_attrs in networkx_graph.nodes(data=True):
            pyvis_graph.add_node(str(node), **node_attrs)

        # for each edge and its attributes in the networkx graph
        for source, target, edge_attrs in networkx_graph.edges(data=True):
            # if value/width not specified directly, and weight is specified, set 'value' to 'weight'
            if not 'value' in edge_attrs and not 'width' in edge_attrs and 'weight' in edge_attrs:
                # place at key 'value' the weight of the edge
                edge_attrs['value'] = edge_attrs['weight']
            # add the edge
            pyvis_graph.add_edge(str(source), str(target), **edge_attrs)

        # turn buttons on
        if show_buttons:
            if only_physics_buttons:
                pyvis_graph.show_buttons(filter_=['physics'])
            else:
                pyvis_graph.show_buttons()

        # return and also save
        pyvis_graph.show(output_filename)
        if html_code:

          def extract_text(tag: str,content: str)-> str:
            reg_str = "<" + tag + ">\s*((?:.|\n)*?)</" + tag + ">"
            extracted = re.findall(reg_str, content)[0]
            return extracted
          with open(output_filename) as f:
            content = f.read()
            head = extract_text('head',content)
            body = extract_text('body',content)
            return head, body
    networkx_graph = convert_to_networkx(df, cola, colb, colweight=colweight)
    head, body = draw_graph(networkx_graph, notebook=False, output_filename='graph.html',
               show_buttons=True, only_physics_buttons=False,html_code = True)
    return head, body







###############################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()




