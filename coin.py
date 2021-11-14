def chkcoin():
  coin = int(input("Enter a coin value: "))

  if coin <= 4:
    print("That's a penny.")
  elif coin == 5 or coin <= 9:
    print("That's a nickel.")
  elif coin == 10 or coin <= 24:
    print("That's a dime.")
  elif coin == 25:
    print("That's a quarter.")
  elif coin >= 26:
    print("That's no a valid coin.")

chkcoin()  
