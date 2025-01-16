import tkinter as tk
from tkinter import ttk
from turtle import RawTurtle, ScrolledCanvas
from LSystem import LSystem
import turtle

drawing = False
outlineFrames = False

rules = {}
behavior = {}

# Create the main application window
root = tk.Tk()
root.title("L-System tinkerer")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)

# Create a canvas for turtle graphics
canvas = ScrolledCanvas(root)
canvas.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  # Use grid for canvas

# Create a frame for the UI controls
ui_frame = tk.Frame(root, width=300, padx=10, pady=10, bg="lightgrey", highlightbackground="red", highlightthickness=int(outlineFrames))
ui_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")  # Use grid for ui_frame

# Function to add rules to the listbox
def add_rule():
    left_rule = left_entry.get()
    right_rule = right_entry.get()
    if (left_rule and right_rule) and not left_rule in rules.keys():  # Ensure both fields are filled
        # rules[left_rule] = right_rule
        # rule = f"{left_rule} → {right_rule}"
        # rules_listbox.insert(tk.END, rule)
        # left_entry.delete(0, tk.END)
        # right_entry.delete(0, tk.END)

        #! UNFINISHED

        ...
# Function to delete a selected rule
def delete_rule():
    try:
        selected_rule_index = rules_listbox.curselection()
        selected_rule:str = rules_listbox.get(selected_rule_index)
        rules.pop(selected_rule.split(" → ")[0])
        rules_listbox.delete(selected_rule_index)
    except Exception:
        pass  # Do nothing if no rule is selected

def add_behavior():
    left_rule = behavior_entry.get()
    right_rule = behavior_combobox.get()
    if (left_rule and right_rule) and not left_rule in behavior.keys():  # Ensure both fields are filled
        match right_rule:
            case "no action":...
            case "forward":...
        
        
        rules[left_rule] = right_rule
        rule = f"{left_rule} → {right_rule}"
        
        behavior_listbox.insert(tk.END, rule)
        behavior_entry.delete(0, tk.END)
        behavior_combobox.set("no action")
def delete_behavior():
    ...
# Function to clear the turtle's drawings and move it to the origin
def clear_turtle():
    global drawing
    if drawing: return
    t.clear()  # Clear the drawing
    t.penup()  # Lift the pen so it doesn't draw while moving
    t.goto(0, 0)  # Move the turtle to the origin (0, 0)
    t.seth(90)
    t.pendown()  # Put the pen back down to continue drawing when needed

# Function to perform drawing actions (can be modified based on your logic)
def draw_turtle():
    global drawing
    if drawing: return
    clear_turtle()
    drawing = True
    t.circle(10)
    drawing = False

#region controls
control_frame = tk.Frame(ui_frame, bg="lightgrey", highlightbackground="red", highlightthickness=int(outlineFrames))
control_frame.grid(row=0, column=0, columnspan=3)

tk.Label(control_frame, text="─────── Control ───────", bg="lightgrey", font=("Fira Code", 10, "bold")).grid(row=0, column=0, columnspan=3, pady=0)

angle_subframe = tk.Frame(control_frame, bg="lightgrey", highlightbackground="red", highlightthickness=int(outlineFrames))
angle_subframe.grid(row=1, column=0, padx=6)

angle_entry = tk.Entry(angle_subframe, validate="key", width=10, validatecommand=(root.register(lambda v: v.isdigit() or v == ""), "%P"))
angle_entry.grid(row=0, column=1, pady=4, padx=10)
tk.Label(angle_subframe, text="angle:", bg="lightgrey").grid(row=0, column=0)

distance_subframe = tk.Frame(control_frame, bg="lightgrey", highlightbackground="red", highlightthickness=int(outlineFrames))
distance_subframe.grid(row=2, column=0, padx=6)

distance_entry = tk.Entry(distance_subframe, validate="key", width=10, validatecommand=(root.register(lambda v: v.isdigit() or v == ""), "%P"))
distance_entry.grid(row=0, column=1, pady=4, padx=10)
tk.Label(distance_subframe, text="distance:", bg="lightgrey").grid(row=0, column=0)

button_subframe = tk.Frame(control_frame, bg="lightgrey", highlightbackground="red", highlightthickness=int(outlineFrames))
button_subframe.grid(row=3, padx=6)

clear_button = tk.Button(button_subframe, text="Clear", command=clear_turtle, width=10)
clear_button.grid(row=0, column=5)

draw_button = tk.Button(button_subframe, text="Draw", command=draw_turtle, width=10)
draw_button.grid(row=0, column=1, padx=5)
#endregion

#region rules
rule_frame = tk.Frame(ui_frame, bg="lightgrey", highlightbackground="red", highlightthickness=int(outlineFrames))
rule_frame.grid(row=1, column=0, columnspan=3, pady=0)

tk.Label(rule_frame, text="──────── Rules ────────", bg="lightgrey", font=("Fira Code", 10, "bold")).grid(row=0, column=0, columnspan=3, pady=5)

entry_subframe = tk.Frame(rule_frame, bg="lightgrey", highlightbackground="red", highlightthickness=int(outlineFrames))
entry_subframe.grid(row=1, column=0, padx=6)

left_entry = tk.Entry(entry_subframe, width=10)
left_entry.grid(row=1, column=0, padx=5)
tk.Label(entry_subframe, text="→", bg="lightgrey", font=("arial", 14)).grid(row=1, column=1, padx=5)
right_entry = tk.Entry(entry_subframe, width=10)
right_entry.grid(row=1, column=2, padx=5)

button_frame = tk.Frame(rule_frame, bg="lightgrey", highlightbackground="red", highlightthickness=int(outlineFrames))
button_frame.grid(row=2, column=0, columnspan=3, pady=0)
# Add button
add_button = tk.Button(button_frame, text="Add Rule", command=add_rule, width=10)
add_button.grid(row=0, column=0, padx=5)

# Delete button
delete_button = tk.Button(button_frame, text="Delete Rule", command=delete_rule, width=10)
delete_button.grid(row=0, column=1, padx=5)

# Listbox to display added rules
rules_listbox = tk.Listbox(rule_frame, height=10, width=30)
rules_listbox.grid(row=3, column=0, columnspan=3, pady=5)
#endregion

#region turtle rules
t_rules_frame  = tk.Frame(ui_frame, bg="lightgrey", highlightbackground="red", highlightthickness=int(outlineFrames))
t_rules_frame.grid(column=0, row=2)
tk.Label(t_rules_frame, text="─── Turtle Behavior ───", bg="lightgrey", font=("Fira Code", 10, "bold")).grid(row=0, column=0)

input_subframe = tk.Frame(t_rules_frame, bg="lightgrey", highlightbackground="red", highlightthickness=int(outlineFrames))
input_subframe.grid(row=1)

behavior_entry = tk.Entry(input_subframe, width=10)
behavior_entry.grid(row=0, column=0)

tk.Label(input_subframe, text="→", bg="lightgrey", font=("arial", 14)).grid(row=0, column=1, padx=5)

behavior_combobox = ttk.Combobox(input_subframe, state="readonly", width=10, values=["no action", "forward", "backward", "leaf", "start branch", "end branch"])
behavior_combobox.set("no action")
behavior_combobox.grid(row=0, column=2)

button_subframe = tk.Frame(t_rules_frame, bg="lightgrey", highlightbackground="red", highlightthickness=int(outlineFrames))
button_subframe.grid(row=2, column=0, columnspan=3, pady=0)
# Add button
add_button = tk.Button(button_subframe, text="Add Behavior", command=add_behavior, width=10)
add_button.grid(row=0, column=0, padx=5)

# Delete button
delete_button = tk.Button(button_frame, text="Delete Behavior", command=delete_behavior, width=10)
delete_button.grid(row=0, column=1, padx=5)

# Listbox to display added rules
behavior_listbox = tk.Listbox(t_rules_frame, height=10, width=30)
behavior_listbox.grid(row=3, column=0, columnspan=3, pady=5)

#endregion

# Create a TurtleScreen using the canvas
screen = turtle.TurtleScreen(canvas)

t = RawTurtle(canvas)
t.seth(90)

# Run the Tkinter main loop
root.mainloop()
