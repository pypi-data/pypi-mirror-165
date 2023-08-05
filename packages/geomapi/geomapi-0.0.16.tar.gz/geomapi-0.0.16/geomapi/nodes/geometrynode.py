"""
GeometryNode - a Python Class to govern the data and metadata of geometric data (Mesh, BIM, PCD)
"""

#IMPORT MODULES
# import resource
import numpy as np
from geomapi.nodes import Node
import geomapi.utils as ut
import geomapi.utils.geometryutils as gt

import open3d as o3d 
from rdflib import Graph, URIRef

class GeometryNode (Node):  
    def __init__(self,  graph: Graph = None, 
                        graphPath: str = None,
                        subject: URIRef = None,
                        path:str=None,
                        cartesianBounds:np.array = None,
                        orientedBounds:np.array = None,
                        orientedBoundingBox:o3d.geometry.OrientedBoundingBox = None,
                        **kwargs):
        """Creates a new Geometry Node

        Args:
            graph (Graph, optional): The RDF Graph to parse. Defaults to None.\n
            graphPath (str, optional): The path of the Graph. Defaults to None.\n
            subject (URIRef, optional): The subject to parse the Graph with. Defaults to None.\n

            cartesianBounds(np.array [6x1]): [xMin,xMax,yMin,yMax,zMin,zMax]\n
            orientedBounds (np.ndarray [8x3]): bounding points of OrientedBoundingBox \n
            orientedBoundingBox (o3d.geometry.OrientedBoundingBox)\n

        """
        #private attributes
        self._cartesianBounds=None      
        self._orientedBounds=None      
        self._orientedBoundingBox=None 

        super().__init__(   graph= graph,
                            graphPath= graphPath,
                            subject= subject,
                            path=path,        
                            **kwargs) 
        #instance variables
        self.cartesianBounds=cartesianBounds      
        self.orientedBounds=orientedBounds      
        self.orientedBoundingBox=orientedBoundingBox 

#---------------------PROPERTIES----------------------------

    #---------------------cartesianBounds----------------------------
    @property
    def cartesianBounds(self): 
        """Get the cartesianBounds (np.array [6x1]) [xMin,xMax,yMin,yMax,zMin,zMax] of the node.
        Valid inputs are:\n
        0.np.array(6x1), list (6 elements) \n
        1.Vector3dVector (n elements)\n
        2.orientedBounds (np.array(8x3))\n 
        3.Open3D.geometry.OrientedBoundingBox\n
        4.Open3D geometry\n
        """
        return self._cartesianBounds

    @cartesianBounds.setter
    def cartesianBounds(self,value):
        if value is None:
            return None
        try: #lists, np.arrays
            self._cartesianBounds=np.reshape(value,6)
        except:
            try: #orientedBounds
                box=gt.get_oriented_bounding_box(value)
                min=box.get_min_bound()
                max=box.get_max_bound()
                self._cartesianBounds=np.array([min[0],max[0],min[1],max[1],min[2],max[2]])
            except:
                try: #orientedBoundingBox
                    min=value.get_min_bound()
                    max=value.get_max_bound()
                    self._cartesianBounds=np.array([min[0],max[0],min[1],max[1],min[2],max[2]])
                except:
                    try: #Vector3dVector
                        box=gt.get_oriented_bounding_box(np.asarray(value))
                        min=box.get_min_bound()
                        max=box.get_max_bound()
                        self._cartesianBounds=np.array([min[0],max[0],min[1],max[1],min[2],max[2]])
                    except:
                        try:#resource
                            self._cartesianBounds=gt.get_cartesian_bounds(self._resource)
                        except:
                            raise ValueError('Input must be cartesianBounds (np.array [6x1]): [xMin,xMax,yMin,yMax,zMin,zMax], list like object, orientedBounds (np.Array(8x3)), or Open3D Bounding Box.')

#---------------------orientedBounds----------------------------
    @property
    def orientedBounds(self): 
        """Get the orientedBounds (np.ndarray [8x3]) bounding points of the Node.
        Valid inputs are:
        0.orientedBounds (np.array(nx3)), list (24 elements) or Vector3dVector (8 elements)
        1.Open3D.geometry.OrientedBoundingBox
        2.Open3D geometry
        """
        return self._orientedBounds

    @orientedBounds.setter
    def orientedBounds(self,value):
        if value is None:
            return None
        try: #array or list
            self._orientedBounds=np.reshape(value,(8,3))
        except:
            try: #orientedBoundingBox
                self._orientedBounds=np.asarray(value.get_box_points())
            except:
                try: #Vector3dVector
                    array=np.asarray(value)
                    self._orientedBounds=np.reshape(array,(8,3))
                except:
                    try:#resource
                        self._orientedBounds=np.asarray(value.get_oriented_bounding_box().get_box_points())
                    except:
                        raise ValueError('Input must be orientedBounds (np.ndarray [8x3]), list like object (len(24)), Vector3dVector (8 elements), or Open3D geometry required')

#---------------------orientedBoundingBox----------------------------
    @property
    def orientedBoundingBox(self): 
        """Get the orientedBoundingBox (o3d.geometry.OrientedBoundingBox) of the Node. 
        Valid inputs are:
        0.Open3D.geometry.OrientedBoundingBox
        1.Open3D geometry
        2.orientedBounds (np.array(nx3)) or Vector3dVector
        """
        return self._orientedBoundingBox

    @orientedBoundingBox.setter
    def orientedBoundingBox(self,value):
        if value is None:
            return None
        if 'orientedBoundingBox' in str(type(value)):
            self._orientedBoundingBox=value
        else:    
            try: #geometry
                self._orientedBoundingBox=value.get_oriented_bounding_box()
            except:
                try: #np.array(nx3)
                    points=o3d.utility.Vector3dVector(value)                    
                    self._orientedBoundingBox=o3d.geometry.OrientedBoundingBox.create_from_points(points)
                except:
                    try: #Vector3dVector
                        self._orientedBoundingBox=o3d.geometry.OrientedBoundingBox.create_from_points(points)
                    except:
                        raise ValueError('Input must be orientedBoundingBox (o3d.geometry.OrientedBoundingBox), an Open3D Geometry or a list of Vector3dVector objects')

#---------------------Methods----------------------------
        
    def set_resource(self,value):
        """Set the resource of the node

        Args:
            value (Open3D.geometry.PointCloud or Open3D.geometry.TriangleMesh)

        Raises:
            ValueError: Resource must be Open3D.geometry
        """
        if 'open3d' in str(type(value)):
            self._resource=value
        else:
            raise ValueError('Resource must be Open3D.geometry')

    def get_oriented_bounding_box(self)->o3d.geometry.OrientedBoundingBox:
        """Gets the Open3D OrientedBoundingBox of the node from the 
        cartesianBounds, orientedBounds, cartesianTransform or the Open3D geometry

        Returns:
            o3d.geometry.orientedBoundingBox
        """
        if self._orientedBoundingBox is not None:
            pass
        elif self._orientedBounds is not None:
            self._orientedBoundingBox=gt.get_oriented_bounding_box(self._orientedBounds)
        elif self.cartesianBounds is not None:
            self._orientedBoundingBox=gt.get_oriented_bounding_box(self._cartesianBounds)   
        elif self._cartesianTransform is not None:
                box=o3d.geometry.TriangleMesh.create_box(width=1.0, height=1.0, depth=1.0)
                boundingbox= box.get_oriented_bounding_box()
                translation=gt.get_translation(self._cartesianTransform)
                self._orientedBoundingBox= boundingbox.translate(translation)
        elif self._resource is not None:
            try:
                self._orientedBoundingBox=self._resource.get_oriented_bounding_box()
            except:
                return None
        else:
            return None
        return self._orientedBoundingBox

    def set_cartesianTransform(self,value):
        """validate cartesianTransform valid inputs are:
        0.cartesianTransform(np.ndarray(4x4))
        1.p.ndarray or Vector3dVector (1x3)  
        2.cartesianBounds (np.ndarray (6x1))
        3.np.ndarray or Vector3dVector (8x3 or nx3)
        4.Open3D.geometry
        """        
        try: #np.ndarray (4x4) 
            self._cartesianTransform=np.reshape(value,(4,4))
        except:
            try: #np.ndarray or Vector3dVector (1x3)  
                self._cartesianTransform=gt.get_cartesian_transform(translation=np.asarray(value))
            except:  
                try: # cartesianBounds (np.ndarray (6x1))
                    self._cartesianTransform=gt.get_cartesian_transform(cartesianBounds=np.asarray(value))
                except:
                    try: # np.ndarray or Vector3dVector (8x3 or nx3)
                        center=np.mean(np.asarray(value),0)
                        self._cartesianTransform=gt.get_cartesian_transform(translation=center)
                    except:
                        try: # Open3D.geometry
                            self._cartesianTransform=gt.get_cartesian_transform(translation=value.get_center())
                        except:
                            raise ValueError('Input must be np.ndarray(6x1,4x4,3x1,nx3), an Open3D geometry or a list of Vector3dVector objects.')

    def get_cartesian_transform(self) -> np.ndarray:
        """Get the cartesianTransform (translation & rotation matrix) (np.ndarray(4x4)) of the node from the 
        cartesianBounds, orientedBounds, orientedBoundingBox an Open3D geometry or a list of Vector3dVector objects.

        Returns:
            cartesianTransform(np.ndarray(4x4))
        """
        if self._cartesianTransform is not None:
            pass
        elif self._cartesianBounds is not None:
            self._cartesianTransform=gt.get_cartesian_transform(cartesianBounds=self._cartesianBounds)
        elif self._orientedBounds is not None:
            center=np.mean(self._orientedBounds,0)
            self._cartesianTransform=gt.get_cartesian_transform(translation=center)
        elif self._orientedBoundingBox is not None:
            self._cartesianTransform=gt.get_cartesian_transform(translation=self._orientedBoundingBox.get_center())
        elif self._resource is not None:
            self._cartesianTransform=gt.get_cartesian_transform(translation=self._resource.get_center())
        else:
            return None
        return self._cartesianTransform

    def get_cartesian_bounds(self) -> np.ndarray:
        """Get the cartesianBounds (np.array [6x1]) [xMin,xMax,yMin,yMax,zMin,zMax]) of the node from the 
        orientedBounds, orientedBoundingBox or resource.

        Returns:
            cartesianBounds (np.array [6x1])        
        """
        if self._cartesianBounds is not None:
            pass
        elif self._orientedBounds is not None:
            box=gt.get_oriented_bounding_box(self._orientedBounds)
            self._cartesianBounds= gt.get_cartesian_bounds(box)
        elif self._orientedBoundingBox is not None:
            self._cartesianBounds=  gt.get_cartesian_bounds(self._orientedBoundingBox)
        elif self._resource is not None:
             self._cartesianBounds=  gt.get_cartesian_bounds(self._resource)
        else:
            return None
        return self._cartesianBounds

    def get_oriented_bounds(self) -> np.ndarray:
        """Get the OrientedBounds (8 bounding points as np.array [8x3]) of the node from the 
        cartesianBounds, orientedBoundingBox or resource.

        Returns:
            OrientedBounds (np.ndarray(8x3))
        """
        if self._orientedBounds is not None:
            pass
        elif self._cartesianBounds is not None:
            self._orientedBounds=np.asarray(gt.get_oriented_bounds(self._cartesianBounds))
        elif self._orientedBoundingBox is not None:
            self._orientedBounds=  np.asarray(self._orientedBoundingBox.get_box_points())
        elif self._resource is not None:
            box=self.resource.get_oriented_bounding_box()
            self._orientedBounds=  np.asarray(box.get_box_points())
        else:
            return None
        return self._orientedBounds

    def get_center(self) -> np.ndarray:
        """Returns the center of the node.

        Returns:
            numpy.ndarray[numpy.float64[3, 1]]
        """        
        if self._cartesianBounds is not None:
            return gt.get_translation(self._cartesianBounds)
        elif self._orientedBounds is not None:
            return gt.get_translation(self._orientedBounds)
        elif self._cartesianTransform is not None:
            return gt.get_translation(self._cartesianTransform)
        elif self._orientedBoundingBox is not None:
            return self._orientedBoundingBox.get_center()
        elif self._resource is not None:
            return self._resource.get_center()
        else:
            return None    

    def visualize(self):
        vis = o3d.visualization.Visualizer()
        vis.create_window()

        if getattr(self,'mesh',None) is not None:
            vis.add_geometry(self.mesh)
        elif getattr(self,'pcd',None) is not None:
            vis.add_geometry(self.pcd)
        else:
            return None
        vis.run()
        vis.destroy_window()