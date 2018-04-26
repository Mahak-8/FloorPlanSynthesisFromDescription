from reduction import *
reduction = Reduction()
text = open('./Input/floor_plan_description.txt').read()
reduction_ratio = 0.4
reduced_text = reduction.reduce(text, reduction_ratio)

file = open("./Output/floor_plan_summary.txt","w") 
for sentence in reduced_text:
	file.write(sentence)
file.close() 
print("Generated Summary")
print(reduced_text)
