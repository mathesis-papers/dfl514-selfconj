import itertools
import json
import math


def powers(base, bound):
    values = [1]
    while values[-1] * base <= bound:
        values.append(values[-1] * base)
    return values


def transpose(rows):
    return tuple(sum(part >= column for part in rows)
                 for column in range(1, rows[0] + 1))


def rows_from_counts(base, counts):
    return tuple(base ** index
                 for index in range(len(counts) - 1, -1, -1)
                 for occurrence in range(counts[index]))


def generated_cmps(row_base, column_base, bound):
    pending = [((1,), 1)]
    seen = set()
    while pending:
        counts, area = pending.pop()
        assert counts not in seen
        seen.add(counts)
        yield counts, area
        raised_area = column_base * area
        if raised_area <= bound:
            pending.append((tuple(column_base * count for count in counts), raised_area))
        migrated_area = area + (row_base - 1) * row_base ** (len(counts) - 1)
        if migrated_area <= bound:
            pending.append((counts[:-1] + (counts[-1] - 1, 1), migrated_area))


def all_ary_rows(base, bound):
    parts = powers(base, bound)

    def descend(index, remaining, counts):
        if index < 0:
            if any(counts):
                yield rows_from_counts(base, counts)
            return
        for multiplicity in range(remaining // parts[index] + 1):
            counts[index] = multiplicity
            yield from descend(index - 1, remaining - multiplicity * parts[index], counts)
        counts[index] = 0

    yield from descend(len(parts) - 1, bound, [0] * len(parts))


def check_partition(row_base, column_base, rows, area):
    columns = transpose(rows)
    assert sum(rows) == area == sum(columns)
    assert set(rows) <= set(powers(row_base, area))
    assert set(columns) <= set(powers(column_base, area))
    assert (area - len(rows) - rows[0] + 1) % ((row_base - 1) * (column_base - 1)) == 0
    self_conjugate = rows == columns
    if row_base == column_base and self_conjugate:
        assert (area - 2 * rows[0] + 1) % (row_base - 1) ** 2 == 0
        if row_base % 2:
            assert (area - 1) % (2 * (row_base - 1)) == 0
            remaining = area
            exponent = 0
            while remaining % row_base == 0:
                remaining //= row_base
                exponent += 1
            if remaining == 1:
                assert exponent % 2 == 0
    if row_base == column_base:
        exponent = exact_exponent(row_base, area)
        if exponent is not None and len(set(rows)) > 1:
            width_exponent = exact_exponent(row_base, rows[0])
            height_exponent = exact_exponent(row_base, len(rows))
            defect = width_exponent + height_exponent - exponent
            assert 1 <= defect <= exponent - 2
            assert defect % (row_base - 1) == 0
            assert exponent >= row_base + 1
            if self_conjugate and row_base % 2 == 0 and exponent % 2 == 0:
                assert exponent >= 2 * row_base
    return self_conjugate


def exact_exponent(base, value):
    exponent = 0
    while value > 1 and value % base == 0:
        exponent += 1
        value //= base
    return exponent if value == 1 else None


def compressed_transpose(base, counts):
    output = {}
    for index in range(len(counts)):
        column_height = sum(counts[index:])
        exponent = exact_exponent(base, column_height)
        assert exponent is not None
        multiplicity = base ** index - (base ** (index - 1) if index else 0)
        output[exponent] = output.get(exponent, 0) + multiplicity
    return tuple(output.get(index, 0) for index in range(max(output) + 1))


def inflate(base, counts):
    return (0,) + tuple(base * multiplicity for multiplicity in counts)


def extend_arms(base, counts):
    height = sum(counts)
    assert height == base ** (len(counts) - 1)
    updated = list(counts)
    updated[-1] -= 1
    updated[0] += (base - 1) * height
    return tuple(updated) + (1,)


def check_compressed(base, counts, exponent, self_conjugate):
    assert sum(multiplicity * base ** index
               for index, multiplicity in enumerate(counts)) == base ** exponent
    columns = compressed_transpose(base, counts)
    assert (columns == counts) == self_conjugate
    assert sum(multiplicity > 0 for multiplicity in counts) > 1


def check_constructions():
    checks = 0
    for base in range(2, 17):
        counts = tuple((base - 1) * base ** (base - index - 1)
                       for index in range(base)) + (1,)
        for inflation in range(4):
            check_compressed(base, counts, base + 1 + 2 * inflation, True)
            checks += 1
            counts = inflate(base, counts)
        for shift in range(4):
            original = tuple((base - 1) * base ** (base - index - 1)
                             for index in range(base)) + (1,)
            shifted = (0,) * shift + original
            check_compressed(base, shifted, base + 1 + shift, shift == 0)
            checks += 1
        if base % 2 == 0:
            counts = extend_arms(base, extend_arms(base, inflate(base, (1,))))
            for index in range((base - 2) // 2 + 1):
                width = base ** (4 * index + 3)
                area = sum(multiplicity * base ** power
                           for power, multiplicity in enumerate(counts))
                assert sum(counts) == width
                assert area == (2 * (index + 1) * base ** (4 * index + 3)
                                + base ** (4 * index + 2)
                                - 2 * (index + 1) * base ** (4 * index + 1))
                assert compressed_transpose(base, counts) == counts
                checks += 1
                if index < (base - 2) // 2:
                    counts = inflate(base, inflate(base, counts))
                    counts = extend_arms(base, extend_arms(base, counts))
            for inflation in range(4):
                check_compressed(base, counts, 2 * base + 2 * inflation, True)
                checks += 1
                counts = inflate(base, counts)
    return {'base_range': [2, 16], 'inflation_range': [0, 3],
            'row_shift_range': [0, 3], 'exact_checks': checks,
            'representation': 'compressed multiplicities; exact integers'}


def main():
    crosschecks = []
    for row_base in range(2, 7):
        direct_sets = {column_base: set() for column_base in range(2, 7)}
        ary_count = 0
        for rows in all_ary_rows(row_base, 64):
            ary_count += 1
            columns = transpose(rows)
            for column_base in range(2, 7):
                if set(columns) <= set(powers(column_base, 64)):
                    direct_sets[column_base].add(rows)
        for column_base in range(2, 7):
            generated = {rows_from_counts(row_base, counts)
                         for counts, area in generated_cmps(row_base, column_base, 64)}
            assert generated == direct_sets[column_base]
            for rows in generated:
                check_partition(row_base, column_base, rows, sum(rows))
            crosschecks.append({'row_base': row_base, 'column_base': column_base,
                                'cmp_count': len(generated), 'ary_count': ary_count})

    mixed = []
    for row_base, column_base in itertools.product(range(2, 7), repeat=2):
        object_count = 0
        for counts, area in generated_cmps(row_base, column_base, 512):
            check_partition(row_base, column_base, rows_from_counts(row_base, counts), area)
            object_count += 1
        mixed.append({'row_base': row_base, 'column_base': column_base,
                      'cmp_count': object_count})

    diagonal = []
    power_counts = []
    for base in range(2, 16):
        object_count = 0
        self_count = 0
        counts_by_exponent = {}
        for counts, area in generated_cmps(base, base, 512):
            rows = rows_from_counts(base, counts)
            is_self = check_partition(base, base, rows, area)
            self_count += is_self
            exponent = exact_exponent(base, area)
            if exponent is not None:
                entry = counts_by_exponent.setdefault(exponent, [0, 0, 0])
                entry[0] += 1
                entry[1] += is_self
                entry[2] += is_self and len(set(rows)) > 1
            object_count += 1
        for exponent, values in sorted(counts_by_exponent.items()):
            total, self_total, nonsquare = values
            assert (total == exponent + 1) == (exponent <= base)
            expected_self = exponent % 2 == 0 or (base % 2 == 0 and exponent >= base + 1)
            expected_nonsquare = ((base % 2 == 1 and exponent % 2 == 0 and exponent >= base + 1)
                                  or (base % 2 == 0 and exponent % 2 == 1 and exponent >= base + 1)
                                  or (base % 2 == 0 and exponent % 2 == 0 and exponent >= 2 * base))
            assert bool(self_total) == expected_self
            assert bool(nonsquare) == expected_nonsquare
            power_counts.append({'base': base, 'exponent': exponent,
                                 'cmp_count': total, 'self_conjugate_count': self_total,
                                 'nonsquare_self_conjugate_count': nonsquare})
        diagonal.append({'base': base, 'cmp_count': object_count,
                         'self_conjugate_count': self_count})
        for exponent in range(4):
            side = base ** exponent
            if side ** 2 <= 512:
                square = (side,) * side
                assert transpose(square) == square
                check_partition(base, base, square, side ** 2)

    assert transpose((4, 2, 1, 1)) == (4, 2, 1, 1)
    for width_limit, height_limit in itertools.product(range(13), repeat=2):
        word_count = sum(math.comb(width + height, width)
                         for width in range(width_limit + 1)
                         for height in range(height_limit + 1))
        assert word_count == math.comb(width_limit + height_limit + 2, width_limit + 1) - 1
    for index in range(1, 65):
        assert math.comb(2 * index, index) ** 2 * (index + 1) <= 16 ** index
    result = {
        'schema_version': 1,
        'status': 'pass',
        'arithmetic': 'exact integers',
        'coverage': {
            'independent_enumeration': 'All m-ary partitions of sizes 1..64, m=2..6, filtered by q-ary conjugates for q=2..6; equality with operator enumeration.',
            'mixed_base_congruence': 'All operator-generated conjugate (m,q)-ary partitions of sizes 1..512 for m,q=2..6.',
            'self_conjugate_congruences': 'All operator-generated CMPs of sizes 1..512 for m=2..15, with explicit transposition.',
            'scope': 'These are finite consistency checks. The all-parameter conclusions follow from the written proofs in note.tex.'
        },
        'independent_enumeration': crosschecks,
        'mixed_base': mixed,
        'same_base': diagonal
    }
    result['coverage']['power_thresholds'] = 'All CMPs of powers at most 512 for bases 2..15; exact counts and self-conjugate existence classifications.'
    result['coverage']['constructions'] = 'Flowers-Lockard and Dietz-Flowers-Lockard constructions for bases 2..16 with three subsequent inflations; arbitrary CMP row shifts 0..3.'
    result['power_counts'] = power_counts
    result['compressed_constructions'] = check_constructions()
    result['density_bound_identities'] = {'word_rectangle_range': [0, 12],
                                          'central_binomial_range': [1, 64],
                                          'arithmetic': 'exact integers'}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
