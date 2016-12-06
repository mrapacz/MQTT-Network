from dumper_setup import Probe


def dump_data(node_id, temperature):
    p = Probe(node_id=node_id, temperature=temperature)
    p.save()
