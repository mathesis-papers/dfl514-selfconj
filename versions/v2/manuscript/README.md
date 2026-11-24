# Sharp thresholds for conjugate m-ary partitions

The note uses Munagi's residue-class criterion and extends Flowers and Lockard's 2021 construction to answer Dietz, Flowers and Lockard's Questions 5.12–5.14 (2026, §5, printed p. 404) in their self-conjugate setting.

## Mathematical results

- Theorem 1: every nonempty conjugate `(m,q)`-ary partition satisfies `N ≡ H+W−1 (mod (m−1)(q−1))`.
- Corollary 2: a nonrectangular CMP of `m^r`, with width `m^a` and height `m^b`, has `1 ≤ a+b−r ≤ r−2` and `m−1 | a+b−r`.
- Corollary 3: nonrectangular CMPs of `m^r` exist exactly for `r ≥ m+1`. Thus `C_m(m^r)=r+1` for `0 ≤ r ≤ m` and is larger thereafter. The first non-square self-conjugate example also has exponent `m+1`.
- Corollary 4: for odd `m ≥ 3`, self-conjugate CMPs of `m^r` exist exactly for even `r`.
- Corollary 5: non-square self-conjugate examples exist exactly for even `r ≥ m+1` when `m` is odd, for odd `r ≥ m+1` when `m` is even, and for even `r ≥ 2m` when `m` is even.
- Corollary 6 partially answers Question 4.9: the integers admitting a conjugate `(m,q)`-ary partition have density zero if `m^(-1/2)+q^(-1/2)<1`, and also for `(m,q)=(4,4)`.

Question 5.13 omits the word “self-conjugate” in its printed wording. The affirmative answer uses its section's self-conjugate setting. If arbitrary non-square rectangles are allowed, `(m)` already partitions `m`. The stronger nonrectangular threshold has no self-conjugacy restriction.

## Files and rebuilding

`note.tex` contains all definitions, proofs, constructions and bibliography. `note.pdf` is the typeset note. `verify.py` uses only the Python 3 standard library, and `verification.json` specifies its exact finite ranges and counts. `metadata.json` identifies the authors, license and covered problem.

`source-v2.zip` contains `note.tex`, this `README.md`, `metadata.json`, `verify.py` and `verification.json`. Extract it into an empty directory and use the commands below; the typeset PDF is supplied separately.

With Tectonic 0.17.0 installed, run:

```sh
tectonic --untrusted note.tex
python3 verify.py > verification.json
```

Alternatively, run `pdflatex note.tex` twice. The bibliography is embedded; BibTeX and external figures are unnecessary.

## Proof coverage

All the mathematical results listed above have written proofs in the note. The constructions at exponents `m+1` and `2m` are credited to Flowers–Lockard (2021, Lemma 4.2, p. 467) and Dietz–Flowers–Lockard (2026, Corollary 5.9, p. 404), respectively.

The declaration `D5.S3.Combinatorics.Partitions.OddPowerSelfConjugateCMP.result` proves precisely odd-power nonexistence for odd bases, the first statement of Corollary 4:

https://github.com/the-omega-institute/trureturing/blob/8acf7efa41af7fc9ddbbd39571e7ef73462f4509/D5/S3/Combinatorics/Partitions/OddPowerSelfConjugateCMP.lean

The supporting declarations `rowLen_zero` and `height_bounds` give structural bounds for finite Young diagrams:

https://github.com/the-omega-institute/trureturing/blob/8acf7efa41af7fc9ddbbd39571e7ef73462f4509/D5/S1/Words/Compositions/StrictFirstSumsGapfreeOddParts.lean

The checker compares independent multiplicity enumeration and generating-operator enumeration through size 64 for all 25 base pairs `m,q=2..6`; checks mixed-base congruences through size 512; and checks same-base objects and power classifications for `m=2..15` through size 512. Compressed exact multiplicities check the constructions for bases `2..16`, including subsequent inflations and row shifts. These finite checks supplement the written proofs.

## References

- G. D. Dietz, T. B. Flowers and S. R. Lockard, *A study of m-ary partitions whose conjugates are q-ary*, J. Algebra Comb. Discrete Struct. Appl. 13(3) (2026), 385–407. https://doi.org/10.13069/jacodesmath.v13i3.393
- T. B. Flowers and S. R. Lockard, *Conjugate m-ary partitions*, Australas. J. Combin. 81(3) (2021), 458–473. https://ajc.maths.uq.edu.au/pdf/81/ajc_v81_p458.pdf
- A. O. Munagi, *Pairing conjugate partitions by residue classes*, Discrete Math. 308(12) (2008), 2492–2501. https://doi.org/10.1016/j.disc.2007.05.022
- OEIS A067357, dated comment by Michael Somos, 25 July 2015. https://oeis.org/A067357
- G. E. Andrews, *The Bhargava-Adiga Summation and Partitions*, J. Indian Math. Soc. 84(3–4) (2017), 151–160. https://doi.org/10.18311/jims/2017/15836
- NIST DLMF, §26.9(i), definitions of Ferrers diagrams and conjugate partitions. https://dlmf.nist.gov/26.9#i

## Authors and license

Haobo Ma — ChronoAI Pte Ltd, Singapore.

Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore.

Copyright 2026 Haobo Ma and Wenlin Zhang. Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0; `cc-by-4.0`).
