# distutils: language = c++
#cython: language_level=3
#cython: c_string_type=unicode, c_string_encoding=utf8

from libcpp cimport bool
from libcpp.string cimport string

from Random_Enemy_Attributes_wrapper cimport Random_Enemy_Attributes

cdef class PyRandom_Enemy_Attributes:
	cdef Random_Enemy_Attributes *thisptr
	with nogil:
		def __cinit__(self, string in_File, string out_File, int gen_Seed, float SCALE_L, float SCALE_H, float HEALTH_L, float HEALTH_H, float SPEED_L, float SPEED_H, float DAMAGE_L, float DAMAGE_H, float KNOCK_L, float KNOCK_H, bool Seperate):
			self.thisptr = new Random_Enemy_Attributes(in_File, out_File, gen_Seed, SCALE_L, SCALE_H, HEALTH_L, HEALTH_H, SPEED_L, SPEED_H, DAMAGE_L, DAMAGE_H, KNOCK_L, KNOCK_H, Seperate)
		def __dealloc__(self):
			del self.thisptr
			
		def start_Here(self):
			return self.thisptr.start_Here()
			
		def return_Data(self, hex_Data, small_Value):
			return self.thisptr.return_Data(hex_Data, small_Value)
			
		def find_Pointer_Size(self, Pointer):
			return self.thisptr.find_Pointer_Size(Pointer)
			
		def ReverseBytes(self, value):
			return self.thisptr.ReverseBytes(value)
			
		def MREA_SEARCH(self, current_Offset, size):
			return self.thisptr.MREA_SEARCH(current_Offset, size)
			
		def SCLY_SEARCH(self, current_Offset):
			return self.thisptr.SCLY_SEARCH(current_Offset)
			
		def enemy_Param_Searcher(self, current_Offset, size):
			return self.thisptr.enemy_Param_Searcher(current_Offset, size)
			
		def enemy_Start_Of_Attributes(self, current_Offset, data_Size, object_ID_Element):
			return self.thisptr.enemy_Start_Of_Attributes(current_Offset, data_Size, object_ID_Element)
			
		def enemy_Param_Editor(self):
			self.thisptr.enemy_Param_Editor()
			
		def write_Data(self, enemy_Data, offset, conditional, small_Value, tiny_Value):
			self.thisptr.write_Data(enemy_Data, offset, conditional, small_Value, tiny_Value)
			
		def randomFloat(self, low, high):
			self.thisptr.randomFloat(low, high)
			
		def add_Offsets_To_Vector(self, current_Offset, o, enemy_Type):
			self.thisptr.add_Offsets_To_Vector(current_Offset, o, enemy_Type)
			
		def instance_ID_Offset(self, v, ID, offset):
			self.thisptr.instance_ID_Offset(v, ID, offset)
			
		def get_Pak_Pointers(self):
			self.thisptr.get_Pak_Pointers()
			
		def clean_Up(self):
			self.thisptr.clean_Up()
		
	property garbage:
		def __get__(self): return self.thisptr.garbage
		def __set__(self, garbage): self.thisptr.garbage = garbage
		
	property scaleLow:
		def __get__(self): return self.thisptr.scaleLow
		def __set__(self, scaleLow): self.thisptr.scaleLow = scaleLow
			
			
	property scaleHigh:
		def __get__(self): return self.thisptr.scaleHigh
		def __set__(self, scaleHigh): self.thisptr.scaleHigh = scaleHigh
			
			
	property healthLow:
		def __get__(self): return self.thisptr.healthLow
		def __set__(self, healthLow): self.thisptr.healthLow = healthLow
			
			
	property healthHigh:
		def __get__(self): return self.thisptr.healthHigh
		def __set__(self, healthHigh): self.thisptr.healthHigh = healthHigh
			
	property speedLow:
		def __get__(self): return self.thisptr.speedLow
		def __set__(self, speedLow): self.thisptr.speedLow = speedLow
			
	property speedHigh:
		def __get__(self): return self.thisptr.speedHigh
		def __set__(self, speedHigh): self.thisptr.speedHigh = speedHigh
			
	property damageLow:
		def __get__(self): return self.thisptr.damageLow
		def __set__(self, damageLow): self.thisptr.damageLow = damageLow
			
	property damageHigh:
		def __get__(self): return self.thisptr.damageHigh
		def __set__(self, damageHigh): self.thisptr.damageHigh = damageHigh
			
	property knockbackPowerLow:
		def __get__(self): return self.thisptr.knockbackPowerLow
		def __set__(self, knockbackPowerLow): self.thisptr.knockbackPowerLow = knockbackPowerLow
			
	property knockbackPowerHigh:
		def __get__(self): return self.thisptr.knockbackPowerHigh
		def __set__(self, knockbackPowerHigh): self.thisptr.knockbackPowerHigh = knockbackPowerHigh
			
	property randoScaleSeperate:
		def __get__(self): return self.thisptr.randoScaleSeperate
		def __set__(self, randoScaleSeperate): self.thisptr.randoScaleSeperate = randoScaleSeperate
		
	property inputLocation:
		def __get__(self): return self.thisptr.inputLocation
		def __set__(self, inputLocation): self.thisptr.inputLocation = inputLocation
		
	property outputLocation:
		def __get__(self): return self.thisptr.outputLocation
		def __set__(self, outputLocation): self.thisptr.outputLocation = outputLocation
		
	property times:
		def __get__(self): return self.thisptr.times
		def __set__(self, times): self.thisptr.times = times

	property cur_Pak:
		def __get__(self): return self.thisptr.cur_Pak
		def __set__(self, cur_Pak): self.thisptr.cur_Pak = cur_Pak