# yaml-builder-for-Home Assistant (HA)

# Description

Batch program in python producing a yaml file in output based on a templates. This was created to ease &amp; have consistency when configuring home assistant with YAML but it works in other use cases where you need to produce YAML files. 

# Features
- Replace a part of a YAML file by inserting a template
- The template rendering engine is Jinja2 (see https://jinja.palletsprojects.com/en/2.11.x/), to replace value, if statement logic etc...
- Possibility to bundle several template into a single file (allowing to group few around a common theme for example)
- Recurcive template processing
- Possibility to pass any custom parameters to the template
- Possibility to pass Home-Assistant objects to the template (if used in HA context of course)

# Example1 - Build automatically 1 automation for each "scene" of a room based on the selection done in a "input_select".
To understand the meaning of the example, you probably need to be knoweldgeable on Homa-Assistant & how its YAML configuraiton works.
In this example, with 10 lines of template + 20 lines of main code, we will generate automatically 200 lines of YAML in this example.
I use this to have a better "semantic" view of my files and this can enforse easily consistency across similar needs (like here all automations uses the same templete, if we change the template you rebuild and have all automations adapted, no risk to forget one update.

You need one template for the automation: template1.yaml
in this case it reprends the "how" a functionality is rendered in native YAML for Home-Assistant
 ```
 - id: 'change input select to {{ j.newstate }} for {{ j.inputselect }}'
  alias: 'change input select to {{ j.newstate }} for {{ j.inputselect }}'
  trigger:
    - platform: state
      entity_id: input_select.{{ j.inputselect }}
      to: '{{ j.newstate }}'
  action:
    - service: scene.turn_on
      entity_id: scene.scene_{{ j.room }}_{{ j.newstate }}
      
```
The main file represents the "what to do" in a more functional way. It does not describe the "how" (this part is managed in the template).
We ra passing parameters to the template using a json structure.
The main file for the builder: main1.yaml
```
#-----------------------------------------------------------------------------
# Scene activation based on input option for bureau
#-----------------------------------------------------------------------------
#include template1.yaml,{"newstate":"day"          ,"inputselect": "state_bureau", "room": "bureau"}
#include template1.yaml,{"newstate":"evening"      ,"inputselect": "state_bureau", "room": "bureau"}
#include template1.yaml,{"newstate":"homeworking"  ,"inputselect": "state_bureau", "room": "bureau"}
#include template1.yaml,{"newstate":"sleep_all"    ,"inputselect": "state_bureau", "room": "bureau"}
#include template1.yaml,{"newstate":"sleep_chronos","inputselect": "state_bureau", "room": "bureau"}
#include template1.yaml,{"newstate":"presence"     ,"inputselect": "state_bureau", "room": "bureau"}

#-----------------------------------------------------------------------------
# Scene activation based on input option for my office
#-----------------------------------------------------------------------------
#include template1.yaml,{"newstate":"all_off"      ,"inputselect": "state_salon", "room": "salon"}
#include template1.yaml,{"newstate":"presence"     ,"inputselect": "state_salon", "room": "salon"}
#include template1.yaml,{"newstate":"ready"        ,"inputselect": "state_salon", "room": "salon"}
#include template1.yaml,{"newstate":"tv_on_day"    ,"inputselect": "state_salon", "room": "salon"}
#include template1.yaml,{"newstate":"tv_on_evening","inputselect": "state_salon", "room": "salon"}
#include template1.yaml,{"newstate":"tv_off"       ,"inputselect": "state_salon", "room": "salon"}

```

