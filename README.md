# Automatic Goggles

Easily manage remote sessions, run pre-configured missions, all in one place!

## How does this work?
0. `./automatic-goggles.py`
1. Initialize a node for connecting
  - Use `listen <bind_port>` or `connect <addr> <port>`
2. Upon receiving a connection you can:
  - List all current nodes: `list`
  - Add tags to your nodes to help organize: `tag <node> <tag_string>`
  - Drop into a shell on a node: `shell <node_id>`
  - Run missions on specific nodes: `assign <node_id> <path_to_script>` & `autostart <node_id>`
  - Close connections: `kill <node_id>`
  - Remove node from list: `remove <node_id>`
  - Export commands ran during sessions with their output: `export`
  - And more!

## FAQ
- *Why would I want to use automatic goggles over other solutions?*
  - I believe that automatic goggles makes handling multiple sessions simple and easy. And it has the unqiue ability to run preconfigured missions with scripts you create yourself (or use the ones I've made even though they aren't super helpful).
- *What do you think is the best part about automatic goggles right now?*
  - It's simplicity :) 

