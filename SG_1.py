# write a function that evaluates and returns the result of a Shotgun query field without knowing the query field's filter conditions in advance.
# find all the Sequences in a given Project and use your function to evaluate two query fields (listed below) for each.
# find all the Shots in a given Project and use your function to evaluate one query field (listed below) for each.

import shotgun_api3
from shotgun_api3 import Shotgun
import pprint
# ideally create a Logger object here

from flask import Flask
app = Flask(__name__)


pp = pprint.PrettyPrinter(indent=2)


sg = Shotgun("https://laika-demo.shotgunstudio.com",
             'code_challenge', '$zvMznkhddo0tgwgwbftzaqob')

print(sg)

# find shots
project = sg.find_one("Project", [["id", "is", 85]])
# filters = [['project', 'is', {'type': 'Project', 'id': project['id']}]]
fields = ['id', 'code', 'Sequence']
# shots = sg.find("Shot", filters, fields)
# print(shots)


# compute the value of a query field with the API
# results of query fields aren't stored -> not supported in UI -> grab fields and calculate?
# Shotgun.summarize()

@app.route('/lk/project/<projectID>/sequences')
def sequences(projectID):
    filters = [['project', 'is', {'type': 'Project', 'id': int(projectID)}]]
    sequences = sg.find('Sequence', filters)
    html = '''<table>
    <thead>
        <tr>
            <td>sequence_id</td>
            <td>sg_cut_durations</td>
            <td>sg_ip_versions</td>
            
        </tr>
    </thead>
    <tbody>
    '''
    for sequence in sequences:
        html += '<tr>'
        html += '<td>' + str(sequence['id']) + '</td>\n'
        html += '<td>' + \
            str(run_query(sequence, 'sg_cut_duration')) + '</td>\n'
        html += '<td>' + str(run_query(sequence, 'sg_ip_versions')) + '</td>\n'
        html += '<tr>'
    html += '<tbody>\n</table>'

    return html

# print(queried)


Qtable = (sg.schema_field_read('Sequence', 'sg_ip_versions'))
pp.pprint(Qtable['sg_ip_versions'])

# filters = [['project', 'is', {'type': 'Project', 'id': project['id']}]]
# filter_operator = 'all'
# sequ_id = 40
# entity_type = 'Sequence'
# summ_default = 'average'
# summary_fields=[{'field': 'sg_cut_duration', 'type': 'average'}]#'type': 'summary_default['value']

# Supported values are "all" and `"any"`. These are just another way of defining if the query is an AND or OR
# query. Defaults to `"all"`.
# pp.pprint(sg.summarize('Shot', filters, summary_fields, filter_operator))


def new_filters(conditions, entity_obj):
    # conditions = [ { 'active': 'true',
    #                 'path': 'sg_sequence',
    #                 'relation': 'is',
    #                 'values': [ { 'id': 0,
    #                                 'name': 'Current '
    #                                         'Sequence',
    #                                 'type': 'Sequence',
    #                                 'valid': 'parent_entity_token'}]}]

    filters = []
    for condition in conditions:
        values = []
        for value in condition['values']:
            if isinstance(value, str):
                values.append(value)
            elif value['id'] == 0:
                values.append(entity_obj)
            else:
                values.append(value)

        filters.append([condition['path'], condition['relation'], *values])

    return filters
    # returns [['sg_sequence' , 'is' , ...]]


def run_query(entity_obj, schema_fname):
    Query_Props = sg.schema_field_read(entity_obj['type'], schema_fname)[
        schema_fname]['properties']
    # [ Query_Props['query']['value']['filters']['conditions']['path'], 'is', entity_obj] # shots where sg_sequence is id 40
    filters = new_filters(
        Query_Props['query']['value']['filters']['conditions'], entity_obj)
    filter_operator = 'all'
    summary_fields = [{'field': Query_Props['summary_field']
                       ['value'], 'type': Query_Props['summary_default']['value']}]
    return sg.summarize(Query_Props['query']['value']['entity_type'], filters, summary_fields, filter_operator)['summaries']


arg1 = {'type': 'Sequence', 'id': 40}  # sg represents entity with type and id
run_query(arg1, 'sg_ip_versions')
app.run()
# {entity_type: id: }, query_field_name
