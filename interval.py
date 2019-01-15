def simplify_interval(interval):
	b = 0
	new_interval = []
	for item in interval:
		if b == 0:
			new_interval.append((item[0], 'b'))
		if item[1] == 'b':
			b += 1
		elif item[1] == 'e':
			b -= 1
		if b == 0:
			new_interval.append((item[0], 'e'))
	return new_interval

def merge_interval(interval, merge_distance):
	new_interval = []
	skip_next = False
	for index, item in enumerate(interval):
		if item[1] == 'b':
			if not skip_next:
				new_interval.append(item)
			else:
				skip_next = False
		elif item[1] == 'e':
			if (index < len(interval) - 1):
				next_item = interval[index+1]
				if next_item[0] - item[0] <= merge_distance:
					skip_next = True
				else:
					new_interval.append(item)
			else:
				new_interval.append(item)
	return new_interval

def delete_interval(interval, deleted_interval):
	index = 0
	d_index = 0
	while index < len(interval) and d_index < len(deleted_interval):
		item_b = interval[index]
		d_item_b = deleted_interval[d_index]
		d_item_e = deleted_interval[d_index + 1]
		item_e = interval[index + 1]
		if item_b[1] == 'b' and item_b[0] < d_item_b[0] and item_e[0] > d_item_b[0]:
			while index + 1 < len(interval) and item_e[0] <= d_item_e[0]:
				del interval[index + 1]
				if index + 1 < len(interval):
					item_e = interval[index + 1]
			if index < len(interval):
				if item_e[1] == 'e' and index + 1 < len(interval):
					interval.insert(index + 1, (d_item_e[0], 'b'))
				interval.insert(index + 1, (d_item_b[0], 'e'))
				d_index += 2
		elif item_b[1] == 'b' and item_b[0] >= d_item_b[0] and item_e[0] > d_item_b[0]:
			while index + 1 < len(interval) and item_e[0] <= d_item_e[0]:
				del interval[index + 1]
				if index + 1 < len(interval):
					item_e = interval[index + 1]
			if index < len(interval):
				interval.insert(index + 1, (d_item_b[0], 'b'))
				if item_e[1] == 'b':
					interval.insert(index + 1, (d_item_e[0], 'e'))
				d_index += 2
		index += 2

def insert_interval(interval, in_command):
	b_interval = int(in_command[1])
	e_interval = int(in_command[2])
	b_insert_index = len(interval)
	e_insert_index = b_insert_index
	b_index_found = False
	e_index_found = False
	for index, item in enumerate(interval):
		if item[0] > b_interval and not b_index_found:
			b_insert_index = index
			b_index_found = True
		if item[0] > e_interval and not e_index_found:
			e_insert_index = index
			e_index_found = True
	interval.insert(b_insert_index, (b_interval, 'b'))
	interval.insert(e_insert_index + 1, (e_interval, 'e'))

def remove_interval(interval, in_command):
	for index, item in enumerate(interval):
		if item[0] == int(in_command[1]) and item[1] == 'b':
			del interval[index]
			break
	for index, item in enumerate(interval):
		if item[0] == int(in_command[2]) and item[1] == 'e':
			del interval[index]
			break

f = open("input.txt", "r")
interval = []
deleted_interval = []
for l in f.readlines():
	print("command: " + l.strip())
	in_command = l.strip().split(',')
	if (in_command[3] == "ADDED"):
		insert_interval(interval, in_command)
	elif (in_command[3] == "REMOVED"):
		remove_interval(interval, in_command)
	elif (in_command[3] == "DELETED"):
		insert_interval(deleted_interval, in_command)
	print(interval)
	simplified_interval = simplify_interval(interval)
	simplified_deleted_interval = simplify_interval(deleted_interval)
	print(simplified_interval)
	merged_interval = merge_interval(simplified_interval, 7)
	print(merged_interval)
	delete_interval(merged_interval, simplified_deleted_interval)
	print(merged_interval)
	print("")


