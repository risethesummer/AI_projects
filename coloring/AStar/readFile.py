def readFile(name):

    with open(name, 'r') as reader:

        lines = reader.readlines()

        numbers = []

        for line in lines:

            temp = []

            for word in line.split(' '):

                if word[0].isdigit():
                    temp.append(int(word))
                else:
                    #Empty cell
                    temp.append(-1)

            numbers.append(temp)

        return numbers