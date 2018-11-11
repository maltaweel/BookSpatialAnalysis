'''
Analysis to look at all possible areas traversed based on road segments and starting points within road segments.

Created on Nov 7, 2018

@author: mark
'''
import pysal
import os
import math
import matplotlib.pyplot as plt
import networkx as nx
import graph
import csv

oldNodes={}
nodes={}
links=[]
nodesS=[]
linkz={}

'''
Load the data and creating the links for the network from street segment file.
@param fileName the shapefile name to assess.
'''
def load(fileName):
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
        
    #The data file path is now created where the data folder and dataFile.csv is referenced
    path=os.path.join(pn,'data')
        
    filename=path+'/'+fileName

    shp = pysal.open(filename)
    
    node1=0
    node2=0
    i = 1
    
    for s in shp:

        
        for p in s._vertices:
           
            node1=p[0]
            nodesS.append(node1)
            
            s1=str(str(node1[0])+":"+str(node1[1]))
            
            node2=p[1]
            s2=str(str(node2[0])+":"+str(node2[1]))
            
            bol=inNodes(node1,nodes)
            if bol is False:
                nodes[node1[0]]=node1[1]
                oldNodes[s1]=node1
            
            else:
                node1=oldNodes[s1]
            
            bol2=inNodes(node2,nodes)
            if bol2 is False:
                nodes[node2[0]]=node2[1]
                oldNodes[s2]=node2
            
            else:
                node2=oldNodes[s2]
                  
            weight=math.fabs(node1[0]-node2[0])+math.fabs(node1[1]-node2[1])
            link=(node1,node2,weight)
            link2=(node1,node2)
            links.append(link)
            linkz[str(link2)]=link
           
                
                
        
        i+=1
    
     
    G=graph.addWeightedEdges(links)
    
    return G
    
'''
Applying the shortest path algorithm from each point of the road segments
@param G the road network
'''
def runLinks(G):
    
    nodes=G.nodes
    nodes2=G.nodes
#    pos = nx.spring_layout(G)
#   nx.draw(G,pos,node_color='k')
    edgesS={}
    for n in nodes:
        for n2 in nodes2:
            if n2==n:
                continue
            else:
                path = nx.shortest_path(G,weight='weight',source=n,target=n2)
                path_edges = zip(path,path[1:])
                
                for e in path_edges:
                    if str(e) in edgesS:
                        nn=edgesS[str(e)]
                        edgesS[str(e)]=nn+1
                    else:
                        edgesS[str(e)]=1
                    
                    
    return edgesS
        
    
'''
Printing the output based on edges traversed from the network and the network.
@param edgesS is segments traversed
@param G the road network
''' 
def output(edgesS,G):
#   pos = nx.spring_layout(G)
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    p=os.path.join(pn,'output')
        
    filename=p+'/'+'results.csv'
        
    fieldnames = ['id','x','y','count']
        
    with open(filename, 'wb') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        writer.writeheader()
            
        i=0
        for ie in linkz:
            count=edgesS[ie]
            link=linkz[ie]
            node1=link[0]
            node2=link[1]
            writer.writerow({'id':i,'x':str(node1[0]),'y':str(node1[1]), 'count' :str(count)})
            writer.writerow({'id':i,'x':str(node2[0]),'y':str(node2[1]), 'count' :str(count)})
            i+=1
            print("Edges:"+ str(ie))
        
#    nx.draw_networkx_nodes(G,pos,nodelist=path,node_color='r')
#    nx.draw_networkx_edges(G,pos,edgelist=path_edges,edge_color='r',width=10)
#    plt.axis('equal')
#    plt.show()
        
    return G
        
'''
Method for checking to see if the nodes already part of the road network
@param node the node to check
@param the container for the nodes to check from.
'''
def inNodes(node, nodes):
    iNodes=False
    if node[0] in nodes:
            y=node[1]
            if nodes[node[0]]==y:
                iNodes=True
                
    return iNodes

'''
Method to call and run the analysis.
'''
fileName='Dura_street_segments.shp'
G=load(fileName)
edgesS=runLinks(G)
output(edgesS,G)