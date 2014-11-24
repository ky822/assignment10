from Questions import Q1, Q2, Q3, Q4, Q5, Q6

def main():
	raw_data = Q1.Run()
	data = Q2.Run(raw_data)
	Q3.Run()
	Q4.Run(data)
	Q5.Run(data)
	Q6.Run(data)

if __name__ == '__main__':
	main()