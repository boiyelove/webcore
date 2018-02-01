# import math
# ordinal = lambda n: "%d%s" * (n, "tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])



# print [ordinal(n) for n in range(1,32)]

# ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th',
# '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st',
# '22nd', '23rd', '24th', '25th', '26th', '27th', '28th', '29th', '30th', '31st']
# For python 3.4+, math.floor is needed:

def gen_pin():
	return random.randint(1000, 9999)