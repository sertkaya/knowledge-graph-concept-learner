from rdflib import Graph, Namespace

# Define the RDF namespaces used in the data
ex = Namespace('http://example.org/')
rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')

# Load the RDF data from a file
graph = Graph()
graph.parse('C:/Users/prana/Desktop/Masters Thesis/test_files/example-product-1.ttl', format='turtle')

# Define the output graph
G = {}

# Iterate over each subject in the RDF data
for key, value, data in graph:
    # Convert the subject, predicate, and object to strings
    key = str(key)
    value = str(value)
    data = str(data)

    # Replace the namespace prefix with the prefix defined in the RDF data
    if key.startswith(ex):
        key = 'ex:' + key[len(ex):]
    if value.startswith(ex):
        value = 'ex:' + value[len(ex):]
    if data.startswith(ex):
        data = 'ex:' + data[len(ex):]
    if value.startswith(rdf):
        value = 'rdf:' + value[len(rdf):]

    # Add the subject to the output graph if it hasn't been added yet
    if key not in G:
        G[key] = {}

    # If the predicate already exists for this subject, append the object to the list
    if value in G[key]:
        if isinstance(G[key][value], list):
            G[key][value].append(data)
        else:
            G[key][value] = [G[key][value], data]
    # Otherwise, create a new list with the object
    else:
        G[key][value] = data

# Sort the keys of the output dictionary
G = {keys: val for keys, val in sorted(G.items())}


# Print the output graph using description graph and description tree
def generate_output_graph(G):
    output = "{\n"

    def unravel(d, depth=1):
        nonlocal output
        for k, v in d.items():
            if isinstance(v, dict):
                output += '\t' * depth + "'" + k + "': {\n"
                unravel(v, depth + 1)
                output += '\t' * depth + '},\n'
            else:
                value_str = str(v)
                if isinstance(v, str):
                    value_str = "'" + value_str + "'"
                output += '\t' * depth + "'" + k + "': " + value_str + ',\n'

    unravel(G, depth=1)

    output += "}\n"

    return output


# Usage:
output_graph = generate_output_graph(G)
with open('examples/example-product-1.txt', 'w') as f:
    f.write(output_graph)
