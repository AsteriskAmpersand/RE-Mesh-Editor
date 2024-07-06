#Author: NSA Cloud
import bpy
import os
from .file_re_mdf import MDFFlags
from bpy.props import (StringProperty,
					   BoolProperty,
					   IntProperty,
					   FloatProperty,
					   FloatVectorProperty,
					   EnumProperty,
					   PointerProperty,
					   CollectionProperty
					   )

from .file_re_mdf import gameNameMDFVersionDict
from .blender_re_mesh_mdf import importMDF
from .re_mdf_presets import reloadPresets

flags = MDFFlags()#Bitflag struct

def update_modDirectoryRelPathToAbs(self,context):
	try:
		
		if "//" in self.modDirectory:
			#print("updated path")
			self.modDirectory = os.path.realpath(bpy.path.abspath(self.modDirectory))
	except:
		pass
def update_textureDirectoryRelPathToAbs(self,context):
	try:
		if "//" in self.textureDirectory:
			#print("updated path")
			self.textureDirectory = os.path.realpath(bpy.path.abspath(self.textureDirectory))
	except:
		pass
def update_listFilter(self, context):
	context.area.tag_redraw()
	
def update_materialName(self, context):
	parentObj = self.id_data
	try:
		#print(parentObj)
		if parentObj != None:
			split = parentObj.name.split("(",1)
			if len(split) == 2:
				parentObj.name = f"{split[0]}({self.materialName})"
			else:
				parentObj.name =f"Material 00 ({self.materialName})"
	except:
		pass

def update_FlagsFromInt(self, context):
	if not self.internal_changingFlagValues: 
		try:
			flags.asInt32 = self.flagIntValue
			self.internal_changingFlagValues = True
			for field_name, field_type, _ in flags.flagValues._fields_:
				#print(f"setting {field_name} to {abs(getattr(flags.flagValues, field_name))}")
				setattr(self,field_name,abs(getattr(flags.flagValues, field_name)))
			self.internal_changingFlagValues = False
		except:
			self.internal_changingFlagValues = False
def update_IntFromFlags(self, context):
	if not self.internal_changingFlagValues:
		try:
			flags.asInt32 = 0
			for field in flags.flagValues._fields_:
				fieldName = field[0]
				if fieldName in self:
					#print(f"setting {fieldName} to {getattr(self,fieldName)}")
					setattr(flags.flagValues,fieldName,getattr(self,fieldName))
					
			self.internal_changingFlagValues = True
			self.flagIntValue = flags.asInt32 
			self.internal_changingFlagValues = False
		except:
			self.internal_changingFlagValues = False
class MDFToolPanelPropertyGroup(bpy.types.PropertyGroup):
	
	def getMaterialPresets(self,context):
		return reloadPresets(context.scene.re_mdf_toolpanel.activeGame)
	mdfCollection: bpy.props.StringProperty(
		name="",
		description = "Set the collection containing the MDF file to edit.\nHint: MDF collections are blue.\nYou can create a new MDF collection by pressing the \"Create MDF Collection\" button",
		
		)
	activeGame: EnumProperty(
		name="",
		description="Set the game to determine which presets to use and which chunk paths to read textures from",
		items=[ 
				("DMC5", "Devil May Cry 5", ""),
				("RE2", "Resident Evil 2", ""),
				("RE3", "Resident Evil 3", ""),
				("MHRSB", "Monster Hunter Rise", ""),
				("RE8", "Resident Evil 8", ""),
				("RE2RT", "Resident Evil 2 Ray Tracing", ""),
				("RE3RT", "Resident Evil 3 Ray Tracing", ""),
				("RE7RT", "Resident Evil 7 Ray Tracing", ""),
				("RE4", "Resident Evil 4 Remake", ""),
				("SF6", "Street Fighter 6", ""),
				("DD2", "Dragon's Dogma 2", ""),
				("KG", "Kunitsu-Gami", ""),
			  ]
		)
	materialPresets: EnumProperty(
		name="",
		description="Set preset to be used by Add Material Preset button",
		items= getMaterialPresets
		)
	meshCollection: bpy.props.StringProperty(
		name="",
		description = "Set the mesh collection to apply the active MDF collection to.\nHint: Mesh collections are red",
		
		)
	modDirectory: bpy.props.StringProperty(
		name="",
		subtype = "DIR_PATH",
		description = "Set the natives directory of your mod.\nThis is used by \"Apply Active MDF\" and \"Copy Converted Tex\".\nThe platform folder must be included. (STM in most cases)\nExample:\n"+r"C:\Modding\Monster Hunter Rise\FluffyManager\Games\MHRISE\Mods\ArmorTest\natives\STM",
		update = update_modDirectoryRelPathToAbs
		)
	textureDirectory: bpy.props.StringProperty(
		name="",
		subtype = "DIR_PATH",
		description = "Set the directory containing images to be converted to .tex files",
		update = update_textureDirectoryRelPathToAbs
		)
	createStreamingTextures: BoolProperty(
		name = "Create Streaming Textures",
		description="Creates a low quality and a high quality texture. This lowers VRAM usage.\nHigh quality textures will be placed in the converted texture folder in a folder called \"streaming\".\nThese textures need to be placed at the same location as the non streaming textures, but the root level folder is called \"streaming\".\nExample:\nNon Streaming Tex Path: "+r"natives\STM\weapon\Bow\custom_bow\bow_Body_ALBD.tex.28"+"\nStreaming Tex Path: "+r"natives\STM\streaming\weapon\Bow\custom_bow\bow_Body_ALBD.tex.28",
		default = False,
		)
	openConvertedFolder: BoolProperty(
		name = "Open Folder After Conversion",
		description="Opens the directory containing the converted image files after conversion",
		default = False,
		)
	
class MDFFlagsPropertyGroup(bpy.types.PropertyGroup):
	ver32Unknown: IntProperty(
		name = "Version 31 Unknown",
		description="Unknown value for version 31 and above, likely flags",#TODO Add description
		)
	ver32Unknown1: IntProperty(
		name = "Version 31 Unknown 2",
		description="Unknown value for version 31 and above, likely flags",#TODO Add description
		)
	ver32Unknown2: IntProperty(
		name = "Version 31 Unknown 3",
		description="Unknown value for version 31 and above, likely flags",#TODO Add description
		)
	flagIntValue: IntProperty(
		name = "Bit Flag",
		description="Integer representation of all flag values.\nChanging this will change all of the flag values",
		update = update_FlagsFromInt
		)
	internal_changingFlagValues: BoolProperty(
		name = "Change Flag Values",
		description="This value is inaccessible by the user, it is used to determine whether the user changed a value or an update function did so that an infinite loop doesn't happen",
		default = False,
		)
	BaseTwoSideEnable: BoolProperty(
		name = "BaseTwoSideEnable",
		description="",
		update = update_IntFromFlags
	)
	BaseAlphaTestEnable: BoolProperty(
		name = "BaseAlphaTestEnable",
		description="",
		update = update_IntFromFlags
		)
	ShadowCastDisable: BoolProperty(
		name = "ShadowCastDisable",
		description="",
		update = update_IntFromFlags
		)
	VertexShaderUsed: BoolProperty(
		name = "VertexShaderUsed",
		description="",
		update = update_IntFromFlags
		)
	EmissiveUsed: BoolProperty(
		name = "EmissiveUsed",
		description="",
		update = update_IntFromFlags
		)
	TessellationEnable: BoolProperty(
		name = "TessellationEnable",
		description="",
		update = update_IntFromFlags
		)
	EnableIgnoreDepth: BoolProperty(
		name = "EnableIgnoreDepth",
		description="",
		update = update_IntFromFlags
		)
	AlphaMaskUsed: BoolProperty(
		name = "AlphaMaskUsed",
		description="",
		update = update_IntFromFlags
		)
	ForcedTwoSideEnable: BoolProperty(
		name = "ForcedTwoSideEnable",
		description="",
		update = update_IntFromFlags
		)
	TwoSideEnable: BoolProperty(
		name = "TwoSideEnable",
		description="",
		update = update_IntFromFlags
		)
	TessFactor: IntProperty(
		name = "TessFactor",
		description="",
		min = 0,
		max = 63,
		update = update_IntFromFlags
		)
	PhongFactor: IntProperty(
		name = "PhongFactor",
		description="",
		min = 0,
		max = 255,
		update = update_IntFromFlags
		)
	RoughTransparentEnable: BoolProperty(
		name = "RoughTransparentEnable",
		description="",
		update = update_IntFromFlags
		)
	ForcedAlphaTestEnable: BoolProperty(
		name = "ForcedAlphaTestEnable",
		description="",
		update = update_IntFromFlags
		)
	AlphaTestEnable: BoolProperty(
		name = "AlphaTestEnable",
		description="",
		update = update_IntFromFlags
		)
	SSSProfileUsed: BoolProperty(
		name = "SSSProfileUsed",
		description="",
		update = update_IntFromFlags
		)
	EnableStencilPriority: BoolProperty(
		name = "EnableStencilPriority",
		description="",
		update = update_IntFromFlags
		)
	RequireDualQuaternion: BoolProperty(
		name = "RequireDualQuaternion",
		description="",
		update = update_IntFromFlags
		)
	PixelDepthOffsetUsed: BoolProperty(
		name = "PixelDepthOffsetUsed",
		description="",
		update = update_IntFromFlags
		)
	NoRayTracing: BoolProperty(
		name = "NoRayTracing",
		description="",
		update = update_IntFromFlags
		)
	
class MDFPropPropertyGroup(bpy.types.PropertyGroup):
    prop_name: bpy.props.StringProperty(
        name="",
    )
    data_type: bpy.props.EnumProperty(
        items=[
            ('FLOAT', 'Float', 'Float'),
            ('BOOL', 'Bool', 'Bool'),
            ('VEC4', 'Vec4', 'Vec4'),
            ('COLOR', 'COLOR', 'COLOR'),
        ],
        name="Data Type",
    )
    float_vector_value: bpy.props.FloatVectorProperty(
        name="",
        size=4,
    )
    float_value: bpy.props.FloatProperty(
        name="",
    )
    bool_value: bpy.props.BoolProperty(
        name="",
        default=False
    )
    color_value: bpy.props.FloatVectorProperty(
        name="",
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
    )
    padding: bpy.props.IntProperty(#Not exposed in editor, used for SF6's weird mmtrs padding
        name="",
        default=0
    )

class MDFTextureBindingPropertyGroup(bpy.types.PropertyGroup):
    textureType: StringProperty(
        name="",
    )
    path: StringProperty(
        name="",
    )

class MDFMMTRSIndexPropertyGroup(bpy.types.PropertyGroup):
    indexString: StringProperty(
        name="Indices",
    )
class MDFGPBFDataPropertyGroup(bpy.types.PropertyGroup):
    gpbfDataString: StringProperty(
        name="GPBF Data",
    )	

class MESH_UL_MDFPropertyList(bpy.types.UIList):
	
	filterString: StringProperty(
		name = "Filter",
		description = "Search the list for items that contain this string.\nPress enter to search",
		default='',
		update = update_listFilter)
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # Display the properties of each item in the UIList
        #col1.label(text=item.name)
		layout.ui_units_y = 1.4
		split = layout.split(factor=0.48)
		col1 = split.column()
		col2 = split.column()
		row = col2.row()
		col2.alignment='RIGHT'
		col1.label(text = item.prop_name)
		if item.data_type == 'VEC4':
			row.prop(item, "float_vector_value")
		elif item.data_type == 'FLOAT':
			row.prop(item, "float_value")
		elif item.data_type == 'BOOL':
			row.prop(item, "bool_value")
		elif item.data_type == 'COLOR':
			row.prop(item, "color_value")
	# Disable double-click to rename
	def invoke(self, context, event):
		return {'PASS_THROUGH'}
	def draw_filter(self, context, layout):
		col = layout.column(align=True)
		row = col.row(align=True)
		row.prop(self, 'filterString', text='', icon='VIEWZOOM')
	def filter_items(self, context, data, propname):
		"""Filter and order items in the list.""" 
		filtered = []
		ordered = []
		items = getattr(data, propname)
		
		# Initialize with all items visible
		if self.filterString:
			filtered = [self.bitflag_filter_item] * len(items)
			for i, item in enumerate(items):
				if self.filterString.lower() not in item.prop_name.lower():
					filtered[i] &= ~self.bitflag_filter_item
		return filtered, ordered

class MESH_UL_MDFTextureBindingList(bpy.types.UIList):
	
	filterString: StringProperty(
		name = "Filter",
		description = "Search the list for items that contain this string.\nPress enter to search",
		default='',
		update = update_listFilter)
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # Display the properties of each item in the UIList
        #col1.label(text=item.name)
		layout.ui_units_y = 1.4
		split = layout.split(factor=0.35)
		col1 = split.column()
		col2 = split.column()
		row = col2.row()
		col2.alignment='RIGHT'
		col1.label(text = item.textureType)
		row.prop(item,"path")
	# Disable double-click to rename
	def invoke(self, context, event):
		return {'PASS_THROUGH'}
	def draw_filter(self, context, layout):
		col = layout.column(align=True)
		row = col.row(align=True)
		row.prop(self, 'filterString', text='', icon='VIEWZOOM')
	def filter_items(self, context, data, propname):
		"""Filter and order items in the list.""" 
		filtered = []
		ordered = []
		items = getattr(data, propname)
		
		# Initialize with all items visible
		if self.filterString:
			filtered = [self.bitflag_filter_item] * len(items)
			for i, item in enumerate(items):
				if self.filterString.lower() not in item.textureType.lower():
					filtered[i] &= ~self.bitflag_filter_item
		return filtered, ordered

class MESH_UL_MDFMMTRSDataList(bpy.types.UIList):
	
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # Display the properties of each item in the UIList
        #col1.label(text=item.name)
		layout.ui_units_y = 1.4
		split = layout.split(factor=0.35)
		col1 = split.column()
		col2 = split.column()
		row = col2.row()
		col2.alignment='RIGHT'
		#col1.label(text = item.textureType)
		layout.prop(item,"indexString")
	# Disable double-click to rename
	def invoke(self, context, event):
		return {'PASS_THROUGH'}

class MESH_UL_MDFGPBFDataList(bpy.types.UIList):
	
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # Display the properties of each item in the UIList
        #col1.label(text=item.name)
		layout.ui_units_y = 1.4
		split = layout.split(factor=0.35)
		col1 = split.column()
		col2 = split.column()
		row = col2.row()
		col2.alignment='RIGHT'
		#col1.label(text = item.textureType)
		layout.prop(item,"gpbfDataString")
	# Disable double-click to rename
	def invoke(self, context, event):
		return {'PASS_THROUGH'}

class MDFMaterialPropertyGroup(bpy.types.PropertyGroup):
	gameName:StringProperty()
	
	materialName: StringProperty(
		name = "Material Name",
		description="The name of the MDF material. The material names must match on both the mesh and mdf file.\nIf the material names and number of materials do not match in the mesh and mdf, you will get a checkerboard texture in game",
		update=update_materialName
		)
	mmtrPath: StringProperty(
		name = "Master Material Path",
		description="Do not change this unless you know what you're doing",
		)
	shaderType: EnumProperty(
		name="Material Shader Type",
		description="Set shader type",
		items=[ ("0", "Standard", ""),
				("1", "Decal", ""),
				("2", "DecalWithMetallic", ""),
				("3", "DecalNRMR", ""),
				("4", "Transparent", ""),
				("5", "Distortion", ""),
				("6", "PrimitiveMesh", ""),
				("7", "PrimitiveSolidMesh", ""),
				("8", "Water", ""),
				("9", "SpeedTree", ""),
				("10", "GUI", ""),
				("11", "GUIMesh", ""),
				("12", "GUIMeshTransparent", ""),
				("13", "ExpensiveTransparent", ""),
				("14", "Forward", ""),
				("15", "RenderTarget", ""),
				("16", "PostProcess", ""),
				("17", "PrimitiveMaterial", ""),
				("18", "PrimitiveSolidMaterial", ""),
				("19", "SpineMaterial", ""),
				("20", "Max", ""),
				
			   ]
		)
	
	flags:PointerProperty(type = MDFFlagsPropertyGroup)
	propertyList_items: CollectionProperty(type=MDFPropPropertyGroup)
	propertyList_index: IntProperty(name="")
	
	textureBindingList_items: CollectionProperty(type=MDFTextureBindingPropertyGroup)
	textureBindingList_index: IntProperty(name="")
	
	mmtrsData_items: CollectionProperty(type = MDFMMTRSIndexPropertyGroup)
	mmtrsData_index: IntProperty(name="")
	
	gpbfData_items: CollectionProperty(type = MDFGPBFDataPropertyGroup)
	gpbfData_index: IntProperty(name="")