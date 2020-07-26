import math
import operator

labels = ["Yes", "No"]
features = {"outlook":["Sunny", "Overcast", "Rain"],
            "temperature":["Hot", "Mild", "Cool"], 
            "humidity":["High", "Normal"], 
            "wind":["Weak", "Strong"]}


training_data = [["No", "Sunny", "Hot", "High", "Weak"],
                 ["No", "Sunny", "Hot", "High", "Strong"],
                 ["Yes", "Overcast", "Hot", "High", "Weak"],
                 ["Yes", "Rain", "Mild", "High", "Weak"],
                 ["Yes", "Rain", "Cool", "Normal", "Weak"],
                 ["No", "Rain", "Cool", "Normal", "Strong"],
                 ["Yes", "Overcast", "Cool", "Normal", "Weak"],
                 ["No", "Sunny", "Mild", "High", "Weak"],
                 ["Yes", "Sunny", "Cool", "Normal", "Weak"],
                 ["No", "Rain", "Mild", "Normal", "Strong"],
                 ["Yes", "Sunny", "Mild", "Normal", "Strong"],
                 ["Yes", "Overcast", "Mild", "High", "Strong"],
                 ["Yes", "Overcast", "Hot", "Normal", "Weak"],
                 ["No", "Rain", "Mild", "High", "Strong"]]

class Node:
    def __init__(self, name):
        self.parent = None
        self.result = None
        self.name = name
        self.training_data = []
        self.path = []
        
def calculate_entropy(training_data, labels):
    entropy_score = 0;
    label_counts = {labels[0]:0, labels[1]:0}
    for item in training_data:
        #which target is satisfied is it yes or no or he or yox etc.
        for label in labels:
            if label in item:
                label_counts[label] += 1

    for label, count in label_counts.items():
        if count == 0:
            return 0
        entropy_score += (-count/len(training_data))*math.log(count/len(training_data), 2)

    return entropy_score


def calculate_information_gain(base_entr_score, feature_list, training_data, labels):
    info_gains = dict()
    for feature, attributes in feature_list.items():
        inf_gain = base_entr_score
        
        for atr in attributes:
            filtered_training_data = [x for x in training_data if atr in x] #training data where the atribute exists
            entr = calculate_entropy(filtered_training_data, labels)
            inf_gain -= (len(filtered_training_data) / len(training_data))*entr
            
        info_gains[feature] = inf_gain
    return info_gains


def get_rules(node):
    rules = []
    while queue:
        atr = queue[-1][1][0]
        if atr is None:
            filtered_features = features.copy()
            training_data = queue[-1][0].training_data
            queue.pop()
        else:
            training_data = [x for x in queue[-1][0].training_data if atr in x]
            if training_data:
                nodes.append(Node(atr))
                nodes[-1].parent = queue[-1][0]
                nodes[-1].path = nodes[-1].parent.path + [atr]
            queue[-1][1].pop(0)
            if not queue[-1][1]:
                queue.pop()
        base_entr_score = calculate_entropy(training_data, labels)
        info_gains = calculate_information_gain(base_entr_score, filtered_features, training_data, labels)
        if all([x == 0 for x in info_gains.values()]):
            yes_count = len([x for x in training_data if x[0] == "Yes"])
            no_count = len([x for x in training_data if x[0] == "No"])
            rules.append((nodes[-1].path, "Yes" if yes_count > no_count else "No"))
            continue
        
        selected_feature = max(info_gains.items(), key=operator.itemgetter(1))[0]
        filtered_features.pop(selected_feature)
        attributes_of_selected_feature = features.get(selected_feature, None)
        nodes.append(Node(selected_feature))
        
        nodes[-1].parent = nodes[-2]
        nodes[-1].path = nodes[-1].parent.path + [selected_feature]

        nodes[-1].training_data = training_data
        queue.append([nodes[-1], attributes_of_selected_feature])
        
    return rules
        

node = Node("Root")
node.training_data = training_data
nodes = list()
nodes.append(node)
queue = [[node, [None]]]
rules = get_rules(node)

with open("rules.txt", "w") as fw:
    for rule in rules:
        string = ""
        for i,x in enumerate(rule[0]):
            if i == 0:
                string += f"If {x} = "
            elif i%2==0:
                string += f" and {x} = "
            else:
                string += f"{x}"
        string += f" then result = {rule[1]}"
        print(string, file = fw)
