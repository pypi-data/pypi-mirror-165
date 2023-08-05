"""
ImageNode - a Python Class to govern the data and metadata of image data (OpenCV, PIL). \n

This node builds upon the OpenCV and PIL API for the image definitions.\n
It directly inherits from Node.\n
Be sure to check the properties defined in the above classes to initialise the Node.
"""
#IMPORT PACKAGES
from ast import Raise
from distutils import extension
import xml.etree.ElementTree as ET
import cv2
import PIL
from rdflib import Graph, URIRef
import numpy as np
import os
import open3d as o3d
import math
import uuid
from scipy.spatial.transform import Rotation as R


#IMPORT MODULES
from geomapi.nodes import Node
import geomapi.utils as ut
import geomapi.utils.geometryutils as gt


class ImageNode(Node):
    # class attributes
    
    def __init__(self,  graph : Graph = None, 
                        graphPath:str=None,
                        subject : URIRef = None,
                        path : str=None, 
                        xmpPath: str = None,
                        xmlPath: str = None,
                        getResource : bool = False,
                        getMetaData : bool = True,
                        **kwargs): 
        """
        Creates a ImageNode. Overloaded function.\n
        This Node can be initialised from one or more of the inputs below.\n
        By default, no data is imported in the Node to speed up processing.\n
        If you also want the data, call node.get_resource() or set getResource() to True.\n

        Args: \n
            0.graph (RDFlib Graph) : Graph with a single subject (if multiple subjects are present, only the first will be used to initialise the MeshNode)\n
            
            1.graphPath (str):  Graph file path with a single subject (if multiple subjects are present, only the first will be used to initialise the MeshNode)\n

            2.path (str) : path to image file (Note that this node will also contain the data) \n

            3.resource (ndarray, PIL Image,Open3D) : OpenCV, PIL (Note that this node will also contain the data)\n

            4.xmlPath (str) : Xml file path from Agisoft Metashape\n

            5.xmpPath (str) :  xmp file path from RealityCapture

            getResource (bool, optional= False): If True, the node will search for its physical resource on drive \n

        Returns:
            A ImageNode with metadata 
        """  
        #private attributes 
        self._xmlPath=None
        self._xmpPath=None
        self.imageWidth = None # (int) number of pixels
        self.imageHeight = None  # (int) number of pixels
        self.focalLength35mm = None # (Float) focal length in mm     

        super().__init__(   graph= graph,
                            graphPath= graphPath,
                            subject= subject,
                            path=path,
                            **kwargs)   

        #instance variables
        self.xmlPath=xmlPath
        self.xmpPath=xmpPath

        #initialisation functionality
        if getMetaData:
            if self.get_metadata_from_xmp_path():
                pass
            elif self.get_metadata_from_xml_path():
                pass

        if getResource:
            self.get_resource()

        if getMetaData:
            self.get_metadata_from_exif_data()
            self.get_metadata_from_resource()

#---------------------PROPERTIES----------------------------

    #---------------------xmlPath----------------------------
    @property
    def xmlPath(self): 
        """Get the xmlPath (str) of the node."""
        return self._xmlPath

    @xmlPath.setter
    def xmlPath(self,value):
        if value is None:
            return None
        elif (type(value) == str and value.endswith('xml') ):
            self._xmlPath=value
        else:
            raise ValueError('self.xmlPath has invalid type, path or extension')    

  #---------------------xmpPath----------------------------
    @property
    def xmpPath(self): 
        """Get the xmpPath (str) of the node."""
        return self._xmpPath

    @xmpPath.setter
    def xmpPath(self,value):
        if value is None:
            return None
        elif (type(value) == str and value.endswith('xmp') ):
            self._xmpPath=value
        else:
            raise ValueError('self.xmpPath has invalid type, path or extension')    

#---------------------METHODS----------------------------
   
    def set_resource(self,value):
        """Set self.resource (np.ndarray) of the Node.\n

        Args:
            1. np.ndarray (OpenCV) \n
            2. PIL Image\n
            3. Open3D Image

        Raises:
            ValueError: Resource must be np.ndarray (OpenCV), PIL Image or Open3D Image.
        """

        if type(value) is np.ndarray : #OpenCV
            self._resource = value
        elif 'Image' in str(type(value)): # PIL
            self._resource=  cv2.cvtColor(np.array(value), cv2.COLOR_RGB2BGR)
        else:
            raise ValueError('Resource must be np.ndarray (OpenCV) or PIL Image')

    def get_resource(self)->np.ndarray: 
        """Returns the image data in the node. \n
        If none is present, it will search for the data on drive from path, graphPath, name or subject. 

        Returns:
            np.ndarray or None
        """
        if self.resource is not None :
            pass
        elif self.get_path():
            self._resource   = cv2.imread(self.path)
        return self._resource  

    def get_path(self) -> str:
        """Find the full path of the resource from this Node.\n

        Valid inputs are:\n
            self._graphPath and (self._name or self._subject)

        Returns:
            path (str)
        """      
        if self._path and os.path.exists(self._path):
            return self._path
        nodeExtensions=ut.get_node_resource_extensions(str(type(self)))
        if self._graphPath and (self._name or self._subject):
            folder=ut.get_folder_path(self._graphPath)
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
        elif self._xmpPath and os.path.exists(self._xmpPath):
            folder=ut.get_folder_path(self._xmpPath)
            allSessionFilePaths=ut.get_list_of_files(folder) 
            for path in allSessionFilePaths:
                if ut.get_extension(path) in nodeExtensions:
                    if ut.get_filename(self._xmpPath) in path :
                        self.name=ut.get_filename(self._xmpPath)
                        self.subject=self._name
                        self.path = path    
                        return self._path
        elif self._xmlPath and os.path.exists(self._xmlPath):
            folder=ut.get_folder_path(self._xmlPath)
            allSessionFilePaths=ut.get_list_of_files(folder) 
            for path in allSessionFilePaths:
                if ut.get_extension(path) in nodeExtensions:
                    if self.get_name() in path or self.get_subject() in path :
                        self._path = path    
                        return self._path
        else:
            # print("No file containing this object's name and extension is found in the graphPath folder")
            return None

    def get_xmp_path(self)->str: 
        """Returns the xmpPath in the node. \n
        If none is present, it will search for the data on drive from path, graphPath, name or subject. 

        Returns:
            str or None
        """
        if self._xmpPath and os.path.exists(self._xmpPath):
            return self._xmpPath            
        elif self._graphPath and (self._name or self._subject):
            folder=ut.get_folder_path(self._graphPath)
            allSessionFilePaths=ut.get_list_of_files(folder) 
            for path in allSessionFilePaths:
                if ut.get_extension(path).endswith('xmp'):
                    if self.get_name() in path or self.get_subject() in path :
                        self._xmpPath = path    
                        return self._xmpPath
        else:
            return None

    def save_resource(self, directory:str=None,extension :str = '.png') ->bool:
        """Export the resource of the Node.\n

        Args:
            directory (str, optional): directory folder to store the data.\n
            extension (str, optional): file extension. Defaults to '.png'.\n

        Raises:
            ValueError: Unsuitable extension. Please check permitted extension types in utils._init_.\n

        Returns:
            bool: return True if export was succesful
        """     
        #check path
        if self.resource is None:
            return False
        
        # check if already exists
        if directory and os.path.exists(os.path.join(directory,self.get_name() + extension)):
            return True
        elif not directory and self.get_path() and os.path.exists(self.path) and extension in ut.IMG_EXTENSION:
            return True    
          
        #get directory
        if (directory):
            pass    
        elif self.path is not None and os.path.exists(self.path):    
            directory=ut.get_folder(self.path)            
        elif(self.graphPath): 
            dir=ut.get_folder(self.graphPath)
            directory=os.path.join(dir,'IMG')   
        else:
            directory=os.path.join(os.getcwd(),'IMG')
        # create directory if not present
        if not os.path.exists(directory):                        
            os.mkdir(directory)       

        #check extension
        if extension in ut.IMG_EXTENSION:
            self.path=os.path.join(directory,ut.get_filename(self.subject.toPython()) + extension)
        else:
            raise ValueError('Erroneous extension ')
        #write files
        if cv2.imwrite(self.path, self.resource):
            return True
        return False
       
    def get_metadata_from_resource(self) ->bool:
        """Returns the metadata from a resource. \n

        Features:
            imageHeight\n
            imageWidth\n

        Returns:
            bool: True if exif data is successfully parsed
        """
        if self._resource is None:
            return False   
              
        try:
            if getattr(self,'imageHeight',None) is None:
                self.imageHeight=self.resource.shape[0]
            if getattr(self,'imageWidth',None) is None:
                self.imageWidth=self.resource.shape[1]
            return True
        except:
            raise ValueError('Metadata extraction from resource failed')
    
    # def get_oriented_bounding_box(self)->o3d.geometry.OrientedBoundingBox:
    #     """Gets the Open3D geometry from cartesianTransform

    #     Returns:
    #         o3d.geometry.orientedBoundingBox
    #     """
    #     if getattr(self,'orientedBoundingBox',None) is None:                
    #         if getattr(self,'cartesianTransform',None) is not None:
    #             box=o3d.geometry.create_mesh_box(width=1.0, height=1.0, depth=1.0)
    #             self.orientedBoundingBox= box.transform(self.cartesianTransform)
    #         else:
    #             return None
    #     return self.orientedBoundingBox

    def get_mesh_geometry(self, depth:float=10, focalLength35mm:float=24)->o3d.geometry.TriangleMesh:
        """Generate a concical mesh representation using the Image's cartesianTransform and focalLength35mm.
    
        .. image:: ../docs/pics/virtual_image2.PNG

        Args:
            depth (float, optional): Viewing depth of the image. Defaults to 10m.
            focalLength35mm (float,optional): standardised focal length on 35mm film (w=36mm, h = 24mm)

        Returns:
            o3d.geometry.TriangleMesh: 
        """
        
        if self.cartesianTransform is not None:
            radius=35/(focalLength35mm*2)*depth        
            mesh= o3d.geometry.TriangleMesh.create_cone(radius=radius, height=depth, resolution=20, split=1)
            rotation=gt.get_rotation_matrix(self.cartesianTransform)
            r=R.from_matrix(rotation)
            rz=R.from_euler('xyz' ,[180, 0, 0], degrees=True)
            t=gt.get_translation(self.cartesianTransform)
            mesh=mesh.translate(t)
            r=rz*r
            # t2=r.as_matrix() * np.array([[1],[0],[0]]) *depth
            A = np.dot( r.as_matrix(),np.array([0,0,-1]) )*depth
            mesh=mesh.translate(A)
            rot=r.as_matrix()
            mesh=mesh.rotate(rot)

            return mesh
        else:
            return None

    def get_virtual_image(self, geometries: o3d.geometry, downsampling:int=2)-> o3d.cpu.pybind.geometry.Image:
        pinholeCamera=self.get_pinhole_camera_parameters(downsampling)
        if pinholeCamera is not None:
            return gt.generate_virtual_image(geometries,pinholeCamera)
        else:
            return None

    def get_pinhole_camera_parameters(self, downsampling:int=2) -> o3d.camera.PinholeCameraParameters():
        param=o3d.camera.PinholeCameraParameters()
        if getattr(self,'cartesianTransform',None) is not None:
            param.extrinsic=np.linalg.inv(self.cartesianTransform)
            param.intrinsic=self.get_intrinsic_camera_parameters(downsampling)
            self.pinholeCamera=param
            return self.pinholeCamera
        else:
            return None

    def get_intrinsic_camera_parameters(self, downsampling:int=2) -> o3d.camera.PinholeCameraIntrinsic():

        width=640
        height=480
        f=25

        if getattr(self,'imageWidth',None) is not None:
            width=int(self.imageWidth/downsampling)
        if getattr(self,'imageHeight',None) is not None:
            height=int(self.imageHeight/downsampling)
        if getattr(self,'focalLength35mm',None) is not None:
            f=self.focalLength35mm

        pixX=width/36 #these are standard 35mm film properties
        pixY=height/24 #these are standard 35mm film properties
        fx=pixX*f
        fy=pixY*f

        if (getattr(self,'principalPointU',None) is not None and
            getattr(self,'principalPointV',None) is not None ):
            cx=width/2-0.5+self.principalPointU
            cy=height/2-0.5+self.principalPointV
        else:
            cx=width/2-0.5
            cy=height/2-0.5
        return o3d.camera.PinholeCameraIntrinsic(width,height,fx,fy,cx,cy)

    def get_metadata_from_exif_data(self) -> bool:
        """Returns the metadata from a resource. \n

        Features:
            GPSInfo (geospatialTransform (np.array(3,1)),coordinateSystem (str)) \n
            DateTime\n
            XResolution\n
            YResolution\n
            ResolutionUnit \n
            ExifImageWidth \n
            ExifImageHeight \n

        Returns:
            bool: True if meta data is successfully parsed
        """
        if  self.get_path() is None or not os.path.exists(self.get_path()) :
            return False
        
        if getattr(self,'timestamp',None) is None :
            self.timestamp=ut.get_timestamp(self.path)
        
        if getattr(self,'name',None) is None:
            self.name=ut.get_filename(self.path)

        if (getattr(self,'imageWidth',None) is not None and
            getattr(self,'imageHeight',None) is not None and
            getattr(self,'geospatialTransform',None) is not None):
            return True

        # pix = PIL.Image.open(self.path) 
        with PIL.Image.open(self.path) as pix:
            exifData=ut.get_exif_data(pix)

        if exifData is not None:
            self.timestamp=ut.get_if_exist(exifData, "DateTime")
            self.resolutionUnit=ut.get_if_exist(exifData,"ResolutionUnit")
            self.imageWidth=ut.get_if_exist(exifData,"ExifImageWidth")
            self.imageHeight=ut.get_if_exist(exifData,"ExifImageHeight")
            
            if 'GPSInfo' in exifData:
                gps_info = exifData["GPSInfo"]
                if gps_info is not None:
                    # self.GlobalPose=GlobalPose # (structure) SphericalTranslation(lat,long,alt), Quaternion(qw,qx,qy,qz)
                    latitude=ut.get_if_exist(gps_info, "GPSLatitude")
                    latReference=ut.get_if_exist(gps_info, "GPSLatitudeRef")
                    newLatitude=ut.filter_exif_gps_data(latitude,latReference)
                    longitude= ut.get_if_exist(gps_info, "GPSLongitude")
                    longReference=ut.get_if_exist(gps_info, "GPSLongitudeRef")
                    newLongitude=ut.filter_exif_gps_data(longitude,longReference)
                    self.geospatialTransform=[  newLatitude, 
                                                newLongitude,
                                                ut.get_if_exist(gps_info, "GPSAltitude")]
                    self.coordinateSystem='geospatial-wgs84'
            
            return True
        else:
            return False
    
    def get_metadata_from_xmp_path(self)->bool:
        """Read Metadata from .xmp file generated by https://www.capturingreality.com/

        Features:
            geospatialTransform\n
            coordinateSystem\n
            focalLength35mm\n
            principalPointU\n
            principalPointV \n
            cartesianTransform \n

        Returns:
            bool: True if metadata is sucesfully parsed
        """
        if self.xmpPath is None or not os.path.exists(self.xmpPath):
            return False

        if (getattr(self,'principalPointU',None) is not None and
            getattr(self,'principalPointV',None) is not None and
            getattr(self,'distortionCoeficients',None) is not None and
            getattr(self,'geospatialTransform',None) is not None ):         
            return True
        
        mytree = ET.parse(self.xmpPath)
        root = mytree.getroot()                       
        
        self.timestamp=ut.get_timestamp(self.xmpPath)
        self.name=ut.get_filename(self.xmpPath)
        self.subject=self.name
        for child in root.iter('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description'):

            #Attributes
            for attribute in child.attrib:
                if ('latitude' in attribute and
                    'longitude'in attribute and
                    'altitude' in attribute):
                    lat=ut.xcr_to_lat(child.attrib['{http://www.capturingreality.com/ns/xcr/1.1#}latitude'])
                    long=ut.xcr_to_long(child.attrib['{http://www.capturingreality.com/ns/xcr/1.1#}longitude'])
                    alt=ut.xcr_to_alt(child.attrib['{http://www.capturingreality.com/ns/xcr/1.1#}altitude'])
                    self.geospatialTransform=np.array([lat, long, alt])
                if 'Coordinates' in attribute:
                    self.coordinateSystem=child.attrib[attribute]
                if 'FocalLength35mm' in attribute:
                    self.focalLength35mm=ut.xml_to_float(child.attrib[attribute])
                if 'PrincipalPointU' in attribute:
                    self.principalPointU=ut.xml_to_float(child.attrib[attribute])
                if 'PrincipalPointV' in attribute:
                    self.principalPointV=ut.xml_to_float(child.attrib[attribute])

            #Nodes
            rotationnode=child.find('{http://www.capturingreality.com/ns/xcr/1.1#}Rotation')
            rotation=None
            if rotationnode is not None:
                rotation=ut.string_to_rotation_matrix(rotationnode.text)

            positionnode=child.find('{http://www.capturingreality.com/ns/xcr/1.1#}Position')
            translation=None
            if positionnode is not None:
                translation=np.asarray(ut.string_to_list(positionnode.text))
             
            self.cartesianTransform=gt.get_cartesian_transform(translation=translation,rotation=rotation)
            
            coeficientnode=child.find('{http://www.capturingreality.com/ns/xcr/1.1#}DistortionCoeficients')
            if coeficientnode is not None:
                self.distortionCoeficients=ut.string_to_list(coeficientnode.text)  
        return True   

    def get_metadata_from_xml_path(self) ->bool:
        """Extract image metadata from XML Node generated by Agisoft Metashape (self.xmlData and self.subject should be present).

        Features:
            cartesianTransform\n
            sxy\n
            sz \n

        Returns:
            bool: True if metadata is sucesfully parsed
        """
        if self.xmlPath is None or not os.path.exists(self.xmlPath):
            return False

        if (getattr(self,'cartesianTransform',None) is not None and
            getattr(self,'sxy',None) is not None and
            getattr(self,'sz',None) is not None ):
            return True
        
        self.timestamp=ut.get_timestamp(self.xmlPath)        
        mytree = ET.parse(self.xmlPath)
        root = mytree.getroot()          
        xmlNode = next(cam for cam in root.findall('.//camera') if (cam.get('label') ==self.name or cam.get('label') ==ut.get_subject_name(self.subject) ))
        
        if xmlNode:
            #AGISOFT PARSING 1
            for child in xmlNode.iter('reference'):  
                #get translation
                x =  child.get('x')
                y =  child.get('y')
                z =  child.get('z')
                if x and y and z:
                    translation=np.array([float(x),float(y),float(z)])
                    self.cartesianTransform= gt.get_cartesian_transform(translation=translation)
                #get rotations
                yaw =  child.get('yaw')
                pitch =  child.get('pitch')
                roll =  child.get('roll')
                if yaw and pitch and roll:
                    rotation = gt.get_rotation_matrix(np.array([float(yaw),float(pitch),float(roll)]))
                    self.cartesianTransform=gt.get_cartesian_transform(translation=translation, rotation=rotation)
                #get accuracies
                sxy =  child.get('sxy')
                if sxy:
                    self.sxy=float(sxy)
                sz =  child.get('sz')
                if sz:
                    self.sz=float(sz)
            
            #AGISOFT PARSING 2
            transform=xmlNode.find('transform')
            if transform is not None:
                self.cartesianTransform=ut.string_to_list(transform.text)
        else:
            raise ValueError ('subject not in xml file') 

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
        elif getattr(self,'_cartesianBounds',None) is not None:
            self._cartesianTransform=gt.get_cartesian_transform(cartesianBounds=self._cartesianBounds)
        elif getattr(self,'_orientedBounds',None) is not None:
            center=np.mean(self._orientedBounds,0)
            self._cartesianTransform=gt.get_cartesian_transform(translation=center)
        elif getattr(self,'_orientedBoundingBox',None) is not None:
            self._cartesianTransform=gt.get_cartesian_transform(translation=self._orientedBoundingBox.get_center())
        elif self._resource is not None:
            self._cartesianTransform=gt.get_cartesian_transform(translation=self._resource.get_center())
        else:
            return None
        return self._cartesianTransform