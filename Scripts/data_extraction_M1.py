def extract_answers_sequence(file_path):
    """ 
    This function takes the input of the data, it then simplifies the data and return its in a list. 
    
    Args: 
        file_path (string): String that contains the file path for where the data is collected from 
    
    Returns: 
        list: The data in a list from the file_path 
    """
    file = open(file_path, "r")
    filelist = []
    templine = ""
    for x in file.read():
        if x == "\n":
            if templine != "":
                filelist.append(templine)
                templine = ""
        else:
            templine += x
    if templine != "":
        filelist.append(templine)
    answerslist = []
    questionoption = 0
    for line in filelist:
        if line[0] == "Q":
            if questionoption not in [0,4]:
                answerslist.append(0)
            questionoption = 0
        elif line[0] == "[":
            if line[1] == "X":
                questionoption += 1
                answerslist.append(questionoption)
            else:
                questionoption += 1
    return answerslist
    
def write_answers_sequence(answers, n, destination_path):
    """ 
    This function takes the answers inputted and records it as a textfile under the name answers_list_respondent_n.txt 

    Args: 
        answers (list): List that contains the data from the corresponding respondent 
        n (integer): Number to show which respondent the data corresponds to 
        destination_path (string): String that contains the file path for where the data needs to go to 
    """
    txtfile = f"{destination_path}/answers_list_respondent_{n}.txt"
    f = open(txtfile, "x")
    for x in answers:
        f.write(f"{x}")    
    