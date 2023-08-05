"""
Node - an abstract Python Class to govern the data and metadata of remote sensing data (pcd, images, meshes, orthomozaik) \n

This is the base class for all other node classes. \n
It contains the base RDF graph functionality and i/o from and to RDF files. \n
   
Goals:\n
- Govern the metadata and geospatial information of big data files in an accesible and lightweight format. \n
- Serialize the metadata of remote sensing and geospatial files (BIM, Point clouds, meshes, etc.) as RDF Graphs  \n
- Attach spatial en temporal analyses through RDF Graph navigation   \n
    
"""

#IMPORT PACKAGES
from operator import contains
import os
from posixpath import relpath
import re
from typing import List
import uuid
import datetime
import numpy as np

from rdflib import Graph, URIRef, Literal
import rdflib
from rdflib.namespace import RDF

#IMPORT MODULES
import geomapi.utils as ut

class Node:
    def __init__(self,  subject: URIRef = None,
                        graph: Graph = None,
                        graphPath: str = None,                        
                        name:str=None,
                        path:str=None,
                        timestamp:str=None,
                        resource=None,
                        cartesianTransform:np.ndarray=None,
                        **kwargs):
        """Creates a Node. Overloaded function. \n
        This Node can be initialised from one or more of the inputs below.

        <ins>IMPORTANT</ins>: the Node class is an archytype class from which specific data classes (e.g. PointCloudNode) inherit.
        Do not use this class directly if you can use a child class with more functionality.

        Args:
            0.graph (Graph, optional): The RDF Graph to parse. Defaults to None. \n
            1.graphPath (str, optional): The path of the Graph. If no subject is provided, the first subject of the graph is withheld. Defaults to None.\n
            2.path(str,optional): The path of the resource. Defaults to None.\n
            3.subject (URIRef, optional): The subject of the Node. If a graph is also present, the subject should be part of the graph. Defaults to None.\n
            4.name (str, optional): Name of the subject.\n
        Returns:
            Node
        """
        #private attributes 
        self._subject=None
        self._graph=None
        self._graphPath=None 
        self._path=None
        self._name=None
        self._timestamp=None 
        self._resource=None 
        self._cartesianTransform=None

        #instance variables
        self.subject=subject
        self.graphPath=graphPath
        self.graph=graph
        self.path=path        
        self.name=name
        self.timestamp=timestamp
        self.resource=resource 
        self.cartesianTransform=cartesianTransform

        #initialisation functionality
        if self._path:
            self.name=ut.get_filename(path)
            if  os.path.exists(self._path):
                self.timestamp=ut.get_timestamp(path) 

        if(graphPath and os.path.exists(self._graphPath) and not self._graph):
            self._graph = Graph().parse(graphPath) 

        self.get_subject()      
        if(self._graph):
            if ut.check_if_subject_is_in_graph(self._graph,self._subject):
                self._graph=ut.get_subject_graph(self._graph,self._subject)
                self.get_metadata_from_graph(self._graph,self._subject) 
            elif 'session' in str(type(self)):
                pass
            else:
                raise ValueError( 'Subject not in graph')
        self.__dict__.update(kwargs)

#---------------------PROPERTIES----------------------------

    #---------------------PATH----------------------------
    @property
    def path(self): 
        """Get the resource path (str) of the node. \n
        If no path is present, a path is reconstructed from either 
        the graphPath or working directory (folder,self.name,nodeExtensions[0]).
        """        
        return self._path
    
    @path.setter
    def path(self,path):
        if path is None:
            return None
        nodeExtensions=ut.get_node_resource_extensions(str(type(self)))
        if (type(path) is str and ut.get_extension(path) in nodeExtensions):
            self._path=path
        else:
            raise ValueError('self.path has invalid type, path or extension')

    #---------------------NAME----------------------------
    @property
    def name(self):
        """Get the name (str) of the node. \n
        This can include characters that the operating
        system does not allow. If no name is provided, 
        it is gathered from the path or graph upon initialisation."""        
        return self._name

    @name.setter
    def name(self,name):
        if name is None:
            return None
        try: 
            self._name=str(name)
        except:
            raise TypeError('self.name should be string compatible')

    #---------------------TIMESTAMP----------------------------
    @property
    def timestamp(self):
        """Get the timestamp (yyyy-MM-ddTHH:mm:ss) of the node. \n
        If no timestamp is provided, it is gathered from the path or graphPath."""
        return self._timestamp

    @timestamp.setter
    def timestamp(self,timestamp):
        if timestamp is None:
            return None
        elif timestamp:
            self._timestamp=ut.validate_timestamp(timestamp)
        else:
            raise ValueError('timestamp should be str(yyyy-MM-ddTHH:mm:ss)')

    #---------------------GRAPHPATH----------------------------    
    @property
    def graphPath(self):
        """Get the path (str) of graph of the node, or the graph in which the subject is contained."""
        return self._graphPath

    @graphPath.setter
    def graphPath(self,graphPath):
        if graphPath is None:
            return None
        elif (type(graphPath) == str and 
              next(graphPath.endswith(extension) for extension in ut.RDF_EXTENSIONS) ):
            self._graphPath=graphPath
        else:
            raise ValueError('self.graphPath has invalid type, path or extension')    

    #---------------------GRAPH----------------------------    
    @property
    def graph(self):
        """Get the graph (RDFLib.Graph) of the node."""       
        # self._graph =self.to_graph()      # this is expensive!       
        return self._graph

    @graph.setter
    def graph(self,graph):
        if graph is None:
            return None
        elif (type(graph) is rdflib.Graph):
            self._graph=graph
        else:
            raise TypeError('type(graph) should be rdflib.Graph')    

    #---------------------SUBJECT----------------------------    
    @property
    def subject(self):
        """Get the subject (RDFLib.URIRef) of the node. \n
        If no subject is present, it is gathered 
        from the graph, name, or path. Otherwise, a random guid is generated."""
        return self._subject

    @subject.setter
    def subject(self,subject):
        if subject is None:
            return None
        elif type(subject) is rdflib.URIRef:
            self._subject=subject
        else:
            string=str(subject)
            prefix='file:///'
            if 'file:///' in string:
                string=string.replace('file:///','')
                prefix='file:///'
            elif 'http://' in string:
                string=string.replace('http://','')
                prefix='http://' 
            self._subject=URIRef(prefix+ut.validate_string(string))  
    
    #---------------------RESOURCE----------------------------    
    @property
    def resource(self):
        """Get the resource (mesh, pcd, etc.) of the node. \n
        If no resource is present, it is gathered from the path. 
        This is the parent could which is specified at every child node."""        
        return self._resource

    @resource.setter
    def resource(self,value):
        if value is None:
            return None
        else:
            self.set_resource(value)

    @resource.deleter
    def resource(self):
        self._resource=None
        #This will be depricated. use resource instead
        if getattr(self,'mesh',None) is not None:
            self._mesh=None
        if getattr(self,'image',None) is not None:
            self._image=None
        if getattr(self,'pcd',None) is not None:
            self._pcd=None
        if getattr(self,'ortho',None) is not None:
            self._ortho=None
         
    #---------------------CARTESIANTRANSFORM----------------------------    
    @property
    def cartesianTransform(self):
        """Get the Cartesian Transform (translation & rotation matrix) (np.ndarray(4x4)) of the node.\n
        Note that the initialisation from different inputs may result in different cartesianTransform values.\n
        E.g. the pose of a mesh is retrieved from the mean of the vertices,
             while the same pose initiated from the cartesianBounds equals the mean of that cartesianBounds array."""      
        return self._cartesianTransform

    @cartesianTransform.setter
    def cartesianTransform(self,value):
        if value is None:
            return None
        else:
            self.set_cartesianTransform(value)

#---------------------METHODS----------------------------     
    def get_metadata_from_graph(self, graph:Graph,subject:URIRef):
        """Convert the data contained in a graph to a set of node attributes. \n 
        If the graph contains multiple subjects, it is reduced to the subject's triples. \n
        The use of a SessionNode is advised when dealing with multi-subject graphs.\n

        Args:
            self.graph (RDFlib.Graph):  Graph to parse\n
            self.subject (RDFlib.URIRef): The subject to parse the graph for
        
        """
        if len([x for x in self._graph.subjects(RDF.type)])>1:
            self._graph=ut.get_subject_graph(graph,subject)

        for predicate, object in graph.predicate_objects(subject=subject):
            attr= ut.get_attribute_from_predicate(graph, predicate) 
            value=object.toPython()
            
            #GEOMETRY
            if attr == 'cartesianBounds':
                self.cartesianBounds=ut.literal_to_array(object) 
            elif attr == 'orientedBounds':
                self.orientedBounds=ut.literal_to_orientedBounds(object) 
            elif attr == 'cartesianTransform':
                self.cartesianTransform=ut.literal_to_cartesianTransform(object) 
            elif attr == 'geospatialTransform':
                self.geospatialTransform=ut.literal_to_array(object)    
            #PATHS
            elif re.search('path', attr, re.IGNORECASE):
                path=ut.literal_to_string(object)
                if path and self._graphPath:
                    if '..' in path:
                        path=path.strip('..\\')
                        folder=ut.get_folder_path(ut.get_folder_path(self._graphPath))
                    else:
                        folder=ut.get_folder_path(self._graphPath)
                    path=os.path.join(folder,path)
                setattr(self,attr,path)
                    
            #INT    
            elif attr in ut.INT_ATTRIBUTES:
                setattr(self,attr,ut.literal_to_int(object)) 
            #FLOAT
            elif attr in ut.FLOAT_ATTRIBUTES:
                setattr(self,attr,ut.literal_to_float(object)) 
            #LISTS
            elif attr in ut.LIST_ATTRIBUTES:
                setattr(self,attr,ut.literal_to_list(object)) 
            #LINKEDSUBEJCTS
            elif attr == 'linkedSubjects':
                # test=ut.literal_to_linked_subjects(object)
                # self.linkedSubjects=test
                setattr(self,attr,ut.literal_to_linked_subjects(object)) 
            
            #STRINGS
            else:
                setattr(self,attr,object.toPython()) 

    def get_subject(self) -> str:
        """Returns and validates the current subject. \n
        If empty, a new subject is created based on a unique GUID. \n

        Returns:
            subject (URIREF)
        """
        #subject
        if self._subject:
            pass
        # self.graph
        elif self._graph:
            self._subject=next(self._graph.subjects(RDF.type))
        #self.path
        elif self._path:
            self._name=ut.get_filename(self._path)
            self._subject=URIRef('file:///'+ut.validate_string(self._name))
        elif self._name:
            self._subject=URIRef('file:///'+ut.validate_string(self._name))
        #guid
        else:
            self._name=str(uuid.uuid1())
            self._subject=URIRef('file:///'+self._name)            
        return self._subject

    def get_timestamp(self):
        """Get the timestamp (str) of the Node.\n
        This can be retrieved from user input, the path, the graphPath or the current time.\n

        Returns:
            timestamp (str): '%Y-%m-%dT%H:%M:%S'
        """
        if self._timestamp is None:
            if self._path and os.path.exists(self._path):
                self._timestamp=ut.get_timestamp(self._path)  
            elif self._graphPath and os.path.exists(self._graphPath):
                self._timestamp=ut.get_timestamp(self._graphPath)  
            else:
                self._timestamp=datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        return self._timestamp

    def get_name(self) -> str:
        """Returns the name (str) of the Node.\n

        Returns:
           name (str)
        """
        if self._name is None:
            if self._path:
                self._name=ut.get_filename(self._path)
            else:                     
                self._name=ut.get_subject_name(self.subject)
        return self.name

    def set_cartesianTransform(self,value):
        """sets the cartesianTransform for the Node type. Overwrite this function for each node type
        """
        # print("This is the base Node functionality, overwite for each childNode to retrieve the relevant cartesianTransform")

    def get_cartesianTransform(self):
        """Returns the cartesianTransform from the Node type. Overwrite this function for each node type"""
        # print("This is the base Node functionality, overwite for each childNode to retrieve the relevant cartesianTransform")

    def get_resource(self):
        """Returns the resource from the Node type. Overwrite this function for each node type
        """
        # print("This is the base Node functionality, overwite for each childNode to import the relevant resource type")

    def set_resource(self,value):
        """sets the resource for the Node type. Overwrite this function for each node type
        """
        # print("This is the base Node functionality, overwite for each childNode to import the relevant resource type")


    def clear_resource(self):
        """Clear all geometries (images, pcd, meshes, ortho's, etc.) in the Node.
        """
        if getattr(self,'resource',None) is not None:
            self.resource=None

        # #TEMP
        # if getattr(self,'mesh',None) is not None:
        #     self.mesh=None
        # if getattr(self,'image',None) is not None:
        #     self.image=None
        # if getattr(self,'pcd',None) is not None:
        #     self.pcd=None
        # if getattr(self,'ortho',None) is not None:
        #     self.ortho=None
            
    def get_path(self) -> str:
        """Find the full path of the resource from this Node.\n

        Valid inputs are:\n
            self._graphPath and (self._name or self._subject)

        Returns:
            path (str)
        """      
        if self._path and os.path.exists(self._path):
            return self._path
        
        elif self._graphPath and (self._name or self._subject):
            folder=ut.get_folder_path(self._graphPath)
            nodeExtensions=ut.get_node_resource_extensions(str(type(self)))
            allSessionFilePaths=ut.get_list_of_files(folder) 
            for path in allSessionFilePaths:
                if ut.get_extension(path) in nodeExtensions:
                    if self.get_name() in path or self.get_subject() in path :
                        self._path = path    
                        return self._path
            if self._name:
                self._path=os.path.join(folder,self._name+nodeExtensions[0])
            else:
                self._path=os.path.join(folder,self._subject+nodeExtensions[0])
            return self._path
        else:
            # print("No file containing this object's name and extension is found in the graphPath folder")
            return None

    def get_graph(self):
        """Returns the graph of the Node.\n

        Valid inputs are:\n
            self._graphPath and/or self._subject)\n

        Returns:
            graph (RDFlib.GRAPH)
        """
        if self._graph is None:
            if self._graphPath and os.path.exists(self._graphPath):
                self._graph=Graph().parse(self._graphPath)
                if self._subject and ut.check_if_subject_is_in_graph(self._graph,self._subject):
                    self._graph=ut.get_subject_graph(self._graph,self._subject)
                else:
                    print( 'Subject not in Graph')
        return self._graph

    def to_graph(self, graphPath : str = None, overwrite:bool=True,save:bool=False) -> Graph:
        """Converts the current Node variables to a graph and optionally save it

        Args:
            graphPath (str, optional): The full path to write the graph to. Defaults to None.\n
            overwrite (bool, optional=True): Overwrite current graph values or not\n
            save (bool, optional=False): Save the graph to the self.graphPath or graphPath.\n
        """
        if graphPath and next(graphPath.endswith(extension) for extension in ut.RDF_EXTENSIONS) :
            self._graphPath=graphPath

        self._graph=Graph() 
        ut.bind_ontologies(self._graph)      
        nodeType=ut.get_node_type(str(type(self)))                
        self._graph.add((self.subject, RDF.type, nodeType ))  

        # enumerate attributes in node and write them to triples
        attributes = ut.get_variables_in_class(self)
        attributes = ut.clean_attributes_list(attributes)        
        pathlist = ut.get_paths_in_class(self)
                
        for attribute in attributes: 
            predicate = ut.match_uri(attribute)
            value=getattr(self,attribute)
            
            if value is not None:
                dataType=ut.get_data_type(value)
                temp=dataType.toPython()
                predtemp=predicate.toPython()

                if self._graph.value(self._subject, predicate, None)== str(value):
                    continue

                #check if exists
                elif overwrite:
                    self._graph.remove((self._subject, predicate, None))

                if 'linkedSubjects' in attribute:
                    if len(value) !=0:
                        value=[subject.toPython() for subject in self.linkedSubjects]
                    else:
                        continue
                
                elif attribute in pathlist:
                    if (self._graphPath):
                        folderPath=ut.get_folder_path(self.graphPath)
                        try:
                            value=os.path.relpath(value,folderPath)
                        except:
                            pass
                if 'string' not in dataType.toPython():        
                    self._graph.add((self._subject, predicate, Literal(value,datatype=dataType)))
                else:
                    self._graph.add((self._subject, predicate, Literal(value)))

        #Save graph
        if(save):
            self.save_graph(graphPath)            
        return self._graph

    def save_graph(self,graphPath : str = None) -> bool:
        """Serialize the graph in an RDF file on drive.\n
        The RDF graph will be stored in self._graphPath or provided graphPath (str)

        Args:
            graphPath (str, optional): Defaults to None.\n

        Raises:
            ValueError: No valid graphPath if file/folder location is not found\n
            ValueError: No valid extension if not in ut.RDF_EXTENSIONS\n
            ValueError: Save failed despite valid graphPath and extension (serialization error).

        Returns:
            bool: True if file is succesfully saved
        """
        #check path validity
        if(graphPath and ut.check_if_path_is_valid(graphPath)): 
            self._graphPath=graphPath
        elif ut.check_if_path_is_valid(self._graphPath):
            pass
        else: 
            raise ValueError('No valid graphPath.')
        #check extension
        if (ut.get_extension(graphPath) not in ut.RDF_EXTENSIONS):
            raise ValueError(''.join(ut.RDF_EXTENSIONS) + ' currently are only supported extensions.')

        try: 
            # f= open(self._graphPath, 'w') 
            # base=ut.get_folder(self.graphPath)
            self._graph.serialize(self._graphPath)#,base=base
            # f.close()
            if os.path.exists(self._graphPath):                
                return True

            return False
        except:
            raise ValueError('Save failed despite valid graphPath.') 

###############################################
