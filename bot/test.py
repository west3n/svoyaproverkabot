from passlib.hash import phpass

password = '9eHNYQ#fnEZYrRNmM*3XJ)@T'
hashed_password = '$P$BCY.HutDhtqGsl7t1dRhq0EF8laB3o/'
compare = phpass.verify(password, hashed_password)
print(compare)
