# PARAMETEREDITOR
Randomizes most enemy (and bosses) stats: scale, health, speed, damage, and knockback power within a user defined range for the game "Metroid Prime"

Build instructions are written for linux but the windows version of them should work. (For windows you can also just run 'python setup.py build_ext --inplace' in the root directory if you have cython and python already)

# Usage

## Python Module
```sh
> pip install PARAMETEREDITOR
> python
>>> import PARAMETEREDITOR
>>> PARAMETEREDITOR.PyPARAMETEREDITOR("input.iso", "output.iso", 601310422, 0.25, 4, 0.25, 4, 0.25, 4, 0.25, 4, 0.25, 4, True) # (Input, Output, Seed, ScaleLow, ScaleHigh, HealthLow, HealthHigh, SpeedLow, Speedhigh, DamageLow, DamageHigh, KnockbackPowerLow, KnockbackPowerHigh, RandoScaleXYZSeperatly)
```

# Windows

## Python

```
tools/venv.sh
tools/build-cython.sh
```

## Standalone
```sh
tools/build-standalone.sh
