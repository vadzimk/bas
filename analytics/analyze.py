from networkx import Network
job_net = Network(height='1000px', width='100%', bgcolor='#222222', font_color='white')

job_net.barnes_hut()
sources = data_graph['Job ID']
targets = data_graph['skills']
values=data_graph['years skills']
sources_resume = data_graph_resume['document']
targets_resume = data_graph_resume['skills']

edge_data = zip(sources, targets, values )
resume_edge=zip(sources_resume, targets_resume)
for j,e in enumerate(edge_data):
    src = e[0]
    dst = e[1]
    w = e[2]


    job_net.add_node(src, src, color='#dd4b39', title=src)
    job_net.add_node(dst, dst, title=dst)


    if str(w).isdigit():
        if w is None:

            job_net.add_edge(src, dst, value=w, color='#00ff1e', label=w)
        if 1<w<=5:
            job_net.add_edge(src, dst, value=w, color='#FFFF00', label=w)
        if w>5:
            job_net.add_edge(src, dst, value=w, color='#dd4b39', label=w)

    else:
        job_net.add_edge(src, dst, value=0.1, dashes=True)for j,e in enumerate(resume_edge):
    src = 'resume'
    dst = e[1]

    job_net.add_node(src, src, color='#dd4b39', title=src)
    job_net.add_node(dst, dst, title=dst)
    job_net.add_edge(src, dst, color='#00ff1e')neighbor_map = job_net.get_adj_list()for node in job_net.nodes:
    node['title'] += ' Neighbors:<br>' + '<br>'.join(neighbor_map[node['id']])
    node['value'] = len(neighbor_map[node['id']])# add neighbor data to node hover data
job_net.show_buttons(filter_=['physics'])
job_net.show('job_knolwedge_graph.html')
