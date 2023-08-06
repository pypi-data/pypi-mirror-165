/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////

/** @file mm7_op_misc.c

 File ``mm7_op_misc.c`` implements the operations on
 vectors in the representation \f$\rho_{7}\f$ of the
 monster.

 The representation \f$\rho_{7}\f$ is equal to the
 196884-dimensional representation  \f$\rho\f$ of the monster,
 with coefficients taken modulo 7, as defined in
 section **The representation of the monster group**
 in the **API reference**.

 An element of \f$\rho_{7}\f$ is implemented as an array
 of integers of type ``uint_mmv_t`` as described in
 section **Description of the mmgroup.mm extension**
 in this document.
*/

#include "mm_op7.h"
#include "clifford12.h"

// %%EXPORT_KWD MM_OP%{P}_API


//  %%GEN h
//  %%GEN c

/** 
  @brief Copy vector ``mv1`` in \f$\rho_{7}\f$ to ``mv2``
*/
// %%EXPORT px
MM_OP7_API
uint32_t mm_op7_copy(uint_mmv_t *mv1, uint_mmv_t *mv2)
// Copy mv1 to mv2. Here mv1 and mv2 are vectors of the
// monster group representation modulo 7.
{
    uint_fast32_t len = 15468; 
    do {
       *mv2++ = *mv1++;
    } while(--len);
    return 0; 
}


/** 
  @brief Compare arrays ``mv1`` and ``mv2`` of integers

  The function compares parts of the two vectors ``mv1``
  and ``mv2``of the representation \f$\rho_{7}\f$.

  Here the function compares ``len`` integers of type
  ``uint_mmv_t`` starting at the pointers ``mv1`` and ``mv2``.
  These integers are interpreted as arrays of bit fields
  containing integers modulo 7.

  The function returns 0 in case of equality and 1 otherwise.
*/
// %%EXPORT px
MM_OP7_API
uint32_t mm_op7_compare_len(uint_mmv_t *mv1, uint_mmv_t *mv2, uint32_t len)
{
    uint_mmv_t a, b, t, c;
    while (len--) {
        a = *mv1++;
        b = *mv2++;
        // Next we compare integers a and b modulo p. 
        // Idea for p = 0x7ULL and unsigned 3-bit integers a, b:
        // t is in [0, p] iff (t ^ (t >> 1)) & 0x3ULL == 0 
        // We have a = +- b (mod p)  iff  a ^ b in [0, p].
        t = a ^ b;
        c = (t ^ (t >> 1)) & 0x3333333333333333ULL; // c = 0 iff a = +- b (mod p)
        // In case c != 0 we already know that a != b holds.
        // So assume c == 0 and hence a = +-b, i.e.  t in [0, p].
        // Then a == b (mod p) iff t == 0 or (t & a) in [0, p].
        // Thus is suffices to check if (t & a) is in [0, p]. 
        t &= a;
        t = (t ^ (t >> 1)) & 0x3333333333333333ULL; // t = 0 iff old t in [0,p]
        if (c | t) return 1;
    }
    return 0; 
}

/** 
  @brief Compare vectors ``mv1`` and ``mv2`` of \f$\rho_{7}\f$

  The function compares two vectors ``mv1`` and ``mv2`` of 
  the representation \f$\rho_{7}\f$.

  It returns 0 in case of equality and 1 otherwise.
*/
// %%EXPORT px
MM_OP7_API
uint32_t mm_op7_compare(uint_mmv_t *mv1, uint_mmv_t *mv2)
//  Compare two vectors of the monster group representation modulo 7..
//  Comparison is done modulo 7.
//  The function returns 0 in case of equality and 1 otherwise.
{
    return mm_op7_compare_len(mv1, mv2, 15468); 
}
   


/** 
  @brief Check if a vector ``mv`` in \f$\rho_{7}\f$ is zero

  The function checks it the vector ``mv`` in the 
  representation \f$\rho_{7}\f$ is zero.

  It returns 0 in case ``mv == 0`` and 1 otherwise. It is optimized
  for the case that ``mv`` is expected to be zero.
*/
// %%EXPORT px
MM_OP7_API
uint32_t mm_op7_checkzero(uint_mmv_t *mv)
{
    uint_mmv_t acc = 0;
    uint_fast32_t i;
    for (i = 0; i < 15468; ++i) acc |= mv[i] ^ (mv[i] >> 1);
    return (acc & 0x3333333333333333ULL) != 0;
}
   
    

    

/** 
  @brief Add vectors ``mv1`` and ``mv2`` of \f$\rho_{7}\f$

  The function adds the two vectors ``mv1`` and ``mv2`` of 
  the representation \f$\rho_{7}\f$ and stores the
  result in the vector ``mv1``.
*/
// %%EXPORT px
MM_OP7_API
void mm_op7_vector_add(uint_mmv_t *mv1, uint_mmv_t *mv2)
//  Vector addition in the monster group representation modulo 7.
//  Put mv1 = mv1 + mv2.
{
    uint_fast32_t len = 15468;
    uint_mmv_t a1, b1;
    do {
        a1 = *mv1;
        b1 = *mv2++;
        a1 = (a1 & 0x7777777777777777ULL) 
              + (b1 & 0x7777777777777777ULL);                     
        a1 = (a1 & 0x7777777777777777ULL) 
              + ((a1 >> 3) & 0x1111111111111111ULL);
        *mv1++ = a1;
    } while (--len);
}


/** 
  @brief Multiply vector ``mv1`` of \f$\rho_{7}\f$ with scalar

  The function multiplies the vector ``mv1`` of the 
  representation \f$\rho_{7}\f$ and with the (signed)
  integer ``factor`` and stores the result in the vector ``mv1``.
*/
// %%EXPORT px
MM_OP7_API
void mm_op7_scalar_mul(int32_t factor, uint_mmv_t *mv1)
//  Scalar multiplication in the monster group representation modulo 7.
//  Put mv1 = factor * mv1.
{
    uint_fast32_t len = 15468;
    uint_mmv_t a1, a2;
    factor %= 7;
    if (factor < 0) factor += 7;
    do {
        a1 = *mv1;
        a2 = ((a1 >> 4) & 0x707070707070707ULL);
        a1 = (a1 & 0x707070707070707ULL);
        a1 *= factor;
        a1 = (a1 & 0x707070707070707ULL) 
              + ((a1 >> 3) & 0x707070707070707ULL);
        a1 = (a1 & 0x707070707070707ULL) 
              + ((a1 >> 3) & 0x101010101010101ULL);
        a2 *= factor;
        a2 = (a2 & 0x707070707070707ULL) 
              + ((a2 >> 3) & 0x707070707070707ULL);
        a2 = (a2 & 0x707070707070707ULL) 
              + ((a2 >> 3) & 0x101010101010101ULL);
        a1 = a1 + (a2 << 4);
        *mv1++ = a1;
    } while (--len);
}



/** 
  @brief Compare two vectors of \f$\rho_{7}\f$ modulo \f$q\f$

  The function compares two vectors ``mv1`` and ``mv2`` of 
  the representation \f$\rho_{7}\f$ modulo a number \f$q\f$.
  Here \f$q\f$ should divide \f$p\f$.

  It returns 0 in case of equality, 1 in case of inequality,
  and 2 if  \f$q\f$ does not divide \f$p\f$.
*/
// %%EXPORT px
MM_OP7_API
uint32_t mm_op7_compare_mod_q(uint_mmv_t *mv1, uint_mmv_t *mv2, uint32_t q)
//  Compare two vectors of the monster group representation modulo 7.
//  Comparison is done modulo q. q must divide 7. The function returns:
//  0  if mmv1 == mmv2 (mod q) 
//  1  if mmv1 != mmv2 (mod q) 
//  2  if q does not divide 7
{
    if (q == 7) return mm_op7_compare(mv1, mv2);
    return q == 1 ? 0 : 2;
}



/** 
  @brief Set a vector in \f$\rho_{7}\f$ to an axis.

  Let ``x`` be an element of the subgroup  \f$Q_{x0}\f$ 
  if the Monster that maps to a short Leech lattice vector.
  Here ``x`` must be given in  **Leech lattice encoding** 
  as in the **Description of the mmgroup.generators extension**
  in the documentation of the **C interface**.

  Then ``x`` corresponds to vector in \f$\rho_{7}\f$
  that is called a **2A axis**. The function stores that
  2A axis in ``mv``.
*/
// %%EXPORT px
MM_OP7_API
int32_t mm_op7_store_axis(uint32_t x, uint_mmv_t *mv)
{
   uint32_t i, j, ind, ua[24];
   int8_t a[24];
   uint8_t  b[32];
   int32_t res;
   
   mm_aux_zero_mmv(7, mv);
   if ((res = xsp2co1_short_2_to_leech(x, a)) < 0) return res;
   for (i = 0; i < 24; ++i) {
       uint32_t entry = ((int32_t)a[i] + (7 << 8)) << 1;
       ua[i] =  entry % 7;
   }
   for (i = 0; i < 24; ++i) {
       uint32_t ua_i = ua[i];
       for (j = 0; j < 24; ++j) {
           b[j] = (uint8_t)(ua_i * ua[j] % 7);
       }
       mm_aux_write_mmv24(7, b, mv + 2 * i, 1);
   }
   ind = mm_aux_index_leech2_to_sparse(x) + 2;
   if ((x & 0x1000000) == 0) ind ^= 7;
   mm_aux_mmv_set_sparse(7, mv, &ind, 1);
   return 0;
}


//  %%GEN h
//  %%GEN c
