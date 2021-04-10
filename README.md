# Valkyrie LoL Deployable Resources 
This is the repository with valkyrie data (images, jsons, scripts etc) which is deployed to each user computer.

Some modifications require throughout testing (modifying logic in core python modules/scripts) and some don't (adding a image / modifying spell database). 

## Some rules before you start modifying stuff
- If you modify core scripts/helper modules please make sure you test throughly that you did not broke anything
- Do not manually modify the following files SpellCalculations.json, ItemData.json, SkinInfo.json these files are automatically updated
- Please respect the coding formatting/style used (so if everywhere variables are named `like_this` don't start naming variable `likeThis`, also tabs instead of spaces)
- More rules will probably come based on what stupid things some people will attempt
 
## Directory structure
```py
│
├───CoreScripts (Here are the valkyrie core scripts (orbwalker, spell tracker etc). All core script begin with 'vk_' by convention)
│       'vk_activator.py'
│       'vk_aimcast.py'
│       'vk_cassiopeia.py'
│       ...
│
└───Deployable (This is the folder that its downloaded in %APPDATA%\Valkyrie on users machines)
    │   'changelog.txt'  # Simple text file with stuff thats been changed from version to version
    │   'vfont.ttf'      # The font used in the menu (Later this might be moved to a directory to allow multiple fonts)
    │
    ├───configs (This must remain empty)
    ├───data (Data used by the cheat)
    │       'icons_champs.zip'       # Icons with champions
    │       'icons_extra.zip'        # Other icons
    │       'icons_spells.zip'       # Icons with spells
    │       'ItemData.json'          # Json item data (this is always updated automatically)
    │       'SkinInfo.json'          # Json skin data for skin changer (this is always updated automatically)
    │       'SpellCalculations.json' # Json spell calculations formulas and values used by damages.py (this is always updated automatically)
    │       'SpellData.json'         # Json with spell data a.k.a spell db (since auto updating doesnt work properly on this we must manually adjust the values)
    │       'UnitData.json'          # Json with unit data (same story as with spelldata)
    │       'WallMask.bin'           # 512x512 grid representing all walkable/wall points in summoners rift
    │
    ├───dependencies (Dlls that are required for valkyrie to run)
    │       'aws-c-common.dll'
    │       'aws-c-event-stream.dll'
    │       'aws-checksums.dll'
	│       ...
    │
    ├───docs (Here you can find the python scripting API docs. It is updated automatically)
    │       'docs.html' # valkyrie module docs generated with python pdoc package
    │
    ├───payload (Here the valkyrie DLL sits)
    └───scripts 
        └───helpers (Helper modules that are imported by normal scripts)
                'damages.py'      # Damage lib, this module reads SpellCalculations.json and provides damage calculations, although champion spells must still be bound manually to the formula
                'drawings.py'     # Utils for drawing stuff
                'flags.py'        # Utils for communicating between scripts
                'inputs.py'       # Utils for input handling
                'items.py'        # Utils for item specific logic
                'prediction.py'   # Utils for prediction (the core prediction still sits in valkyrie dll)
                'spells.py'       # Utils for spells
                'targeting.py'    # Utils for unit targeting
                'templates.py'    # Easy to use templates for reusing logic (ex: ChampionScript)
```
