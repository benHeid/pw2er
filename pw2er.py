import peewee
import argparse

def load_entities(m):
    entities = []
    for o in m.__dir__():
        t = m.__getattribute__(o)
        if (t != peewee.Model and
            peewee.ModelBase == type(t) and
            peewee.Model.__subclasscheck__(t)):
            entities.append(t)
    return entities

def load_relations(entities, module):
    rels = []
    for e in entities:
        rels.append(e._meta.model_refs)
    return rels

def clear_entities(entities):
    temp = []
    for e in entities:
        print(e.__bases__)
        for base in e.__bases__:
            if base in entities:
                temp.append(base)

    for m in temp:
        del entities[entities.index(m)]
    return entities

def plot_er(entities, rels, outputfile):  
    from graphviz import Digraph
    f = Digraph('ER', filename=outputfile)
    f.attr(rankdir='LR', size='8,5')
    f.attr('node', shape='box')

    for e in entities:
        fields = ""
        for field in e._meta.fields:
            fields += "<TR><TD>{} : {}</TD></TR>".format(field, type(e._meta.fields[field]).__name__)
        table = '''<
        <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="4">
          <TR>
            <TD BGCOLOR="grey"><B>{}</B></TD>
          </TR>

            {}
        </TABLE>>'''.format(e._meta.name, fields)
        f.node(e._meta.name, table)

    for rel in rels:
        for fk in rel:
            source = fk._meta.name          
            dist = rel[fk][0].model._meta.name
            f.edge(source, dist)
    f.render()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates ER Diagram.')
    parser.add_argument('file', type=str, help='the python file, where the peewee model is defined')
    parser.add_argument('output', help='the output file')

    args = parser.parse_args()

    m = __import__(args.file)
    entities = load_entities(m)
    entities = clear_entities(entities)
    rels = load_relations(entities, m)
    plot_er(entities, rels, args.output)