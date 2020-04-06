import numpy as np
from sklearn.cluster import KMeans

class Worker:
    def __init__(self, company, bonus, skills):
        self.company = company
        self.bonus = bonus
        self.skills = skills
        self.x = None
        self.y = None

def print_worker(worker):
    print(worker.company)
    print(worker.bonus)
    print(worker.skills)

filename = "f_glitch"

with open(filename + '.txt') as f:
    width, height = [int(x) for x in next(f).split()] # read first line
    floor = []

    for i in range(height):
        floor.append([char for char in next(f)[:-1]])
    # print(np.array(floor))

    developers_ordered_list = []
    developers = {}
    num_of_developers = int(next(f))
    for i in range(num_of_developers):
        line = next(f).split()
        company = line[0]
        bonus = line[1]
        num_of_skills= line[2]
        skills = set(line[3:])
        new_dev = Worker(company, bonus, skills)

        if company not in developers.values(): 
            developers[company] = []
        developers[company].append(new_dev)
        developers_ordered_list.append(new_dev)

    managers_ordered_list = []
    managers = {}
    num_of_managers = int(next(f))
    for i in range(num_of_managers):
        line = next(f).split()
        company = line[0]
        bonus = line[1]
        new_manager = Worker(company, bonus, None)

        if company not in managers.values(): 
            managers[company] = []
        managers[company].append(new_manager)
        managers_ordered_list.append(new_manager)

f.close()

# Developers

data = np.array(floor)
temp_positions = np.where(data=="_")
developer_positions = []


for i in range(len(temp_positions[0])):
    developer_positions.append([temp_positions[0][i], temp_positions[1][i]])

kmeans = KMeans(n_clusters=int(len(developer_positions)/(num_of_developers/len(developers))), random_state=0).fit(developer_positions)


clusters = []
for i in range(kmeans.n_clusters):
    clusters.append(np.where(kmeans.labels_ == i)[0])


clusters = sorted(clusters, key=lambda x: len(x), reverse=True)

companies = sorted(developers, key=lambda x: len(x), reverse=True)


flag = False
counter = 0
for company in companies:
    for developer in developers[company]:
        pos = clusters[0][0]
        developer.x = developer_positions[pos][0]
        developer.y = developer_positions[pos][1]
        clusters[0] = np.delete(clusters[0], 0)
        counter += 1
        if len(clusters[0]) == 0:
            clusters = np.delete(clusters, 0)
            if len(clusters) == 0:
                flag = True
                break
    if flag:
        break



# ==========================
# Managers

data=np.array(floor)
temp_positions = np.where(data=="M")
manager_positions = []

for i in range(len(temp_positions[0])):
    manager_positions.append([temp_positions[0][i], temp_positions[1][i]])

kmeans = KMeans(n_clusters=int(len(manager_positions)/(num_of_managers/len(managers))), random_state=0).fit(manager_positions)


clusters = []
for i in range(kmeans.n_clusters):
    clusters.append(np.where(kmeans.labels_ == i)[0])


clusters = sorted(clusters, key=lambda x: len(x), reverse=True)

companies = sorted(managers, key=lambda x: len(x), reverse=True)


flag = False

for company in companies:
    for manager in managers[company]:
        pos = clusters[0][0]
        manager.x = manager_positions[pos][0]
        manager.y = manager_positions[pos][1]
        clusters[0] = np.delete(clusters[0], 0)
        if len(clusters[0]) == 0:
            clusters = np.delete(clusters, 0)
            if len(clusters) == 0:
                flag = True
                break
    if flag:
        break



with open(filename + "-out.txt", "w+") as output:

    for developer in developers_ordered_list:
        if developer.x == None:
            output.write("X\n")
        else:
            output.write(str(developer.y) + " " + str(developer.x) + "\n")

    for manager in managers_ordered_list:
        if manager.x == None:
            output.write("X\n")
        else:
            output.write(str(manager.y) + " " + str(manager.x) + "\n")

output.close()
