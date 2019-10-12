# Plant Game

A basic plant game, where plants grow in a garden. There are rocks and water, which act as obstacles for plants and the character. The character can run around and collect "mature" flowers. When all the flowers are dead, the game is over.

All pixel art is original and was created by the author for this game. 

<img src="https://github.com/sonjabrits/plant_game/blob/master/plant_game.PNG?raw=true" alt="Plant Game Screenshot" height="400">

## Current features
### Flowers
* One flower spawns at a random location at the beginning of the game.
* Flowers have different life stages: growing, mature, wilting, dying, dead.
* At each stage transition, there is a chance to spawn a child plant, within a certain radius.
* If the location of the spawn is already occupied, the spawn fails.
* In the "mature" phase, the flowers can be collected by the character, causing them to disappear

### Environment elements
* Rocks or water patches are spawned in random location at the start of the game
* Flowers cannot spawn on an environment element
* The character cannot walk over environment elements 

### Character
* The character can be controlled by the AWSD or arrow keys
* The character has a flower count in its inventory which increases if he collects a flower 

## Planned features
* Environmental elements have an affect on the growth of plants
* NPCs who walk around and affect plants (eg worms or birds)
* Different difficulty mode, where plant growth is affected
