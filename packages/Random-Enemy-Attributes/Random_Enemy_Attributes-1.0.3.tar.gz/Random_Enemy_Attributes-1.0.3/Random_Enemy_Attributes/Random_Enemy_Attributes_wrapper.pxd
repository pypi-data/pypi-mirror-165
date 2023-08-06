#cython: c_string_type=unicode, c_string_encoding=utf8

from cpython cimport float 

from libc.stdint cimport uint32_t
from libcpp cimport bool
from libcpp.string cimport string
from libcpp.vector cimport vector

cdef extern from "Random_Enemy_Attributes.h":
	cdef cppclass Random_Enemy_Attributes:
		Random_Enemy_Attributes()
		Random_Enemy_Attributes(string, string, int, float, float, float, float, float, float, float, float, float, float, bool) except +
		void start_Here()
		int return_Data(unsigned int, bool)
		void find_Pointer_Size(unsigned int)
		uint32_t ReverseBytes(uint32_t)
		void MREA_SEARCH(unsigned int, unsigned int)
		void SCLY_SEARCH(unsigned int)
		void enemy_Param_Searcher(unsigned int, unsigned int)
		void enemy_Start_Of_Attributes(unsigned int, unsigned int, unsigned int)
		void enemy_Param_Editor()
		void write_Data(vector[unsigned int], unsigned int, unsigned int, bool, unsigned int)
		float randomFloat(float, float)
		void add_Offsets_To_Vector(unsigned int, int, unsigned int)
		vector[unsigned int] instance_ID_Offset(const vector[vector[unsigned int]], unsigned int, bool)
		void get_Pak_Pointers()
		void clean_Up()
		
		bool garbage
		float scaleLow
		float scaleHigh
		float healthLow
		float healthHigh
		float speedLow
		float speedHigh
		float damageLow
		float damageHigh
		float knockbackPowerLow
		float knockbackPowerHigh
		bool randoScaleSeperate
		string inputLocation
		string outputLocation
		int times
		int cur_Pak