# write a function that evaluates and returns the result of a Shotgun query field without knowing the query field's filter conditions in advance.
# find all the Sequences in a given Project and use your function to evaluate two query fields (listed below) for each.
# find all the Shots in a given Project and use your function to evaluate one query field (listed below) for each.

import shotgun_api3
from shotgun_api3 import Shotgun
from flask import Flask
app = Flask(__name__)

sg = Shotgun("https://laika-demo.shotgunstudio.com",
             'code_challenge', '$zvMznkhddo0tgwgwbftzaqob')

# ideally add a Logger


@app.route('/lk/project/<projectID>/shots')
def shots(projectID):
    """ Renders table of sg_latest_version all shots in given projectID"""

    filters = [['project', 'is', {'type': 'Project', 'id': int(projectID)}]]
    shots = sg.find('Shot', filters)

    html = '''<table>
        <thead>
            <tr>
                <td>shot_id</td>
                <td>sg_latest_version</td>
            </tr>
        </thead>
        <tbody>
        '''
    for shot in shots:
        html += '<tr>'
        html += '<td>' + str(shot['id']) + '</td>\n'
        html += '<td>' + \
            str(run_query(shot, 'sg_latest_version')) + '</td>\n'
        html += '<tr>'
    html += '<tbody>\n</table>'

    return html


@app.route('/lk/project/<projectID>/sequences')
def sequences(projectID):
    """ Renders table of sg_cut_duration and sg_ip_versions for all sequences in given projectID"""

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


def filters_from_schema(conditions, parent):
    """ Constructs filters based on the conditions in a schema_field_read() call

            Parameters:
                conditions: list of query field filters from schema_field_read() call
                parent: Shotgun entity object representing parent element of query field

            Returns: List of filter conditions

    """

    filters = []
    for condition in conditions:
        values = []
        for value in condition['values']:
            if isinstance(value, str):
                values.append(value)
            # SG id 0 represents parent entity
            elif value['id'] == 0:
                values.append(parent)
            else:
                values.append(value)

        filters.append([condition['path'], condition['relation'], *values])

    return filters


def order_from_schema(Query_Props):
    """ Constructs order list based on the conditions in a schema_field_read() call

            Parameters:
                Query_Props: Properties from a schema_field_read() call

            Returns: Order list to sort by

    """

    return [{'field_name': Query_Props['summary_value']['value']['column'],
             'direction': Query_Props['summary_value']['value']['direction']}]


def run_query(entity_obj, schema_fname):
    """ Evaluates and returns the result of a Shotgun query field without knowing its filter conditions

            Parameters:
                entity_obj: Shotgun entity object representing parent element of query field
                schema_fname: Name of the query field

            Returns: List of query data

    """
    Query_Props = sg.schema_field_read(entity_obj['type'], schema_fname)[
        schema_fname]['properties']

    filters = filters_from_schema(
        Query_Props['query']['value']['filters']['conditions'], entity_obj)
    filter_operator = 'all'
    summary_fields = [{'field': Query_Props['summary_field']
                       ['value'], 'type': Query_Props['summary_default']['value']}]

    # single_record not a valid summary type, use sg.find_one()
    if (Query_Props['summary_default']['value']) == 'single_record':
        # query field sort order
        order_list = order_from_schema(Query_Props)
        return sg.find_one(Query_Props['query']['value']['entity_type'], filters, fields=None, order=order_list)
    return sg.summarize(Query_Props['query']['value']['entity_type'], filters, summary_fields, filter_operator)['summaries']


if __name__ == '__main__':
    app.run()
