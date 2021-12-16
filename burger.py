# Imported libraries
import os
from time import sleep

# Banner
banner = """ 
  _____         __               ___                       
 / ___/_ _____ / /____  __ _    / _ )__ _________ ____ ____
/ /__/ // (_-</ __/ _ \/  ' \  / _  / // / __/ _ `/ -_) __/
\___/\_,_/___/\__/\___/_/_/_/ /____/\_,_/_/  \_, /\__/_/   
                                            /___/          
"""

# Global variable mainBurger
mainBurger = []

# List of Burger components
burgerComponents = ['MEAT','FRUITVEG','SPICES','CHEESE','SAUCES','BREAD','SALAD','BACON']

# Function meat
def meat():
    meatList = ['no meat','beef','lamb'] # List of meat
    print("Choose your meat from our selection:\n")
    print(meatList) # Display meatList
    opt = str(input("What is your choice? "))

    # Check user input if matches on the list
    if opt in meatList:
        mainBurger.append(opt)   # Append the user input to global variable mainBurger
        meatList.remove(opt) # Removes the user input from fruitvegList

    elif opt not in meatList:
        print("The option is invalid.")
        sleep(2)
        meat()

    if len(burgerComponents) == 0:
        print("\nYour burger is fully customized.")
        print(f"Your burger components: {mainBurger}")
    elif len(burgerComponents) > 0:
        burgerComponents.remove('MEAT')

    main()

# Function fruitveg    
def fruitveg():
    fruitvegList = ['no fruitandveggies','onion','celery','courgette','red pepper','fresh apples','apricots','pineapple','mushroom'] # List of Fruits and Veggies
    print("Choose your fruit and veggies from our selection:\n")
    print(fruitvegList) # Display fruitvegList
    opt = str(input("What is your choice? "))

    # Check user input if matches on the list
    if opt in fruitvegList:
        mainBurger.append(opt)   # Append the user input to global variable mainBurger
        fruitvegList.remove(opt) # Removes the user input from fruitvegList

    elif opt not in fruitvegList:
        print("The option is invalid.")
        sleep(2)
        fruitveg()
        
    if len(burgerComponents) == 0:
        print("\nYour burger is fully customized.")
        print(f"Your burger components: {mainBurger}")
    elif len(burgerComponents) > 0:
        burgerComponents.remove('FRUITVEG')
        
    main()

# Function spices
def spices():
    spicesList = ['no spices','ginger','5spice','herbs','currypaste','parsley','rosemary','chilly flakes','garlic','mint'] # List of spices
    print("Choose your spices from our selection:\n")
    print(spicesList) # Display spicesList
    opt = str(input("What is your choice? "))

    # Check user input if matches on the list
    if opt in spicesList:
        mainBurger.append(opt)  # Append the user input to global variable mainBurger
        spicesList.remove(opt)  # Removes the user input from spicesList

    elif opt not in spicesList:
        print("The option is invalid.")
        sleep(2)
        spices()

    if len(burgerComponents) == 0:
        print("\nYour burger is fully customized.")
        print(f"Your burger components: {mainBurger}")
    elif len(burgerComponents) > 0:
        burgerComponents.remove('SPICES')

    main()

# Function cheese
def cheese():
    cheeseList = ['no cheese','cheddar','stilton','feta','mozzarella'] # List od cheese
    print("Choose your cheese from our selection:\n")
    print(cheeseList) # Display cheeseList
    opt = str(input("What is your choice? "))

    # Check user input if matches on the list
    if opt in cheeseList:
        mainBurger.append(opt)  # Append the user input to global variable mainBurger
        cheeseList.remove(opt)  # Removes the user input from cheeseList

    elif opt not in cheeseList:
        print("The option is invalid.")
        sleep(2)
        cheese()

    if len(burgerComponents) == 0:
        print("\nYour burger is fully customized.")
        print(f"Your burger components: {mainBurger}")
    elif len(burgerComponents) > 0:
        burgerComponents.remove('CHEESE')

    main()    

# Function sauces
def sauces():
    sauceList = ['no sauces','pesto','tomato puree','bbq','hotsauce','sweet chili','marmalade','chutney','ketchup','mayo'] # List of sauces
    print("Choose your sauce from our selection:\n")
    print(sauceList) # Display sauceList
    opt = str(input("What is your choice? "))

   # Check user input if matches on the list
    if opt in sauceList:
        mainBurger.append(opt)  # Append the user input to global variable mainBurger
        sauceList.remove(opt)   # Removes the user input from sauceList 

    elif opt not in sauceList:
        print("The option is invalid.")
        sleep(2)
        sauces()

    if len(burgerComponents) == 0:
        print("\nYour burger is fully customized.")
        print(f"Your burger components: {mainBurger}")
    elif len(burgerComponents) > 0:
        burgerComponents.remove('SAUCES')

    main()    

# Function bread
def bread():
    breadList = ['no bread','wrap','gluten free','bao','bun','wholemeal','sesame','pitta','baguette','brioche','naan','bagel'] # List of breads
    print("Choose your bread from our selection:\n")
    print(breadList) # Display breadList
    opt = str(input("What is your choice? "))

   # Check user input if matches on the list
    if opt in breadList:
        mainBurger.append(opt)  # Append the user input to global variable mainBurger
        breadList.remove(opt)   # Removes the user input from breadList

    elif opt not in breadList:
        print("The option is invalid.")
        sleep(2)
        bread()

    if len(burgerComponents) == 0:
        print("\nYour burger is fully customized.")
        print(f"Your burger components: {mainBurger}")
    elif len(burgerComponents) > 0:    
        burgerComponents.remove('BREAD')

    main()

# Function salad
def salad():
    saladList = ['no salad','pineapple','pepper','avocado','tomato','celery','onion','letuce','beetroot','pickle','cucumber'] # List od salads
    print("Choose your salad from our selection:\n")
    print(saladList) # Display saladList
    opt = str(input("What is your choice? "))

    # Check user input if matches on the list
    if opt in saladList:
        mainBurger.append(opt)  # Append the user input to global variable mainBurger
        saladList.remove(opt)   # Removes the user input from saladList

    elif opt not in saladList:
        print("The option is invalid.")
        sleep(2)
        salad()

    if len(burgerComponents) == 0:
        print("\nYour burger is fully customized.")
        print(f"Your burger components: {mainBurger}")
    elif len(burgerComponents) > 0:
       burgerComponents.remove('SALAD')

    main()

# Function bacon
def bacon():
    baconList = ['no bacon','lean baked bacon','bacon','turkey'] # List of bacons
    print(baconList) # Display baconList
    opt = str(input("What is your choice? "))

    # Check user input if matches on the list
    if opt in baconList:
        mainBurger.append(opt)  # Append the user input to global variable mainBurger
        baconList.remove(opt)   # Removes the user input from baconList

    elif opt not in baconList:
        print("The option is invalid.")
        sleep(2)
        bacon()

    if len(burgerComponents) == 0:
        print("\nYour burger is fully customized.")
        print(f"Your burger components: {mainBurger}")
    elif len(burgerComponents) > 0:
        burgerComponents.remove('BACON')

    main()       

# Function main / Driver funtion
def main():
    os.system("clear")
    print("Welcome to Custom Burgers\n")
    print("You may customize any of these parts of the burger.\n")
    print(burgerComponents) # Display burgerComponents
    if len(burgerComponents) == 0:
        os.system("clear")
        print(banner)
        print("\nYour burger is fully customized.")
        print(f"Your burger components: {mainBurger}")
    else:
        opt = input("Which part will you change first? ")
       
        if opt == 'meat' or opt == 'MEAT':
            # Check if the mainBurger has 8 items / check if all the components are customized
            if len(mainBurger) < 8:
                meat() # Call the function meat
            elif len(mainBurger) == 8:
                print("\nYour burger is fully customized.")
                print(f"Your burger components: {mainBurger}")
            else:
                main()

        elif opt == 'fruitveg' or opt == 'FRUITVEG':
            # Check if the mainBurger has 8 items / check if all the components are customized
            if len(mainBurger) < 8:
                fruitveg() # Call the function fruitveg
            elif len(mainBurger) == 8:
                print("\nYour burger is fully customized.")
                print(f"Your burger components: {mainBurger}")
            else:
                main()

        elif opt == 'spices' or opt == 'SPICES':
            # Check if the mainBurger has 8 items / check if all the components are customized
            if len(mainBurger) < 8:
                spices() # Call the function spices
            elif len(mainBurger) == 8:
                print("\nYour burger is fully customized.")
                print(f"Your burger components: {mainBurger}")
            else:
                main()

        elif opt == 'cheese' or opt == 'CHEESE':
            # Check if the mainBurger has 8 items / check if all the components are customized
            if len(mainBurger) < 8:
                cheese() # Call the function cheese
            elif len(mainBurger) == 8:
                print("\nYour burger is fully customized.")
                print(f"Your burger components: {mainBurger}")
            else:
                main()

        elif opt == 'sauces' or opt == 'SAUCES':
            # Check if the mainBurger has 8 items / check if all the components are customized
            if len(mainBurger) < 8:
                sauces() # Call the function sauces
            elif len(mainBurger) == 8:
                print("\nYour burger is fully customized.")
                print(f"Your burger components: {mainBurger}")
            else:
                main()

        elif opt == 'bread' or opt == 'BREAD':
            # Check if the mainBurger has 8 items / check if all the components are customized
            if len(mainBurger) < 8:
                bread() # Call the function bread
            elif len(mainBurger) == 8:
                print("\nYour burger is fully customized.")
                print(f"Your burger components: {mainBurger}")
            else:
                main()
        
        elif opt == 'salad' or opt == 'SALAD':
            # Check if the mainBurger has 8 items / check if all the components are customized
            if len(mainBurger) < 8:
                salad() # Call the function salad
            elif len(mainBurger) == 8:
                print("\nYour burger is fully customized.")
                print(f"Your burger components: {mainBurger}")
            else:
                main()
        
        elif opt == 'bacon' or opt == 'BACON':
            # Check if the mainBurger has 8 items / check if all the components are customized
            if len(mainBurger) < 8:
                bacon() # Call the function bacon
            elif len(mainBurger) == 8:
                print("\nYour burger is fully customized.")
                print(f"Your burger components: {mainBurger}")
            else:
                main()
                
        elif opt not in burgerComponents: # Check if the user input is valid
            print("The option is invalid.")
            sleep(2)
            main()
        else:
            os.system("clear")
            quit() # Exit the program if invalid input

# Execute main function
if __name__=="__main__":
    main()
