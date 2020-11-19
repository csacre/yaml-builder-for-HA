# yaml-builder-for-Home Assistant (HA)

# Description

Batch program in python producing a yaml file in output based on a functional template decomposition. This was created to ease &amp; have consistency when configuring home assistant with YAML but it works in other use cases where you need to produce YAML files. 

# Features
- The template engine is Jinja2 (see https://jinja.palletsprojects.com/en/2.11.x/)
- Replace a part of a YAML file by inserting a template
- Can run Jinja2 on the template file (to replace value, if statement logic etc...)
- Recurcive replacement (template refered in template etc...)
- Possibility to pass any custom parameters to the template
- Possibility to pass Home-Assistant objects to the template

# Example1 - Build a list of automations for each scene
You need one template for the automation: template1.yaml
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
The main file for the builder: main1.yaml
```
#-----------------------------------------------------------------------------
# Scene activation based on input option
#-----------------------------------------------------------------------------
#include template1.yaml,{"#block": "1", "newstate":"day"          ,"inputselect": "state_bureau", "room": "bureau"}
#include template1.yaml,{"#block": "1", "newstate":"evening"      ,"inputselect": "state_bureau", "room": "bureau"}
#include template1.yaml,{"#block": "1", "newstate":"homeworking"  ,"inputselect": "state_bureau", "room": "bureau"}
#include template1.yaml,{"#block": "1", "newstate":"sleep_all"    ,"inputselect": "state_bureau", "room": "bureau"}
#include template1.yaml,{"#block": "1", "newstate":"sleep_chronos","inputselect": "state_bureau", "room": "bureau"}
#include template1.yaml,{"#block": "1", "newstate":"presence"     ,"inputselect": "state_bureau", "room": "bureau"}
```

