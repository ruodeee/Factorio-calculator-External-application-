import tkinter as tk
from tkinter import ttk 
from PIL import ImageTk, Image
import FactorioCalc
import IconExtractor
import io
from zipfile import ZipFile
import re

def setup(modfp):
    global micons 
    global bicons
    micons = IconExtractor.GetmodIcons(modfp)
    bicons = IconExtractor.GetBaseIcons(basefp)

def show_image(tar):
    imagefile = findicon(tar)
    image = ImageTk.PhotoImage(data=io.BytesIO(imagefile).read())
    parent.config(image=image)
    parent.image = image

def findicon(tar):
    if tar == "motor":
        tar = "single-cylinder-engine"
    if tar == "electric-motor":
        tar = "small-electric-motor"
    if tar == "se-rocket-science-pack":
        tar = "orange"
    if tar.startswith("se-"):
        tar = tar.replace("se-","")
    print(f"Getting icon: {tar}")
    for item in bicons:
        if item == (f"{tar}.png"):
            with open(f"{bicons[item]}", "rb") as image:
                img = Image.open(f"{bicons[item]}")
                image = img.crop((0,0,64,64))
                image.save("test.png")
                with open("test.png", "rb") as image:
                    f = image.read()
                    print(f"icon found:{bicons[item]}")
                    b = bytearray(f)
                return b
    for mod in micons:
        for item in micons[mod]:
            if item.filename.endswith(f"/{tar}.png"):
                with ZipFile(mod) as myzip:
                    with myzip.open(item) as myfile:
                        print(f"icon found:{item}")
                        image = myfile.read()
                        return image
    print(f"Icon not found: {tar}")
    with open(f"placeholder.png", "rb") as image:
                img = Image.open(f"placeholder.png")
                image = img.crop((0,0,64,64))
                image.save("test.png")
                with open("test.png", "rb") as image:
                    f = image.read()
                    b = bytearray(f)
                    return b

def TreePop(item):
    global ids
    ipms = ipm.get()
    tree.delete(*tree.get_children())
    ids = []
    global storedimgs
    recipes = FactorioCalc.GetRecipes(filepath)
    for name in recipes:
        if item in name:
            if name.startswith("se-"):
                item = name
                break
        if item == name:
            item = name
            break
    print(recipes[item]['ingredients'])
    jsn = FactorioCalc.HumanFriendly(item)
    imagefile = findicon(item)
    image =ImageTk.PhotoImage(data=io.BytesIO(imagefile).read())
    storedimgs.append(image)
    a = float(ipms)/float(recipes[item]['products'][0]['amount'])
    tree.insert('', tk.END,jsn, open=False,image= image, values=(f"{jsn}",recipes[item]['products'][0]['amount']*a,FactorioCalc.NumOfAss(item,recipes,ipms)))
    items = FactorioCalc.GetSubIngredient(item,recipes)
    for ingr in items:
        imagefile = findicon(ingr['name'])
        image =ImageTk.PhotoImage(data=io.BytesIO(imagefile).read())
        storedimgs.append(image)
        idn = f"{ingr['name']}0"
        ids.append(idn)
        tree.insert(f'{jsn}', tk.END,idn, open=False,image= image, values=(f"{ingr['name']}",ingr['amount']*a,FactorioCalc.NumOfAss(ingr['name'],recipes,ingr['amount']*a)))
        subitems = FactorioCalc.GetSubIngredient(ingr['name'],recipes)
        subingri(subitems,idn,a)

def subingri(subitems,parent,ipm):
    recipes = FactorioCalc.GetRecipes(filepath)
    for subingr in subitems:
        imagefile = findicon(subingr['name'])
        image =ImageTk.PhotoImage(data=io.BytesIO(imagefile).read())
        storedimgs.append(image)
        high = 0
        for idno in ids:
            x = re.search(f"{subingr['name']}",idno)
            if x:
                if int(idno[-1]) > high:
                    high = int(idno[-1])
            idn = f"{subingr['name']}{high+1}"
        ids.append(idn)
        tree.insert(parent, tk.END,idn, open=False,image= image, values=(f"{subingr['name']}",subingr['amount']*ipm,FactorioCalc.NumOfAss(subingr['name'],recipes,subingr['amount']*ipm)))
        sub = FactorioCalc.GetSubIngredient(subingr['name'],recipes)
        if sub != None:
            subingri(sub,idn,ipm)

filepath = r"C:\Users\rudyb\AppData\Roaming\Factorio\script-output\recipe-lister"
modfp= r"C:\Users\rudyb\AppData\Roaming\Factorio\mods"
basefp = r"C:\Program Files (x86)\Steam\steamapps\common\Factorio\data\base\graphics\icons"
setup(modfp)
root = tk.Tk()
root.title("Demo")
root.geometry("750x900")

frame = tk.Frame(root)
frame.pack()

frame3 = tk.Frame(root)
frame3.pack()

button = tk.Button(frame, text="QUIT", fg="red", command=quit)
button.pack(side=tk.LEFT)

#dropdown menu
recipes = FactorioCalc.GetRecipes(filepath)
temp = []
storedimgs = []
for item in recipes:
    temp.append(FactorioCalc.HumanFriendly(item))
recipes = temp
recipesDD = ttk.Combobox(frame3,values=recipes, state='normal')
Assemblers = FactorioCalc.GetAssMachines(filepath)
temp = []
for item in Assemblers:
    temp.append(FactorioCalc.HumanFriendly(item))
Assemblers = temp
AssemblersDD = ttk.Combobox(frame3,values=Assemblers, state='normal')
AssemblersDD.set("assembling machine 1")
furnace = FactorioCalc.GetFurnace(filepath)
temp = []
for item in furnace:
    temp.append(FactorioCalc.HumanFriendly(item))
furnace = temp
furnaceDD = ttk.Combobox(frame3, values=furnace, state='normal')
recipesDD.pack(side=tk.LEFT)
AssemblersDD.pack(side=tk.LEFT)
furnaceDD.pack(side=tk.LEFT)

#Buttons
image = tk.Button(frame, text="image", command=lambda: show_image(FactorioCalc.JsonFriendly(recipesDD.get())))
image.pack(side=tk.LEFT)
calculater = tk.Button(frame, text="calculate", command=lambda: show_image(FactorioCalc.JsonFriendly(recipesDD.get())))
calculater.pack(side=tk.LEFT)
treeB = tk.Button(frame,text="TreeB", command= lambda:TreePop(FactorioCalc.JsonFriendly(recipesDD.get())))
treeB.pack(side=tk.LEFT)
#IPM input
entry_float = tk.DoubleVar()
entry_float.set(1.0)
ipm = ttk.Entry(frame3,textvariable=entry_float)
ipm.pack(side=tk.LEFT)

# label to show the image
frame2 = tk.Frame(root)
frame2.pack()
parent = tk.Label(frame2)
parent.pack()
#treeview
style = ttk.Style()
style.configure('Treeview',rowheight=64)
coloumns = ('#0','#1','#2','#3')
tree = ttk.Treeview(frame2,columns=coloumns, height=900)
tree.heading('#0', text='icon', anchor=tk.W)
tree.heading('#1', text='Item', anchor=tk.W)
tree.heading('#2', text='Ratios', anchor=tk.W)
tree.heading('#3', text='Assemblers', anchor=tk.W)
tree.pack()

root.mainloop()