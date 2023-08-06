/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////

/** @file mm7_op_xy.c

 File ``mm7_op_xy.c`` implements the operation of the element
 \f$y_f \cdot x_e \cdot x_\epsilon\f$ of the monster group
 on a vector in the representation \f$\rho_{7}\f$ of the
 monster.

 Here the generators \f$y_f, x_e\f$ and \f$x_\epsilon\f$ of the
 monster group are defined as in section **The monster group**
 of the **API reference**. The values  \f$f, e\f$  are integers
 encoding elements of the Parker loop, and the value \f$\epsilon\f$
 (or ``eps`` in a C program) is an integer encoding an element of 
 the Golay cocode, as described in ibid.

 The representation \f$\rho_{7}\f$ is equal to the
 196884-dimensional representation  \f$\rho\f$ of the monster,
 with coefficients taken modulo 7, as defined in
 section **The representation of the monster group**
 in the **API reference**.

 An element of \f$\rho_{7}\f$ is implemented as an array of
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
#include "mm_op7.h"   
   
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
// The array TABLE_PERM64_LOW[4*x,..., 4*x + 3]
// contains the vector TL(x) = (TL(x, 0) * 7, ..., TL(x, 63) * 7),
// stored as a vector of length 64 in internal representation.
// 
// The array TABLE_PERM64_HIGH[4*x,..., 4*x + 3]
// contains the vector TH(x) = (TH(x, 0) * 7, ..., TH(x, 63) * 7),
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
0x7700007700777700ULL,0x0077770077000077ULL,
0x0077770077000077ULL,0x7700007700777700ULL,
0x7070070707077070ULL,0x0707707070700707ULL,
0x0707707070700707ULL,0x7070070707077070ULL,
0x0770077007700770ULL,0x0770077007700770ULL,
0x0770077007700770ULL,0x0770077007700770ULL,
0x7007700707700770ULL,0x0770077070077007ULL,
0x0770077070077007ULL,0x7007700707700770ULL,
0x0707707007077070ULL,0x0707707007077070ULL,
0x0707707007077070ULL,0x0707707007077070ULL,
0x0077770000777700ULL,0x0077770000777700ULL,
0x0077770000777700ULL,0x0077770000777700ULL,
0x7777777700000000ULL,0x0000000077777777ULL,
0x0000000077777777ULL,0x7777777700000000ULL,
0x7007077070070770ULL,0x0770700707707007ULL,
0x0770700707707007ULL,0x7007077070070770ULL,
0x0707070770707070ULL,0x0707070770707070ULL,
0x0707070770707070ULL,0x0707070770707070ULL,
0x0077007777007700ULL,0x0077007777007700ULL,
0x0077007777007700ULL,0x0077007777007700ULL,
0x7777000077770000ULL,0x0000777700007777ULL,
0x0000777700007777ULL,0x7777000077770000ULL,
0x0000777777770000ULL,0x0000777777770000ULL,
0x0000777777770000ULL,0x0000777777770000ULL,
0x7700770077007700ULL,0x0077007700770077ULL,
0x0077007700770077ULL,0x7700770077007700ULL,
0x7070707070707070ULL,0x0707070707070707ULL,
0x0707070707070707ULL,0x7070707070707070ULL,
0x0770700770070770ULL,0x0770700770070770ULL,
0x0770700770070770ULL,0x0770700770070770ULL
}; 


static const uint_mmv_t TABLE_PERM64_HIGH[] = {
   // %%TABLE TABLE_PERM64_XY_HIGH, uint%{INT_BITS}
0x0000000000000000ULL,0x0000000000000000ULL,
0x0000000000000000ULL,0x0000000000000000ULL,
0x0770700770070770ULL,0x0770700770070770ULL,
0x7007077007707007ULL,0x7007077007707007ULL,
0x0770700770070770ULL,0x7007077007707007ULL,
0x0770700770070770ULL,0x7007077007707007ULL,
0x0000000000000000ULL,0x7777777777777777ULL,
0x7777777777777777ULL,0x0000000000000000ULL,
0x7777777777777777ULL,0x7777777777777777ULL,
0x7777777777777777ULL,0x7777777777777777ULL,
0x7007077007707007ULL,0x7007077007707007ULL,
0x0770700770070770ULL,0x0770700770070770ULL,
0x7007077007707007ULL,0x0770700770070770ULL,
0x7007077007707007ULL,0x0770700770070770ULL,
0x7777777777777777ULL,0x0000000000000000ULL,
0x0000000000000000ULL,0x7777777777777777ULL,
0x0007077707777770ULL,0x7000000700070777ULL,
0x7000000700070777ULL,0x7770700070000007ULL,
0x0777777077707000ULL,0x7770700070000007ULL,
0x0007077707777770ULL,0x0777777077707000ULL,
0x0777777077707000ULL,0x0007077707777770ULL,
0x7770700070000007ULL,0x0777777077707000ULL,
0x0007077707777770ULL,0x0777777077707000ULL,
0x0777777077707000ULL,0x7770700070000007ULL,
0x7770700070000007ULL,0x0777777077707000ULL,
0x0777777077707000ULL,0x0007077707777770ULL,
0x7000000700070777ULL,0x0007077707777770ULL,
0x7770700070000007ULL,0x7000000700070777ULL,
0x7000000700070777ULL,0x7770700070000007ULL,
0x0007077707777770ULL,0x7000000700070777ULL,
0x7770700070000007ULL,0x7000000700070777ULL,
0x7000000700070777ULL,0x0007077707777770ULL
}; 



static const uint32_t TABLE24_START[4] = {
   MM_OP7_OFS_X, MM_OP7_OFS_Z, MM_OP7_OFS_Y
};


/// @endcond





/// @cond DO_NOT_DOCUMENT 

static inline void
op7_do_ABC(uint_mmv_t *v_in, mm_sub_op_xy_type *p_op, uint32_t mode, uint_mmv_t *v_out)
{

    uint_mmv_t mask[8];
    uint_mmv_t neg_mask[2];
    uint_mmv_t f = p_op->f_i, ef = p_op->ef_i, eps;
    uint32_t i;

    mask[0] = f >>  0;
    mask[2] = ef >> 0;
    // %%IF i < V24_INTS_USED - 1 or 24 % INT_FIELDS == 0
    neg_mask[0] = 0x7777777777777777ULL;
    // %%END IF
    mask[1] = f >>  16;
    mask[3] = ef >> 16;
    // %%IF i < V24_INTS_USED - 1 or 24 % INT_FIELDS == 0
    // %%ELSE
    neg_mask[1] = 0x77777777ULL;
    // %%END IF
    for (i = 0; i < 4; ++i) {
        uint_mmv_t x = mask[i];
        // %%MMV_UINT_SPREAD x, x
        // Spread bits 0,...,15 of x to the (4-bit long) fields
        // of x. A field of x is set to 0x7 if its 
        // corresponding bit in input x is one and to 0 otherwise.
        x = (x & 0xffULL) + ((x & 0xff00ULL) << 24);
        x = (x & 0xf0000000fULL) 
            +  ((x & 0xf0000000f0ULL) << 12);
        x = (x & 0x3000300030003ULL) 
            +  ((x & 0xc000c000c000cULL) << 6);
        x = (x & 0x101010101010101ULL) 
            +  ((x & 0x202020202020202ULL) << 3);
        x *= 7;
        // Bit spreading done.
        mask[i] = x = x & neg_mask[i & 1];
        mask[i + 4] = x ^ neg_mask[i & 1];
    }

    f =  p_op->f_i << 2;
    for (i = 0; i < 48; i += 2) {
        uint_mmv_t t, t1;
        // process uint_mmv_t 0 of row i/2 for tag A
        t1 = v_in[i + MM_OP7_OFS_A + 0]; 
        t = mask[0 + (f & 0x4ULL)];
        v_out[i + MM_OP7_OFS_A + 0] = t1 ^ t; 
        // process uint_mmv_t 1 of row i/2 for tag A
        t1 = v_in[i + MM_OP7_OFS_A + 1]; 
        t = mask[1 + (f & 0x4ULL)];
        v_out[i + MM_OP7_OFS_A + 1] = t1 ^ t; 
        f >>= 1;    
    }

    if (mode) return;

    f =  p_op->f_i << 2;
    ef =  p_op->ef_i << 2;
    eps = 0 - ((p_op->eps >> 11) & 0x1ULL);
    for (i = 0; i < 48; i += 2) {
        uint_mmv_t t, t1, t2;
        // %%FOR j in range(V24_INTS_USED)
        // process uint_mmv_t 0 of row i/2 for tags B, C
        t1 = v_in[i + MM_OP7_OFS_B + 0]; 
        t2 = v_in[i + MM_OP7_OFS_C + 0];
        t = mask[0 + (f & 0x4ULL)];
        t &= (t1 ^ t2);
        t ^= mask[2 + (ef & 0x4ULL)];
        v_out[i + MM_OP7_OFS_B + 0] = t1 ^ t;
        t2 ^= eps & neg_mask[0];
        v_out[i + MM_OP7_OFS_C + 0] = t2 ^ t;
        // process uint_mmv_t 1 of row i/2 for tags B, C
        t1 = v_in[i + MM_OP7_OFS_B + 1]; 
        t2 = v_in[i + MM_OP7_OFS_C + 1];
        t = mask[1 + (f & 0x4ULL)];
        t &= (t1 ^ t2);
        t ^= mask[3 + (ef & 0x4ULL)];
        v_out[i + MM_OP7_OFS_B + 1] = t1 ^ t;
        t2 ^= eps & neg_mask[1];
        v_out[i + MM_OP7_OFS_C + 1] = t2 ^ t;
        // %%END FOR
        f >>= 1; ef >>= 1;      
    }
}

/// @endcond 



/// @cond DO_NOT_DOCUMENT 

/**
  @brief Workhorse for function ``mm_op7_xy``

  ``mm_op7_xy(v_in, f, e, eps, v_out)`` is equivalent to

        mm_sub_op_xy_type s_op;  // defined in mm_basics.h
          ... // allocate storage for s_op.sign_XYZ and s_op.p_T
        mm_sub_prep_xy(f, e, eps, &s_op);
        mm_op7_do_xy(v_in, &s_op, v_out);

   So the functions called by function ``mm_op7_xy``
   can be tested individually.
*/
static
void mm_op7_do_xy(uint_mmv_t *v_in, mm_sub_op_xy_type *p_op, uint_mmv_t *v_out)
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
            uint_mmv_t a_sign[2][2];
            uint_mmv_t d_xor = p_op->lin_d[i];
            uint8_t *p_sign = p_op->sign_XYZ;
    
            for (i1 = 0; i1 < 2; ++i1) {
                uint_mmv_t x = p_op->lin_i[i] >> (i1 << 4); 
                // %%MMV_UINT_SPREAD x, x
                // Spread bits 0,...,15 of x to the (4-bit long) fields
                // of x. A field of x is set to 0x7 if its 
                // corresponding bit in input x is one and to 0 otherwise.
                x = (x & 0xffULL) + ((x & 0xff00ULL) << 24);
                x = (x & 0xf0000000fULL) 
                    +  ((x & 0xf0000000f0ULL) << 12);
                x = (x & 0x3000300030003ULL) 
                    +  ((x & 0xc000c000c000cULL) << 6);
                x = (x & 0x101010101010101ULL) 
                    +  ((x & 0x202020202020202ULL) << 3);
                x *= 7;
                // Bit spreading done.
                a_sign[0][i1] = x;
                a_sign[1][i1] = x ^ 0x7777777777777777ULL;
            }
            a_sign[1][1] &= 0x77777777ULL;
         
            for (i1 = 0; i1 < 2048; ++i1) {
                uint_mmv_t *ps = p_src + ((i1 ^ d_xor) << 1);
                uint_fast8_t sign = (p_sign[i1] >> i) & 1;
                // %%FOR j in range(V24_INTS_USED)
                p_dest[0] = ps[0] ^ a_sign[sign][0];
                p_dest[1] = ps[1] ^ a_sign[sign][1];
                // %%END FOR
                p_dest +=  2;      
            }
        }    
    }    

    // Step 2: do rows with 64 entries, tag T // TODO: comment properly!!!!
    {
        uint_mmv_t *p_src = v_in + MM_OP7_OFS_T;
        uint_mmv_t *p_dest = v_out + MM_OP7_OFS_T;
        uint16_t* p_T =  p_op->s_T;
        for (i = 0; i < 759; ++i) {
            uint_fast16_t ofs_l = *p_T;
            uint_fast16_t ofs_h = (ofs_l & 63) >> 4;
            const uint_mmv_t *ps_h = TABLE_PERM64_HIGH +
                ((ofs_l & 0xf000) >> 10);
            const uint_mmv_t *ps_l = TABLE_PERM64_LOW + 
                ((ofs_l & 0xf00) >> 6);
            ofs_l = (ofs_l << 2) & 0x3fULL;
            // %%FOR j in range(V64_INTS)
            p_dest[0] =  ps_h[0] ^ ps_l[0] ^
               (((p_src[0 ^ ofs_h] >> (0 ^ ofs_l)) & 7) << 0) ^
               (((p_src[0 ^ ofs_h] >> (4 ^ ofs_l)) & 7) << 4) ^
               (((p_src[0 ^ ofs_h] >> (8 ^ ofs_l)) & 7) << 8) ^
               (((p_src[0 ^ ofs_h] >> (12 ^ ofs_l)) & 7) << 12) ^
               (((p_src[0 ^ ofs_h] >> (16 ^ ofs_l)) & 7) << 16) ^
               (((p_src[0 ^ ofs_h] >> (20 ^ ofs_l)) & 7) << 20) ^
               (((p_src[0 ^ ofs_h] >> (24 ^ ofs_l)) & 7) << 24) ^
               (((p_src[0 ^ ofs_h] >> (28 ^ ofs_l)) & 7) << 28) ^
               (((p_src[0 ^ ofs_h] >> (32 ^ ofs_l)) & 7) << 32) ^
               (((p_src[0 ^ ofs_h] >> (36 ^ ofs_l)) & 7) << 36) ^
               (((p_src[0 ^ ofs_h] >> (40 ^ ofs_l)) & 7) << 40) ^
               (((p_src[0 ^ ofs_h] >> (44 ^ ofs_l)) & 7) << 44) ^
               (((p_src[0 ^ ofs_h] >> (48 ^ ofs_l)) & 7) << 48) ^
               (((p_src[0 ^ ofs_h] >> (52 ^ ofs_l)) & 7) << 52) ^
               (((p_src[0 ^ ofs_h] >> (56 ^ ofs_l)) & 7) << 56) ^
               (((p_src[0 ^ ofs_h] >> (60 ^ ofs_l)) & 7) << 60);
            p_dest[1] =  ps_h[1] ^ ps_l[1] ^
               (((p_src[1 ^ ofs_h] >> (0 ^ ofs_l)) & 7) << 0) ^
               (((p_src[1 ^ ofs_h] >> (4 ^ ofs_l)) & 7) << 4) ^
               (((p_src[1 ^ ofs_h] >> (8 ^ ofs_l)) & 7) << 8) ^
               (((p_src[1 ^ ofs_h] >> (12 ^ ofs_l)) & 7) << 12) ^
               (((p_src[1 ^ ofs_h] >> (16 ^ ofs_l)) & 7) << 16) ^
               (((p_src[1 ^ ofs_h] >> (20 ^ ofs_l)) & 7) << 20) ^
               (((p_src[1 ^ ofs_h] >> (24 ^ ofs_l)) & 7) << 24) ^
               (((p_src[1 ^ ofs_h] >> (28 ^ ofs_l)) & 7) << 28) ^
               (((p_src[1 ^ ofs_h] >> (32 ^ ofs_l)) & 7) << 32) ^
               (((p_src[1 ^ ofs_h] >> (36 ^ ofs_l)) & 7) << 36) ^
               (((p_src[1 ^ ofs_h] >> (40 ^ ofs_l)) & 7) << 40) ^
               (((p_src[1 ^ ofs_h] >> (44 ^ ofs_l)) & 7) << 44) ^
               (((p_src[1 ^ ofs_h] >> (48 ^ ofs_l)) & 7) << 48) ^
               (((p_src[1 ^ ofs_h] >> (52 ^ ofs_l)) & 7) << 52) ^
               (((p_src[1 ^ ofs_h] >> (56 ^ ofs_l)) & 7) << 56) ^
               (((p_src[1 ^ ofs_h] >> (60 ^ ofs_l)) & 7) << 60);
            p_dest[2] =  ps_h[2] ^ ps_l[2] ^
               (((p_src[2 ^ ofs_h] >> (0 ^ ofs_l)) & 7) << 0) ^
               (((p_src[2 ^ ofs_h] >> (4 ^ ofs_l)) & 7) << 4) ^
               (((p_src[2 ^ ofs_h] >> (8 ^ ofs_l)) & 7) << 8) ^
               (((p_src[2 ^ ofs_h] >> (12 ^ ofs_l)) & 7) << 12) ^
               (((p_src[2 ^ ofs_h] >> (16 ^ ofs_l)) & 7) << 16) ^
               (((p_src[2 ^ ofs_h] >> (20 ^ ofs_l)) & 7) << 20) ^
               (((p_src[2 ^ ofs_h] >> (24 ^ ofs_l)) & 7) << 24) ^
               (((p_src[2 ^ ofs_h] >> (28 ^ ofs_l)) & 7) << 28) ^
               (((p_src[2 ^ ofs_h] >> (32 ^ ofs_l)) & 7) << 32) ^
               (((p_src[2 ^ ofs_h] >> (36 ^ ofs_l)) & 7) << 36) ^
               (((p_src[2 ^ ofs_h] >> (40 ^ ofs_l)) & 7) << 40) ^
               (((p_src[2 ^ ofs_h] >> (44 ^ ofs_l)) & 7) << 44) ^
               (((p_src[2 ^ ofs_h] >> (48 ^ ofs_l)) & 7) << 48) ^
               (((p_src[2 ^ ofs_h] >> (52 ^ ofs_l)) & 7) << 52) ^
               (((p_src[2 ^ ofs_h] >> (56 ^ ofs_l)) & 7) << 56) ^
               (((p_src[2 ^ ofs_h] >> (60 ^ ofs_l)) & 7) << 60);
            p_dest[3] =  ps_h[3] ^ ps_l[3] ^
               (((p_src[3 ^ ofs_h] >> (0 ^ ofs_l)) & 7) << 0) ^
               (((p_src[3 ^ ofs_h] >> (4 ^ ofs_l)) & 7) << 4) ^
               (((p_src[3 ^ ofs_h] >> (8 ^ ofs_l)) & 7) << 8) ^
               (((p_src[3 ^ ofs_h] >> (12 ^ ofs_l)) & 7) << 12) ^
               (((p_src[3 ^ ofs_h] >> (16 ^ ofs_l)) & 7) << 16) ^
               (((p_src[3 ^ ofs_h] >> (20 ^ ofs_l)) & 7) << 20) ^
               (((p_src[3 ^ ofs_h] >> (24 ^ ofs_l)) & 7) << 24) ^
               (((p_src[3 ^ ofs_h] >> (28 ^ ofs_l)) & 7) << 28) ^
               (((p_src[3 ^ ofs_h] >> (32 ^ ofs_l)) & 7) << 32) ^
               (((p_src[3 ^ ofs_h] >> (36 ^ ofs_l)) & 7) << 36) ^
               (((p_src[3 ^ ofs_h] >> (40 ^ ofs_l)) & 7) << 40) ^
               (((p_src[3 ^ ofs_h] >> (44 ^ ofs_l)) & 7) << 44) ^
               (((p_src[3 ^ ofs_h] >> (48 ^ ofs_l)) & 7) << 48) ^
               (((p_src[3 ^ ofs_h] >> (52 ^ ofs_l)) & 7) << 52) ^
               (((p_src[3 ^ ofs_h] >> (56 ^ ofs_l)) & 7) << 56) ^
               (((p_src[3 ^ ofs_h] >> (60 ^ ofs_l)) & 7) << 60);
            // %%END FOR
            p_src += 4; 
            p_dest += 4; 
            ++p_T;
        }
    }


    // Step 3: do rows with 24 entries, tags A, B, C // TODO: comment properly!!!!
    op7_do_ABC(v_in, p_op, 0, v_out);



    // If eps is odd: 
    //    negate entries X_d,i with scalar product <d,i> = 1
    if (p_op->eps & 0x800) mm_op7_neg_scalprod_d_i(v_out + MM_OP7_OFS_X); 
} 


/// @endcond



/**
  @brief Compute an operation of the monster group on a vector

  Let ``v_in`` be a vector of the representation \f$\rho_{7}\f$
  of the monster group.


  The function implements the operation of the element
  \f$y_f \cdot x_e \cdot x_\epsilon\f$ of the monster group
  on a vector ``v_in`` in the representation \f$\rho_{7}\f$ of
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
MM_OP7_API
void mm_op7_xy(uint_mmv_t *v_in, uint32_t f, uint32_t e, uint32_t eps, uint_mmv_t *v_out)
{
    uint16_t s_T[759];
    mm_sub_op_xy_type s_op;
    s_op.sign_XYZ =  (uint8_t*)(v_out + MM_OP7_OFS_T);
    s_op.s_T = s_T;
    mm_sub_prep_xy(f, e, eps, &s_op);
    mm_op7_do_xy(v_in, &s_op, v_out);
}



/**
  @brief Compute an operation of the monster group on a vector

  Let ``v`` be a vector of the representation \f$\rho_{7}\f$
  of the monster group. 

  The function implements the operation of the element
  \f$x_d\f$ of the monster group  on a vector ``v`` in the 
  representation \f$\rho_{7}\f$ of the monster. Here ``d`` must be 
  one of the integers ``0, 0x800, 0x1000``, or ``0x1800``, encoding
  the generators \f$x_1, x_\Omega, x_{-1}\f$, or \f$x_{-\Omega}\f$,
  respectively.
   
  The function computes the operation \f$x_d\f$ on the
  vector ``v`` and overwrites the vector ``v`` with the result.
  The function can  be considered as a simplified (and much faster)
  version of function ``mm_op7_xy``.
*/
// %%EXPORT px
MM_OP7_API
void mm_op7_omega(uint_mmv_t *v, uint32_t d)
// Multiply vector ``v`` with ``x_d`` inplace. Here ``d`` must be
// 0, -1, \Omega or -\Omega.
{
    uint_fast32_t i0, i1, sh;
    uint_mmv_t *pv;
     
    v += MM_OP7_OFS_X;
    d &= 0x1800;
    if (d == 0) return;
    sh = 0x01120200UL >> ((d >> 11) << 3);

    for (i0 = 0; i0 < 8; i0 += 4) {
        pv = v + (((sh >> i0) & 0xf) << (5 + 11 - 4));
        for (i1 = 0; i1 < 2048; ++i1) {
            // %%FOR j in range(V24_INTS_USED)
            pv[0] ^=  0x7777777777777777ULL;
            pv[1] ^=  0x77777777ULL;
            // %%END FOR
            pv +=  2;      
        }
    }
}


/**
  @brief Restriction of function ``mm_op7_xy`` to tag ``A``

  Function ``mm_op7_xy`` computes a certain operation of the
  monster group on a vector ``v_in``. That operation depends
  on parameters ``f, e,`` and ``eps``.
  
  Function ``mm_op7_xy_tag_ABC`` computes the same
  operation on the entries of the vector ``v = v_in`` with
  tag ``A, B, C`` only, and ignores the other entries of ``v``.
  See section **The representation of the monster group**
  in the **API reference** for tags of entries of a vector in
  the representation of the monster.

  The function overwrites the vector ``v`` with the result.
  Here only entries of ``v`` with tag ``A, B, C`` are changed. 
  If parameter ``mode`` is not zero the we update the entries
  with  tag ``A`` only. This function is much faster than
  function ``mm_op7_xy``.
*/
// %%EXPORT px
MM_OP7_API
void mm_op7_xy_tag_ABC(uint_mmv_t *v, uint32_t f, uint32_t e, uint32_t eps, uint32_t mode)
{
    mm_sub_op_xy_type s_op;
    s_op.sign_XYZ = NULL;
    s_op.s_T = NULL;
    mm_sub_prep_xy(f, e, eps, &s_op);
    op7_do_ABC(v, &s_op, mode, v);
}

//  %%GEN h
//  %%GEN c

