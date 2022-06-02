import tau_extrema_sequence
import math

def find_constants(p,q,r):
	'''
    Args:
        p, q, r (int): parameters of the Brieskorn sphere

    Returns (tuple of 4 ints): the important constants e_0, pprime, qprime, and rprime
    '''
	# compute -1 times the modular inverses of q*r modulo p, etc.
	pprime = p-pow(q*r, -1, p)
	qprime = q-pow(p*r, -1, q)
	rprime = r-pow(p*q, -1, r)

	# compute e_0
	e_0 = int((-1*pprime*q*r - p*qprime*r - p*q*rprime - 1)/(p*q*r))
	consts = (e_0, pprime, qprime, rprime)
	return consts

def dedekind(p,q):
	'''
	Args:
		p, q (int): parameters of the Dedekind sum s(p,q) to be computed

	Returns (float): the Dedekind sum s(p,q)
	'''
	if p == 1 and q == 1:
		return 0
	if p > q:
		return dedekind(p-q,q)
	else:
		# use the recursive Dedekind reciprocity law
		return -0.25 + 1/12 * (p/q + q/p + 1/(p*q)) - dedekind(q,p)

def find_d_invariant(p,q,r):
	'''
	Args:
		p, q, r (int): parameters of the Brieskorn sphere

	Returns (int): the d-invariant of the Brieskorn sphere
	'''
	# the parameters of a Brieskorn sphere must be pairwise coprime
	assert math.gcd(p,q) == 1, "p and q are not relatively prime"
	assert math.gcd(q,r) == 1, "q and r are not relatively prime"
	assert math.gcd(r,p) == 1, "r and p are not relatively prime"

	consts = find_constants(p,q,r)
	e = -1.0/(p*q*r)
	N0 = p*q*r - p*q - q*r - p*r 
	tau_min = min(tau_extrema_sequence.compute_tau(p,q,r))

	# use the formula due to Nemethi, Nicolaescu (2002) for the d-invariant based on the important constants, Dedekind sums, and the global minima of the tau sequence
	ans = (1/4)*(N0*N0*e + e + 5 - 12*(dedekind(consts[1],p) + dedekind(consts[2],q) + dedekind(consts[3],r))) - 2*tau_min
	return int(round(ans))

def main():
	# p = int(input("p: "))
	# q = int(input("q: "))
	# r = int(input("r: "))

	# print(find_constants(p,q,r))
	# print(find_d_invariant(p,q,r))

	N=50

	for a in range(2, 3):
		for b in range(a+1,N):
			if math.gcd(a,b) == 1:
				for c in range(1,b+1+a*b):
					if math.gcd(a,c) == 1 and math.gcd(b,c) == 1:
						if not (a == 2 and b == 3 and c == 5):
							print(f'{a}, {b}, {c}: {find_d_invariant(a,b,c)}')            

if __name__ == "__main__":
	main()