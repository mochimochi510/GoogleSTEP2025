import sys
from collections import deque

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Example: Find the longest titles.
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Example: Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()


    # Homework #1: Find the shortest path.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
     
    def get_id_from_title(self, title):
        for k, v in self.titles.items():
            if v == title:
                return k
        return None
    
    def find_shortest_path(self, start, goal):
        # bfs
        queue = deque()
        visited = {}
        parent = {} # 通った経路の親ノードを保存するset
        start_id = self.get_id_from_title(start)
        queue.append(start_id)
        visited.add(start_id)
        parent[start_id] = None
        
        while queue:
            node_id = queue.popleft()
            if self.titles[node_id] == goal:
                print("found")
                
                # たどった経路を復元する
                path = []
                while node_id is not None:
                    path.append(self.titles[node_id])
                    node_id = parent[node_id]
                path.reverse()
                print("path", path)
                return path
            for child in self.links[node_id]:
                if not (child in visited):
                    visited.add(child)
                    parent[child] = node_id
                    queue.append(child)
        print("not found")
        return "not found"


    # Homework #2: Calculate the page ranks and print the most popular pages.
    def calc_double_distance(self, new_pageranks, old_pageranks):
        rank_distance = [(new_pageranks[x] - old_pageranks[x])**2 for x in range(len(new_pageranks))]
        distance = sum(rank_distance)
        return distance
    
    def find_most_popular_pages(self):
        # Random surfer model
        new_pageranks = [1] * len(self.titles)
        old_pageranks = [0] * len(self.titles)
        
        while self.calc_double_distance(new_pageranks, old_pageranks) > 0.01:
            old_pageranks = new_pageranks.copy()
            new_pageranks = [0] * len(self.titles)
            for i in range(len(self.titles)):
                page_id = i+1
                if page_id not in self.links:
                    new_pageranks = [new_pageranks[x]+ old_pageranks[i]/len(self.titles) for x in new_pageranks]
                else:
                    for j in self.links[page_id]:
                        new_pageranks[j] = new_pageranks[j] + 0.85*old_pageranks[page_id]/len(self.links[page_id])
                    for j in list(set(list(self.titles.keys())) - set(self.links[page_id])):
                        new_pageranks[j] = 0.15*old_pageranks[page_id]/len(self.titles)
        return new_pageranks
        # pass

    

    # Homework #3 (optional):
    # Search the longest path with heuristics.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_longest_path(self, start, goal):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


    # Helper function for Homework #3:
    # Please use this function to check if the found path is well formed.
    # 'path': An array of page IDs that stores the found path.
    #     path[0] is the start page. path[-1] is the goal page.
    #     path[0] -> path[1] -> ... -> path[-1] is the path from the start
    #     page to the goal page.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def assert_path(self, path, start, goal):
        assert(start != goal)
        assert(len(path) >= 2)
        assert(self.titles[path[0]] == start)
        assert(self.titles[path[-1]] == goal)
        for i in range(len(path) - 1):
            assert(path[i + 1] in self.links[path[i]])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # Example
    # wikipedia.find_longest_titles()
    # Example
    # wikipedia.find_most_linked_pages()
    # Homework #1
    wikipedia.find_shortest_path("F", "D") #test for small
    wikipedia.find_shortest_path("渋谷", "パレートの法則")
    
    # Homework #2
    wikipedia.find_most_popular_pages()
    # Homework #3 (optional)
    # wikipedia.find_longest_path("渋谷", "池袋")