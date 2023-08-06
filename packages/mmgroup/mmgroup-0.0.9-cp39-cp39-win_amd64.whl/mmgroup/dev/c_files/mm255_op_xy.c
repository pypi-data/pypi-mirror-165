/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////

/** @file mm255_op_xy.c

 File ``mm255_op_xy.c`` implements the operation of the element
 \f$y_f \cdot x_e \cdot x_\epsilon\f$ of the monster group
 on a vector in the representation \f$\rho_{255}\f$ of the
 monster.

 Here the generators \f$y_f, x_e\f$ and \f$x_\epsilon\f$ of the
 monster group are defined as in section **The monster group**
 of the **API reference**. The values  \f$f, e\f$  are integers
 encoding elements of the Parker loop, and the value \f$\epsilon\f$
 (or ``eps`` in a C program) is an integer encoding an element of 
 the Golay cocode, as described in ibid.

 The representation \f$\rho_{255}\f$ is equal to the
 196884-dimensional representation  \f$\rho\f$ of the monster,
 with coefficients taken modulo 255, as defined in
 section **The representation of the monster group**
 in the **API reference**.

 An element of \f$\rho_{255}\f$ is implemented as an array of
 integers of type ``uint_mmv_t`` as described in
 section **Description of the mmgroup.mm extension** 
 in this document.

 A formula for the operation of \f$y_f \cdot x_e \cdot x_\epsilon\f$
 on \f$\rho\f$ is given in
 section **Implementing generators of the monster group**
 in the **mmgroup guide for developers**.

 Internally, we use the C function ``mm_sub_prep_xy`` in 
 file ``mm_tables.c`` for computing the opetation stated above.
*/


#include <string.h>
#include "mm_op255.h"   
   
// %%EXPORT_KWD MM_OP%{P}_API


//  %%GEN h
//  %%GEN c



/// @cond DO_NOT_DOCUMENT 

// Tables TABLE_PERM64_LOW, TABLE_PERM64_HIGH contain the following data.
//
// For bits e, s and suboctads 0 <= alpha, delta < 64 define the bit
// TP(e, s, alpha, delta) = e * |delta| / 2 + s + <alpha, delta> (mod 2),
// and put T(128*e + 64*s + alpha, delta) = TP(e, s, alpha, delta).
// Here |delta| is the bit weight of the suboctad delta (modulo 4),
// which can be computed as the bit weight of  2*delta + Par(delta), 
// where Par(delta) is the bit parity of delta.   <alpha, delta> is the
// parity of the intersection of suboctads alpha and delta, which can be 
// computed as   Par(alpha & delta) ^ (Par(alpha) & Par(delta)).
// 
// Note that TP() is linear in the bit vector alpha; so  T(x, delta)
// can be decomposed as 
//
//  T(x, delta) = TH(x >> 4, delta) ^ TL(x & 0xf, delta)
//
//  for 0 <= x < 256, 0 <= delta < 64.
// 
// The array TABLE_PERM64_LOW[8*x,..., 8*x + 7]
// contains the vector TL(x) = (TL(x, 0) * 255, ..., TL(x, 63) * 255),
// stored as a vector of length 64 in internal representation.
// 
// The array TABLE_PERM64_HIGH[8*x,..., 8*x + 7]
// contains the vector TH(x) = (TH(x, 0) * 255, ..., TH(x, 63) * 255),
// stored as a vector of length 64 in internal representation.
//
// Let V be a vector of length 64 in internal representation
// containing entries with tags  ('T', d, 0), ...,  ('T', d, 63).
// Then XORing vectors  TL(x) and TH(x) to the vector V is equivalent
// multiplying the sign of the entry with tag  ('T', d, delta) by
// (-1) ** T(x, delta) for 0 <= delta < 64. Here '**' denotes
// exponentiation. 


static const uint_mmv_t TABLE_PERM64_LOW[] = {
   // %%TABLE TABLE_PERM64_XY_LOW, uint%{INT_BITS}
0x0000000000000000ULL,0x0000000000000000ULL,
0x0000000000000000ULL,0x0000000000000000ULL,
0x0000000000000000ULL,0x0000000000000000ULL,
0x0000000000000000ULL,0x0000000000000000ULL,
0x0000ffffffff0000ULL,0xffff00000000ffffULL,
0xffff00000000ffffULL,0x0000ffffffff0000ULL,
0xffff00000000ffffULL,0x0000ffffffff0000ULL,
0x0000ffffffff0000ULL,0xffff00000000ffffULL,
0x00ff00ffff00ff00ULL,0xff00ff0000ff00ffULL,
0xff00ff0000ff00ffULL,0x00ff00ffff00ff00ULL,
0xff00ff0000ff00ffULL,0x00ff00ffff00ff00ULL,
0x00ff00ffff00ff00ULL,0xff00ff0000ff00ffULL,
0x00ffff0000ffff00ULL,0x00ffff0000ffff00ULL,
0x00ffff0000ffff00ULL,0x00ffff0000ffff00ULL,
0x00ffff0000ffff00ULL,0x00ffff0000ffff00ULL,
0x00ffff0000ffff00ULL,0x00ffff0000ffff00ULL,
0x00ffff0000ffff00ULL,0xff0000ffff0000ffULL,
0xff0000ffff0000ffULL,0x00ffff0000ffff00ULL,
0xff0000ffff0000ffULL,0x00ffff0000ffff00ULL,
0x00ffff0000ffff00ULL,0xff0000ffff0000ffULL,
0x00ff00ffff00ff00ULL,0x00ff00ffff00ff00ULL,
0x00ff00ffff00ff00ULL,0x00ff00ffff00ff00ULL,
0x00ff00ffff00ff00ULL,0x00ff00ffff00ff00ULL,
0x00ff00ffff00ff00ULL,0x00ff00ffff00ff00ULL,
0x0000ffffffff0000ULL,0x0000ffffffff0000ULL,
0x0000ffffffff0000ULL,0x0000ffffffff0000ULL,
0x0000ffffffff0000ULL,0x0000ffffffff0000ULL,
0x0000ffffffff0000ULL,0x0000ffffffff0000ULL,
0x0000000000000000ULL,0xffffffffffffffffULL,
0xffffffffffffffffULL,0x0000000000000000ULL,
0xffffffffffffffffULL,0x0000000000000000ULL,
0x0000000000000000ULL,0xffffffffffffffffULL,
0xff0000ff00ffff00ULL,0xff0000ff00ffff00ULL,
0x00ffff00ff0000ffULL,0x00ffff00ff0000ffULL,
0x00ffff00ff0000ffULL,0x00ffff00ff0000ffULL,
0xff0000ff00ffff00ULL,0xff0000ff00ffff00ULL,
0xff00ff00ff00ff00ULL,0x00ff00ff00ff00ffULL,
0xff00ff00ff00ff00ULL,0x00ff00ff00ff00ffULL,
0xff00ff00ff00ff00ULL,0x00ff00ff00ff00ffULL,
0xff00ff00ff00ff00ULL,0x00ff00ff00ff00ffULL,
0xffff0000ffff0000ULL,0x0000ffff0000ffffULL,
0xffff0000ffff0000ULL,0x0000ffff0000ffffULL,
0xffff0000ffff0000ULL,0x0000ffff0000ffffULL,
0xffff0000ffff0000ULL,0x0000ffff0000ffffULL,
0xffffffff00000000ULL,0xffffffff00000000ULL,
0x00000000ffffffffULL,0x00000000ffffffffULL,
0x00000000ffffffffULL,0x00000000ffffffffULL,
0xffffffff00000000ULL,0xffffffff00000000ULL,
0xffffffff00000000ULL,0x00000000ffffffffULL,
0xffffffff00000000ULL,0x00000000ffffffffULL,
0xffffffff00000000ULL,0x00000000ffffffffULL,
0xffffffff00000000ULL,0x00000000ffffffffULL,
0xffff0000ffff0000ULL,0xffff0000ffff0000ULL,
0x0000ffff0000ffffULL,0x0000ffff0000ffffULL,
0x0000ffff0000ffffULL,0x0000ffff0000ffffULL,
0xffff0000ffff0000ULL,0xffff0000ffff0000ULL,
0xff00ff00ff00ff00ULL,0xff00ff00ff00ff00ULL,
0x00ff00ff00ff00ffULL,0x00ff00ff00ff00ffULL,
0x00ff00ff00ff00ffULL,0x00ff00ff00ff00ffULL,
0xff00ff00ff00ff00ULL,0xff00ff00ff00ff00ULL,
0xff0000ff00ffff00ULL,0x00ffff00ff0000ffULL,
0xff0000ff00ffff00ULL,0x00ffff00ff0000ffULL,
0xff0000ff00ffff00ULL,0x00ffff00ff0000ffULL,
0xff0000ff00ffff00ULL,0x00ffff00ff0000ffULL
}; 


static const uint_mmv_t TABLE_PERM64_HIGH[] = {
   // %%TABLE TABLE_PERM64_XY_HIGH, uint%{INT_BITS}
0x0000000000000000ULL,0x0000000000000000ULL,
0x0000000000000000ULL,0x0000000000000000ULL,
0x0000000000000000ULL,0x0000000000000000ULL,
0x0000000000000000ULL,0x0000000000000000ULL,
0xff0000ff00ffff00ULL,0x00ffff00ff0000ffULL,
0xff0000ff00ffff00ULL,0x00ffff00ff0000ffULL,
0x00ffff00ff0000ffULL,0xff0000ff00ffff00ULL,
0x00ffff00ff0000ffULL,0xff0000ff00ffff00ULL,
0xff0000ff00ffff00ULL,0x00ffff00ff0000ffULL,
0x00ffff00ff0000ffULL,0xff0000ff00ffff00ULL,
0xff0000ff00ffff00ULL,0x00ffff00ff0000ffULL,
0x00ffff00ff0000ffULL,0xff0000ff00ffff00ULL,
0x0000000000000000ULL,0x0000000000000000ULL,
0xffffffffffffffffULL,0xffffffffffffffffULL,
0xffffffffffffffffULL,0xffffffffffffffffULL,
0x0000000000000000ULL,0x0000000000000000ULL,
0xffffffffffffffffULL,0xffffffffffffffffULL,
0xffffffffffffffffULL,0xffffffffffffffffULL,
0xffffffffffffffffULL,0xffffffffffffffffULL,
0xffffffffffffffffULL,0xffffffffffffffffULL,
0x00ffff00ff0000ffULL,0xff0000ff00ffff00ULL,
0x00ffff00ff0000ffULL,0xff0000ff00ffff00ULL,
0xff0000ff00ffff00ULL,0x00ffff00ff0000ffULL,
0xff0000ff00ffff00ULL,0x00ffff00ff0000ffULL,
0x00ffff00ff0000ffULL,0xff0000ff00ffff00ULL,
0xff0000ff00ffff00ULL,0x00ffff00ff0000ffULL,
0x00ffff00ff0000ffULL,0xff0000ff00ffff00ULL,
0xff0000ff00ffff00ULL,0x00ffff00ff0000ffULL,
0xffffffffffffffffULL,0xffffffffffffffffULL,
0x0000000000000000ULL,0x0000000000000000ULL,
0x0000000000000000ULL,0x0000000000000000ULL,
0xffffffffffffffffULL,0xffffffffffffffffULL,
0x00ffffffffffff00ULL,0x000000ff00ffffffULL,
0x000000ff00ffffffULL,0xff000000000000ffULL,
0x000000ff00ffffffULL,0xff000000000000ffULL,
0xff000000000000ffULL,0xffffff00ff000000ULL,
0xffffff00ff000000ULL,0x00ffffffffffff00ULL,
0xff000000000000ffULL,0xffffff00ff000000ULL,
0x00ffffffffffff00ULL,0x000000ff00ffffffULL,
0xffffff00ff000000ULL,0x00ffffffffffff00ULL,
0xffffff00ff000000ULL,0x00ffffffffffff00ULL,
0x00ffffffffffff00ULL,0x000000ff00ffffffULL,
0xff000000000000ffULL,0xffffff00ff000000ULL,
0xffffff00ff000000ULL,0x00ffffffffffff00ULL,
0x00ffffffffffff00ULL,0x000000ff00ffffffULL,
0xffffff00ff000000ULL,0x00ffffffffffff00ULL,
0xffffff00ff000000ULL,0x00ffffffffffff00ULL,
0xff000000000000ffULL,0xffffff00ff000000ULL,
0xff000000000000ffULL,0xffffff00ff000000ULL,
0xffffff00ff000000ULL,0x00ffffffffffff00ULL,
0xffffff00ff000000ULL,0x00ffffffffffff00ULL,
0x00ffffffffffff00ULL,0x000000ff00ffffffULL,
0x000000ff00ffffffULL,0xff000000000000ffULL,
0x00ffffffffffff00ULL,0x000000ff00ffffffULL,
0xff000000000000ffULL,0xffffff00ff000000ULL,
0x000000ff00ffffffULL,0xff000000000000ffULL,
0x000000ff00ffffffULL,0xff000000000000ffULL,
0xff000000000000ffULL,0xffffff00ff000000ULL,
0x00ffffffffffff00ULL,0x000000ff00ffffffULL,
0x000000ff00ffffffULL,0xff000000000000ffULL,
0xff000000000000ffULL,0xffffff00ff000000ULL,
0x000000ff00ffffffULL,0xff000000000000ffULL,
0x000000ff00ffffffULL,0xff000000000000ffULL,
0x00ffffffffffff00ULL,0x000000ff00ffffffULL
}; 



static const uint32_t TABLE24_START[4] = {
   MM_OP255_OFS_X, MM_OP255_OFS_Z, MM_OP255_OFS_Y
};


/// @endcond





/// @cond DO_NOT_DOCUMENT 

static inline void
op255_do_ABC(uint_mmv_t *v_in, mm_sub_op_xy_type *p_op, uint32_t mode, uint_mmv_t *v_out)
{

    uint_mmv_t mask[16];
    uint_mmv_t neg_mask[4];
    uint_mmv_t f = p_op->f_i, ef = p_op->ef_i, eps;
    uint32_t i;

    mask[0] = f >>  0;
    mask[4] = ef >> 0;
    // %%IF i < V24_INTS_USED - 1 or 24 % INT_FIELDS == 0
    neg_mask[0] = 0xffffffffffffffffULL;
    // %%END IF
    mask[1] = f >>  8;
    mask[5] = ef >> 8;
    // %%IF i < V24_INTS_USED - 1 or 24 % INT_FIELDS == 0
    neg_mask[1] = 0xffffffffffffffffULL;
    // %%END IF
    mask[2] = f >>  16;
    mask[6] = ef >> 16;
    // %%IF i < V24_INTS_USED - 1 or 24 % INT_FIELDS == 0
    neg_mask[2] = 0xffffffffffffffffULL;
    // %%END IF
    for (i = 0; i < 7; ++i) {
        uint_mmv_t x = mask[i];
        // %%MMV_UINT_SPREAD x, x
        // Spread bits 0,...,7 of x to the (8-bit long) fields
        // of x. A field of x is set to 0xff if its 
        // corresponding bit in input x is one and to 0 otherwise.
        x = (x & 0xfULL) + ((x & 0xf0ULL) << 28);
        x = (x & 0x300000003ULL) 
            +  ((x & 0xc0000000cULL) << 14);
        x = (x & 0x1000100010001ULL) 
            +  ((x & 0x2000200020002ULL) << 7);
        x *= 255;
        // Bit spreading done.
        mask[i] = x = x & neg_mask[i & 3];
        mask[i + 8] = x ^ neg_mask[i & 3];
    }

    f =  p_op->f_i << 3;
    for (i = 0; i < 96; i += 4) {
        uint_mmv_t t, t1;
        // process uint_mmv_t 0 of row i/4 for tag A
        t1 = v_in[i + MM_OP255_OFS_A + 0]; 
        t = mask[0 + (f & 0x8ULL)];
        v_out[i + MM_OP255_OFS_A + 0] = t1 ^ t; 
        // process uint_mmv_t 1 of row i/4 for tag A
        t1 = v_in[i + MM_OP255_OFS_A + 1]; 
        t = mask[1 + (f & 0x8ULL)];
        v_out[i + MM_OP255_OFS_A + 1] = t1 ^ t; 
        // process uint_mmv_t 2 of row i/4 for tag A
        t1 = v_in[i + MM_OP255_OFS_A + 2]; 
        t = mask[2 + (f & 0x8ULL)];
        v_out[i + MM_OP255_OFS_A + 2] = t1 ^ t; 
        v_out[i + MM_OP255_OFS_A + 3] = 0;
        f >>= 1;    
    }

    if (mode) return;

    f =  p_op->f_i << 3;
    ef =  p_op->ef_i << 3;
    eps = 0 - ((p_op->eps >> 11) & 0x1ULL);
    for (i = 0; i < 96; i += 4) {
        uint_mmv_t t, t1, t2;
        // %%FOR j in range(V24_INTS_USED)
        // process uint_mmv_t 0 of row i/4 for tags B, C
        t1 = v_in[i + MM_OP255_OFS_B + 0]; 
        t2 = v_in[i + MM_OP255_OFS_C + 0];
        t = mask[0 + (f & 0x8ULL)];
        t &= (t1 ^ t2);
        t ^= mask[4 + (ef & 0x8ULL)];
        v_out[i + MM_OP255_OFS_B + 0] = t1 ^ t;
        t2 ^= eps & neg_mask[0];
        v_out[i + MM_OP255_OFS_C + 0] = t2 ^ t;
        // process uint_mmv_t 1 of row i/4 for tags B, C
        t1 = v_in[i + MM_OP255_OFS_B + 1]; 
        t2 = v_in[i + MM_OP255_OFS_C + 1];
        t = mask[1 + (f & 0x8ULL)];
        t &= (t1 ^ t2);
        t ^= mask[5 + (ef & 0x8ULL)];
        v_out[i + MM_OP255_OFS_B + 1] = t1 ^ t;
        t2 ^= eps & neg_mask[1];
        v_out[i + MM_OP255_OFS_C + 1] = t2 ^ t;
        // process uint_mmv_t 2 of row i/4 for tags B, C
        t1 = v_in[i + MM_OP255_OFS_B + 2]; 
        t2 = v_in[i + MM_OP255_OFS_C + 2];
        t = mask[2 + (f & 0x8ULL)];
        t &= (t1 ^ t2);
        t ^= mask[6 + (ef & 0x8ULL)];
        v_out[i + MM_OP255_OFS_B + 2] = t1 ^ t;
        t2 ^= eps & neg_mask[2];
        v_out[i + MM_OP255_OFS_C + 2] = t2 ^ t;
        // %%END FOR
        v_out[i + MM_OP255_OFS_B + 3] = 0;
        v_out[i + MM_OP255_OFS_C + 3] = 0;
        f >>= 1; ef >>= 1;      
    }
}

/// @endcond 



/// @cond DO_NOT_DOCUMENT 

/**
  @brief Workhorse for function ``mm_op255_xy``

  ``mm_op255_xy(v_in, f, e, eps, v_out)`` is equivalent to

        mm_sub_op_xy_type s_op;  // defined in mm_basics.h
          ... // allocate storage for s_op.sign_XYZ and s_op.p_T
        mm_sub_prep_xy(f, e, eps, &s_op);
        mm_op255_do_xy(v_in, &s_op, v_out);

   So the functions called by function ``mm_op255_xy``
   can be tested individually.
*/
static
void mm_op255_do_xy(uint_mmv_t *v_in, mm_sub_op_xy_type *p_op, uint_mmv_t *v_out)
{
    uint_fast32_t i;

    
    // Step 1: do rows with 24 entries, tags X, Z, Y 
    {
        uint32_t table24_dest[3];
        // TODO: comment properly!!!!
        for (i = 0; i < 3; ++i) table24_dest[i] = TABLE24_START[i];
        i = (TABLE24_START[1] ^ TABLE24_START[2]) & 
            (0 - ((p_op->eps >> 11) & 1));
        table24_dest[1] ^= i;  table24_dest[2] ^= i; 

        for (i = 0; i < 3; ++i)  {
            uint_mmv_t *p_src = v_in + TABLE24_START[i];
            uint_mmv_t *p_dest = v_out + table24_dest[i];
            uint_fast32_t i1;
            uint_mmv_t a_sign[2][4];
            uint_mmv_t d_xor = p_op->lin_d[i];
            uint8_t *p_sign = p_op->sign_XYZ;
    
            for (i1 = 0; i1 < 3; ++i1) {
                uint_mmv_t x = p_op->lin_i[i] >> (i1 << 3); 
                // %%MMV_UINT_SPREAD x, x
                // Spread bits 0,...,7 of x to the (8-bit long) fields
                // of x. A field of x is set to 0xff if its 
                // corresponding bit in input x is one and to 0 otherwise.
                x = (x & 0xfULL) + ((x & 0xf0ULL) << 28);
                x = (x & 0x300000003ULL) 
                    +  ((x & 0xc0000000cULL) << 14);
                x = (x & 0x1000100010001ULL) 
                    +  ((x & 0x2000200020002ULL) << 7);
                x *= 255;
                // Bit spreading done.
                a_sign[0][i1] = x;
                a_sign[1][i1] = x ^ 0xffffffffffffffffULL;
            }
         
            for (i1 = 0; i1 < 2048; ++i1) {
                uint_mmv_t *ps = p_src + ((i1 ^ d_xor) << 2);
                uint_fast8_t sign = (p_sign[i1] >> i) & 1;
                // %%FOR j in range(V24_INTS_USED)
                p_dest[0] = ps[0] ^ a_sign[sign][0];
                p_dest[1] = ps[1] ^ a_sign[sign][1];
                p_dest[2] = ps[2] ^ a_sign[sign][2];
                // %%END FOR
                p_dest[3] = 0;
                p_dest +=  4;      
            }
        }    
    }    

    // Step 2: do rows with 64 entries, tag T // TODO: comment properly!!!!
    {
        uint_mmv_t *p_src = v_in + MM_OP255_OFS_T;
        uint_mmv_t *p_dest = v_out + MM_OP255_OFS_T;
        uint16_t* p_T =  p_op->s_T;
        for (i = 0; i < 759; ++i) {
            uint_fast16_t ofs_l = *p_T;
            uint_fast16_t ofs_h = (ofs_l & 63) >> 3;
            const uint_mmv_t *ps_h = TABLE_PERM64_HIGH +
                ((ofs_l & 0xf000) >> 9);
            const uint_mmv_t *ps_l = TABLE_PERM64_LOW + 
                ((ofs_l & 0xf00) >> 5);
            ofs_l = (ofs_l << 3) & 0x3fULL;
            // %%FOR j in range(V64_INTS)
            p_dest[0] =  ps_h[0] ^ ps_l[0] ^
               (((p_src[0 ^ ofs_h] >> (0 ^ ofs_l)) & 255) << 0) ^
               (((p_src[0 ^ ofs_h] >> (8 ^ ofs_l)) & 255) << 8) ^
               (((p_src[0 ^ ofs_h] >> (16 ^ ofs_l)) & 255) << 16) ^
               (((p_src[0 ^ ofs_h] >> (24 ^ ofs_l)) & 255) << 24) ^
               (((p_src[0 ^ ofs_h] >> (32 ^ ofs_l)) & 255) << 32) ^
               (((p_src[0 ^ ofs_h] >> (40 ^ ofs_l)) & 255) << 40) ^
               (((p_src[0 ^ ofs_h] >> (48 ^ ofs_l)) & 255) << 48) ^
               (((p_src[0 ^ ofs_h] >> (56 ^ ofs_l)) & 255) << 56);
            p_dest[1] =  ps_h[1] ^ ps_l[1] ^
               (((p_src[1 ^ ofs_h] >> (0 ^ ofs_l)) & 255) << 0) ^
               (((p_src[1 ^ ofs_h] >> (8 ^ ofs_l)) & 255) << 8) ^
               (((p_src[1 ^ ofs_h] >> (16 ^ ofs_l)) & 255) << 16) ^
               (((p_src[1 ^ ofs_h] >> (24 ^ ofs_l)) & 255) << 24) ^
               (((p_src[1 ^ ofs_h] >> (32 ^ ofs_l)) & 255) << 32) ^
               (((p_src[1 ^ ofs_h] >> (40 ^ ofs_l)) & 255) << 40) ^
               (((p_src[1 ^ ofs_h] >> (48 ^ ofs_l)) & 255) << 48) ^
               (((p_src[1 ^ ofs_h] >> (56 ^ ofs_l)) & 255) << 56);
            p_dest[2] =  ps_h[2] ^ ps_l[2] ^
               (((p_src[2 ^ ofs_h] >> (0 ^ ofs_l)) & 255) << 0) ^
               (((p_src[2 ^ ofs_h] >> (8 ^ ofs_l)) & 255) << 8) ^
               (((p_src[2 ^ ofs_h] >> (16 ^ ofs_l)) & 255) << 16) ^
               (((p_src[2 ^ ofs_h] >> (24 ^ ofs_l)) & 255) << 24) ^
               (((p_src[2 ^ ofs_h] >> (32 ^ ofs_l)) & 255) << 32) ^
               (((p_src[2 ^ ofs_h] >> (40 ^ ofs_l)) & 255) << 40) ^
               (((p_src[2 ^ ofs_h] >> (48 ^ ofs_l)) & 255) << 48) ^
               (((p_src[2 ^ ofs_h] >> (56 ^ ofs_l)) & 255) << 56);
            p_dest[3] =  ps_h[3] ^ ps_l[3] ^
               (((p_src[3 ^ ofs_h] >> (0 ^ ofs_l)) & 255) << 0) ^
               (((p_src[3 ^ ofs_h] >> (8 ^ ofs_l)) & 255) << 8) ^
               (((p_src[3 ^ ofs_h] >> (16 ^ ofs_l)) & 255) << 16) ^
               (((p_src[3 ^ ofs_h] >> (24 ^ ofs_l)) & 255) << 24) ^
               (((p_src[3 ^ ofs_h] >> (32 ^ ofs_l)) & 255) << 32) ^
               (((p_src[3 ^ ofs_h] >> (40 ^ ofs_l)) & 255) << 40) ^
               (((p_src[3 ^ ofs_h] >> (48 ^ ofs_l)) & 255) << 48) ^
               (((p_src[3 ^ ofs_h] >> (56 ^ ofs_l)) & 255) << 56);
            p_dest[4] =  ps_h[4] ^ ps_l[4] ^
               (((p_src[4 ^ ofs_h] >> (0 ^ ofs_l)) & 255) << 0) ^
               (((p_src[4 ^ ofs_h] >> (8 ^ ofs_l)) & 255) << 8) ^
               (((p_src[4 ^ ofs_h] >> (16 ^ ofs_l)) & 255) << 16) ^
               (((p_src[4 ^ ofs_h] >> (24 ^ ofs_l)) & 255) << 24) ^
               (((p_src[4 ^ ofs_h] >> (32 ^ ofs_l)) & 255) << 32) ^
               (((p_src[4 ^ ofs_h] >> (40 ^ ofs_l)) & 255) << 40) ^
               (((p_src[4 ^ ofs_h] >> (48 ^ ofs_l)) & 255) << 48) ^
               (((p_src[4 ^ ofs_h] >> (56 ^ ofs_l)) & 255) << 56);
            p_dest[5] =  ps_h[5] ^ ps_l[5] ^
               (((p_src[5 ^ ofs_h] >> (0 ^ ofs_l)) & 255) << 0) ^
               (((p_src[5 ^ ofs_h] >> (8 ^ ofs_l)) & 255) << 8) ^
               (((p_src[5 ^ ofs_h] >> (16 ^ ofs_l)) & 255) << 16) ^
               (((p_src[5 ^ ofs_h] >> (24 ^ ofs_l)) & 255) << 24) ^
               (((p_src[5 ^ ofs_h] >> (32 ^ ofs_l)) & 255) << 32) ^
               (((p_src[5 ^ ofs_h] >> (40 ^ ofs_l)) & 255) << 40) ^
               (((p_src[5 ^ ofs_h] >> (48 ^ ofs_l)) & 255) << 48) ^
               (((p_src[5 ^ ofs_h] >> (56 ^ ofs_l)) & 255) << 56);
            p_dest[6] =  ps_h[6] ^ ps_l[6] ^
               (((p_src[6 ^ ofs_h] >> (0 ^ ofs_l)) & 255) << 0) ^
               (((p_src[6 ^ ofs_h] >> (8 ^ ofs_l)) & 255) << 8) ^
               (((p_src[6 ^ ofs_h] >> (16 ^ ofs_l)) & 255) << 16) ^
               (((p_src[6 ^ ofs_h] >> (24 ^ ofs_l)) & 255) << 24) ^
               (((p_src[6 ^ ofs_h] >> (32 ^ ofs_l)) & 255) << 32) ^
               (((p_src[6 ^ ofs_h] >> (40 ^ ofs_l)) & 255) << 40) ^
               (((p_src[6 ^ ofs_h] >> (48 ^ ofs_l)) & 255) << 48) ^
               (((p_src[6 ^ ofs_h] >> (56 ^ ofs_l)) & 255) << 56);
            p_dest[7] =  ps_h[7] ^ ps_l[7] ^
               (((p_src[7 ^ ofs_h] >> (0 ^ ofs_l)) & 255) << 0) ^
               (((p_src[7 ^ ofs_h] >> (8 ^ ofs_l)) & 255) << 8) ^
               (((p_src[7 ^ ofs_h] >> (16 ^ ofs_l)) & 255) << 16) ^
               (((p_src[7 ^ ofs_h] >> (24 ^ ofs_l)) & 255) << 24) ^
               (((p_src[7 ^ ofs_h] >> (32 ^ ofs_l)) & 255) << 32) ^
               (((p_src[7 ^ ofs_h] >> (40 ^ ofs_l)) & 255) << 40) ^
               (((p_src[7 ^ ofs_h] >> (48 ^ ofs_l)) & 255) << 48) ^
               (((p_src[7 ^ ofs_h] >> (56 ^ ofs_l)) & 255) << 56);
            // %%END FOR
            p_src += 8; 
            p_dest += 8; 
            ++p_T;
        }
    }


    // Step 3: do rows with 24 entries, tags A, B, C // TODO: comment properly!!!!
    op255_do_ABC(v_in, p_op, 0, v_out);



    // If eps is odd: 
    //    negate entries X_d,i with scalar product <d,i> = 1
    if (p_op->eps & 0x800) mm_op255_neg_scalprod_d_i(v_out + MM_OP255_OFS_X); 
} 


/// @endcond



/**
  @brief Compute an operation of the monster group on a vector

  Let ``v_in`` be a vector of the representation \f$\rho_{255}\f$
  of the monster group.


  The function implements the operation of the element
  \f$y_f \cdot x_e \cdot x_\epsilon\f$ of the monster group
  on a vector ``v_in`` in the representation \f$\rho_{255}\f$ of
  the monster.

  The integers ``f`` and ``e`` occuring in the generators \f$y_f\f$
  and  \f$x_e\f$ encode elements of the Parker loop. The integer
  ``eps`` encodes the element \f$\epsilon\f$ of the Golay cocode
  occuring in the generator  \f$x_\epsilon\f$,  as indicated in the
  header of this file. The function computes this operation of
  the element of the monster (given by parameters ``f, e, eps``)
  on the input  vector ``v_in`` and  stores the result in the output 
  vector ``v_out.`` 

  Input vector  ``v_in`` is not changed.
*/
// %%EXPORT px
MM_OP255_API
void mm_op255_xy(uint_mmv_t *v_in, uint32_t f, uint32_t e, uint32_t eps, uint_mmv_t *v_out)
{
    uint16_t s_T[759];
    mm_sub_op_xy_type s_op;
    s_op.sign_XYZ =  (uint8_t*)(v_out + MM_OP255_OFS_T);
    s_op.s_T = s_T;
    mm_sub_prep_xy(f, e, eps, &s_op);
    mm_op255_do_xy(v_in, &s_op, v_out);
}



/**
  @brief Compute an operation of the monster group on a vector

  Let ``v`` be a vector of the representation \f$\rho_{255}\f$
  of the monster group. 

  The function implements the operation of the element
  \f$x_d\f$ of the monster group  on a vector ``v`` in the 
  representation \f$\rho_{255}\f$ of the monster. Here ``d`` must be 
  one of the integers ``0, 0x800, 0x1000``, or ``0x1800``, encoding
  the generators \f$x_1, x_\Omega, x_{-1}\f$, or \f$x_{-\Omega}\f$,
  respectively.
   
  The function computes the operation \f$x_d\f$ on the
  vector ``v`` and overwrites the vector ``v`` with the result.
  The function can  be considered as a simplified (and much faster)
  version of function ``mm_op255_xy``.
*/
// %%EXPORT px
MM_OP255_API
void mm_op255_omega(uint_mmv_t *v, uint32_t d)
// Multiply vector ``v`` with ``x_d`` inplace. Here ``d`` must be
// 0, -1, \Omega or -\Omega.
{
    uint_fast32_t i0, i1, sh;
    uint_mmv_t *pv;
     
    v += MM_OP255_OFS_X;
    d &= 0x1800;
    if (d == 0) return;
    sh = 0x01120200UL >> ((d >> 11) << 3);

    for (i0 = 0; i0 < 8; i0 += 4) {
        pv = v + (((sh >> i0) & 0xf) << (5 + 11 - 3));
        for (i1 = 0; i1 < 2048; ++i1) {
            // %%FOR j in range(V24_INTS_USED)
            pv[0] ^=  0xffffffffffffffffULL;
            pv[1] ^=  0xffffffffffffffffULL;
            pv[2] ^=  0xffffffffffffffffULL;
            // %%END FOR
            pv[3] = 0;
            pv +=  4;      
        }
    }
}


/**
  @brief Restriction of function ``mm_op255_xy`` to tag ``A``

  Function ``mm_op255_xy`` computes a certain operation of the
  monster group on a vector ``v_in``. That operation depends
  on parameters ``f, e,`` and ``eps``.
  
  Function ``mm_op255_xy_tag_ABC`` computes the same
  operation on the entries of the vector ``v = v_in`` with
  tag ``A, B, C`` only, and ignores the other entries of ``v``.
  See section **The representation of the monster group**
  in the **API reference** for tags of entries of a vector in
  the representation of the monster.

  The function overwrites the vector ``v`` with the result.
  Here only entries of ``v`` with tag ``A, B, C`` are changed. 
  If parameter ``mode`` is not zero the we update the entries
  with  tag ``A`` only. This function is much faster than
  function ``mm_op255_xy``.
*/
// %%EXPORT px
MM_OP255_API
void mm_op255_xy_tag_ABC(uint_mmv_t *v, uint32_t f, uint32_t e, uint32_t eps, uint32_t mode)
{
    mm_sub_op_xy_type s_op;
    s_op.sign_XYZ = NULL;
    s_op.s_T = NULL;
    mm_sub_prep_xy(f, e, eps, &s_op);
    op255_do_ABC(v, &s_op, mode, v);
}

//  %%GEN h
//  %%GEN c

