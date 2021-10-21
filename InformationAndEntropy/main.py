import math
import sys

def stats(filename):
  arr = {}
  chars = 0

  with open(filename, encoding = 'utf-8') as file:
    for line in file:
      for char in line:
        try:
          arr[char] = arr[char] + 1
        except KeyError:
          arr[char] = 1
        chars += 1

  print("\nUnique chars: " + str(len(arr)))
  print("Read chars: " + str(chars))
  print(arr)

  sum = 0
  entropy = 0

  for k,v in arr.items():
    # amount of information
    pe = v/chars
    p = 1/pe
    ie = math.log(p,2) * 8 # to be verified amount of bits in logarithm base
    ie_bin = math.log(p,2)/math.log(2*8,2) # logarithm transformed to base 2
    print(str(k) + " ie = " + str(ie))
    
    # entropy
    hxi = pe * ie
    entropy += hxi
    
    # checksum for probability
    sum += pe

  print(entropy)
  print(sum)
  print("\n")

def main():
    # print command line arguments
  for arg in sys.argv[1:]:
    stats(arg)

if __name__ == "__main__":
  main()