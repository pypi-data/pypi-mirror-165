import json
class Jsonvjson:
    def __init__(self):
        pass

    def compare_file(file1,file2):
        d1={}
        d2={}

        with open(file1,"r") as f1:
            json_file1 = json.loads(f1.read())
        with open(file2,"r") as f2:
            json_file2 = json.loads(f2.read())
        
        for item in json_file2:
            if item not in json_file1:
                d1[item]=json_file2[item]
                json_object=json.dumps(d1,indent=4)
                print(d1)
                print(f"Found differences in file1: {item}")
        with open("data not in file1.json","w") as outfile:
            outfile.write(json_object)

        for item in json_file1:
            if item not in json_file2:
                d2[item]=json_file1[item]
                json_object=json.dumps(d2,indent=4)
                print(d2)
                print(f"Found differences in file2: {item}")
        with open("data not in file2.json","w") as outfile:
            outfile.write(json_object)


    