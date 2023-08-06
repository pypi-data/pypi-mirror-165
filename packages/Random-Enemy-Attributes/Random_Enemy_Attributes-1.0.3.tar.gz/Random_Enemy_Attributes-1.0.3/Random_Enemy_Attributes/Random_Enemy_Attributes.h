#pragma once
#include <fstream>
#include <vector>


using namespace std;


class Random_Enemy_Attributes
{

public:

	Random_Enemy_Attributes();
	Random_Enemy_Attributes(string in_File, string out_File, int gen_Seed, float SCALE_L, float SCALE_H, float HEALTH_L, float HEALTH_H, float SPEED_L, float SPEED_H, float DAMAGE_L, float DAMAGE_H, float KNOCK_L, float KNOCK_H, bool Seperate);
	void start_Here();
	int return_Data(unsigned int hex_Data, bool small_Value);
	void find_Pointer_Size(unsigned int Pointer);
	static uint32_t ReverseBytes(uint32_t value);
	void MREA_SEARCH(unsigned int current_Offset, unsigned int size);
	void SCLY_SEARCH(unsigned int current_Offset);
	void enemy_Param_Searcher(unsigned int current_Offset, unsigned int size);
	void enemy_Start_Of_Attributes(unsigned int current_Offset, unsigned int data_Size, unsigned int object_ID_Element);
	void enemy_Param_Editor();
	void write_Data(vector<unsigned int> enemy_Data, unsigned int offset, unsigned int conditional, bool small_Value = false, unsigned int tiny_Value = 0xFF);
	float randomFloat(float low, float high);
	void add_Offsets_To_Vector(unsigned int current_Offset, int o, unsigned int enemy_Type);
	vector<unsigned int> instance_ID_Offset(const vector< vector<unsigned int> >& v, unsigned int ID, bool offset = false);
	void get_Pak_Pointers();
	void clean_Up();
	bool garbage = false;
	float scaleLow = 0.1;
	float scaleHigh = 4.0;
	float healthLow = 0.1;
	float healthHigh = 4.0;
	float speedLow = 0.1;
	float speedHigh = 4.0;
	float damageLow = 0.1;
	float damageHigh = 4.0;
	float knockbackPowerLow = 0.1;
	float knockbackPowerHigh = 40.0;
	bool randoScaleSeperate = true;
	string inputLocation;
	string outputLocation;
	int times = 0;
	int cur_Pak = 0;
};