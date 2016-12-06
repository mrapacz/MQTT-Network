from dumper_setup import Probe


def dump_data():
    p = Probe(node_id=123123, temperature=20.0)
    p.save()


if __name__ == '__main__':
    dump_data()
