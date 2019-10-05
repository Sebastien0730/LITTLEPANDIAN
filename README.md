# Python-seed

## Dependency

Version: Python 3

Download packages
```bash
pip install signalrcore
```
---
## Run locally

```bash
python main.py GAME_SERVER=ws://localhost:5001
```
---
## Instructions

Code your bot logic in the function **get_next_direction()**  which you can find in the **bot.py**

Param:   
**GameInfo game_info**: Information send by the server. You can find a map, some information about your adversary and some other information about yourself. 

Return:     
**Direction**: Return direction that bot will take in its next move