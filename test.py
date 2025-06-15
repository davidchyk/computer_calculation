list_args = []

for x in range(4, 0, -1): list_args.append(f"X_{x}")

is_upper = any(x.isupper() for x in list_args)

print(is_upper)