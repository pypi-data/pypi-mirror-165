"""
linkeddatatools - a Python library for RDF graph structuring and exchange.
"""
#IMPORT PACKAGES
from dis import dis
from lib2to3.pytree import Node
import numpy as np 
import cv2 
import open3d as o3d 
import os 
import re
import pye57 #conda install xerces-c  =>  pip install pye57
import xml.etree.ElementTree as ET 
from typing import List,Tuple

# import APIs
import rdflib
from rdflib import Graph, plugin
from rdflib.serializer import Serializer #pip install rdflib-jsonld https://pypi.org/project/rdflib-jsonld/
from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
                           PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
                           VOID, XMLNS, XSD
import ifcopenshell
import ifcopenshell.geom as geom
import ifcopenshell.util
from ifcopenshell.util.selector import Selector
import multiprocessing

#IMPORT MODULES 
from geomapi.nodes import *
from geomapi.nodes.sessionnode import create_node 
import geomapi.utils as ut
import geomapi.utils.geometryutils as gt

from warnings import warn

#### NODE CREATION ####

def e57xml_to_nodes(e57XmlPath :str, **kwargs) -> List[PointCloudNode]:
    """Parse XML file that is created with E57lib e57xmldump.exe.

    Args:
        path (string):  e57 xml file path e.g. "D:\\Data\\2018-06 Werfopvolging Academiestraat Gent\\week 22\\PCD\\week 22 lidar_CC.xml"
            
    Returns:
        A list of pointcloudnodes with the xml metadata 
    """
    if os.path.exists(e57XmlPath) and e57XmlPath.endswith('.xml'):    
        #E57 XML file structure
        #e57Root
        #   >data3D
        #       >vectorChild
        #           >pose
        #               >rotation
        #               >translation
        #           >cartesianBounds
        #           >guid
        #           >name
        #           >points recordCount
        #   >images2D
        mytree = ET.parse(e57XmlPath)
        root = mytree.getroot()  
        nodelist=[]   
        e57Path=e57XmlPath.replace('.xml','.e57')       

        for idx,child in enumerate(root.iter('{http://www.astm.org/COMMIT/E57/2010-e57-v1.0}vectorChild')):
            nodelist.append(PointCloudNode(e57XmlPath=e57XmlPath,e57Index=idx,path=e57Path,**kwargs))
        return nodelist
    else:
        raise ValueError('No valid e57XmlPath.')

def img_xml_to_nodes(xmlPath :str, **kwargs) -> List[ImageNode]:
    """Parse XML file that is created with https://www.agisoft.com/.

    Args:
        path (string):  e57 xml file path e.g. "D:\\Data\\2018-06 Werfopvolging Academiestraat Gent\\week 22\\PCD\\week 22 lidar_CC.xml"
            
    Returns:
        A list of pointcloudnodes with the xml metadata 
    """
    if os.path.exists(xmlPath) and xmlPath.endswith('.xml'):    
        mytree = ET.parse(xmlPath)
        root = mytree.getroot()  
        nodelist=[]   
        for child in root.iter('camera'):
            nodelist.append(ImageNode(xmlPath=xmlPath,name=child.get('label'),**kwargs))
        return nodelist
    else:
        raise ValueError('No valid xmlPath.')

def e57header_to_nodes(e57Path:str, **kwargs) -> List[PointCloudNode]:
    """
    Parse e57 file header that is created with E57lib e57xmldump.exe.

    Args:
        path (string):  e57 xml file path e.g. "D:\\Data\\2018-06 Werfopvolging Academiestraat Gent\\week 22\\PCD\\week 22 lidar_CC.xml"
            
    Returns:
        A list of pointcloudnodes with the xml metadata 
    """
    if os.path.exists(e57Path) and e57Path.endswith('.e57'):    

        nodelist=[]   
        e57 = pye57.E57(e57Path)   
        for idx in range(e57.scan_count):
            nodelist.append(PointCloudNode(path=e57Path,e57Index=idx, **kwargs))
        return nodelist
    else:
        raise ValueError('No valid e57Path.')

def ifc_to_nodes(ifcPath:str, classes:str='.IfcBuildingElement',getResource : bool=True,**kwargs)-> List[BIMNode]:
    """
    Parse ifc file to a list of BIMNodes, one for each ifcElement.\n

    **NOTE**: classes are not case sensitive. It is advised to solely focus on IfcBuildingElement classes or inherited classes as these typically have geometry representations that can be used by GEOMAPI.

    **NOTE**: If you intend to parse 1000+ elements, use the multithreading of the entire file instead and filter the BIMNodes afterwards as it will be faster. 

    **WARNING**: IfcOpenShell strugles with some ifc serializations. In our experience, IFC4 serializations is more robust.

    .. image:: ../docs/pics/ifc_inheritance.PNG

    Args:
        1. ifcPath (string):  absolute ifc file path e.g. "D:\\myifc.ifc"\n
        2. classes (string, optional): ifcClasses seperated by | e.g. '.IfcBeam | .IfcColumn '#'.IfcWall | .IfcSlab | .IfcBeam | .IfcColumn | .IfcStair | .IfcWindow | .IfcDoor'. Defaults to '.IfcBuildingElement'.   
    
    Raises:
        ValueError: 'No valid ifcPath.'

    Returns:
        List[BIMNode]
    """   
    if os.path.exists(ifcPath) and ifcPath.endswith('.ifc'):    
        nodelist=[]   
        ifc = ifcopenshell.open(ifcPath)   
        selector = Selector()
        for ifcElement in selector.parse(ifc, classes):
            # print(ifcElement.Name) # THIS IS TEMP
            node=BIMNode(resource=ifcElement,getResource=getResource, **kwargs)          
            node.ifcPath=ifcPath
            nodelist.append(node)
        return nodelist
    else:
        raise ValueError('No valid ifcPath.')


def ifc_to_nodes_by_type(ifcPath:str, types:list=['IfcBuildingElement'],getResource : bool=True,**kwargs)-> List[BIMNode]:
    """
    Parse ifc file to a list of BIMNodes, one for each ifcElement.\n

    **NOTE**: classes are not case sensitive. It is advised to solely focus on IfcBuildingElement classes or inherited classes as these typically have geometry representations that can be used by GEOMAPI.

    **WARNING**: IfcOpenShell strugles with some ifc serializations. In our experience, IFC4 serializations is more robust.

    .. image:: ../docs/pics/ifc_inheritance.PNG

    Args:
        1. ifcPath (string):  absolute ifc file path e.g. "D:\\myifc.ifc"\n
        2. types (list of strings, optional): ifcClasses you want to parse e.g. ['IfcWall','IfcSlab','IfcBeam','IfcColumn','IfcStair','IfcWindow','IfcDoor']. Defaults to ['IfcBuildingElement']. \n  
    
    Raises:
        ValueError: 'No valid ifcPath.'

    Returns:
        List[BIMNode]
    """   
    #validate types

    if os.path.exists(ifcPath) and ifcPath.endswith('.ifc'):    
        try:
            ifc_file = ifcopenshell.open(ifcPath)
        except:
            print(ifcopenshell.get_log())
        else:
            nodelist=[]   
            for type in types:
                ifcElements = ifc_file.by_type(type)
                for ifcElement in ifcElements:
                    node=BIMNode(resource=ifcElement,getResource=getResource, **kwargs)          
                    node.ifcPath=ifcPath
                    nodelist.append(node)
            return nodelist
    else:
        raise ValueError('No valid ifcPath.')

def ifc_to_nodes_multiprocessing(ifcPath:str, **kwargs)-> List[BIMNode]:
    """Returns the contents of geometry elements in an ifc file as BIMNodes.\n
    This method is 3x faster than other parsing methods due to its multi-threading.\n
    However, only the entire ifc can be parsed.\n

    **WARNING**: IfcOpenShell strugles with some ifc serializations. In our experience, IFC4 serializations is more robust.


    Args:
        ifcPath (str): path (string):  absolute ifc file path e.g. "D:\\myifc.ifc"\n

    Raises:
        ValueError: 'No valid ifcPath.'

    Returns:
        List[BIMNode]
    """
    if os.path.exists(ifcPath) and ifcPath.endswith('.ifc'):  
        try:
            ifc_file = ifcopenshell.open(ifcPath)
        except:
            print(ifcopenshell.get_log())
        else: 
            nodelist=[]   
            timestamp=ut.get_timestamp(ifcPath)
            settings = ifcopenshell.geom.settings()
            settings.set(settings.USE_WORLD_COORDS, True) 
            iterator = ifcopenshell.geom.iterator(settings, ifc_file, multiprocessing.cpu_count())
            if iterator.initialize():
                while True:
                    shape = iterator.get()
                    ifcElement = ifc_file.by_guid(shape.guid) 
                    faces = shape.geometry.faces # Indices of vertices per triangle face e.g. [f1v1, f1v2, f1v3, f2v1, f2v2, f2v3, ...]
                    verts = shape.geometry.verts # X Y Z of vertices in flattened list e.g. [v1x, v1y, v1z, v2x, v2y, v2z, ...]
                    # materials = shape.geometry.materials # Material names and colour style information that are relevant to this shape
                    # material_ids = shape.geometry.material_ids # Indices of material applied per triangle face e.g. [f1m, f2m, ...]

                    # Since the lists are flattened, you may prefer to group them per face like so depending on your geometry kernel
                    grouped_verts = [[verts[i], verts[i + 1], verts[i + 2]] for i in range(0, len(verts), 3)]
                    grouped_faces = [[faces[i], faces[i + 1], faces[i + 2]] for i in range(0, len(faces), 3)]

                    #Convert grouped vertices/faces to Open3D objects 
                    o3dVertices = o3d.utility.Vector3dVector(np.asarray(grouped_verts))
                    o3dTriangles = o3d.utility.Vector3iVector(np.asarray(grouped_faces))

                    # Create the Open3D mesh object
                    mesh=o3d.geometry.TriangleMesh(o3dVertices,o3dTriangles)

                    #if mesh, create node
                    if len(mesh.triangles)>1:
                        node=BIMNode(**kwargs)
                        node.name=ifcElement.Name
                        node.className=ifcElement.is_a()
                        node.globalId=ifcElement.GlobalId
                        if node.name and node.globalId:
                            node.subject= node.name +'_'+node.globalId 
                        node.resource=mesh
                        node.get_metadata_from_resource()
                        node.timestamp=timestamp
                        node.ifcPath=ifcPath
                        nodelist.append(node)
                        
                    if not iterator.next():
                        break
            return nodelist
    else:
        raise ValueError('No valid ifcPath.') 


##### NODE SELECTION #####

def select_k_nearest_nodes(node:Node,nodelist:List[Node],k:int=10) -> Tuple[List [Node], o3d.utility.DoubleVector]:
    """ Select k nearest nodes based on Euclidean distance between centroids.\n

    .. image:: ../docs/pics/selection_k_nearest.PNG

    Args:
        0. node (Node): node to search from\n
        1. nodelist (List[Node])\n
        2. k (int, optional): number of neighbors. Defaults to 10.\n

    Returns:
        List of Nodes
    """
    if k <=0:
        raise ValueError('k must be positive and non-negative.')

    #get node center
    if node.get_cartesian_transform() is not None:
        point=gt.get_translation(node.cartesianTransform)
        #create pcd from nodelist centers
        pcd = o3d.geometry.PointCloud()
        array=np.empty(shape=(len(nodelist),3))
        for idx,node in enumerate(nodelist):
            if node.get_cartesian_transform() is not None:
                array[idx]=gt.get_translation(node.cartesianTransform)
            else:
                array[idx]=[-10000.0,-10000.0,-10000.0]
        pcd.points = o3d.utility.Vector3dVector(array)

        #Create KDTree from pcd
        pcdTree = o3d.geometry.KDTreeFlann(pcd)

        #Find 200 nearest neighbors
        _, idxList, distances = pcdTree.search_knn_vector_3d(point, k)
        selectedNodeList=[node for idx,node in enumerate(nodelist) if idx in idxList]

        if any(selectedNodeList):        
            return selectedNodeList, distances
    else:
        return None,None

def select_nodes_with_centers_in_radius(node:Node,nodelist:List[Node],r:float=0.5) -> List [Node]:
    """Select nodes within radius of the node centroid based on Euclidean distance between node centroids.\n

    .. image:: ../docs/pics/selection_radius_nearest.PNG
    
    Args:
        0. node (Node): node to search from\n
        1. nodelist (List[Node])\n
        2. r (float, optional): radius to search. Defaults to 0.5m.\n

    Returns:
        List of Nodes
    """
    
    if r <=0:
        raise ValueError('r must be positive and non-negative.')
    #get node center
    if node.get_cartesian_transform() is not None:
        point=gt.get_translation(node.cartesianTransform)
        #create pcd from nodelist centers
        pcd = o3d.geometry.PointCloud()
        array=np.empty(shape=(len(nodelist),3))
        for idx,node in enumerate(nodelist):
            if node.get_cartesian_transform() is not None:
                array[idx]=gt.get_translation(node.cartesianTransform)
            else:
                array[idx]=[-10000.0,-10000.0,-10000.0]
        pcd.points = o3d.utility.Vector3dVector(array)

        #Create KDTree from pcd
        pcdTree = o3d.geometry.KDTreeFlann(pcd)

        #Find 200 nearest neighbors
        [_, idxList, distances] = pcdTree.search_radius_vector_3d(point, r)
        selectedNodeList=[node for idx,node in enumerate(nodelist) if idx in idxList ]
        selectedNodeList=[node for i,node in enumerate(selectedNodeList) if distances[i]<=r ]
        
        if any(selectedNodeList):        
            return selectedNodeList,distances
    else:
        return None,None

def select_nodes_with_centers_in_bounding_box(node:Node,nodelist:List[Node],u:float=0.5,v:float=0.5,w:float=0.5) -> List [Node]: 
    """Select the nodes of which the center lies within the oriented Bounding Box of the source node given an offset.\n

    .. image:: ../docs/pics/selection_box_inliers.PNG
    
    Args:
        0. node (Node): source Node \n
        1. nodelist (List[Node]): target nodelist\n
        2. u (float, optional): Offset in X. Defaults to 0.5m.\n
        3. v (float, optional): Offset in Y. Defaults to 0.5m.\n
        4. w (float, optional): Offset in Z. Defaults to 0.5m.\n

    Returns:
        List [Node]
    """
    #get box source node
    if node.get_oriented_bounding_box() is not None:
        box=node.orientedBoundingBox
        box=gt.expand_box(box,u=u,v=v,w=w)

        # get centers
        centers=np.empty((len(nodelist),3),dtype=float)
        for idx,node in enumerate(nodelist):
            if node.get_cartesian_transform() is not None:
                centers[idx]=gt.get_translation(node.cartesianTransform)

        #points are the centers of all the nodes
        pcd = o3d.geometry.PointCloud()
        points = o3d.utility.Vector3dVector(centers)
        pcd.points=points

        # Find the nodes that lie within the index box 
        idxList=box.get_point_indices_within_bounding_box(points)
        selectedNodeList=[node for idx,node in enumerate(nodelist) if idx in idxList]
        if any(selectedNodeList):        
            return selectedNodeList
    else:
        return None

def select_nodes_with_bounding_points_in_bounding_box(node:Node,nodelist:List[Node],u:float=0.5,v:float=0.5,w:float=0.5) -> List [Node]: 
    """Select the nodes of which atleast one of the bounding points lies within the oriented Bounding Box of the source node given an offset.\n

    .. image:: ../docs/pics/selection_BB_intersection.PNG
    
    Args:
        0. node (Node): source Node \n
        1. nodelist (List[Node]): target nodelist\n
        2. u (float, optional): Offset in X. Defaults to 0.5m.\n
        3. v (float, optional): Offset in Y. Defaults to 0.5m.\n
        4. w (float, optional): Offset in Z. Defaults to 0.5m.\n

    Returns:
        List [Node]
    """
    #get box source node
    if node.get_oriented_bounding_box() is not None:
        box=node.orientedBoundingBox
        box=gt.expand_box(box,u=u,v=v,w=w)

        # get boxes nodelist
        boxes=np.empty((len(nodelist),1),dtype=o3d.geometry.OrientedBoundingBox)
        for idx,node in enumerate(nodelist):
            boxes[idx]=node.get_oriented_bounding_box()

        # Find the nodes of which the bounding points lie in the source node box
        idxList=gt.get_box_inliers(box,boxes)
        selectedNodeList=[node for idx,node in enumerate(nodelist) if idx in idxList]
        if any(selectedNodeList):        
            return selectedNodeList
    else:
        return None
    
def select_nodes_with_intersecting_bounding_box(node:Node,nodelist:List[Node],u:float=0.5,v:float=0.5,w:float=0.5) -> List [Node]: 
    """Select the nodes of which the bounding boxes intersect.\n

    .. image:: ../docs/pics/selection_BB_intersection2.PNG

    Args:
        0. node (Node): source Node \n
        1. nodelist (List[Node]): target nodelist\n
        2. u (float, optional): Offset in X. Defaults to 0.5m.\n
        3. v (float, optional): Offset in Y. Defaults to 0.5m.\n
        4. w (float, optional): Offset in Z. Defaults to 0.5m.\n

    Returns:
        List [Node]
    """
    #get box source node
    if node.get_oriented_bounding_box() is not None:
        box=node.orientedBoundingBox
        box=gt.expand_box(box,u=u,v=v,w=w)

        # get boxes nodelist
        boxes=np.empty((len(nodelist),1),dtype=o3d.geometry.OrientedBoundingBox)
        for idx,node in enumerate(nodelist):
            boxes[idx]=node.get_oriented_bounding_box()
        
        # Find the nodes of which the bounding box itersects with the source node box
        idxList=gt.get_box_intersections(box,boxes)
        selectedNodeList=[node for idx,node in enumerate(nodelist) if idx in idxList]
        if any(selectedNodeList):        
            return selectedNodeList
    else:
        return None

def select_nodes_with_intersecting_resources(node:Node,nodelist:List[Node]) -> List [Node]: 
    """Select the nodes of which the o3d.geometry.TriangleMeshes intersect.\n
    This method relies on trimesh and fcl libraries for collision detection.\n
    For PointCloudNodes, the convex hull is used.\n
    For ImageNodes, a virtual mesh cone is used with respect to the field of view.\n

    .. image:: ../docs/pics/collision_5.PNG

    Args:
        0. node (Node): source Node \n
        1. nodelist (List[Node]): target nodelist\n

    Returns:
        List [Node] 
    """
    #get geometry source node
    if node.get_resource() is not None: 
        mesh=get_mesh_representation(node)
        # get geometries nodelist        
        # meshes=np.empty((len(nodelist),1),dtype=o3d.geometry.TriangleMesh)
        
        meshes=[None]*len(nodelist)
        for idx,testnode in enumerate(nodelist):
            if testnode.get_resource() is not None: 
                    meshes[idx]=get_mesh_representation(testnode)

        # Find the nodes of which the geometry itersects with the source node box
        idxList=gt.get_mesh_inliers(reference=mesh,sources=meshes)

        # idxList=gt.get_mesh_collisions_trimesh(mesh,meshes)
        selectedNodeList=[node for idx,node in enumerate(nodelist) if idx in idxList]
        if any(selectedNodeList):        
            return selectedNodeList
    return None

#### GRAPH CREATION #####

def get_mesh_representation(node: Node)->o3d.geometry.TriangleMesh:
    """Returns the mesh representation of a node resource\n
    Returns the convex hull if it is a PointCloudNode.\n
    For ImageNodes, a virtual mesh cone is used with respect to the field of view.

    Args:
        Node

    Returns:
        o3d.geometry.TriangleMesh 
    """
    nodeType=str(type(node))
    resource= node.get_resource()
   
    if 'PointCloudNode' in str(type(node)):
        hull, _ =resource.compute_convex_hull()
        return hull
    elif 'ImageNode' in nodeType:
        return node.get_mesh_geometry()
    elif 'OrthoNode' in nodeType:
        print('not implemented')
        return None
    else:
        return resource

def nodes_to_graph(nodelist : List[Node], graphPath:str =None, overwrite: bool =False,save: bool =False) -> Graph:
    """Convert list of nodes to an RDF graph.\n

    Args:
        0. nodelist (List[Node])\n
        1. graphPath (str, optional): path that serves as the basepath for all path information in the graph. This is also the storage location of the graph.\n
        2. overwrite (bool, optional): Overwrite the existing graph triples. Defaults to False.\n
        3. save (bool, optional): Save the Graph to file. Defaults to False.\n

    Returns:
        Graph 
    """
    g=Graph()
    g=ut.bind_ontologies(g)
    for node in nodelist:
            node.to_graph(graphPath,overwrite=overwrite)
            g+= node.graph
    if(graphPath and save):
        g.serialize(graphPath)     
    return g  

#### OBSOLETE #####

def graph_path_to_nodes(graphPath : str,**kwargs) -> List[Node]:
    """Convert a graphPath to a set of Nodes.

    Args:
        0. graphPath (str):  absolute path to .ttl RDF Graph\n
        1. kwargs (Any) \n

    Returns:
        A list of pointcloudnodes, imagenodes, meshnodes, bimnodes, orthonodes with metadata 
    """    
    if os.path.exists(graphPath) and graphPath.endswith('.ttl'):
        nodelist=[]
        graph=Graph().parse(graphPath)
        for subject in graph.subjects(RDF.type):
            myGraph=ut.get_subject_graph(graph,subject)
            nodelist.append(create_node(graph=myGraph,graphPath=graphPath,subject=subject,**kwargs) )
        return nodelist
    else:
        raise ValueError('No valid graphPath (only .ttl).')

def graph_to_nodes(graph : Graph,**kwargs) -> List[Node]:
    """Convert a graph to a set of Nodes.

    Args:
        0. graph (RDFlib.Graph):  Graph to parse\n
        1. kwargs (Any) \n

    Returns:
        A list of pointcloudnodes, imagenodes, meshnodes, bimnodes, orthonodes with metadata 
    """    
    nodelist=[]
    for subject in graph.subjects(RDF.type):
        node=create_node(graph=graph,subject=subject,**kwargs) 
        nodelist.append(node)
    return nodelist

# def subject_to_node_type(graph: Graph , subject:URIRef, **kwargs)-> Node:
#     # warn("This function is depricated use a SessionNode instead")

#     nodeType = ut.literal_to_string(graph.value(subject=subject,predicate=RDF.type))
#     g = Graph()
#     g += graph.triples((subject, None, None))
#     if 'BIMNode' in nodeType:
#         node=BIMNode(graph=g,**kwargs)
#     elif 'MeshNode' in nodeType:
#         node=MeshNode(graph=g,**kwargs)
#     elif 'PointCloudNode' in nodeType:
#         node=PointCloudNode(graph=g,**kwargs)
#     elif 'ImageNode' in nodeType:
#         node=ImageNode(graph=g,**kwargs)
#     elif 'SessionNode' in nodeType:
#         node=SessionNode(graph=g,**kwargs)  
#     else:
#         node=Node(graph=g,**kwargs) 
#     return node
def create_node(graph: Graph = None, graphPath: str =None, subject: URIRef = None, resource = None, **kwargs)-> Node:
    """_summary_

    Args:
        graph (Graph, optional): _description_. Defaults to None.
        graphPath (str, optional): _description_. Defaults to None.
        subject (URIRef, optional): _description_. Defaults to None.

    Returns:
        Node (PointCloudNode,MeshNode,GeometryNode,ImageNode)
    """
    #input validation
    if(graphPath and not graph):
            graph = Graph().parse(graphPath)
    if(graph and not subject):
        subject=next(graph.subjects(RDF.type))
    if (subject and graph):    
        nodeType = ut.literal_to_string(graph.value(subject=subject,predicate=RDF.type))
    elif (resource):
        if type(resource) is o3d.geometry.PointCloud:
            nodeType='PointCloudNode'
        elif type(resource) is o3d.geometry.TriangleMesh:
            nodeType='MeshNode'
        elif type(resource) is o3d.geometry:
            nodeType='GeometryNode'
        elif type(resource) is np.ndarray:
            nodeType='ImageNode'        
    else:        
        nodeType = 'Node'

    #node creation
    if 'BIMNode' in nodeType:
        node=BIMNode(graph=graph, graphPath=graphPath, resource=resource,subject=subject, **kwargs)
    elif 'MeshNode' in nodeType:
        node=MeshNode(graph=graph, graphPath=graphPath, resource=resource, subject=subject, **kwargs)
    elif 'GeometryNode' in nodeType:
        node=GeometryNode(graph=graph, graphPath=graphPath, resource=resource, subject=subject, **kwargs)
    elif 'PointCloudNode' in nodeType:
        node=PointCloudNode(graph=graph, graphPath=graphPath, resource=resource, subject=subject, **kwargs)
    elif 'ImageNode' in nodeType:
        node=ImageNode(graph=graph, graphPath=graphPath, resource=resource, subject=subject, **kwargs)
    elif 'SessionNode' in nodeType:
        node=SessionNode(graph=graph, graphPath=graphPath, resource=resource, subject=subject, **kwargs)  
    else:
        node=Node(graph=graph, graphPath=graphPath, resource=resource, subject=subject, **kwargs) 
    return node

def get_linked_nodes(node: Node ,graph:Graph, getResource=False, **kwargs) -> List[Node]:
    """Get related nodes based on linkedNodes variable.\n

    Args:
        0. node (Node): source node to evaluate. \n
        1. graph (Graph): Graph that contains the linkedNodes. \n
        2. getResource (bool, optional): Retrieve the reources. Defaults to False.\n

    Returns:
        List[Node]
    """
    warn("This function is depricated use a SessionNode instead")
    nodelist=[]
    if getattr(node,'linkedNodes',None) is not None:  
        for subject in node.linkedNodes:
            if graph.value(subject=subject,predicate=RDF.type) is not None:
                nodelist.append(create_node(graph=graph,subject=subject, getResource=getResource, **kwargs)) 
    return nodelist