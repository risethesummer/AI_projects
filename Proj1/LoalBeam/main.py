from fileUtilities import *
from beamSearch import BeamSearch

def main():
    
    expressions = readFile("input.txt")

    result = BeamSearch(expressions)

    print("The limit time is 5 minutes")
    
    if result is None:
        print("NO SOLUTION")
    else:
        keys = list(result.getKeyToVal())
        keys.sort()
        res = ''
        for k in keys:
            res += str(result[k])
        with open("output.txt", 'w') as writer:
            writer.write(res)

        

if __name__ == "__main__":
    main()