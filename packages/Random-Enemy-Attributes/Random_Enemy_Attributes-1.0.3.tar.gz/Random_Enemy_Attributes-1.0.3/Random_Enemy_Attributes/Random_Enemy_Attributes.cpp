#include <iostream>
#include <Random_Enemy_Attributes.h>
#include <patternedAI_Array.h>
#include <Enemy_Offset_Locations.h>
#include <fstream>
#include <string>
#include <sstream>
#include <cstdint>
#include <vector>
#include <random>
#include <cctype>
#include <set>
#include <iomanip>
using namespace std;
unsigned int INSTANCE_ID;
unsigned int SCYL_SIZE;
unsigned int TYPE;
fstream in_out;
bool problem_Skiped = false;
float randomized_Value = 0;
std::random_device rd;
std::mt19937 gen;
unsigned int pak_Pointers[7] = { 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0 };
unsigned int pak_Locations[7] = { 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0 };
unsigned int temp;
unsigned int ttemp;
unsigned int tteemmpp;
float random_Scale;
float random_Health;
float random_Speed;
float random_Damage;
float random_Knockback;
unsigned file_Size;

int main()
{
    new Random_Enemy_Attributes();
    return 0;
}

Random_Enemy_Attributes::Random_Enemy_Attributes()
{
    gen.seed(1533968409);
    in_out.open("C:/Users/nevin/Documents/Dolphin-x64/Games/b.iso", std::ios::in | std::ios::out | std::ios::binary | std::ios::ate);
    Random_Enemy_Attributes::start_Here();
}

void Random_Enemy_Attributes::get_Pak_Pointers()
{
    //20450 - 20CC0
    unsigned int pointer = 0x00020450;
    unsigned int current_Offset;
    string area_Name;
    int pointer_size = 0;
    unsigned int pointer_Offset = 0;
    while (pointer_size < 7 && pointer + pointer_Offset < 0x00020CC0)
    {
        current_Offset = Random_Enemy_Attributes::return_Data(pointer + pointer_Offset, false);
        if (current_Offset >= file_Size - 0x1000)
        {
            continue;
        }
        for (unsigned int i = 0, data = 0; data != 0x54585452; i++)
        {
            if (i >= 0x20)
            {
                break;
            }
            data = Random_Enemy_Attributes::return_Data(current_Offset + i, false);
            //MLVL in hex
            if (data == 0x4D4C564C)
            {
                i += 0xE;
                while (data != 0x00)
                {
                    data = Random_Enemy_Attributes::return_Data(current_Offset + i, true);
                    area_Name.push_back(data);
                    i++;
                }
                if (area_Name.substr(0, 10) == "IntroLevel" || area_Name.substr(0, 10) == "IntroWorld")
                {
                    pak_Pointers[0] = pointer + pointer_Offset;
                    pointer_size++;
                }
                else if (area_Name.substr(0, 14) == "TalonOverworld" || area_Name.substr(0, 9) == "OverWorld")
                {
                    pak_Pointers[3] = pointer + pointer_Offset;
                    pointer_size++;
                }
                else if (area_Name.substr(0, 10) == "RuinsWorld")
                {
                    pak_Pointers[1] = pointer + pointer_Offset;
                    pointer_size++;
                }
                else if (area_Name.substr(0, 8) == "IceWorld")
                {
                    pak_Pointers[2] = pointer + pointer_Offset;
                    pointer_size++;
                }
                else if (area_Name.substr(0, 10) == "MinesWorld" || area_Name.substr(0, 9) == "Mines0201")
                {
                    pak_Pointers[4] = pointer + pointer_Offset;
                    pointer_size++;
                }
                else if (area_Name.substr(0, 9) == "LavaWorld")
                {
                    pak_Pointers[5] = pointer + pointer_Offset;
                    pointer_size++;
                }
                else if (area_Name.substr(0, 11) == "CraterWorld")
                {
                    pak_Pointers[6] = pointer + pointer_Offset;
                    pointer_size++;
                }
                area_Name.clear();
                break;
            }
        }
        pointer_Offset += 0xC;
    }
    if (pointer_size != 7)
    {
        throw invalid_argument("\nCouldn't find pak offsets, your iso version may not be supported\nAborting enemy stat randomizer.\n");
    }
}

void Random_Enemy_Attributes::start_Here()
{
    file_Size = in_out.tellg();
    Random_Enemy_Attributes::get_Pak_Pointers();
    for (int i = 0; i < 7; i++)
    {
        pak_Locations[i] = Random_Enemy_Attributes::return_Data(pak_Pointers[i], false);
    }
    for (int pak_Offset = 0; pak_Offset < 7; pak_Offset++)
    {
        if (pak_Locations[pak_Offset] >= file_Size - 0x1000)
        {
            throw invalid_argument("\nCouldn't find pak offsets, your iso version may not be supported\nAborting enemy stat randomizer.\n");
        }
    }
    for (int i = 0; i < 7; i++)
    {
        if (cur_Pak == 0)
        {
            cout << "\nRetriving enemy locations from 'Space Pirate Frigate'";
        }
        else if (cur_Pak == 1)
        {
            cout << " DONE\n";
            cout << "Retriving enemy locations from 'Chozo Ruins'";
        }
        else if (cur_Pak == 2)
        {
            cout << " DONE\n";
            cout << "Retriving enemy locations from 'Phendrana Drifts'";
        }
        else if (cur_Pak == 3)
        {
            cout << " DONE\n";
            cout << "Retriving enemy locations from 'Tallon Overworld'";
        }
        else if (cur_Pak == 4)
        {
            cout << " DONE\n";
            cout << "Retriving enemy locations from 'Phazon Mines'";
        }
        else if (cur_Pak == 5)
        {
            cout << " DONE\n";
            cout << "Retriving enemy locations from 'Magmoor Caverns'";
        }
        else if (cur_Pak == 6)
        {
            cout << " DONE\n";
            cout << "Retriving enemy locations from 'Impact Crater'";
        }
        Random_Enemy_Attributes::find_Pointer_Size(pak_Locations[i]);
        cur_Pak++;
    }
    cout << " DONE\n";
    for (int i = 0; i < 47; i++)
    {
        unsigned int vector_Size = EnemyOffsets[i].size(); // Wheel for linux and mac-os throw an error if I do it the saner way.
        vector_Size++;
        vector<unsigned int> enemy_Data = { vector_Size };
        //EnemyOffsets[i].insert(EnemyOffsets[i].begin(), vector<unsigned int>( EnemyOffsets[i].size() + 1 ));
        EnemyOffsets[i].insert(EnemyOffsets[i].begin(), enemy_Data);
    }

    cout << "Randomizing enemy stats";
    Random_Enemy_Attributes::enemy_Param_Editor();
    cout << " DONE" << endl;
    clean_Up();
}

void Random_Enemy_Attributes::clean_Up()
{
    in_out.close();
    randomized_Value = 0;
    fill(pak_Pointers, pak_Pointers + 7, 0);
    fill(pak_Locations, pak_Locations + 7, 0);
    garbage = false;
    scaleLow = 0.0;
    scaleHigh = 0.0;
    healthLow = 0.0;
    healthHigh = 0.0;
    speedLow = 0.0;
    speedHigh = 0.0;
    damageLow = 0.0;
    damageHigh = 0.0;
    knockbackPowerLow = 0.0;
    knockbackPowerHigh = 0.0;
    randoScaleSeperate = false;
    times = 0;
    cur_Pak = 0;
    file_Size = 0;
    problem_Skiped = false;
}

Random_Enemy_Attributes::Random_Enemy_Attributes(string in_File, string out_File, int gen_Seed, float SCALE_L, float SCALE_H, float HEALTH_L, float HEALTH_H, float SPEED_L, float SPEED_H, float DAMAGE_L, float DAMAGE_H, float KNOCK_L, float KNOCK_H, bool Seperate)
{
    inputLocation = in_File;
    outputLocation = out_File;
    scaleLow = SCALE_L;
    scaleHigh = SCALE_H;
    healthLow = HEALTH_L;
    healthHigh = HEALTH_H;
    speedLow = SPEED_L;
    speedHigh = SPEED_H;
    damageLow = DAMAGE_L;
    damageHigh = DAMAGE_H;
    knockbackPowerLow = KNOCK_L;
    knockbackPowerHigh = KNOCK_H;
    randoScaleSeperate = Seperate;
    gen.seed(gen_Seed);

    int position = outputLocation.find_last_of(".");
    string file_Extension = outputLocation.substr(position + 1);
    if (file_Extension != "iso")
    {
        stringstream exception_Message;
        exception_Message << "Enemy Stat Randomizer only supports output file extension of type 'iso', not '" << file_Extension << "'\nAborting enemy stat randomizer.\n" << endl;
        const std::string s = exception_Message.str();
        clean_Up();
        throw invalid_argument(s);
    }


    if (scaleLow > scaleHigh)
    {
        float original_scaleLow = scaleLow;
        scaleLow = scaleHigh;
        scaleHigh = original_scaleLow;
    }
    if (healthLow > healthHigh)
    {
        float original_healthLow = healthLow;
        healthLow = healthHigh;
        healthHigh = original_healthLow;
    }
    if (speedLow > speedHigh)
    {
        float original_speedLow = speedLow;
        speedLow = speedHigh;
        speedHigh = original_speedLow;
    }
    if (damageLow > damageHigh)
    {
        float original_damageLow = damageLow;
        damageLow = damageHigh;
        damageHigh = original_damageLow;
    }
    if (knockbackPowerLow > knockbackPowerHigh)
    {
        float original_knockbackPowerLow = knockbackPowerLow;
        knockbackPowerLow = knockbackPowerHigh;
        knockbackPowerHigh = original_knockbackPowerLow;
    }

    //input.open(inputLocation, std::ios::in | std::ios::out | std::ios::binary | std::ios::ate);
    in_out.open(outputLocation, std::ios::in | std::ios::out | std::ios::binary | std::ios::ate);

    if (in_out.is_open())
    {
        Random_Enemy_Attributes::start_Here();
    }
    else
    {
        throw invalid_argument("Couldn't find output file.\nAborting Enemy Stat Randomizer");
    }
}

uint32_t Random_Enemy_Attributes::ReverseBytes(uint32_t value)
{
    return (value & 0x000000FFU) << 24 | (value & 0x0000FF00U) << 8 |
        (value & 0x00FF0000U) >> 8 | (value & 0xFF000000U) >> 24;
}

int Random_Enemy_Attributes::return_Data(unsigned int hex_Data, bool small_Value)
{
    if (in_out.is_open())
    {
        char data[4];
        in_out.seekg(hex_Data);
        in_out.read(data, (ifstream::pos_type)4);
        if (small_Value)
        {
            return (unsigned char)data[0];
        }

        int* value = (int*)(&data[0]); //alternately (int*)(data+23)
        int offset = ReverseBytes(value[0]);

        return offset;
    }
    else
    {
        clean_Up();
        throw invalid_argument("File closed during reading, aborting enemy stat randomizer\n");
    }
}

void Random_Enemy_Attributes::find_Pointer_Size(unsigned int pointer)
{
    bool correct_Pak_Data = false;
    for (unsigned int i = 0, data = 0; data != 0x54585452; i++)
    {
        if (i > 30 && !correct_Pak_Data)
        {
            clean_Up();
            throw invalid_argument("\nCouldn't find pak offsets, your iso version may not be supported\nAborting enemy stat randomizer.\n");
        }
        data = Random_Enemy_Attributes::return_Data(pointer + i, false);
        //MLVL in hex
        if (data == 0x4D4C564C)
        {
            correct_Pak_Data = true;
        }
        //TXTR in hex
        if (data == 0x54585452 && correct_Pak_Data)
        {
            pointer += (i + 12);
        }
    }
    unsigned int pointer_Size = Random_Enemy_Attributes::return_Data(pointer, false);
    Random_Enemy_Attributes::MREA_SEARCH((pointer - 12), pointer_Size);
}

void Random_Enemy_Attributes::MREA_SEARCH(unsigned int current_Offset, unsigned int size)
{
    for (unsigned int i = 0, data = 0; i < size; i += 0x14)
    {
        data = Random_Enemy_Attributes::return_Data(current_Offset + i, false);

        //MREA in hex
        if (data == 0x4D524541)
        {
            data = Random_Enemy_Attributes::return_Data(current_Offset + i + 12, false);
            Random_Enemy_Attributes::SCLY_SEARCH(data + pak_Locations[cur_Pak]);
        }
    }
}

void Random_Enemy_Attributes::SCLY_SEARCH(unsigned int current_Offset)
{
    unsigned int data_sections = Random_Enemy_Attributes::return_Data(current_Offset + 0x3C, false);
    unsigned int section_index = Random_Enemy_Attributes::return_Data(current_Offset + 0x44, false);
    unsigned int new_Offset = 0;
    current_Offset += 0x60;
    unsigned int data_Size = Random_Enemy_Attributes::return_Data(current_Offset + (section_index * 4), false);
    for (int unsigned i = 0; i < section_index; i++)
    {
        new_Offset += Random_Enemy_Attributes::return_Data(current_Offset + (4 * i), false);
    }
    current_Offset += new_Offset + (data_sections * 4);

    //SCLY in hex
    while (Random_Enemy_Attributes::return_Data(current_Offset, false) != 0x53434C59)
    {
        current_Offset += 4;
    }
Random_Enemy_Attributes::enemy_Param_Searcher(current_Offset, data_Size);
}

void Random_Enemy_Attributes::enemy_Param_Searcher(unsigned int current_Offset, unsigned int size)
{
    unsigned saved_Offset = 0;
    unsigned int initial_Offset = current_Offset;
    current_Offset += 8;
    current_Offset += (Random_Enemy_Attributes::return_Data(current_Offset, false) * 4) + 9;
    while (initial_Offset + size - 0x10 > current_Offset)
    {
        TYPE = Random_Enemy_Attributes::return_Data(current_Offset, true);
        SCYL_SIZE = Random_Enemy_Attributes::return_Data(current_Offset + 1, false);
        INSTANCE_ID = Random_Enemy_Attributes::return_Data(current_Offset + 5, false);
        tteemmpp = Random_Enemy_Attributes::return_Data(current_Offset, false);
        if (SCYL_SIZE != 0x00000000 && SCYL_SIZE < 0x0000FFFF && initial_Offset + size - 100 > current_Offset && tteemmpp <= 0x00000000)
        {
            temp = current_Offset + SCYL_SIZE + 6;
            ttemp = Random_Enemy_Attributes::return_Data(temp, false);
            if (temp >= 0x0000FFFF)
            {
                if ((SCYL_SIZE + 6 + current_Offset + 100) < (initial_Offset + size))
                {
                    current_Offset += 5;
                    for (int i = 0; i < 0xFF; i++)
                    {
                        int TEMP_A = Random_Enemy_Attributes::return_Data(current_Offset + 1 + i, true);
                        int TEMP_B = Random_Enemy_Attributes::return_Data(current_Offset + 2 + i, true);
                        if (TEMP_A == 0x00 && TEMP_B == 0x00)
                        {
                            current_Offset += i;
                            break;
                        }
                        else if (i > 0xF0)
                        {
                            clean_Up();
                            throw invalid_argument("Uh oh something went wrong in garbage data-tiny. (yes I know this is vauge)\nAborting Enemy Stat Randomizer\n");
                        }
                    }
                    continue;
                }
            }
        }
        if (SCYL_SIZE == 0x00000000)
        {
            garbage = true;
            while (garbage == true)
            {
                if (Random_Enemy_Attributes::return_Data(current_Offset, true) != 0x00)
                {
                    current_Offset += 3;
                    while (Random_Enemy_Attributes::return_Data(current_Offset, true) < 0x10)
                    {
                        current_Offset++;
                    }
                    current_Offset -= 9;
                    garbage = false;

                }
                else
                {
                    current_Offset++;
                }
            }
            current_Offset += SCYL_SIZE + 5;
            INSTANCE_ID = 0;
            continue;
        }
        unsigned int value = Random_Enemy_Attributes::return_Data(current_Offset, true);
        for (unsigned int i = 0; i < 47; i++)
        {
            if (value == objectPatterned_ID[i])
            {
                Random_Enemy_Attributes::enemy_Start_Of_Attributes(current_Offset, SCYL_SIZE, i);
                break;
            }
        }
        current_Offset += SCYL_SIZE + 5;
    }
}


void Random_Enemy_Attributes::enemy_Start_Of_Attributes(unsigned int current_Offset, unsigned int data_Size, unsigned int object_ID_Element)
{
    unsigned int TYPE = Random_Enemy_Attributes::return_Data(current_Offset, true);
    //unsigned int Start_Of_Data = current_Offset + 5;
    current_Offset += 9;
    unsigned int size = Random_Enemy_Attributes::return_Data(current_Offset, false);
    current_Offset += 8 + (size * 0x0C);
    if (object_ID_Element == 40)
    {
        current_Offset += 4;
    }
    while (Random_Enemy_Attributes::return_Data(current_Offset, true) != 0x00)
    {
        current_Offset++;
    }
    current_Offset++;
    if (!(set<unsigned int>{0x04090078, 0x002900A6, 0x1433007C}.count(INSTANCE_ID)))
    {
        vector<unsigned int> enemy_Data = { INSTANCE_ID, current_Offset, TYPE };
        EnemyOffsets[object_ID_Element].push_back(enemy_Data);
    }

}

void Random_Enemy_Attributes::add_Offsets_To_Vector(unsigned int current_Offset, int o, unsigned int enemy_Type)
{
    vector<unsigned int> enemy_Data = { INSTANCE_ID, current_Offset, enemy_Type };
    switch (o)
    {
    case 0:
        vector_BabySheegoth_offsets.push_back(enemy_Data);
        break;
    case 1:
        vector_Beetle_offsets.push_back(enemy_Data);
        break;
    case 2:
        vector_BloodFlower_offsets.push_back(enemy_Data);
        break;
    case 3:
        vector_ChozoGhost_offsets.push_back(enemy_Data);
        break;
    case 4:
        vector_Drone_offsets.push_back(enemy_Data);
        break;
    case 5:
        vector_ElitePirate_offsets.push_back(enemy_Data);
        break;
    case 6:
        vector_Eyon_offsets.push_back(enemy_Data);
        break;
    case 7:
        vector_FlyingPirate_offsets.push_back(enemy_Data);
        break;
    case 8:
        vector_HunterMetroid_offsets.push_back(enemy_Data);
        break;
    case 9:
        vector_IceSheegoth_offsets.push_back(enemy_Data);
        break;
    case 10:
        vector_Jelzap_offsets.push_back(enemy_Data);
        break;
    case 11:
        vector_Magmoor_offsets.push_back(enemy_Data);
        break;
    case 12:
        vector_Metroid_offsets.push_back(enemy_Data);
        break;
    case 13:
        vector_PuddleSpore_offsets.push_back(enemy_Data);
        break;
    case 14:
        vector_Puffer_offsets.push_back(enemy_Data);
        break;
    case 15:
        vector_PulseBombu_offsets.push_back(enemy_Data);
        break;
    case 16:
        vector_ReaperVine_offsets.push_back(enemy_Data);
        break;
    case 17:
        vector_ScatterBombu_offsets.push_back(enemy_Data);
        break;
    case 18:
        vector_Seedling_offsets.push_back(enemy_Data);
        break;
    case 19:
        vector_Shriekbat_offsets.push_back(enemy_Data);
        break;
    case 20:
        vector_SpacePirate_offsets.push_back(enemy_Data);
        break;
    case 21:
        vector_StoneToad_offsets.push_back(enemy_Data);
        break;
    case 22:
        vector_Flaahgra_offsets.push_back(enemy_Data);
        break;
    case 23:
        vector_Thardus_offsets.push_back(enemy_Data);
        break;
    case 24:
        vector_OmegaPirate_offsets.push_back(enemy_Data);
        break;
    case 25:
        vector_MetaRidley_offsets.push_back(enemy_Data);
        break;
    case 26:
        vector_MetroidPrimeStage2_offsets.push_back(enemy_Data);
        break;
    case 27:
        vector_Flickerbat_offsets.push_back(enemy_Data);
        break;
    case 28:
        vector_GroundProwlers_offsets.push_back(enemy_Data);
        break;
    case 29:
        vector_Glider_offsets.push_back(enemy_Data);
        break;
    case 30:
        vector_Burrower_offsets.push_back(enemy_Data);
        break;
    case 31:
        vector_Oculus_offsets.push_back(enemy_Data);
        break;
    case 32:
        vector_Plazmite_offsets.push_back(enemy_Data);
        break;
    case 33:
        vector_Triclops_offsets.push_back(enemy_Data);
        break;
    case 34:
        vector_WarWasp_offsets.push_back(enemy_Data);
        break;
    case 35:
        vector_ParasiteQueen_offsets.push_back(enemy_Data);
        break;
    case 36:
        vector_FlaahgraTentacle_offsets.push_back(enemy_Data);
        break;
    case 37:
        vector_Turret_offsets.push_back(enemy_Data);
        break;
    case 38:
        vector_AmbientAI_offsets.push_back(enemy_Data);
        break;
    case 39:
        vector_Swarm_offsets.push_back(enemy_Data);
        break;
    case 40:
        vector_MetroidPrimeStage1_offsets.push_back(enemy_Data);
        break;
    case 41:
        vector_IncineratorDrone_offsets.push_back(enemy_Data);
        break;
    case 42:
        vector_ActorKeyFrame_offsets.push_back(enemy_Data);
        break;
    case 43:
        vector_Timer_offsets.push_back(enemy_Data);
        break;
    case 44:
        vector_Actor_offsets.push_back(enemy_Data);
        break;
    case 45:
        vector_Platform_offsets.push_back(enemy_Data);
        break;
    default:
        clean_Up();
        throw invalid_argument("Attempting to add enemy offset to a vector outside its index range\nAborting Enemy Stat Randomizer");
    }
}


void Random_Enemy_Attributes::enemy_Param_Editor()
{
    unsigned int enemy_Data_Size;
    unsigned int instance_ID;
    unsigned int enemy_Type;
    vector_Thardus_offsets = EnemyOffsets[23];
    vector_ActorKeyFrame_offsets = EnemyOffsets[42];
    vector_Timer_offsets = EnemyOffsets[43];
    vector_Actor_offsets = EnemyOffsets[44];
    vector_Platform_offsets = EnemyOffsets[45];
    vector_ShadowProjector_offsets = EnemyOffsets[46];
    for (unsigned int i = 0; i < 42; i++)
    {
        for (unsigned int o = 1; o < EnemyOffsets[i][0][0]; o++)
        {
            instance_ID = EnemyOffsets[i][o][0];
            enemy_Type = EnemyOffsets[i][o][2];
            for (unsigned int c = 0; c < 6; c++)
            {
                switch (c)
                {
                case 0:
                    randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
                    random_Scale = randomized_Value;
                    break;
                case 1:
                    randomized_Value = Random_Enemy_Attributes::randomFloat(healthLow, healthHigh);
                    random_Health = randomized_Value;
                    break;
                case 2:
                    randomized_Value = Random_Enemy_Attributes::randomFloat(speedLow, speedHigh);
                    random_Speed = randomized_Value;
                    break;
                case 3:
                    break;
                case 4:
                    randomized_Value = Random_Enemy_Attributes::randomFloat(damageLow, damageHigh);
                    random_Damage = randomized_Value;
                    break;
                case 5:
                    randomized_Value = Random_Enemy_Attributes::randomFloat(knockbackPowerLow, knockbackPowerHigh);
                    random_Knockback = randomized_Value;
                    break;
                default:
                    clean_Up();
                    throw invalid_argument("This error will never happen but its in a switch statement and I need a default\nAborting Enemy Stat Randomizer");
                }


                if (i < 27)
                {
                    enemy_Data_Size = EnemyInfo[i][c][0];
                }
                else
                {
                    enemy_Data_Size = 0;
                }
                if (enemy_Data_Size != 0x000)
                {
                    for (unsigned int e = 1; e < enemy_Data_Size; e++)
                    {
                        if (c == 0 && randoScaleSeperate == true)
                        {
                            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
                        }
                        Random_Enemy_Attributes::write_Data(EnemyOffsets[i][o], EnemyInfo[i][c][e], c);
                    }
                }
                if (i == 23 && c == 0)
                {
                    if (randomized_Value < 0.5)
                    {
                        float temp = randomized_Value;
                        randomized_Value = 2.0 / randomized_Value;
                        Random_Enemy_Attributes::write_Data(vector_Thardus_offsets[1], 0x244, 0xFF); //ThardusRollSpeed
                        randomized_Value = temp;
                    }
                    else if (randomized_Value < 1.0)
                    {
                        float temp = randomized_Value;
                        randomized_Value = 1.0 / randomized_Value;
                        Random_Enemy_Attributes::write_Data(vector_Thardus_offsets[1], 0x244, 0xFF); //ThardusRollSpeed
                        randomized_Value = temp;
                    }
                }
                if (i < 37)
                {
                    enemy_Data_Size = PatternedAI[c][0];
                }
                else
                {
                    enemy_Data_Size = 0;
                }
                if (enemy_Data_Size != 0x000)
                {
                    for (unsigned int e = 1; e < enemy_Data_Size; e++)
                    {
                        if (c == 0 && i != 0 && i != 3 && i != 9 && i != 23 && i != 25 && randoScaleSeperate == true && EnemyOffsets[i][o][1] != 0x53411AAD && EnemyOffsets[i][o][1] != 0x53411D44 && EnemyOffsets[i][o][1] != 0x53411821 && EnemyOffsets[i][o][1] != 0x49f9c846 && EnemyOffsets[i][o][1] != 0x406e14c9)
                        {
                            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
                        }
                        //if (i == 23)
                        //{
                        //    Random_Enemy_Attributes::write_Data(0x49F9CC10, Array_ThardusRock[c][e], c);
                        //}
                        Random_Enemy_Attributes::write_Data(EnemyOffsets[i][o], PatternedAI[c][e], c);
                        if (c == 3 && e == 1 && i == 23) //??25001E
                        {
                            float temp = randomized_Value;
                            randomized_Value *= 2;
                            for (int f = 0; f < 4; f++)
                            {
                                const unsigned int timer_ID_Array[4] = {0x0425004C, 0x04250060, 0x04250051, 0x04250053};
                                vector<unsigned int> object_Data = instance_ID_Offset(vector_Timer_offsets, timer_ID_Array[f]);
                                Random_Enemy_Attributes::write_Data(object_Data, 0x0, c);
                            }
                            randomized_Value = temp;
                        }
                        //BIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIG
                        if (instance_ID == 0x00190004 && enemy_Type == ParasiteQueen)
                        {
                            if (c == 0)
                            {
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x0019006C), 0x18 + ((e - 1) * 4), 0xFF);
                            }
                            else if (c == 2 && e == 1)
                            {
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_ActorKeyFrame_offsets, 0x001900C6), 0xE, 0xFF);
                            }
                        }
                    //Metroids In Phendrana Drifts
                        else if (instance_ID == 0x002802E1 && c == 0 && enemy_Type == MetroidAlpha)
                        {
                            Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x0028026c), 0x18 + ((e - 1) * 4), 0xFF);
                        }
                        else if (instance_ID == 0x002802E0 && c == 0 && enemy_Type == MetroidAlpha)
                        {
                            Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x0028026d), 0x18 + ((e - 1) * 4), 0xFF);
                        }
                        else if (instance_ID == 0x002802E2 && c == 0 && enemy_Type == MetroidAlpha)
                        {
                            Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x0028026e), 0x18 + ((e - 1) * 4), 0xFF);
                        }
                        else if (instance_ID == 0x00330038 && c == 0 && enemy_Type == MetroidAlpha)
                        {
                            Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x0033004b), 0x18 + ((e - 1) * 4), 0xFF);
                        }
                        else if (instance_ID == 0x083301C8 && c == 0 && enemy_Type == MetroidAlpha)
                        {
                            Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x083301c7), 0x18 + ((e - 1) * 4), 0xFF);
                        }
                        else if (instance_ID == 0x143300AA && c == 0 && enemy_Type == MetroidAlpha)
                        {
                            Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x14330004), 0x18 + ((e - 1) * 4), 0xFF);
                        }
                        else if (instance_ID == 0x08190599 && c == 0 && enemy_Type == MetroidAlpha)
                        {
                            Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x081901cc), 0x18 + ((e - 1) * 4), 0xFF);
                        }
                        else if (instance_ID == 0x08190598 && c == 0 && enemy_Type == MetroidAlpha)
                        {
                            Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x0819026b), 0x18 + ((e - 1) * 4), 0xFF);
                        }
                        else if (instance_ID == 0x04100101 && enemy_Type == Ridley)
                        {
                            if (c == 0)
                            {
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x381003d6), 0x18 + ((e - 1) * 4), 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x3810028c), 0x18 + ((e - 1) * 4), 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x38100377), 0x18 + ((e - 1) * 4), 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x381003c3), 0x18 + ((e - 1) * 4), 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x381003e1), 0x18 + ((e - 1) * 4), 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x38100472), 0x18 + ((e - 1) * 4), 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x38100222), 0x18 + ((e - 1) * 4), 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x38100218), 0x18 + ((e - 1) * 4), 0xFF);
                            }
                            else if (c == 2 && e == 1)
                            {
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_ActorKeyFrame_offsets, 0x38100299), 0xE, 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_ActorKeyFrame_offsets, 0x3810029a), 0xE, 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_ActorKeyFrame_offsets, 0x3810029b), 0xE, 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_ActorKeyFrame_offsets, 0x3810029c), 0xE, 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_ActorKeyFrame_offsets, 0x3810030f), 0xE, 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_ActorKeyFrame_offsets, 0x38100444), 0xE, 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_ActorKeyFrame_offsets, 0x38100572), 0xE, 0xFF);
                            }
                        }
                        else if (instance_ID == 0x0C180137 && c == 0 && enemy_Type == ElitePirate)
                        {
                            Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x0c180126), 0x18 + ((e - 1) * 4), 0xFF);
                        }
                        else if (instance_ID == 0x04100338 && c == 0 && enemy_Type == ElitePirate)
                        {
                            Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x04100337), 0x18 + ((e - 1) * 4), 0xFF);
                            Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x0410036a), 0x18 + ((e - 1) * 4), 0xFF);
                            if (c == 2 && e == 1)
                            {
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_ActorKeyFrame_offsets, 0x0410036b), 0xE, 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_ActorKeyFrame_offsets, 0x0410036c), 0xE, 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_ActorKeyFrame_offsets, 0x0410036e), 0xE, 0xFF);
                            }
                        }
                        else if (instance_ID == 0x040D01A4 && c == 0 && enemy_Type == ElitePirate)
                        {
                            Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x140d03fa), 0x18 + ((e - 1) * 4), 0xFF);
                            Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x040d01a7), 0x18 + ((e - 1) * 4), 0xFF);
                        }
                        else if (instance_ID == 0x081401CE && c == 0 && enemy_Type == ElitePirate)
                        {
                            Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x04140385), 0x18 + ((e - 1) * 4), 0xFF);
                        }
                        else if (instance_ID == 0x081401CE && c == 2 && e == 1 && enemy_Type == ElitePirate)
                        {
                            Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_ActorKeyFrame_offsets, 0x0c18010c), 0xE, 0xFF);
                        }
                        else if (instance_ID == 0x141A0126 && enemy_Type == OmegaPirate)
                        {
                            if (c == 0)
                            {
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Platform_offsets, 0x041A0441), 0x18 + ((e - 1) * 4), 0xFF); //platform
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x041a046d), 0x18 + ((e - 1) * 4), 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x041a03ad), 0x18 + ((e - 1) * 4), 0xFF);
                            }
                            else if (c == 2 && e == 1)
                            {
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_ActorKeyFrame_offsets, 0x41a03ae), 0xE, 0xFF);
                            }
                        }
                    //Metroids in Phazon Mines
                        else if (instance_ID == 0x08200256 && c == 0 && enemy_Type == MetroidAlpha)
                        {
                            Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x0820074d), 0x18 + ((e - 1) * 4), 0xFF);
                        }
                        else if (instance_ID == 0x08200255 && c == 0 && enemy_Type == MetroidAlpha)
                        {
                            Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x0820074e), 0x18 + ((e - 1) * 4), 0xFF);
                        }
                        else if (instance_ID == 0x141F02F3 && c == 0 && enemy_Type == MetroidAlpha)
                        {
                            Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x141f035a), 0x18 + ((e - 1) * 4), 0xFF);
                        }
                        else if (instance_ID == 0x141F02F4 && c == 0 && enemy_Type == MetroidAlpha)
                        {
                            Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x141f035b), 0x18 + ((e - 1) * 4), 0xFF);
                        }
                        else if (instance_ID == 0x3870f0ca && enemy_Type == MetroidPrimeEssence)
                        {
                            if (c == 0)
                            {
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x000b009f), 0x18 + ((e - 1) * 4), 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x000b00d2), 0x18 + ((e - 1) * 4), 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x000b00ee), 0x18 + ((e - 1) * 4), 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x000b00f4), 0x18 + ((e - 1) * 4), 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x000b0101), 0x18 + ((e - 1) * 4), 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x000b0121), 0x18 + ((e - 1) * 4), 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x000b012b), 0x18 + ((e - 1) * 4), 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x000b015d), 0x18 + ((e - 1) * 4), 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x000b0162), 0x18 + ((e - 1) * 4), 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x000b0163), 0x18 + ((e - 1) * 4), 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x000b0168), 0x18 + ((e - 1) * 4), 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x000b0195), 0x18 + ((e - 1) * 4), 0xFF);

                            }
                            else if (c == 2 && e == 1)
                            {
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_ActorKeyFrame_offsets, 0x000b015b), 0xE, 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_ActorKeyFrame_offsets, 0x000b00a3), 0xE, 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_ActorKeyFrame_offsets, 0x000b00d4), 0xE, 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_ActorKeyFrame_offsets, 0x000b00f8), 0xE, 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_ActorKeyFrame_offsets, 0x000b00f9), 0xE, 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_ActorKeyFrame_offsets, 0x000b00fe), 0xE, 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_ActorKeyFrame_offsets, 0x000b012d), 0xE, 0xFF);
                                Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_ActorKeyFrame_offsets, 0x000b0131), 0xE, 0xFF);
                            }
                        }
                        //END BIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIG
                        if (enemy_Type == OmegaPirate && instance_ID == 0x141A0126)
                        {
                            if (c == 0)
                            {
                                for (int f = 0; f < 4; f++)
                                {
                                    const unsigned int platform_ID_Array[4] = { 0x141A019B, 0x141A019C, 0x141A019D, 0x141A019E };
                                    vector<unsigned int> object_Data = instance_ID_Offset(vector_Platform_offsets, platform_ID_Array[f]);
                                    Random_Enemy_Attributes::write_Data(object_Data, 0x18 + ((e - 1) * 4), c);
                                }
                            }
                            else if (c == 1 && e == 1)
                            {
                                for (int f = 0; f < 4; f++)
                                {
                                    const unsigned int platform_ID_Array[4] = { 0x141A019B, 0x141A019C, 0x141A019D, 0x141A019E };
                                    vector<unsigned int> object_Data = instance_ID_Offset(vector_Platform_offsets, platform_ID_Array[f]);
                                    Random_Enemy_Attributes::write_Data(object_Data, 0xD6, c);
                                }
                            }
                        }
                    }
                }
                else if (i == 37)
                {
                    enemy_Data_Size = Array_Turret[c][0];
                    for (unsigned int e = 1; e < enemy_Data_Size; e += 1)
                    {
                        if (c == 0 && randoScaleSeperate == true)
                        {
                            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
                        }
                        Random_Enemy_Attributes::write_Data(EnemyOffsets[i][o], Array_Turret[c][e], c);
                    }
                }
                else if (i == 38)
                {
                    enemy_Data_Size = Array_AmbientAI[c][0];
                    for (unsigned int e = 1; e < enemy_Data_Size; e++)
                    {
                        if (c == 0 && randoScaleSeperate == true)
                        {
                            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
                        }
                        Random_Enemy_Attributes::write_Data(EnemyOffsets[i][o], Array_AmbientAI[c][e], c);
                    }
                }
                else if (i == 39)
                {
                    enemy_Data_Size = Array_Swarm[c][0];
                    for (unsigned int e = 1; e < enemy_Data_Size; e++)
                    {
                        if (c == 0 && randoScaleSeperate == true)
                        {
                            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
                        }
                        Random_Enemy_Attributes::write_Data(EnemyOffsets[i][o], Array_Swarm[c][e], c);
                    }
                }
                else if (i == 40)
                {
                    enemy_Data_Size = Array_MetroidPrimeStage1[c][0];
                    for (unsigned int e = 1; e < enemy_Data_Size; e++)
                    {
                        Random_Enemy_Attributes::write_Data(EnemyOffsets[i][o], Array_MetroidPrimeStage1[c][e], c);
                    }
                }
                else if (i == 41)
                {
                enemy_Data_Size = Array_IncineratorDrone[c][0];
                for (unsigned int e = 1; e < enemy_Data_Size; e++)
                {
                    if (c == 0 && randoScaleSeperate == true)
                    {
                        randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
                    }
                    Random_Enemy_Attributes::write_Data(EnemyOffsets[i][o], Array_IncineratorDrone[c][e], c);
                    if (c == 0)
                    {
                        vector<unsigned int> object_Data = instance_ID_Offset(vector_Actor_offsets, 0x00300004); // Actor Contraption Eye
                        Random_Enemy_Attributes::write_Data(object_Data, Array_IncineratorDrone[c][e], c);
                    }
                    if (c == 0 && e == 3)
                    {
                        randomized_Value = Random_Enemy_Attributes::randomFloat(speedLow, speedHigh);

                        for (int f = 0; f < 17; f++)
                        {
                            const unsigned int actorKeyFrame_ID_Array[17] = { 0x00300030, 0x00300032, 0x0030004A, 0x0030004B, 0x00300055, 
                                0x00300056, 0x0030005A, 0x0030005B, 0x00300065, 0x00300069, 0x00300071, 0x00300072,
                                0x00300073, 0x00300074, 0x00300075, 0x00300076, 0x00302745 };
                            vector<unsigned int> object_Data = instance_ID_Offset(vector_ActorKeyFrame_offsets, actorKeyFrame_ID_Array[f]);
                            Random_Enemy_Attributes::write_Data(object_Data, 0xE, c);
                        }
                        for (int f = 0; f < 21; f++)
                        {
                            const unsigned int timer_ID_Array[21] = { 0x0030017B, 0x00302732, 0x00300012, 0x0030006A, 0x00300007,
                                0x003027D6, 0x0030005C, 0x00300079, 0x00300050, 0x00300078, 0x00302737, 0x00302744,
                                0x0030005D, 0x0030004D, 0x00302743, 0x00302742, 0x00300062, 0x00300041, 0x00300014,
                                0x00302744, 0x00302742 };
                            vector<unsigned int> object_Data = instance_ID_Offset(vector_Timer_offsets, timer_ID_Array[f]);
                            Random_Enemy_Attributes::write_Data(object_Data, 0x0, 3);
                            Random_Enemy_Attributes::write_Data(object_Data, 0x4, 3);
                        }
                    }
                }
                }
            }
        }
    }
    // Extra Actors to randomize Scale
    // Parasite Queens in tube
    randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
    for (int i = 0; i < 3; i++)
    {
        //Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, instance_ID_Offset(vector_Actor_offsets, 0x0028026e), 0x18 + ((e - 1) * 4), 0xFF);
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x000E0093), 0x18 + (i * 4), 0xFF); //Actor 
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x040e000a), 0x18 + (i * 4), 0xFF); //Actor
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    randomized_Value = Random_Enemy_Attributes::randomFloat(speedLow, speedHigh);
    Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_ActorKeyFrame_offsets, 0x000E0092), 0xE, 0xFF); //ActorKeyFrame
    Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_ActorKeyFrame_offsets, 0x040E000D), 0xE, 0xFF); //ActorKeyFrame
    Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_ActorKeyFrame_offsets, 0x040E0023), 0xE, 0xFF); //ActorKeyFrame

    //Samples in Biohazard Containment

    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x00140028), 0x18 + (i * 4), 0xFF); //Actor 
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x00140029), 0x18 + (i * 4), 0xFF); //Actor
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x0014002a), 0x18 + (i * 4), 0xFF); //Actor 
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x0014002c), 0x18 + (i * 4), 0xFF); //Actor
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x0014002d), 0x18 + (i * 4), 0xFF); //Actor 
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x0014002e), 0x18 + (i * 4), 0xFF); //Actor
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x00140030), 0x18 + (i * 4), 0xFF); //Actor 
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x00140031), 0x18 + (i * 4), 0xFF); //Actor
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x00140032), 0x18 + (i * 4), 0xFF); //Actor 
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x00140033), 0x18 + (i * 4), 0xFF); //Actor
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x00140036), 0x18 + (i * 4), 0xFF); //Actor 
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x00140037), 0x18 + (i * 4), 0xFF); //Actor
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x00140046), 0x18 + (i * 4), 0xFF); //Actor 
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    //Space Frigate Ridley Break Free
    randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x00070098), 0x18 + (i * 4), 0xFF); //Actor
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    randomized_Value = Random_Enemy_Attributes::randomFloat(speedLow, speedHigh);
    Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_ActorKeyFrame_offsets, 0x000700D0), 0xE, 0xFF); //ActorKeyFrame
    //Ridely Flyby in Phendrana Drifts
    randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Platform_offsets, 0x100202A3), 0x18 + (i * 4), 0xFF); //Platform
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_ActorKeyFrame_offsets, 0x1002029E), 0xE, 0xFF); //ActorKeyFrame
    Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_ShadowProjector_offsets, 0x1002029c), 0xD, 0xFF); //Shadow Projector
    //Drone in Research Entrance
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x081402e4), 0x18 + (i * 4), 0xFF); //Actor
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x081402f9), 0x18 + (i * 4), 0xFF); //Actor
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    //Chozo Ghosts in Artifact Temple
    randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x381004a6), 0x18 + (i * 4), 0xFF); //Actor
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x381004a7), 0x18 + (i * 4), 0xFF); //Actor
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x381004a8), 0x18 + (i * 4), 0xFF); //Actor
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x381004a9), 0x18 + (i * 4), 0xFF); //Actor
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x381004aa), 0x18 + (i * 4), 0xFF); //Actor
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x381004ab), 0x18 + (i * 4), 0xFF); //Actor
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x381004ac), 0x18 + (i * 4), 0xFF); //Actor
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x381004ad), 0x18 + (i * 4), 0xFF); //Actor
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x381004ae), 0x18 + (i * 4), 0xFF); //Actor
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x381004af), 0x18 + (i * 4), 0xFF); //Actor
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x381004b0), 0x18 + (i * 4), 0xFF); //Actor
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x381004b1), 0x18 + (i * 4), 0xFF); //Actor
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    //Elite Pirates With No Real Pirate
    randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x001401c4), 0x18 + (i * 4), 0xFF); //Actor
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x001401c3), 0x18 + (i * 4), 0xFF); //Actor
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }

    //Elite Pirate Actors to make not solid
    Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x001401c4), 0x153, 0xFF, true, 0x00);
    Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x001401c3), 0x153, 0xFF, true, 0x00);
    Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x04140385), 0x153, 0xFF, true, 0x00);
    // Metroid Prime Exo Intro
    randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
    for (int i = 0; i < 3; i++)
    {
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x00050002), 0x18 + (i * 4), 0xFF); //Actor
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x00050090), 0x18 + (i * 4), 0xFF); //Actor
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x00050076), 0x18 + (i * 4), 0xFF); //Actor
        Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_Actor_offsets, 0x0005008f), 0x18 + (i * 4), 0xFF); //Actor
        if (randoScaleSeperate == true)
        {
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
    }
    randomized_Value = Random_Enemy_Attributes::randomFloat(speedLow, speedHigh);
    Random_Enemy_Attributes::write_Data(instance_ID_Offset(vector_ActorKeyFrame_offsets, 0x0005006E), 0xE, 0xFF); //ActorKeyFrame
}

void Random_Enemy_Attributes::write_Data(vector<unsigned int> enemy_Data, unsigned int offset, unsigned int conditional, bool small_Value, unsigned int tiny_Value)
{
    unsigned int instance_ID = enemy_Data[0];
    unsigned int current_Offset = enemy_Data[1];
    unsigned int enemy_Type = enemy_Data[2];
    if (current_Offset < 0x00001000)
    {
        cout << "whoops, better add 1 to the iteration" << endl;
        return;
    }
    if (small_Value == false)
    {
        if (set <unsigned int> {Beetle, Drone, Eyon, MetroidAlpha, PuddleSpore, StoneToad, FlickerBat, Parasite, Ripper, WarWasp, GunTurret}.count(enemy_Type))
        {
            offset += 0x4;
            if (enemy_Type == Drone && conditional != 0)
            {
                offset += 0x4;
            }
        }
        times = 0;
        if (enemy_Type == BabySheegoth && conditional == 2 && randomized_Value > 1.0)
        {
            randomized_Value /= random_Scale;
        }
        while (enemy_Type == Drone && conditional == 0 && (randomized_Value > 6 || randomized_Value < 0.05))
        {
            if (times >= 50)
            {
                randomized_Value = Random_Enemy_Attributes::randomFloat(0.05, 6);
                break;
            }
            if ((scaleLow < 0.05 && scaleHigh < 0.05) || (scaleLow > 6 && scaleHigh > 6))
            {
                if (scaleHigh > 6)
                {
                    randomized_Value = 6;
                }
                else if (scaleLow < 0.05)
                {
                    randomized_Value = 0.05;
                }
                break;
            }
            times++;
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
        times = 0;
        while (enemy_Type == ElitePirate && conditional == 0 && (randomized_Value > 2.3 || randomized_Value < 0.05) && instance_ID == 0x0C180137)
        {
            if (times >= 50)
            {
                randomized_Value = Random_Enemy_Attributes::randomFloat(0.05, 2.3);
                break;
            }
            if ((scaleLow < 0.05 && scaleHigh < 0.05) || (scaleLow > 2.3 && scaleHigh > 2.3))
            {
                if (scaleHigh > 2.3)
                {
                    randomized_Value = 2.3;
                }
                else if (scaleLow < 0.05)
                {
                    randomized_Value = 0.05;
                }
                break;
            }
            times++;
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
        times = 0;
        while (enemy_Type == ElitePirate && conditional == 0 && (randomized_Value > 1.3 || randomized_Value < 0.05) && (set <int> {0x040D01A4, 0x04100338}.count(instance_ID)))
        {
            if (times >= 50)
            {
                randomized_Value = Random_Enemy_Attributes::randomFloat(0.05, 1.3);
                break;
            }
            if ((scaleLow < 0.05 && scaleHigh < 0.05) || (scaleLow > 1.3 && scaleHigh > 1.3))
            {
                if (scaleHigh > 1.3)
                {
                    randomized_Value = 1.3;
                }
                else if (scaleLow < 0.05)
                {
                    randomized_Value = 0.05;
                }
                break;
            }
            times++;
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
        times = 0;
        //while (enemy_Type == ElitePirate && conditional == 0 && (randomized_Value > 2 || randomized_Value < 0.1) && offset_Position == 4)
        //{
            //if (times >= 50)
            //{
                //randomized_Value = Random_Enemy_Attributes::randomFloat(0.1, 2.0);
                //break;
            //}
            //if ((scaleLow < 0.1 && scaleHigh < 0.1) || (scaleLow > 2 && scaleHigh > 2))
            //{
                //if (scaleHigh > 2)
                //{
                    //randomized_Value = 2;
                //}
                //else if (scaleLow < 0.1)
                //{
                    //randomized_Value = 0.1;
                //}
                //break;
            //}
            //times++;
            //randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        //}
        //times = 0;
        if (instance_ID == 0x000E0010 && enemy_Type == IceSheegoth && conditional == 0)
        {
            while (randomized_Value > 1.5 || randomized_Value < 0.1)
            {
                if (times >= 50)
                {
                    randomized_Value = Random_Enemy_Attributes::randomFloat(0.1, 1.5);
                    break;
                }
                if ((scaleLow < 0.1 && scaleHigh < 0.1) || (scaleLow > 1.5 && scaleHigh > 1.5))
                {
                    if (scaleHigh > 1.5)
                    {
                        randomized_Value = 1.5;
                    }
                    else if (scaleLow < 0.1)
                    {
                        randomized_Value = 0.1;
                    }
                    break;
                }
                times++;
                randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
            }
        }
        else if (enemy_Type == IceSheegoth && conditional == 0)
        {
            while (randomized_Value > 1.1 || randomized_Value < 0.1)
            {
                if (times >= 50)
                {
                    randomized_Value = Random_Enemy_Attributes::randomFloat(0.1, 1.1);
                    break;
                }
                if ((scaleLow < 0.1 && scaleHigh < 0.1) || (scaleLow > 1.1 && scaleHigh > 1.1))
                {
                    if (scaleHigh > 1.1)
                    {
                        randomized_Value = 1.1;
                    }
                    else if (scaleLow < 0.1)
                    {
                        randomized_Value = 0.1;
                    }
                    break;
                }
                times++;
                randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
            }
        }
        times = 0;
        while (enemy_Type == Flaahgra && conditional == 0 && (randomized_Value > 3.3 || randomized_Value < 0.15))
        {
            if (times >= 50)
            {
                randomized_Value = Random_Enemy_Attributes::randomFloat(0.15, 3.3);
                break;
            }
            if ((scaleLow < 0.15 && scaleHigh < 0.15) || (scaleLow > 3.3 && scaleHigh > 3.3))
            {
                if (scaleHigh > 3.3)
                {
                    randomized_Value = 3.3;
                }
                else if (scaleLow < 0.15)
                {
                    randomized_Value = 0.15;
                }
                break;
            }
            times++;
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
        times = 0;
        while ((enemy_Type == Flaahgra || enemy_Type == FlaahgraTentacle) && conditional == 2 && (randomized_Value > 3 || randomized_Value < 0.05))
        {
            if (times >= 50)
            {
                randomized_Value = Random_Enemy_Attributes::randomFloat(0.05, 3.0);
                break;
            }
            if ((speedLow < 0.05 && speedHigh < 0.05) || (speedLow > 2 && speedHigh > 2))
            {
                if (speedHigh > 3)
                {
                    randomized_Value = 3;
                }
                else if (speedLow < 0.05)
                {
                    randomized_Value = 0.05;
                }
                break;
            }
            times++;
            randomized_Value = Random_Enemy_Attributes::randomFloat(speedLow, speedHigh);
        }
        times = 0;
        while (enemy_Type == Thardus && conditional == 0 && (randomized_Value > 2 || randomized_Value < 0.05))
        {
            if (times >= 50)
            {
                randomized_Value = Random_Enemy_Attributes::randomFloat(0.05, 2.0);
                break;
            }
            if ((scaleLow < 0.05 && scaleHigh < 0.05) || (scaleLow > 2 && scaleHigh > 2))
            {
                if (scaleHigh > 2)
                {
                    randomized_Value = 2;
                }
                else if (scaleLow < 0.05)
                {
                    randomized_Value = 0.05;
                }
                break;
            }
            times++;
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
        times = 0;
        while (enemy_Type == OmegaPirate && conditional == 0 && (randomized_Value > 2 || randomized_Value < 0.05))
        {
            if (times >= 50)
            {
                randomized_Value = Random_Enemy_Attributes::randomFloat(0.05, 2.0);
                break;
            }
            if ((scaleLow < 0.05 && scaleHigh < 0.05) || (scaleLow > 2 && scaleHigh > 2))
            {
                if (scaleHigh > 2)
                {
                    randomized_Value = 2;
                }
                else if (scaleLow < 0.05)
                {
                    randomized_Value = 0.05;
                }
                break;
            }
            times++;
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
        times = 0;
        while (enemy_Type == OmegaPirate && conditional == 2 && (randomized_Value > 1.5 || randomized_Value < 0.50))
        {
            if (times >= 50)
            {
                randomized_Value = Random_Enemy_Attributes::randomFloat(0.05, 1.5);
                break;
            }
            if ((speedLow < 0.50 && speedHigh < 0.50) || (speedLow > 1.5 && speedHigh > 1.5))
            {
                if (speedHigh > 1.5)
                {
                    randomized_Value = 1.5;
                }
                else if (speedLow < 0.50)
                {
                    randomized_Value = 0.50;
                }
                break;
            }
            times++;
            randomized_Value = Random_Enemy_Attributes::randomFloat(speedLow, speedHigh);
        }
        times = 0;
        while (enemy_Type == Ridley && conditional == 0 && (randomized_Value > 1.3 || randomized_Value < 0.2))
        {
            if (times >= 50)
            {
                randomized_Value = Random_Enemy_Attributes::randomFloat(0.2, 1.3);
                break;
            }
            if ((scaleLow < 0.2 && scaleHigh < 0.2) || (scaleLow > 1.3 && scaleHigh > 1.3))
            {
                if (scaleHigh > 1.3)
                {
                    randomized_Value = 1.3;
                }
                else if (scaleLow < 0.2)
                {
                    randomized_Value = 0.2;
                }
                break;
            }
            times++;
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
        times = 0;
        while (enemy_Type == MetroidPrimeEssence && conditional == 0 && (randomized_Value > 1.8 || randomized_Value < 0.05))
        {
            if (times >= 50)
            {
                randomized_Value = Random_Enemy_Attributes::randomFloat(0.05, 1.8);
                break;
            }
            if ((scaleLow < 0.05 && scaleHigh < 0.05) || (scaleLow > 1.8 && scaleHigh > 1.8))
            {
                if (scaleHigh > 1.8)
                {
                    randomized_Value = 1.8;
                }
                else if (scaleLow < 0.05)
                {
                    randomized_Value = 0.05;
                }
                break;
            }
            times++;
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
        times = 0;
        while (enemy_Type == MetroidPrimeExoskelton && conditional == 0 && (randomized_Value > 1.8 || randomized_Value < 0.15))
        {
            if (times >= 50)
            {
                randomized_Value = Random_Enemy_Attributes::randomFloat(0.15, 1.8);
                break;
            }
            if ((scaleLow < 0.15 && scaleHigh < 0.15) || (scaleLow > 1.8 && scaleHigh > 1.8))
            {
                if (scaleHigh > 1.8)
                {
                    randomized_Value = 1.8;
                }
                else if (scaleLow < 0.15)
                {
                    randomized_Value = 0.15;
                }
                break;
            }
            times++;
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
        times = 0;
        while (enemy_Type == ParasiteQueen && conditional == 0 && (randomized_Value > 3 || randomized_Value < 0.1))
        {
            if (times >= 50)
            {
                randomized_Value = Random_Enemy_Attributes::randomFloat(0.1, 3.0);
                break;
            }
            if ((scaleLow < 0.1 && scaleHigh < 0.1) || (scaleLow > 3 && scaleHigh > 3))
            {
                if (scaleHigh > 3)
                {
                    randomized_Value = 3;
                }
                else if (scaleLow < 0.1)
                {
                    randomized_Value = 0.1;
                }
                break;
            }
            times++;
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
        times = 0;
        while (enemy_Type == FlaahgraTentacle && conditional == 0 && (randomized_Value > 3 || randomized_Value < 0.05))
        {
            if (times >= 50)
            {
                randomized_Value = Random_Enemy_Attributes::randomFloat(0.05, 3.0);
                break;
            }
            if ((scaleLow < 0.05 && scaleHigh < 0.05) || (scaleLow > 3 && scaleHigh > 3))
            {
                if (scaleHigh > 3)
                {
                    randomized_Value = 3;
                }
                else if (scaleLow < 0.05)
                {
                    randomized_Value = 0.05;
                }
                break;
            }
            times++;
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
        times = 0;
        while (enemy_Type == Zoid && conditional == 0 && (randomized_Value > 3 || randomized_Value < 0.2))
        {
            if (times >= 50)
            {
                randomized_Value = Random_Enemy_Attributes::randomFloat(0.2, 3.0);
                break;
            }
            if ((scaleLow < 0.2 && scaleHigh < 0.2) || (scaleLow > 3 && scaleHigh > 3))
            {
                if (scaleHigh > 3)
                {
                    randomized_Value = 3;
                }
                else if (scaleLow < 0.2)
                {
                    randomized_Value = 0.2;
                }
                break;
            }
            times++;
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
        times = 0;
        while (enemy_Type == Drone && (set <int> {0x081C008F, 0x081C0094, 0x082C006C, 0x082C0124}.count(instance_ID)) && conditional == 0 && (randomized_Value > 1.75 || randomized_Value < 0.05))
        {
            if (times >= 50)
            {
                randomized_Value = Random_Enemy_Attributes::randomFloat(0.05, 1.75);
                break;
            }
            if ((scaleLow < 0.05 && scaleHigh < 0.05) || (scaleLow > 1.75 && scaleHigh > 1.75))
            {
                if (scaleHigh > 1.75)
                {
                    randomized_Value = 1.75;
                }
                else if (scaleLow < 0.05)
                {
                    randomized_Value = 0.05;
                }
                break;
            }
            times++;
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
        times = 0;
        // change this so that Flaahgra's yellow health is randomized
        if (enemy_Type == Flaahgra && conditional == 1)
        {
            return;
        }
        if (enemy_Type == ReaperVine || enemy_Type == StoneToad)
        {
            if (conditional == 0)
            {
                return;
            }
        }
        if ((enemy_Type == Eyon || enemy_Type == StoneToad || enemy_Type == Ridley) && (conditional == 2 || conditional == 3))
        {
            return;
        }
        while (enemy_Type == ChozoGhost && conditional == 2 && (randomized_Value > 2.5 || randomized_Value < 0.05))
        {
            if (times >= 50)
            {
                randomized_Value = Random_Enemy_Attributes::randomFloat(0.05, 2.5);
                break;
            }
            if ((speedLow < 0.05 && speedHigh < 0.05) || (speedLow > 4 && speedHigh > 4))
            {
                if (speedHigh > 4)
                {
                    randomized_Value = 4;
                }
                else if (speedLow < 0.05)
                {
                    randomized_Value = 0.05;
                }
                break;
            }
            times++;
            randomized_Value = Random_Enemy_Attributes::randomFloat(speedLow, speedHigh);
        }
        times = 0;
        // If Chozo ghost is to small sometimes it can't reach its "waypoint" when it spawns
        while (enemy_Type == ChozoGhost && conditional == 0 && (randomized_Value > 2.0 || randomized_Value < 0.5))
        {
            if (times >= 50)
            {
                randomized_Value = 0.5;
                break;
            }
            if ((scaleLow < 0.5 && scaleHigh < 0.5) || (scaleLow > 2.0 && scaleHigh > 2.0))
            {
                if (scaleHigh > 2.0)
                {
                    randomized_Value = 2.0;
                }
                else if (scaleLow < 0.5)
                {
                    randomized_Value = 0.5;
                }
                break;
            }
            times++;
            randomized_Value = Random_Enemy_Attributes::randomFloat(scaleLow, scaleHigh);
        }
        times = 0;
        // Limit speed of space pirates in Elite Pirate room
        while (enemy_Type == SpacePirate && conditional == 2 && randomized_Value > 2 && (set <unsigned int> {0x141A0273, 0x141A0274, 0x141A02FE, 0x141A0448, 
            0x141A0463, 0x141A0464, 0x141A0465, 0x141A0466}.count(instance_ID)))
        {
            if (times >= 50)
            {
                randomized_Value = Random_Enemy_Attributes::randomFloat(0.05, 2.0);
                break;
            }
            if (speedLow > 2 || (speedLow > 2 && speedHigh > 2))
            {
                randomized_Value = 2;
                break;
            }
            times++;
            randomized_Value = Random_Enemy_Attributes::randomFloat(speedLow, speedHigh);
        }

        unsigned int value = Random_Enemy_Attributes::return_Data(current_Offset + offset, false);
        float* pp = (float*)&value;
        if (conditional == 0xDD)
        {
            (*pp) = randomized_Value;
        }
        else if (conditional == 3)
        {
            (*pp) /= randomized_Value;
        }
        else
        {
            (*pp) *= randomized_Value;
        }
        if (in_out.is_open())
        {
            in_out.seekp(current_Offset + offset);
        }
        unsigned char* address = (unsigned char*)&value;
        unsigned char c0 = address[0];
        unsigned char c1 = address[1];
        unsigned char c2 = address[2];
        unsigned char c3 = address[3];
        address[0] = c3;
        address[1] = c2;
        address[2] = c1;
        address[3] = c0;
        if (randomized_Value == INFINITY)
        {
            throw invalid_argument("randomized Value is 'INFINITY', Fantaselion dun goofed");
        }
        if (in_out.is_open())
        {
            in_out.write((char*)&value, 4);
        }
    }
    else if (enemy_Type != StoneToad)
    {
        if (set <unsigned int> {Beetle, ChozoGhost, Eyon, MetroidAlpha, PuddleSpore, StoneToad, FlickerBat, Parasite, Ripper, WarWasp, GunTurret}.count(enemy_Type))
        {
            offset += 0x4;
        }
        unsigned int value = 0;
        float* pp = (float*)&value;
        (*pp) = tiny_Value;
        if (in_out.is_open())
        {
            in_out.seekp(current_Offset + offset);
            in_out.write((char*)&value, 1);
        }
    }
}

float Random_Enemy_Attributes::randomFloat(float low, float high)
{
    if (low == high)
    {
        return high;
    }

    uniform_real_distribution<> RNG(low, high);

    return RNG(gen);
}

vector <unsigned int> Random_Enemy_Attributes::instance_ID_Offset(const vector< vector<unsigned int> >&v, unsigned int ID, bool offset)
{
    bool take_second = false;
    if (set <unsigned int> {0x00050090, 0x0005008f, 0x001401c3, 0x001401c4}.count(ID))
    {
        take_second = true;
    }
    for (int first_element = 1; first_element < v[0][0]; first_element++)
    {
        if (v[first_element][0] == ID && !offset)
        {
            if (take_second)
            {
                take_second = false;
                continue;
            }
            return v[first_element];
        }
        else if (v[first_element][1] == ID && offset)
        {
            if (take_second)
            {
                take_second = false;
                continue;
            }
            return v[first_element];
        }
    }
    stringstream exception_Message;
    if (offset)
    {
        exception_Message << "Offset" << "0x" << hex << setw(8) << setfill('0') << ID << " not found in vector" << endl;
    }
    else
    {
        exception_Message << "Instance ID " << "0x" << hex << setw(8) << setfill('0') << ID << " not found in vector" << endl;
    }
    const std::string s = exception_Message.str();
    clean_Up();
    throw invalid_argument(s);
}