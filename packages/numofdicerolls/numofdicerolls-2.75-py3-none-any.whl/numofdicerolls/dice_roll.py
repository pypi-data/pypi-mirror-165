#!/usr/bin/python
import random

def rolldice():
	rolls = []

	while True:
		try:
			num_rolls = int(input("How many rolls of the dice do you want?: "))
		except (NameError, ValueError):
			print("Please enter a correct number")
			continue
		if num_rolls <= 0:
			print("Please enter a positive number")
			continue
		else:
			break

	for i in range(num_rolls):
		rolls.append(random.randint(1,6)+random.randint(1,6))
	return rolls
