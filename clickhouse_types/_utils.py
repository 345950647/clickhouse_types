def _split_skipping_parenthesis(
        seq: str,
        sep: str = ',',
):
    seqs = []
    n = 0
    i = 0
    for j, s in enumerate(seq):
        if s == '(':
            n += 1
        elif s == ')':
            n -= 1
        elif s == sep and not n:
            seqs.append(seq[i:j])
            i = j + 1
    else:
        seqs.append(seq[i:])
    return seqs


def _split_with_padding(
        seq: str,
        length: int,
        sep: str = ',',
):
    seqs = seq.split(sep)
    length -= len(seqs)
    if length:
        seqs += [None] * length
    return seqs
