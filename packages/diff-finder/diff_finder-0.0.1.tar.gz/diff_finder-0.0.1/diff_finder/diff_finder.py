import json
class Compare_file:
    """
    Compares two json files and returns output json files
    Attributes:
        file1 : json file name
        file2 : json file name
    """
    def __init__(self,file1,file2):
        self.file1=file1
        self.file2=file2
    def compare_file(self):
        d1={}
        d2={}
        with open(self.file1,"r") as f1:
            json_file1 = json.loads(f1.read())
        with open(self.file2,"r") as f2:
            json_file2 = json.loads(f2.read())
        
        for item in json_file2:
            if item not in json_file1:
                d1[item]=json_file2[item]
                print(d1)
                print(f"Found differences in file1: {item}")
        json_object=json.dumps(d1,indent=4)
        with open("data not present in file1.json","w") as outfile:
            outfile.write(json_object)

        for item in json_file1:
            if item not in json_file2:
                d2[item]=json_file1[item]
                print(d2)
                print(f"Found differences in file2: {item}")
        json_object=json.dumps(d2,indent=4)
        with open("data not present in file2.json","w") as outfile:
            outfile.write(json_object)

    @classmethod
    def get_user_input(self):
        while 1:
            try:
                file1 = input('Enter first file name: ').strip("'")
                file2 = input('Enter second file name: ').strip("'")
                return self(file1,file2)
            except:
                print('Invalid input!')
                continue


"""file1=input()+".json"
file2=input()+".json"
files=Compare_file(file1,file2)
files.compare_file()
"""
    