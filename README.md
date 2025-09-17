L-System tinkerer
=
- A fun tkinter gui to mess with l-systems and turtle graphics in.
- If you don't know what L-systems are, look at the [wiki](https://en.wikipedia.org/wiki/L-system)

Build
-
- To build DOWNLOAD PYTHON and click run as user. (an .exe will come eventually i'm just lazy)
- So far it has no dependencies

Features
-
Upon launching the program you will see a large turtle canvas on the left and a bunch of fields on the right.
The ui is split into a few categories:
  1. Control - defines the fundamental properties of the system
  2. Rules - defines the behavior of the system
  3. Turtle Behavior - defines the behavior of the turtle (shocker ik)
  4. Presets - let you save and load your l-systems, or acces some default ones

Control
-
has several labeled fields and 2 buttons:
  1. angle - accepts an int from -360 to 360 and defines how much left or right is the turtle gonna turn when a + or - constant is hit
  2. distance - accepts an int from 1 to 100 and defines how far forward or back is the turtle gonna move each segment
  3. depth - accepts an int from 1 to 20 and defines to which recursion level the l-system is drawn (you are most likely not gonna need more that 20 depth but if you do, just edit the code ¯\\\_(ツ)\_/¯ )
  4. start - accepts one chatacter and defines the l-system's start state
  5. animate - will supress the turtles animation when unchecked (eg. for simple operations the turtle will finish instantly, for more complex ones you'll have to wait a bit)
  6. draw button - will start drawing the defined l-system (assuming all fields are filled in correctly)
  7. reset button - will empty all the fields and reset the turtle

Rules
-
Has 2 fields an add button a remove button and a list containing the active rules.
  - To add another rule put the input of the rule into the left field (accepts only a single character) and the outcome into the right field, then press "add rule".
  - To delete a rule, seleft it in the list and press "delete rule"
  - As for constants +,-,\[ and \] are constants by default. to add another just make a rule in which the input and output match

Turtle Behavior
-
Has a field, a dropdown, and 2 buttons similar to those in rules.
  - To add a behavior type a character into the left and choose an action from the dropdown.
  - All the actions should be pretty self explanatory, except for start and end branch, so let me explain those. on start branch the current position of the turtle gets saved to a LIFO stack and on end branch a position         is popped and restored
  - The buttons work the same way as in rules

Presets
-
Has a list containing all saved presets and 3 buttons:
  - Load - will load the selected item overriding the fields
  - Save - will save the current field data under a name (and add it to the list)
  - Delete - Will delete the sected **User created** preset

----------
- there are warnings in places where work might be lost (such as reset, load etc.)
- it is still under development _(that's a lie younger me made)_



