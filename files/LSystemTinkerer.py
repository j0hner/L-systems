import os
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.scrolledtext
from turtle import RawTurtle, ScrolledCanvas

import LSystem
from LSystem import LSystem, setPos, can_deserialze
import turtle

drawing = False
outlineFrames = False

rules = {}
behavior = {}
presets = {}

TRDropdownItems = ["none", "forward","jump forward", "backward","left", "right", "turn around" "leaf", "start branch", "end branch", "start poly", "add point", "end poly"]

#region window setup + scrollbar

root = tk.Tk()
root.geometry("1000x700")
root.title("L-System tinkerer")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)

scrollable_container = tk.Frame(root)
scrollable_container.grid(row=0, column=1, sticky="nsew")
scrollable_container.grid_rowconfigure(0, weight=1)
scrollable_container.grid_columnconfigure(0, weight=1)

ui_canvas = tk.Canvas(scrollable_container, bg="lightgrey")
ui_canvas.grid(row=0, column=0, sticky="nsew")

scrollbar = ttk.Scrollbar(scrollable_container, orient="vertical", command=ui_canvas.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
ui_canvas.configure(yscrollcommand=scrollbar.set)

ui_canvas.configure(width=210)
ui_frame = tk.Frame(ui_canvas, width=300, padx=10, pady=10, bg="lightgrey", highlightbackground="red", highlightthickness=int(outlineFrames))
ui_canvas.create_window((0, 0), window=ui_frame, anchor="nw", width=210)
ui_frame.bind("<Configure>", lambda _: ui_canvas.configure(scrollregion=ui_canvas.bbox("all")))

#endregion

turtle_canvas = ScrolledCanvas(root)
turtle_canvas.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

screen = turtle.TurtleScreen(turtle_canvas)

t = RawTurtle(screen)
t.speed(0)

def add_rule():
    left_rule = left_entry.get()
    right_rule = right_entry.get()
    if (left_rule and right_rule) and not left_rule in rules.keys():  # Ensure both fields are filled
        rules[left_rule] = right_rule
        rule = f"{left_rule} → {right_rule}"
        rules_listbox.insert(tk.END, rule)
        left_entry.delete(0, tk.END)
        right_entry.delete(0, tk.END)
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
        
        rule = f"{left_rule} → {right_rule}"
        behavior_listbox.insert(tk.END, rule)
        behavior_entry.delete(0, tk.END)
        behavior_combobox.set("none")
        
        behavior[left_rule] = right_rule
def delete_behavior():
    try:
        selected_rule_index = behavior_listbox.curselection()
        selected_rule:str = behavior_listbox.get(selected_rule_index)
        if selected_rule.split(" → ")[1] != "none": behavior.pop(selected_rule.split(" → ")[0])
        behavior_listbox.delete(selected_rule_index)
    except Exception:
        pass  # Do nothing if no rule is selected

def clear_turtle():
    global drawing
    if drawing: return
    setPos(t, (0,-300), 90)
def draw():
    global drawing
    if drawing: return
    if not fields_ok(): return
    system_from_fields().DrawState(int(depth_entry.get()), not animate.get(), (0,-300), 90)

    drawing = False

def reset(ask:bool = True):
    global rules, behavior,presets, drawing
    
    if ask and not messagebox.askokcancel("Reset", "Are you sure? The default values will be restored.\nThis action does not affect presets."): return

    drawing = False
    clear_turtle()
    setPos(t, (0,-300), 90)
    rules_listbox.delete(0, tk.END)
    rules = {}
    
    behavior_listbox.delete(0, tk.END)
    rules_listbox.delete(0, tk.END) 
    preset_listbox.delete(0, tk.END) 
    
    behavior = {}
    behavior_items = ["+ → right", "- → left", "[ → start branch", "] → end branch", "| → turn around", "{ → start poly", ". → add point", "} → end poly"]
    for item in behavior_items:
        behavior_listbox.insert(tk.END, item)
        behavior[item.split(" → ")[0]] = item.split(" → ")[1]

    presets = {}

    # Walk through the directory and its subdirectories
    for root, _, files in os.walk(f"{os.path.dirname(__file__)}/save", onerror=lambda e: print(e)):
        for file in files:
            if not os.path.join(root, file).endswith('.json'): continue
            
            path = os.path.join(root, file)
            
            # Open and read the file content
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    preset_json = f.read()
                    if not can_deserialze(t, preset_json): continue
                    presets[file.replace(".json", "").replace("_", " ")] = preset_json
            except Exception as e:
                print(f"failed to read '{path}': {e}")
    
    for key in presets.keys():
        preset_listbox.insert(tk.END, key)
def error(message:str):
    messagebox.showerror("Error", message)
def fields_ok() -> bool:
    if not start_entry.get(): error("the start field must contain a value") ;  return False
    if not depth_entry.get(): error("the depth field must contain a value") ; return False
    if not angle_entry.get(): error("the angle field must contain a value") ; return False
    if not distance_entry.get(): error("the distance field must contain a value") ; return False
    return True
def system_from_fields():
    
    
    variables = []
    constants = ["[","]","+","-", "{", ".", "}"]
    for key in rules.keys():
        if key not in variables: variables.append(key)
        for char in rules.get(key):
            if char not in variables and char.isalpha(): variables.append(char)
            elif char not in constants and not char.isalpha(): constants.append(char)

    return LSystem(
        rules,
        constants,
        variables,
        start_entry.get(),
        behavior,
        t,
        int(angle_entry.get()),
        int(distance_entry.get())
    )
def FillFieldsWithSys(lSys:LSystem):
    global rules, behavior
    if not isinstance(lSys, LSystem): raise ValueError(f"Can't fill fields with {type(lSys)}. (only LSystem)")
    
    angle_entry.set(lSys.angle)
    distance_entry.set(lSys.length)
    start_entry.delete(0,tk.END)
    start_entry.insert(0, lSys.initState)

    rules_listbox.delete(0,tk.END)
    rules = lSys.rules
    for key in rules.keys():
        rules_listbox.insert(tk.END, f"{key} → {lSys.rules[key]}")

    behavior_listbox.delete(0,tk.END)
    behavior = lSys.turtleRules
    for key in behavior.keys():
        behavior_listbox.insert(tk.END, f"{key} → {lSys.turtleRules[key]}")

def Load_preset(ask:bool = True, name:str = None):
    try:
        if not name:
            selected_preset_index = preset_listbox.curselection()
            name = preset_listbox.get(selected_preset_index)
            if ask and not messagebox.askokcancel("Load", "Are you sure? This will load the selected preset and override the fields.\nMake sure to save your work!"): return
        FillFieldsWithSys(LSystem.deserialize(t,presets[name]))
    except Exception:
        pass  # Do nothing if no rule is selected    
def Save_preset():
    if not fields_ok(): return
    
    def save():
        name = save_field.get()
        if name in presets.keys():
            error("That name is occupied.")
            return

        with open(f"{os.path.dirname(__file__)}/save/user/{name.replace(" ", "_")}.json", "w+") as f:
            f.write(system_from_fields().serialize())

        reset(False)
        Load_preset(False, name)
        save_popup.destroy()

    save_popup = tk.Toplevel(root)
    save_popup.attributes("-topmost", True)
    save_popup.title("Save preset")

    save_label = tk.Label(save_popup, text="Name your preset: ")
    save_label.grid(row=0, column=0, pady=2, padx=2)

    save_field = tk.Entry(save_popup)
    save_field.grid(row=0, column=1, pady=2, padx=2)

    close_button = tk.Button(save_popup, text="Cancel", width=10, command=save_popup.destroy)
    close_button.grid(row = 1, column = 0, pady=2, padx=2)

    widget_save_button = tk.Button(save_popup, text="Save", width=10, command=save)
    widget_save_button.grid(row = 1, column = 1, pady=2, padx=2)
def Delete_preset(ask:bool = True):
    try:
        selected_preset_index = preset_listbox.curselection()
        selected_preset:str = preset_listbox.get(selected_preset_index)
        def_path = os.path.join(f"{os.path.dirname(__file__)}/save/default/", f"{selected_preset.replace(" ", "_")}.json")
        usr_path = os.path.join(f"{os.path.dirname(__file__)}/save/user/", f"{selected_preset.replace(" ", "_")}.json")
        if os.path.exists(def_path): error("Default presets can't be deleted from the GUI.");return
        if ask and not messagebox.askokcancel("Delete", "Are you sure? This will PERMANENTLY delete the selected preset."): return
        print(usr_path, def_path, sep="\n")
        os.remove(usr_path)
        reset(False)
    except Exception:
        pass  # Do nothing if no rule is selected

#region controls
control_frame = tk.Frame(ui_frame, bg="lightgrey", highlightbackground="red", highlightthickness=int(outlineFrames))
control_frame.grid(row=0, column=0, columnspan=3)
tk.Label(control_frame, text="─────── Control ───────", bg="lightgrey", font=("Fira Code", 10, "bold")).grid(row=0, column=0, columnspan=3, pady=0)

field_frame = tk.Frame(control_frame, bg="lightgrey", highlightbackground="red", highlightthickness=int(outlineFrames))
field_frame.grid(row=1, column=0)

angle_subframe = tk.Frame(field_frame, bg="lightgrey", highlightbackground="red", highlightthickness=int(outlineFrames))
angle_subframe.grid(row=1, column=0, padx=6, sticky="w")

tk.Label(angle_subframe, text="angle:", bg="lightgrey", font=("Fira Code", 10)).grid(row=0, column=0)
angle_entry = ttk.Spinbox(angle_subframe, from_=-360, to=360, width=10)
angle_entry.grid(row=0, column=1, pady=4, padx=10)

distance_subframe = tk.Frame(field_frame, bg="lightgrey", highlightbackground="red", highlightthickness=int(outlineFrames))
distance_subframe.grid(row=2, column=0, padx=6, sticky="w")

tk.Label(distance_subframe, text="distance:", bg="lightgrey", font=("Fira Code", 10)).grid(row=0, column=0)
distance_entry = ttk.Spinbox(distance_subframe, from_=1, to=100, width=6)
distance_entry.grid(row=0, column=1, pady=4, padx=10)

depth_subframe = tk.Frame(field_frame, bg="lightgrey", highlightbackground="red", highlightthickness=int(outlineFrames))
depth_subframe.grid(row=3, column=0, padx=6, sticky="w")

tk.Label(depth_subframe, text="depth:", bg="lightgrey", font=("Fira Code", 10)).grid(row=0, column=0)
depth_entry = ttk.Spinbox(depth_subframe, from_=1, to=20, width=10)
depth_entry.grid(row=0, column=1, pady=4, padx=10)

start_subframe = tk.Frame(field_frame, bg="lightgrey", highlightbackground="red", highlightthickness=int(outlineFrames))
start_subframe.grid(row=4, column=0, padx=6, sticky="w")

start_entry = tk.Entry(start_subframe, width=12)
start_entry.grid(row=0, column=1, pady=4, padx=10)
tk.Label(start_subframe, text="start:", bg="lightgrey", font=("Fira Code", 10)).grid(row=0, column=0)
anim_subframe = tk.Frame(field_frame, bg="lightgrey", highlightbackground="red", highlightthickness=int(outlineFrames))
anim_subframe.grid(row=5, column=0, padx=6)

animate = tk.BooleanVar()
anim_entry = tk.Checkbutton(anim_subframe, variable=animate, bg="lightgrey")
anim_entry.grid(row=0, column=0)
tk.Label(anim_subframe, text="animate", bg="lightgrey", font=("Fira Code", 10)).grid(row=0, column=1)

button_subframe = tk.Frame(control_frame, bg="lightgrey", highlightbackground="red", highlightthickness=int(outlineFrames))
button_subframe.grid(row=6, padx=6)

reset_button = tk.Button(button_subframe, text="Reset", command=reset, width=10)
reset_button.grid(row=0, column=1, padx=2)

draw_button = tk.Button(button_subframe, text="Draw", command=draw, width=10)
draw_button.grid(row=0, column=0, padx=2)
#endregion

#region rules
rule_frame = tk.Frame(ui_frame, bg="lightgrey", highlightbackground="red", highlightthickness=int(outlineFrames))
rule_frame.grid(row=1, column=0, columnspan=3, pady=0)

tk.Label(rule_frame, text="──────── Rules ────────", bg="lightgrey", font=("Fira Code", 10, "bold")).grid(row=0, column=0, columnspan=3, pady=5)

entry_subframe = tk.Frame(rule_frame, bg="lightgrey", highlightbackground="red", highlightthickness=int(outlineFrames))
entry_subframe.grid(row=1, column=0, padx=6)

left_entry = tk.Entry(entry_subframe, width=10, validate="key", validatecommand=(root.register(lambda v: len(v) < 2), "%P"))
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

behavior_entry = tk.Entry(input_subframe, width=10, validate="key", validatecommand=(root.register(lambda v: len(v) < 2), "%P"))
behavior_entry.grid(row=0, column=0)

tk.Label(input_subframe, text="→", bg="lightgrey", font=("arial", 14)).grid(row=0, column=1, padx=5)

behavior_combobox = ttk.Combobox(input_subframe, state="readonly", width=10, values=TRDropdownItems)
behavior_combobox.set("none")
behavior_combobox.grid(row=0, column=2)

button_subframe = tk.Frame(t_rules_frame, bg="lightgrey", highlightbackground="red", highlightthickness=int(outlineFrames))
button_subframe.grid(row=2, column=0, columnspan=3, pady=0)
# Add button
add_button = tk.Button(button_subframe, text="Add Behavior", command=add_behavior, width=10)
add_button.grid(row=0, column=0, padx=5)

# Delete button
delete_button = tk.Button(button_subframe, text="Delete Behavior", command=delete_behavior)
delete_button.grid(row=0, column=1, padx=5)

# Listbox to display added rules
behavior_listbox = tk.Listbox(t_rules_frame, height=10, width=30)
behavior_listbox.grid(row=3, column=0, columnspan=3, pady=5)
#endregion

#region presets
presets_frame  = tk.Frame(ui_frame, bg="lightgrey", highlightbackground="red", highlightthickness=int(outlineFrames))
presets_frame.grid(column=0, row=3)
tk.Label(presets_frame, text="─────── Presets ───────", bg="lightgrey", font=("Fira Code", 10, "bold")).grid(row=0, column=0)

preset_listbox = tk.Listbox(presets_frame, height=10, width=30)
preset_listbox.grid(row=1)

preset_buttons_subframe = tk.Frame(presets_frame)
preset_buttons_subframe.grid(row=2, pady=4)

load_button = tk.Button(preset_buttons_subframe, text="Load", command=Load_preset, width=7)
load_button.grid(row=3, column=0)

save_button = tk.Button(preset_buttons_subframe, text="Save", command=Save_preset, width=7)
save_button.grid(row=3, column=1)

delete_button = tk.Button(preset_buttons_subframe, text="Delete", command=Delete_preset, width=7)
delete_button.grid(row=3, column=2)
#endregion

reset(False)
root.mainloop()
