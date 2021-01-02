from random import randint

def main():
	M = generate_grid()
	step = randint(0, 15)
	A = (randint(1, len(M) - 1), randint(1, len(M[0]) - 1))
	B = (randint(1, len(M) - 1), randint(1, len(M[0]) - 1))
	return M, step, A, B

def generate_grid():
	heigh = randint(1, 80)
	width = randint(1, 80)
	half_result = []
	result = []
	for i in range(width):
		for i in range(heigh):
			half_result.append(randint(0, 10000))
		result.append(half_result)
		half_result = []
	return result

if __name__ == "__main__":
	main()