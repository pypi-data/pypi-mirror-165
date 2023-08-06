/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////

/** @file mm3_op_xi.c

 File ``mm3_op_xi.c`` implements the operation of the element
 \f$\xi^e\f$ of the monster group on a vector in the
 representation \f$\rho_{3}\f$ of the monster.

 Here the generator \f$\xi\f$ of the monster group is defined as 
 in section **The monster group** of the **API reference**.

 The representation \f$\rho_{3}\f$ is equal to the
 196884-dimensional representation  \f$\rho\f$ of the monster,
 with coefficients taken modulo 3, as defined in
 section **The representation of the monster group**
 in the **API reference**.

 An element of \f$\rho_{3}\f$ is implemented as an array of
 integers of type ``uint_mmv_t`` as described in
 section **Description of the mmgroup.mm extension**
 in this document.

 We have \f$\xi^3 = 1\f$, and the opration of \f$\xi^e, e = 1,2\f$
 on \f$\rho\f$ is given in [Seysen19], section 9.4 - 9.6. The
 non-monomial part of the operation of \f$\xi^e\f$ can be decomposed
 into a product of monomial matrices and matrices containing
 blocks of \f$2 \times 2\f$ Hadamard matrices. We use the Python
 functions and classes in files ``hadamard_codegen.py`` and
 ``hadamard_xi.py`` in subdirectory ``mmgroup/dev/hadamard`` for
 generating C code that implements the products of Hadamard
 matrices corresponding to the generator \f$\xi^e\f$.

 Although the monomial part of the operation of \f$\xi^e\f$ is
 described in [Seysen19], we have not found an easy way to 
 convert that description to a C function. So we use (rather
 large) tables for implementing these operations. The C file
 ``mm_tables_xi.c`` contains these tables as static arrays and
 also an array ``mm_sub_table_xi`` that provides public 
 access to these tables. The same tables are used for the
 operations on \f$\rho_p\f$ for all characteritics \f$p\f$. 
*/

#include <string.h>
#include "mat24_functions.h"
#include "mm_op3.h"   

// %%EXPORT_KWD MM_OP%{P}_API


//  %%GEN h
//  %%GEN c




/// @cond DO_NOT_DOCUMENT 

static void mm_op3_xi_mon(
    uint_mmv_t * v_in,  
    uint32_t exp1, 
    uint_mmv_t * v_out
)
{
    // Caution: this uses v_out[MM_OP3_OFS_Z:] as temporary storage
    uint_mmv_t *p_src, *p_dest;
    uint_fast32_t i, j;
    uint_fast32_t diff = exp1 ? 1024 : 0;
    uint8_t *b =  (uint8_t*)(v_out + MM_OP3_OFS_Z), *p_b;
    mm_sub_table_xi_type *p_tables = mm_sub_table_xi[exp1];
    uint16_t *p_perm;
    uint32_t *p_sign;



    ///////////////////////////////////////////////////////////////
    // Map tag BC to tag BC.
    ///////////////////////////////////////////////////////////////
    p_src = v_in + 24;
    p_dest = v_out + 24;
    p_sign = p_tables[0].p_sign;
    p_perm = p_tables[0].p_perm;

    for (i = 0; i < 1; ++i) {
        p_b = b;
        
        for (j = 0; j < 78; ++j) {
           // %%OP_XI_LOAD p_src, p_b, %{i_src.SHAPE[2]}, uint8_t
           uint_mmv_t r0, r1, r2, r3;
           r0 =  (p_src)[0];
           r1 = (r0 >> 2) & 0x303030303030303ULL;
           r2 = (r0 >> 4) & 0x303030303030303ULL;
           r3 = (r0 >> 6) & 0x303030303030303ULL;
           r0 &= 0x303030303030303ULL;
           (p_b)[0] = (uint8_t)(r0 >> 0);
           (p_b)[1] = (uint8_t)(r1 >> 0);
           (p_b)[2] = (uint8_t)(r2 >> 0);
           (p_b)[3] = (uint8_t)(r3 >> 0);
           (p_b)[4] = (uint8_t)(r0 >> 8);
           (p_b)[5] = (uint8_t)(r1 >> 8);
           (p_b)[6] = (uint8_t)(r2 >> 8);
           (p_b)[7] = (uint8_t)(r3 >> 8);
           (p_b)[8] = (uint8_t)(r0 >> 16);
           (p_b)[9] = (uint8_t)(r1 >> 16);
           (p_b)[10] = (uint8_t)(r2 >> 16);
           (p_b)[11] = (uint8_t)(r3 >> 16);
           (p_b)[12] = (uint8_t)(r0 >> 24);
           (p_b)[13] = (uint8_t)(r1 >> 24);
           (p_b)[14] = (uint8_t)(r2 >> 24);
           (p_b)[15] = (uint8_t)(r3 >> 24);
           (p_b)[16] = (uint8_t)(r0 >> 32);
           (p_b)[17] = (uint8_t)(r1 >> 32);
           (p_b)[18] = (uint8_t)(r2 >> 32);
           (p_b)[19] = (uint8_t)(r3 >> 32);
           (p_b)[20] = (uint8_t)(r0 >> 40);
           (p_b)[21] = (uint8_t)(r1 >> 40);
           (p_b)[22] = (uint8_t)(r2 >> 40);
           (p_b)[23] = (uint8_t)(r3 >> 40);
           (p_b)[24] = (uint8_t)(r0 >> 48);
           (p_b)[25] = (uint8_t)(r1 >> 48);
           (p_b)[26] = (uint8_t)(r2 >> 48);
           (p_b)[27] = (uint8_t)(r3 >> 48);
           (p_b)[28] = (uint8_t)(r0 >> 56);
           (p_b)[29] = (uint8_t)(r1 >> 56);
           (p_b)[30] = (uint8_t)(r2 >> 56);
           (p_b)[31] = (uint8_t)(r3 >> 56);
           p_src += 1;
           p_b += 32;
        }
        
        for (j = 0; j < 78; ++j) {
           // %%OP_XI_STORE b, p_perm, p_sign, p_dest, %{i_dest.SHAPE[2]}
           uint_mmv_t r0, r1;
           r0 = ((uint_mmv_t)(b[p_perm[0]]) << 0)
             + ((uint_mmv_t)(b[p_perm[1]]) << 2)
             + ((uint_mmv_t)(b[p_perm[2]]) << 4)
             + ((uint_mmv_t)(b[p_perm[3]]) << 6)
             + ((uint_mmv_t)(b[p_perm[4]]) << 8)
             + ((uint_mmv_t)(b[p_perm[5]]) << 10)
             + ((uint_mmv_t)(b[p_perm[6]]) << 12)
             + ((uint_mmv_t)(b[p_perm[7]]) << 14)
             + ((uint_mmv_t)(b[p_perm[8]]) << 16)
             + ((uint_mmv_t)(b[p_perm[9]]) << 18)
             + ((uint_mmv_t)(b[p_perm[10]]) << 20)
             + ((uint_mmv_t)(b[p_perm[11]]) << 22)
             + ((uint_mmv_t)(b[p_perm[12]]) << 24)
             + ((uint_mmv_t)(b[p_perm[13]]) << 26)
             + ((uint_mmv_t)(b[p_perm[14]]) << 28)
             + ((uint_mmv_t)(b[p_perm[15]]) << 30)
             + ((uint_mmv_t)(b[p_perm[16]]) << 32)
             + ((uint_mmv_t)(b[p_perm[17]]) << 34)
             + ((uint_mmv_t)(b[p_perm[18]]) << 36)
             + ((uint_mmv_t)(b[p_perm[19]]) << 38)
             + ((uint_mmv_t)(b[p_perm[20]]) << 40)
             + ((uint_mmv_t)(b[p_perm[21]]) << 42)
             + ((uint_mmv_t)(b[p_perm[22]]) << 44)
             + ((uint_mmv_t)(b[p_perm[23]]) << 46)
             + ((uint_mmv_t)(b[p_perm[24]]) << 48)
             + ((uint_mmv_t)(b[p_perm[25]]) << 50)
             + ((uint_mmv_t)(b[p_perm[26]]) << 52)
             + ((uint_mmv_t)(b[p_perm[27]]) << 54)
             + ((uint_mmv_t)(b[p_perm[28]]) << 56)
             + ((uint_mmv_t)(b[p_perm[29]]) << 58)
             + ((uint_mmv_t)(b[p_perm[30]]) << 60)
             + ((uint_mmv_t)(b[p_perm[31]]) << 62);
           r1 = (p_sign)[0] >> 0;
           // Spread bits 0,...,31 of r1 to the (2-bit long) fields
           // of r1. A field of r1 is set to 0x3 if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xffffULL) 
               +  ((r1 & 0xffff0000ULL) << 16);
           r1 = (r1 & 0xff000000ffULL) 
               +  ((r1 & 0xff000000ff00ULL) << 8);
           r1 = (r1 & 0xf000f000f000fULL) 
               +  ((r1 & 0xf000f000f000f0ULL) << 4);
           r1 = (r1 & 0x303030303030303ULL) 
               +  ((r1 & 0xc0c0c0c0c0c0c0cULL) << 2);
           r1 = (r1 & 0x1111111111111111ULL) 
               +  ((r1 & 0x2222222222222222ULL) << 1);
           r1 *= 3;
           // Bit spreading done.
           (p_dest)[0] = r0 ^ r1;
           p_dest += 1;
           p_perm += 32;
           p_sign += 1;
        }
        
    }

    ///////////////////////////////////////////////////////////////
    // Map tag T0 to tag T0.
    ///////////////////////////////////////////////////////////////
    p_src = v_in + 102;
    p_dest = v_out + 102;
    p_sign = p_tables[1].p_sign;
    p_perm = p_tables[1].p_perm;

    for (i = 0; i < 45; ++i) {
        p_b = b;
        
        for (j = 0; j < 16; ++j) {
           // %%OP_XI_LOAD p_src, p_b, %{i_src.SHAPE[2]}, uint8_t
           uint_mmv_t r0, r1, r2, r3;
           r0 =  (p_src)[0];
           r1 = (r0 >> 2) & 0x303030303030303ULL;
           r2 = (r0 >> 4) & 0x303030303030303ULL;
           r3 = (r0 >> 6) & 0x303030303030303ULL;
           r0 &= 0x303030303030303ULL;
           (p_b)[0] = (uint8_t)(r0 >> 0);
           (p_b)[1] = (uint8_t)(r1 >> 0);
           (p_b)[2] = (uint8_t)(r2 >> 0);
           (p_b)[3] = (uint8_t)(r3 >> 0);
           (p_b)[4] = (uint8_t)(r0 >> 8);
           (p_b)[5] = (uint8_t)(r1 >> 8);
           (p_b)[6] = (uint8_t)(r2 >> 8);
           (p_b)[7] = (uint8_t)(r3 >> 8);
           (p_b)[8] = (uint8_t)(r0 >> 16);
           (p_b)[9] = (uint8_t)(r1 >> 16);
           (p_b)[10] = (uint8_t)(r2 >> 16);
           (p_b)[11] = (uint8_t)(r3 >> 16);
           (p_b)[12] = (uint8_t)(r0 >> 24);
           (p_b)[13] = (uint8_t)(r1 >> 24);
           (p_b)[14] = (uint8_t)(r2 >> 24);
           (p_b)[15] = (uint8_t)(r3 >> 24);
           (p_b)[16] = (uint8_t)(r0 >> 32);
           (p_b)[17] = (uint8_t)(r1 >> 32);
           (p_b)[18] = (uint8_t)(r2 >> 32);
           (p_b)[19] = (uint8_t)(r3 >> 32);
           (p_b)[20] = (uint8_t)(r0 >> 40);
           (p_b)[21] = (uint8_t)(r1 >> 40);
           (p_b)[22] = (uint8_t)(r2 >> 40);
           (p_b)[23] = (uint8_t)(r3 >> 40);
           (p_b)[24] = (uint8_t)(r0 >> 48);
           (p_b)[25] = (uint8_t)(r1 >> 48);
           (p_b)[26] = (uint8_t)(r2 >> 48);
           (p_b)[27] = (uint8_t)(r3 >> 48);
           (p_b)[28] = (uint8_t)(r0 >> 56);
           (p_b)[29] = (uint8_t)(r1 >> 56);
           (p_b)[30] = (uint8_t)(r2 >> 56);
           (p_b)[31] = (uint8_t)(r3 >> 56);
           p_src += 1;
           p_b += 32;
        }
        
        for (j = 0; j < 16; ++j) {
           // %%OP_XI_STORE b, p_perm, p_sign, p_dest, %{i_dest.SHAPE[2]}
           uint_mmv_t r0, r1;
           r0 = ((uint_mmv_t)(b[p_perm[0]]) << 0)
             + ((uint_mmv_t)(b[p_perm[1]]) << 2)
             + ((uint_mmv_t)(b[p_perm[2]]) << 4)
             + ((uint_mmv_t)(b[p_perm[3]]) << 6)
             + ((uint_mmv_t)(b[p_perm[4]]) << 8)
             + ((uint_mmv_t)(b[p_perm[5]]) << 10)
             + ((uint_mmv_t)(b[p_perm[6]]) << 12)
             + ((uint_mmv_t)(b[p_perm[7]]) << 14)
             + ((uint_mmv_t)(b[p_perm[8]]) << 16)
             + ((uint_mmv_t)(b[p_perm[9]]) << 18)
             + ((uint_mmv_t)(b[p_perm[10]]) << 20)
             + ((uint_mmv_t)(b[p_perm[11]]) << 22)
             + ((uint_mmv_t)(b[p_perm[12]]) << 24)
             + ((uint_mmv_t)(b[p_perm[13]]) << 26)
             + ((uint_mmv_t)(b[p_perm[14]]) << 28)
             + ((uint_mmv_t)(b[p_perm[15]]) << 30)
             + ((uint_mmv_t)(b[p_perm[16]]) << 32)
             + ((uint_mmv_t)(b[p_perm[17]]) << 34)
             + ((uint_mmv_t)(b[p_perm[18]]) << 36)
             + ((uint_mmv_t)(b[p_perm[19]]) << 38)
             + ((uint_mmv_t)(b[p_perm[20]]) << 40)
             + ((uint_mmv_t)(b[p_perm[21]]) << 42)
             + ((uint_mmv_t)(b[p_perm[22]]) << 44)
             + ((uint_mmv_t)(b[p_perm[23]]) << 46)
             + ((uint_mmv_t)(b[p_perm[24]]) << 48)
             + ((uint_mmv_t)(b[p_perm[25]]) << 50)
             + ((uint_mmv_t)(b[p_perm[26]]) << 52)
             + ((uint_mmv_t)(b[p_perm[27]]) << 54)
             + ((uint_mmv_t)(b[p_perm[28]]) << 56)
             + ((uint_mmv_t)(b[p_perm[29]]) << 58)
             + ((uint_mmv_t)(b[p_perm[30]]) << 60)
             + ((uint_mmv_t)(b[p_perm[31]]) << 62);
           r1 = (p_sign)[0] >> 0;
           // Spread bits 0,...,31 of r1 to the (2-bit long) fields
           // of r1. A field of r1 is set to 0x3 if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xffffULL) 
               +  ((r1 & 0xffff0000ULL) << 16);
           r1 = (r1 & 0xff000000ffULL) 
               +  ((r1 & 0xff000000ff00ULL) << 8);
           r1 = (r1 & 0xf000f000f000fULL) 
               +  ((r1 & 0xf000f000f000f0ULL) << 4);
           r1 = (r1 & 0x303030303030303ULL) 
               +  ((r1 & 0xc0c0c0c0c0c0c0cULL) << 2);
           r1 = (r1 & 0x1111111111111111ULL) 
               +  ((r1 & 0x2222222222222222ULL) << 1);
           r1 *= 3;
           // Bit spreading done.
           (p_dest)[0] = r0 ^ r1;
           p_dest += 1;
           p_perm += 32;
           p_sign += 1;
        }
        
    }

    ///////////////////////////////////////////////////////////////
    // Map tag T1 to tag X0 if e = 1
    // Map tag T1 to tag X1 if e = 2
    ///////////////////////////////////////////////////////////////
    p_src = v_in + 822;
    p_dest = v_out + 1590;
    p_dest += diff;
    p_sign = p_tables[2].p_sign;
    p_perm = p_tables[2].p_perm;

    for (i = 0; i < 64; ++i) {
        p_b = b;
        
        for (j = 0; j < 12; ++j) {
           // %%OP_XI_LOAD p_src, p_b, %{i_src.SHAPE[2]}, uint8_t
           uint_mmv_t r0, r1, r2, r3;
           r0 =  (p_src)[0];
           r1 = (r0 >> 2) & 0x303030303030303ULL;
           r2 = (r0 >> 4) & 0x303030303030303ULL;
           r3 = (r0 >> 6) & 0x303030303030303ULL;
           r0 &= 0x303030303030303ULL;
           (p_b)[0] = (uint8_t)(r0 >> 0);
           (p_b)[1] = (uint8_t)(r1 >> 0);
           (p_b)[2] = (uint8_t)(r2 >> 0);
           (p_b)[3] = (uint8_t)(r3 >> 0);
           (p_b)[4] = (uint8_t)(r0 >> 8);
           (p_b)[5] = (uint8_t)(r1 >> 8);
           (p_b)[6] = (uint8_t)(r2 >> 8);
           (p_b)[7] = (uint8_t)(r3 >> 8);
           (p_b)[8] = (uint8_t)(r0 >> 16);
           (p_b)[9] = (uint8_t)(r1 >> 16);
           (p_b)[10] = (uint8_t)(r2 >> 16);
           (p_b)[11] = (uint8_t)(r3 >> 16);
           (p_b)[12] = (uint8_t)(r0 >> 24);
           (p_b)[13] = (uint8_t)(r1 >> 24);
           (p_b)[14] = (uint8_t)(r2 >> 24);
           (p_b)[15] = (uint8_t)(r3 >> 24);
           (p_b)[16] = (uint8_t)(r0 >> 32);
           (p_b)[17] = (uint8_t)(r1 >> 32);
           (p_b)[18] = (uint8_t)(r2 >> 32);
           (p_b)[19] = (uint8_t)(r3 >> 32);
           (p_b)[20] = (uint8_t)(r0 >> 40);
           (p_b)[21] = (uint8_t)(r1 >> 40);
           (p_b)[22] = (uint8_t)(r2 >> 40);
           (p_b)[23] = (uint8_t)(r3 >> 40);
           (p_b)[24] = (uint8_t)(r0 >> 48);
           (p_b)[25] = (uint8_t)(r1 >> 48);
           (p_b)[26] = (uint8_t)(r2 >> 48);
           (p_b)[27] = (uint8_t)(r3 >> 48);
           (p_b)[28] = (uint8_t)(r0 >> 56);
           (p_b)[29] = (uint8_t)(r1 >> 56);
           (p_b)[30] = (uint8_t)(r2 >> 56);
           (p_b)[31] = (uint8_t)(r3 >> 56);
           p_src += 1;
           p_b += 32;
        }
        
        for (j = 0; j < 16; ++j) {
           // %%OP_XI_STORE b, p_perm, p_sign, p_dest, %{i_dest.SHAPE[2]}
           uint_mmv_t r0, r1;
           r0 = ((uint_mmv_t)(b[p_perm[0]]) << 0)
             + ((uint_mmv_t)(b[p_perm[1]]) << 2)
             + ((uint_mmv_t)(b[p_perm[2]]) << 4)
             + ((uint_mmv_t)(b[p_perm[3]]) << 6)
             + ((uint_mmv_t)(b[p_perm[4]]) << 8)
             + ((uint_mmv_t)(b[p_perm[5]]) << 10)
             + ((uint_mmv_t)(b[p_perm[6]]) << 12)
             + ((uint_mmv_t)(b[p_perm[7]]) << 14)
             + ((uint_mmv_t)(b[p_perm[8]]) << 16)
             + ((uint_mmv_t)(b[p_perm[9]]) << 18)
             + ((uint_mmv_t)(b[p_perm[10]]) << 20)
             + ((uint_mmv_t)(b[p_perm[11]]) << 22)
             + ((uint_mmv_t)(b[p_perm[12]]) << 24)
             + ((uint_mmv_t)(b[p_perm[13]]) << 26)
             + ((uint_mmv_t)(b[p_perm[14]]) << 28)
             + ((uint_mmv_t)(b[p_perm[15]]) << 30)
             + ((uint_mmv_t)(b[p_perm[16]]) << 32)
             + ((uint_mmv_t)(b[p_perm[17]]) << 34)
             + ((uint_mmv_t)(b[p_perm[18]]) << 36)
             + ((uint_mmv_t)(b[p_perm[19]]) << 38)
             + ((uint_mmv_t)(b[p_perm[20]]) << 40)
             + ((uint_mmv_t)(b[p_perm[21]]) << 42)
             + ((uint_mmv_t)(b[p_perm[22]]) << 44)
             + ((uint_mmv_t)(b[p_perm[23]]) << 46);
           r1 = (p_sign)[0] >> 0;
           // Spread bits 0,...,31 of r1 to the (2-bit long) fields
           // of r1. A field of r1 is set to 0x3 if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xffffULL) 
               +  ((r1 & 0xffff0000ULL) << 16);
           r1 = (r1 & 0xff000000ffULL) 
               +  ((r1 & 0xff000000ff00ULL) << 8);
           r1 = (r1 & 0xf000f000f000fULL) 
               +  ((r1 & 0xf000f000f000f0ULL) << 4);
           r1 = (r1 & 0x303030303030303ULL) 
               +  ((r1 & 0xc0c0c0c0c0c0c0cULL) << 2);
           r1 = (r1 & 0x1111111111111111ULL) 
               +  ((r1 & 0x2222222222222222ULL) << 1);
           r1 *= 3;
           // Bit spreading done.
           (p_dest)[0] = r0 ^ r1;
           p_dest += 1;
           p_perm += 24;
           p_sign += 1;
        }
        
    }

    ///////////////////////////////////////////////////////////////
    // Map tag X0 to tag X1 if e = 1
    // Map tag X1 to tag X0 if e = 2
    ///////////////////////////////////////////////////////////////
    p_src = v_in + 1590;
    p_src += diff;
    p_dest = v_out + 2614;
    p_dest -= diff;
    p_sign = p_tables[3].p_sign;
    p_perm = p_tables[3].p_perm;

    for (i = 0; i < 64; ++i) {
        p_b = b;
        
        for (j = 0; j < 16; ++j) {
           // %%OP_XI_LOAD p_src, p_b, %{i_src.SHAPE[2]}, uint8_t
           uint_mmv_t r0, r1, r2, r3;
           r0 =  (p_src)[0];
           r1 = (r0 >> 2) & 0x303030303030303ULL;
           r2 = (r0 >> 4) & 0x303030303030303ULL;
           r3 = (r0 >> 6) & 0x303030303030303ULL;
           r0 &= 0x303030303030303ULL;
           (p_b)[0] = (uint8_t)(r0 >> 0);
           (p_b)[1] = (uint8_t)(r1 >> 0);
           (p_b)[2] = (uint8_t)(r2 >> 0);
           (p_b)[3] = (uint8_t)(r3 >> 0);
           (p_b)[4] = (uint8_t)(r0 >> 8);
           (p_b)[5] = (uint8_t)(r1 >> 8);
           (p_b)[6] = (uint8_t)(r2 >> 8);
           (p_b)[7] = (uint8_t)(r3 >> 8);
           (p_b)[8] = (uint8_t)(r0 >> 16);
           (p_b)[9] = (uint8_t)(r1 >> 16);
           (p_b)[10] = (uint8_t)(r2 >> 16);
           (p_b)[11] = (uint8_t)(r3 >> 16);
           (p_b)[12] = (uint8_t)(r0 >> 24);
           (p_b)[13] = (uint8_t)(r1 >> 24);
           (p_b)[14] = (uint8_t)(r2 >> 24);
           (p_b)[15] = (uint8_t)(r3 >> 24);
           (p_b)[16] = (uint8_t)(r0 >> 32);
           (p_b)[17] = (uint8_t)(r1 >> 32);
           (p_b)[18] = (uint8_t)(r2 >> 32);
           (p_b)[19] = (uint8_t)(r3 >> 32);
           (p_b)[20] = (uint8_t)(r0 >> 40);
           (p_b)[21] = (uint8_t)(r1 >> 40);
           (p_b)[22] = (uint8_t)(r2 >> 40);
           (p_b)[23] = (uint8_t)(r3 >> 40);
           p_src += 1;
           p_b += 32;
        }
        
        for (j = 0; j < 16; ++j) {
           // %%OP_XI_STORE b, p_perm, p_sign, p_dest, %{i_dest.SHAPE[2]}
           uint_mmv_t r0, r1;
           r0 = ((uint_mmv_t)(b[p_perm[0]]) << 0)
             + ((uint_mmv_t)(b[p_perm[1]]) << 2)
             + ((uint_mmv_t)(b[p_perm[2]]) << 4)
             + ((uint_mmv_t)(b[p_perm[3]]) << 6)
             + ((uint_mmv_t)(b[p_perm[4]]) << 8)
             + ((uint_mmv_t)(b[p_perm[5]]) << 10)
             + ((uint_mmv_t)(b[p_perm[6]]) << 12)
             + ((uint_mmv_t)(b[p_perm[7]]) << 14)
             + ((uint_mmv_t)(b[p_perm[8]]) << 16)
             + ((uint_mmv_t)(b[p_perm[9]]) << 18)
             + ((uint_mmv_t)(b[p_perm[10]]) << 20)
             + ((uint_mmv_t)(b[p_perm[11]]) << 22)
             + ((uint_mmv_t)(b[p_perm[12]]) << 24)
             + ((uint_mmv_t)(b[p_perm[13]]) << 26)
             + ((uint_mmv_t)(b[p_perm[14]]) << 28)
             + ((uint_mmv_t)(b[p_perm[15]]) << 30)
             + ((uint_mmv_t)(b[p_perm[16]]) << 32)
             + ((uint_mmv_t)(b[p_perm[17]]) << 34)
             + ((uint_mmv_t)(b[p_perm[18]]) << 36)
             + ((uint_mmv_t)(b[p_perm[19]]) << 38)
             + ((uint_mmv_t)(b[p_perm[20]]) << 40)
             + ((uint_mmv_t)(b[p_perm[21]]) << 42)
             + ((uint_mmv_t)(b[p_perm[22]]) << 44)
             + ((uint_mmv_t)(b[p_perm[23]]) << 46);
           r1 = (p_sign)[0] >> 0;
           // Spread bits 0,...,31 of r1 to the (2-bit long) fields
           // of r1. A field of r1 is set to 0x3 if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xffffULL) 
               +  ((r1 & 0xffff0000ULL) << 16);
           r1 = (r1 & 0xff000000ffULL) 
               +  ((r1 & 0xff000000ff00ULL) << 8);
           r1 = (r1 & 0xf000f000f000fULL) 
               +  ((r1 & 0xf000f000f000f0ULL) << 4);
           r1 = (r1 & 0x303030303030303ULL) 
               +  ((r1 & 0xc0c0c0c0c0c0c0cULL) << 2);
           r1 = (r1 & 0x1111111111111111ULL) 
               +  ((r1 & 0x2222222222222222ULL) << 1);
           r1 *= 3;
           // Bit spreading done.
           (p_dest)[0] = r0 ^ r1;
           p_dest += 1;
           p_perm += 24;
           p_sign += 1;
        }
        
    }

    ///////////////////////////////////////////////////////////////
    // Map tag X1 to tag T1 if e = 1
    // Map tag X0 to tag T1 if e = 2
    ///////////////////////////////////////////////////////////////
    p_src = v_in + 2614;
    p_src -= diff;
    p_dest = v_out + 822;
    p_sign = p_tables[4].p_sign;
    p_perm = p_tables[4].p_perm;

    for (i = 0; i < 64; ++i) {
        p_b = b;
        
        for (j = 0; j < 16; ++j) {
           // %%OP_XI_LOAD p_src, p_b, %{i_src.SHAPE[2]}, uint8_t
           uint_mmv_t r0, r1, r2, r3;
           r0 =  (p_src)[0];
           r1 = (r0 >> 2) & 0x303030303030303ULL;
           r2 = (r0 >> 4) & 0x303030303030303ULL;
           r3 = (r0 >> 6) & 0x303030303030303ULL;
           r0 &= 0x303030303030303ULL;
           (p_b)[0] = (uint8_t)(r0 >> 0);
           (p_b)[1] = (uint8_t)(r1 >> 0);
           (p_b)[2] = (uint8_t)(r2 >> 0);
           (p_b)[3] = (uint8_t)(r3 >> 0);
           (p_b)[4] = (uint8_t)(r0 >> 8);
           (p_b)[5] = (uint8_t)(r1 >> 8);
           (p_b)[6] = (uint8_t)(r2 >> 8);
           (p_b)[7] = (uint8_t)(r3 >> 8);
           (p_b)[8] = (uint8_t)(r0 >> 16);
           (p_b)[9] = (uint8_t)(r1 >> 16);
           (p_b)[10] = (uint8_t)(r2 >> 16);
           (p_b)[11] = (uint8_t)(r3 >> 16);
           (p_b)[12] = (uint8_t)(r0 >> 24);
           (p_b)[13] = (uint8_t)(r1 >> 24);
           (p_b)[14] = (uint8_t)(r2 >> 24);
           (p_b)[15] = (uint8_t)(r3 >> 24);
           (p_b)[16] = (uint8_t)(r0 >> 32);
           (p_b)[17] = (uint8_t)(r1 >> 32);
           (p_b)[18] = (uint8_t)(r2 >> 32);
           (p_b)[19] = (uint8_t)(r3 >> 32);
           (p_b)[20] = (uint8_t)(r0 >> 40);
           (p_b)[21] = (uint8_t)(r1 >> 40);
           (p_b)[22] = (uint8_t)(r2 >> 40);
           (p_b)[23] = (uint8_t)(r3 >> 40);
           p_src += 1;
           p_b += 32;
        }
        
        for (j = 0; j < 12; ++j) {
           // %%OP_XI_STORE b, p_perm, p_sign, p_dest, %{i_dest.SHAPE[2]}
           uint_mmv_t r0, r1;
           r0 = ((uint_mmv_t)(b[p_perm[0]]) << 0)
             + ((uint_mmv_t)(b[p_perm[1]]) << 2)
             + ((uint_mmv_t)(b[p_perm[2]]) << 4)
             + ((uint_mmv_t)(b[p_perm[3]]) << 6)
             + ((uint_mmv_t)(b[p_perm[4]]) << 8)
             + ((uint_mmv_t)(b[p_perm[5]]) << 10)
             + ((uint_mmv_t)(b[p_perm[6]]) << 12)
             + ((uint_mmv_t)(b[p_perm[7]]) << 14)
             + ((uint_mmv_t)(b[p_perm[8]]) << 16)
             + ((uint_mmv_t)(b[p_perm[9]]) << 18)
             + ((uint_mmv_t)(b[p_perm[10]]) << 20)
             + ((uint_mmv_t)(b[p_perm[11]]) << 22)
             + ((uint_mmv_t)(b[p_perm[12]]) << 24)
             + ((uint_mmv_t)(b[p_perm[13]]) << 26)
             + ((uint_mmv_t)(b[p_perm[14]]) << 28)
             + ((uint_mmv_t)(b[p_perm[15]]) << 30)
             + ((uint_mmv_t)(b[p_perm[16]]) << 32)
             + ((uint_mmv_t)(b[p_perm[17]]) << 34)
             + ((uint_mmv_t)(b[p_perm[18]]) << 36)
             + ((uint_mmv_t)(b[p_perm[19]]) << 38)
             + ((uint_mmv_t)(b[p_perm[20]]) << 40)
             + ((uint_mmv_t)(b[p_perm[21]]) << 42)
             + ((uint_mmv_t)(b[p_perm[22]]) << 44)
             + ((uint_mmv_t)(b[p_perm[23]]) << 46)
             + ((uint_mmv_t)(b[p_perm[24]]) << 48)
             + ((uint_mmv_t)(b[p_perm[25]]) << 50)
             + ((uint_mmv_t)(b[p_perm[26]]) << 52)
             + ((uint_mmv_t)(b[p_perm[27]]) << 54)
             + ((uint_mmv_t)(b[p_perm[28]]) << 56)
             + ((uint_mmv_t)(b[p_perm[29]]) << 58)
             + ((uint_mmv_t)(b[p_perm[30]]) << 60)
             + ((uint_mmv_t)(b[p_perm[31]]) << 62);
           r1 = (p_sign)[0] >> 0;
           // Spread bits 0,...,31 of r1 to the (2-bit long) fields
           // of r1. A field of r1 is set to 0x3 if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xffffULL) 
               +  ((r1 & 0xffff0000ULL) << 16);
           r1 = (r1 & 0xff000000ffULL) 
               +  ((r1 & 0xff000000ff00ULL) << 8);
           r1 = (r1 & 0xf000f000f000fULL) 
               +  ((r1 & 0xf000f000f000f0ULL) << 4);
           r1 = (r1 & 0x303030303030303ULL) 
               +  ((r1 & 0xc0c0c0c0c0c0c0cULL) << 2);
           r1 = (r1 & 0x1111111111111111ULL) 
               +  ((r1 & 0x2222222222222222ULL) << 1);
           r1 *= 3;
           // Bit spreading done.
           (p_dest)[0] = r0 ^ r1;
           p_dest += 1;
           p_perm += 32;
           p_sign += 1;
        }
        
    }
}

static uint_mmv_t TAB3_XI64_MASK[] = {
// %%TABLE TABLE_MUL_MATRIX_XI64, uint%{INT_BITS}
0x0000030303030303ULL,0x0000000000000000ULL,
0x0000030303030303ULL,0x0000ffffffffffffULL,
0x0000000000000000ULL,0x0000030303030303ULL,
0x0000ffffffffffffULL,0x0000030303030303ULL
};


#define HALF_YZ_SHIFT 10

static uint32_t TAB3_XI64_OFFSET[2][4] = {
    {
        MM_OP3_OFS_Z + (2 << HALF_YZ_SHIFT),
        MM_OP3_OFS_Z + (0 << HALF_YZ_SHIFT),
        MM_OP3_OFS_Z + (1 << HALF_YZ_SHIFT),
        MM_OP3_OFS_Z + (3 << HALF_YZ_SHIFT)
    },
    {
        MM_OP3_OFS_Z + (1 << HALF_YZ_SHIFT),
        MM_OP3_OFS_Z + (2 << HALF_YZ_SHIFT),
        MM_OP3_OFS_Z + (0 << HALF_YZ_SHIFT),
        MM_OP3_OFS_Z + (3 << HALF_YZ_SHIFT)
    },
};




static void mm_op3_xi_yz(uint_mmv_t *v_in,  uint32_t exp1, uint_mmv_t *v_out)
{
    uint_fast32_t i1;
    uint_mmv_t *p_mask =  TAB3_XI64_MASK + exp1;
    for (i1 = 0; i1 < 64; ++i1) {
        // %%MUL_MATRIX_XI64 v_in, p_mask, v_out

        // This is an automatically generated matrix operation, do not change!
        {
        uint_mmv_t r0, r1, r2, r3, r4;
        uint_mmv_t r5, r6, r7, r8, r9;
        uint_mmv_t r10, r11, r12, r13, r14;
        uint_mmv_t r15, r16, r17;

        r0 = v_in[0] ^  p_mask[2];
        r16 = ((r0 ^ (r0 >> 2)) & 0xc0c0c0c0c0cULL); // 3 ops
        r0 ^= (r16 | (r16 << 2)); // 3 ops
        r1 = v_in[14] ^  p_mask[0];
        r16 = ((r1 ^ (r1 >> 2)) & 0xc0c0c0c0c0cULL); // 3 ops
        r1 ^= (r16 | (r16 << 2)); // 3 ops
        r2 = v_in[13] ^  p_mask[0];
        r16 = ((r2 ^ (r2 >> 2)) & 0xc0c0c0c0c0cULL); // 3 ops
        r2 ^= (r16 | (r16 << 2)); // 3 ops
        r3 = v_in[3] ^  p_mask[0];
        r16 = ((r3 ^ (r3 >> 2)) & 0xc0c0c0c0c0cULL); // 3 ops
        r3 ^= (r16 | (r16 << 2)); // 3 ops
        r4 = v_in[11] ^  p_mask[0];
        r16 = ((r4 ^ (r4 >> 2)) & 0xc0c0c0c0c0cULL); // 3 ops
        r4 ^= (r16 | (r16 << 2)); // 3 ops
        r5 = v_in[5] ^  p_mask[0];
        r16 = ((r5 ^ (r5 >> 2)) & 0xc0c0c0c0c0cULL); // 3 ops
        r5 ^= (r16 | (r16 << 2)); // 3 ops
        r6 = v_in[6] ^  p_mask[0];
        r16 = ((r6 ^ (r6 >> 2)) & 0xc0c0c0c0c0cULL); // 3 ops
        r6 ^= (r16 | (r16 << 2)); // 3 ops
        r7 = v_in[8] ^  p_mask[2];
        r16 = ((r7 ^ (r7 >> 2)) & 0xc0c0c0c0c0cULL); // 3 ops
        r7 ^= (r16 | (r16 << 2)); // 3 ops
        r8 = v_in[7] ^  p_mask[0];
        r16 = ((r8 ^ (r8 >> 2)) & 0xc0c0c0c0c0cULL); // 3 ops
        r8 ^= (r16 | (r16 << 2)); // 3 ops
        r9 = v_in[9] ^  p_mask[0];
        r16 = ((r9 ^ (r9 >> 2)) & 0xc0c0c0c0c0cULL); // 3 ops
        r9 ^= (r16 | (r16 << 2)); // 3 ops
        r10 = v_in[10] ^  p_mask[0];
        r16 = ((r10 ^ (r10 >> 2)) & 0xc0c0c0c0c0cULL); // 3 ops
        r10 ^= (r16 | (r16 << 2)); // 3 ops
        r11 = v_in[4] ^  p_mask[2];
        r16 = ((r11 ^ (r11 >> 2)) & 0xc0c0c0c0c0cULL); // 3 ops
        r11 ^= (r16 | (r16 << 2)); // 3 ops
        r12 = v_in[12] ^  p_mask[0];
        r16 = ((r12 ^ (r12 >> 2)) & 0xc0c0c0c0c0cULL); // 3 ops
        r12 ^= (r16 | (r16 << 2)); // 3 ops
        r13 = v_in[2] ^  p_mask[2];
        r16 = ((r13 ^ (r13 >> 2)) & 0xc0c0c0c0c0cULL); // 3 ops
        r13 ^= (r16 | (r16 << 2)); // 3 ops
        r14 = v_in[1] ^  p_mask[2];
        r16 = ((r14 ^ (r14 >> 2)) & 0xc0c0c0c0c0cULL); // 3 ops
        r14 ^= (r16 | (r16 << 2)); // 3 ops
        r15 = v_in[15] ^  p_mask[2];
        r16 = ((r15 ^ (r15 >> 2)) & 0xc0c0c0c0c0cULL); // 3 ops
        r15 ^= (r16 | (r16 << 2)); // 3 ops
        // 48 lines of code, 96 operations
        // Butterfly: v[i], v[i+1] = v[i]+v[i+1], v[i]-v[i+1]
        r16 = (((r0 << 2) & 0xccccccccccccccccULL)
            | ((r0 & 0xccccccccccccccccULL) >> 2)); // 5 ops
        r0 = (r0 ^ 0xccccccccccccccccULL);
        r17 = (r0 & r16);
        r17 |= ((r17 << 1) & (r0 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r0 = (((r0 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r1 << 2) & 0xccccccccccccccccULL)
            | ((r1 & 0xccccccccccccccccULL) >> 2)); // 5 ops
        r1 = (r1 ^ 0xccccccccccccccccULL);
        r17 = (r1 & r16);
        r17 |= ((r17 << 1) & (r1 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r1 = (((r1 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r2 << 2) & 0xccccccccccccccccULL)
            | ((r2 & 0xccccccccccccccccULL) >> 2)); // 5 ops
        r2 = (r2 ^ 0xccccccccccccccccULL);
        r17 = (r2 & r16);
        r17 |= ((r17 << 1) & (r2 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r2 = (((r2 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r3 << 2) & 0xccccccccccccccccULL)
            | ((r3 & 0xccccccccccccccccULL) >> 2)); // 5 ops
        r3 = (r3 ^ 0xccccccccccccccccULL);
        r17 = (r3 & r16);
        r17 |= ((r17 << 1) & (r3 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r3 = (((r3 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r4 << 2) & 0xccccccccccccccccULL)
            | ((r4 & 0xccccccccccccccccULL) >> 2)); // 5 ops
        r4 = (r4 ^ 0xccccccccccccccccULL);
        r17 = (r4 & r16);
        r17 |= ((r17 << 1) & (r4 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r4 = (((r4 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r5 << 2) & 0xccccccccccccccccULL)
            | ((r5 & 0xccccccccccccccccULL) >> 2)); // 5 ops
        r5 = (r5 ^ 0xccccccccccccccccULL);
        r17 = (r5 & r16);
        r17 |= ((r17 << 1) & (r5 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r5 = (((r5 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r6 << 2) & 0xccccccccccccccccULL)
            | ((r6 & 0xccccccccccccccccULL) >> 2)); // 5 ops
        r6 = (r6 ^ 0xccccccccccccccccULL);
        r17 = (r6 & r16);
        r17 |= ((r17 << 1) & (r6 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r6 = (((r6 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r7 << 2) & 0xccccccccccccccccULL)
            | ((r7 & 0xccccccccccccccccULL) >> 2)); // 5 ops
        r7 = (r7 ^ 0xccccccccccccccccULL);
        r17 = (r7 & r16);
        r17 |= ((r17 << 1) & (r7 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r7 = (((r7 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r8 << 2) & 0xccccccccccccccccULL)
            | ((r8 & 0xccccccccccccccccULL) >> 2)); // 5 ops
        r8 = (r8 ^ 0xccccccccccccccccULL);
        r17 = (r8 & r16);
        r17 |= ((r17 << 1) & (r8 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r8 = (((r8 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r9 << 2) & 0xccccccccccccccccULL)
            | ((r9 & 0xccccccccccccccccULL) >> 2)); // 5 ops
        r9 = (r9 ^ 0xccccccccccccccccULL);
        r17 = (r9 & r16);
        r17 |= ((r17 << 1) & (r9 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r9 = (((r9 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r10 << 2) & 0xccccccccccccccccULL)
            | ((r10 & 0xccccccccccccccccULL) >> 2)); // 5 ops
        r10 = (r10 ^ 0xccccccccccccccccULL);
        r17 = (r10 & r16);
        r17 |= ((r17 << 1) & (r10 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r10 = (((r10 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r11 << 2) & 0xccccccccccccccccULL)
            | ((r11 & 0xccccccccccccccccULL) >> 2)); // 5 ops
        r11 = (r11 ^ 0xccccccccccccccccULL);
        r17 = (r11 & r16);
        r17 |= ((r17 << 1) & (r11 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r11 = (((r11 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r12 << 2) & 0xccccccccccccccccULL)
            | ((r12 & 0xccccccccccccccccULL) >> 2)); // 5 ops
        r12 = (r12 ^ 0xccccccccccccccccULL);
        r17 = (r12 & r16);
        r17 |= ((r17 << 1) & (r12 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r12 = (((r12 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r13 << 2) & 0xccccccccccccccccULL)
            | ((r13 & 0xccccccccccccccccULL) >> 2)); // 5 ops
        r13 = (r13 ^ 0xccccccccccccccccULL);
        r17 = (r13 & r16);
        r17 |= ((r17 << 1) & (r13 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r13 = (((r13 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r14 << 2) & 0xccccccccccccccccULL)
            | ((r14 & 0xccccccccccccccccULL) >> 2)); // 5 ops
        r14 = (r14 ^ 0xccccccccccccccccULL);
        r17 = (r14 & r16);
        r17 |= ((r17 << 1) & (r14 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r14 = (((r14 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r15 << 2) & 0xccccccccccccccccULL)
            | ((r15 & 0xccccccccccccccccULL) >> 2)); // 5 ops
        r15 = (r15 ^ 0xccccccccccccccccULL);
        r17 = (r15 & r16);
        r17 |= ((r17 << 1) & (r15 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r15 = (((r15 + r16) - r17) - (r17 >> 1)); // 4 ops
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        // Butterfly: v[i], v[i+2] = v[i]+v[i+2], v[i]-v[i+2]
        r16 = (((r0 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r0 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r0 = (r0 ^ 0xf0f0f0f0f0f0f0f0ULL);
        r17 = (r0 & r16);
        r17 |= ((r17 << 1) & (r0 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r0 = (((r0 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r1 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r1 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r1 = (r1 ^ 0xf0f0f0f0f0f0f0f0ULL);
        r17 = (r1 & r16);
        r17 |= ((r17 << 1) & (r1 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r1 = (((r1 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r2 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r2 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r2 = (r2 ^ 0xf0f0f0f0f0f0f0f0ULL);
        r17 = (r2 & r16);
        r17 |= ((r17 << 1) & (r2 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r2 = (((r2 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r3 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r3 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r3 = (r3 ^ 0xf0f0f0f0f0f0f0f0ULL);
        r17 = (r3 & r16);
        r17 |= ((r17 << 1) & (r3 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r3 = (((r3 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r4 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r4 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r4 = (r4 ^ 0xf0f0f0f0f0f0f0f0ULL);
        r17 = (r4 & r16);
        r17 |= ((r17 << 1) & (r4 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r4 = (((r4 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r5 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r5 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r5 = (r5 ^ 0xf0f0f0f0f0f0f0f0ULL);
        r17 = (r5 & r16);
        r17 |= ((r17 << 1) & (r5 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r5 = (((r5 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r6 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r6 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r6 = (r6 ^ 0xf0f0f0f0f0f0f0f0ULL);
        r17 = (r6 & r16);
        r17 |= ((r17 << 1) & (r6 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r6 = (((r6 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r7 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r7 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r7 = (r7 ^ 0xf0f0f0f0f0f0f0f0ULL);
        r17 = (r7 & r16);
        r17 |= ((r17 << 1) & (r7 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r7 = (((r7 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r8 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r8 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r8 = (r8 ^ 0xf0f0f0f0f0f0f0f0ULL);
        r17 = (r8 & r16);
        r17 |= ((r17 << 1) & (r8 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r8 = (((r8 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r9 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r9 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r9 = (r9 ^ 0xf0f0f0f0f0f0f0f0ULL);
        r17 = (r9 & r16);
        r17 |= ((r17 << 1) & (r9 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r9 = (((r9 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r10 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r10 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r10 = (r10 ^ 0xf0f0f0f0f0f0f0f0ULL);
        r17 = (r10 & r16);
        r17 |= ((r17 << 1) & (r10 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r10 = (((r10 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r11 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r11 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r11 = (r11 ^ 0xf0f0f0f0f0f0f0f0ULL);
        r17 = (r11 & r16);
        r17 |= ((r17 << 1) & (r11 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r11 = (((r11 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r12 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r12 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r12 = (r12 ^ 0xf0f0f0f0f0f0f0f0ULL);
        r17 = (r12 & r16);
        r17 |= ((r17 << 1) & (r12 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r12 = (((r12 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r13 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r13 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r13 = (r13 ^ 0xf0f0f0f0f0f0f0f0ULL);
        r17 = (r13 & r16);
        r17 |= ((r17 << 1) & (r13 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r13 = (((r13 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r14 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r14 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r14 = (r14 ^ 0xf0f0f0f0f0f0f0f0ULL);
        r17 = (r14 & r16);
        r17 |= ((r17 << 1) & (r14 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r14 = (((r14 + r16) - r17) - (r17 >> 1)); // 4 ops
        r16 = (((r15 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r15 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r15 = (r15 ^ 0xf0f0f0f0f0f0f0f0ULL);
        r17 = (r15 & r16);
        r17 |= ((r17 << 1) & (r15 ^ r16)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r15 = (((r15 + r16) - r17) - (r17 >> 1)); // 4 ops
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        // Butterfly: v[i], v[i+32] = v[i]+v[i+32], v[i]-v[i+32]
        r17 = (r0 & r1);
        r17 |= ((r17 << 1) & (r0 ^ r1)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r0 + r1) - r17) - (r17 >> 1)); // 4 ops
        r1 = (r1 ^ 0xffffffffffffffffULL);
        r17 = (r0 & r1);
        r17 |= ((r17 << 1) & (r0 ^ r1)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r1 = (((r0 + r1) - r17) - (r17 >> 1)); // 4 ops
        r0 = r16;
        r17 = (r2 & r3);
        r17 |= ((r17 << 1) & (r2 ^ r3)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r2 + r3) - r17) - (r17 >> 1)); // 4 ops
        r3 = (r3 ^ 0xffffffffffffffffULL);
        r17 = (r2 & r3);
        r17 |= ((r17 << 1) & (r2 ^ r3)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r3 = (((r2 + r3) - r17) - (r17 >> 1)); // 4 ops
        r2 = r16;
        r17 = (r4 & r5);
        r17 |= ((r17 << 1) & (r4 ^ r5)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r4 + r5) - r17) - (r17 >> 1)); // 4 ops
        r5 = (r5 ^ 0xffffffffffffffffULL);
        r17 = (r4 & r5);
        r17 |= ((r17 << 1) & (r4 ^ r5)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r5 = (((r4 + r5) - r17) - (r17 >> 1)); // 4 ops
        r4 = r16;
        r17 = (r6 & r7);
        r17 |= ((r17 << 1) & (r6 ^ r7)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r6 + r7) - r17) - (r17 >> 1)); // 4 ops
        r7 = (r7 ^ 0xffffffffffffffffULL);
        r17 = (r6 & r7);
        r17 |= ((r17 << 1) & (r6 ^ r7)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r7 = (((r6 + r7) - r17) - (r17 >> 1)); // 4 ops
        r6 = r16;
        r17 = (r8 & r9);
        r17 |= ((r17 << 1) & (r8 ^ r9)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r8 + r9) - r17) - (r17 >> 1)); // 4 ops
        r9 = (r9 ^ 0xffffffffffffffffULL);
        r17 = (r8 & r9);
        r17 |= ((r17 << 1) & (r8 ^ r9)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r9 = (((r8 + r9) - r17) - (r17 >> 1)); // 4 ops
        r8 = r16;
        r17 = (r10 & r11);
        r17 |= ((r17 << 1) & (r10 ^ r11)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r10 + r11) - r17) - (r17 >> 1)); // 4 ops
        r11 = (r11 ^ 0xffffffffffffffffULL);
        r17 = (r10 & r11);
        r17 |= ((r17 << 1) & (r10 ^ r11)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r11 = (((r10 + r11) - r17) - (r17 >> 1)); // 4 ops
        r10 = r16;
        r17 = (r12 & r13);
        r17 |= ((r17 << 1) & (r12 ^ r13)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r12 + r13) - r17) - (r17 >> 1)); // 4 ops
        r13 = (r13 ^ 0xffffffffffffffffULL);
        r17 = (r12 & r13);
        r17 |= ((r17 << 1) & (r12 ^ r13)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r13 = (((r12 + r13) - r17) - (r17 >> 1)); // 4 ops
        r12 = r16;
        r17 = (r14 & r15);
        r17 |= ((r17 << 1) & (r14 ^ r15)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r14 + r15) - r17) - (r17 >> 1)); // 4 ops
        r15 = (r15 ^ 0xffffffffffffffffULL);
        r17 = (r14 & r15);
        r17 |= ((r17 << 1) & (r14 ^ r15)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r15 = (((r14 + r15) - r17) - (r17 >> 1)); // 4 ops
        r14 = r16;
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        // Butterfly: v[i], v[i+64] = v[i]+v[i+64], v[i]-v[i+64]
        r17 = (r0 & r2);
        r17 |= ((r17 << 1) & (r0 ^ r2)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r0 + r2) - r17) - (r17 >> 1)); // 4 ops
        r2 = (r2 ^ 0xffffffffffffffffULL);
        r17 = (r0 & r2);
        r17 |= ((r17 << 1) & (r0 ^ r2)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r2 = (((r0 + r2) - r17) - (r17 >> 1)); // 4 ops
        r0 = r16;
        r17 = (r1 & r3);
        r17 |= ((r17 << 1) & (r1 ^ r3)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r1 + r3) - r17) - (r17 >> 1)); // 4 ops
        r3 = (r3 ^ 0xffffffffffffffffULL);
        r17 = (r1 & r3);
        r17 |= ((r17 << 1) & (r1 ^ r3)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r3 = (((r1 + r3) - r17) - (r17 >> 1)); // 4 ops
        r1 = r16;
        r17 = (r4 & r6);
        r17 |= ((r17 << 1) & (r4 ^ r6)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r4 + r6) - r17) - (r17 >> 1)); // 4 ops
        r6 = (r6 ^ 0xffffffffffffffffULL);
        r17 = (r4 & r6);
        r17 |= ((r17 << 1) & (r4 ^ r6)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r6 = (((r4 + r6) - r17) - (r17 >> 1)); // 4 ops
        r4 = r16;
        r17 = (r5 & r7);
        r17 |= ((r17 << 1) & (r5 ^ r7)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r5 + r7) - r17) - (r17 >> 1)); // 4 ops
        r7 = (r7 ^ 0xffffffffffffffffULL);
        r17 = (r5 & r7);
        r17 |= ((r17 << 1) & (r5 ^ r7)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r7 = (((r5 + r7) - r17) - (r17 >> 1)); // 4 ops
        r5 = r16;
        r17 = (r8 & r10);
        r17 |= ((r17 << 1) & (r8 ^ r10)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r8 + r10) - r17) - (r17 >> 1)); // 4 ops
        r10 = (r10 ^ 0xffffffffffffffffULL);
        r17 = (r8 & r10);
        r17 |= ((r17 << 1) & (r8 ^ r10)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r10 = (((r8 + r10) - r17) - (r17 >> 1)); // 4 ops
        r8 = r16;
        r17 = (r9 & r11);
        r17 |= ((r17 << 1) & (r9 ^ r11)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r9 + r11) - r17) - (r17 >> 1)); // 4 ops
        r11 = (r11 ^ 0xffffffffffffffffULL);
        r17 = (r9 & r11);
        r17 |= ((r17 << 1) & (r9 ^ r11)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r11 = (((r9 + r11) - r17) - (r17 >> 1)); // 4 ops
        r9 = r16;
        r17 = (r12 & r14);
        r17 |= ((r17 << 1) & (r12 ^ r14)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r12 + r14) - r17) - (r17 >> 1)); // 4 ops
        r14 = (r14 ^ 0xffffffffffffffffULL);
        r17 = (r12 & r14);
        r17 |= ((r17 << 1) & (r12 ^ r14)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r14 = (((r12 + r14) - r17) - (r17 >> 1)); // 4 ops
        r12 = r16;
        r17 = (r13 & r15);
        r17 |= ((r17 << 1) & (r13 ^ r15)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r13 + r15) - r17) - (r17 >> 1)); // 4 ops
        r15 = (r15 ^ 0xffffffffffffffffULL);
        r17 = (r13 & r15);
        r17 |= ((r17 << 1) & (r13 ^ r15)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r15 = (((r13 + r15) - r17) - (r17 >> 1)); // 4 ops
        r13 = r16;
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        // Butterfly: v[i], v[i+128] = v[i]+v[i+128], v[i]-v[i+128]
        r17 = (r0 & r4);
        r17 |= ((r17 << 1) & (r0 ^ r4)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r0 + r4) - r17) - (r17 >> 1)); // 4 ops
        r4 = (r4 ^ 0xffffffffffffffffULL);
        r17 = (r0 & r4);
        r17 |= ((r17 << 1) & (r0 ^ r4)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r4 = (((r0 + r4) - r17) - (r17 >> 1)); // 4 ops
        r0 = r16;
        r17 = (r1 & r5);
        r17 |= ((r17 << 1) & (r1 ^ r5)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r1 + r5) - r17) - (r17 >> 1)); // 4 ops
        r5 = (r5 ^ 0xffffffffffffffffULL);
        r17 = (r1 & r5);
        r17 |= ((r17 << 1) & (r1 ^ r5)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r5 = (((r1 + r5) - r17) - (r17 >> 1)); // 4 ops
        r1 = r16;
        r17 = (r2 & r6);
        r17 |= ((r17 << 1) & (r2 ^ r6)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r2 + r6) - r17) - (r17 >> 1)); // 4 ops
        r6 = (r6 ^ 0xffffffffffffffffULL);
        r17 = (r2 & r6);
        r17 |= ((r17 << 1) & (r2 ^ r6)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r6 = (((r2 + r6) - r17) - (r17 >> 1)); // 4 ops
        r2 = r16;
        r17 = (r3 & r7);
        r17 |= ((r17 << 1) & (r3 ^ r7)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r3 + r7) - r17) - (r17 >> 1)); // 4 ops
        r7 = (r7 ^ 0xffffffffffffffffULL);
        r17 = (r3 & r7);
        r17 |= ((r17 << 1) & (r3 ^ r7)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r7 = (((r3 + r7) - r17) - (r17 >> 1)); // 4 ops
        r3 = r16;
        r17 = (r8 & r12);
        r17 |= ((r17 << 1) & (r8 ^ r12)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r8 + r12) - r17) - (r17 >> 1)); // 4 ops
        r12 = (r12 ^ 0xffffffffffffffffULL);
        r17 = (r8 & r12);
        r17 |= ((r17 << 1) & (r8 ^ r12)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r12 = (((r8 + r12) - r17) - (r17 >> 1)); // 4 ops
        r8 = r16;
        r17 = (r9 & r13);
        r17 |= ((r17 << 1) & (r9 ^ r13)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r9 + r13) - r17) - (r17 >> 1)); // 4 ops
        r13 = (r13 ^ 0xffffffffffffffffULL);
        r17 = (r9 & r13);
        r17 |= ((r17 << 1) & (r9 ^ r13)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r13 = (((r9 + r13) - r17) - (r17 >> 1)); // 4 ops
        r9 = r16;
        r17 = (r10 & r14);
        r17 |= ((r17 << 1) & (r10 ^ r14)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r10 + r14) - r17) - (r17 >> 1)); // 4 ops
        r14 = (r14 ^ 0xffffffffffffffffULL);
        r17 = (r10 & r14);
        r17 |= ((r17 << 1) & (r10 ^ r14)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r14 = (((r10 + r14) - r17) - (r17 >> 1)); // 4 ops
        r10 = r16;
        r17 = (r11 & r15);
        r17 |= ((r17 << 1) & (r11 ^ r15)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r11 + r15) - r17) - (r17 >> 1)); // 4 ops
        r15 = (r15 ^ 0xffffffffffffffffULL);
        r17 = (r11 & r15);
        r17 |= ((r17 << 1) & (r11 ^ r15)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r15 = (((r11 + r15) - r17) - (r17 >> 1)); // 4 ops
        r11 = r16;
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        // Butterfly: v[i], v[i+256] = v[i]+v[i+256], v[i]-v[i+256]
        r17 = (r0 & r8);
        r17 |= ((r17 << 1) & (r0 ^ r8)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r0 + r8) - r17) - (r17 >> 1)); // 4 ops
        r8 = (r8 ^ 0xffffffffffffffffULL);
        r17 = (r0 & r8);
        r17 |= ((r17 << 1) & (r0 ^ r8)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r8 = (((r0 + r8) - r17) - (r17 >> 1)); // 4 ops
        r0 = r16;
        r17 = (r1 & r9);
        r17 |= ((r17 << 1) & (r1 ^ r9)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r1 + r9) - r17) - (r17 >> 1)); // 4 ops
        r9 = (r9 ^ 0xffffffffffffffffULL);
        r17 = (r1 & r9);
        r17 |= ((r17 << 1) & (r1 ^ r9)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r9 = (((r1 + r9) - r17) - (r17 >> 1)); // 4 ops
        r1 = r16;
        r17 = (r2 & r10);
        r17 |= ((r17 << 1) & (r2 ^ r10)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r2 + r10) - r17) - (r17 >> 1)); // 4 ops
        r10 = (r10 ^ 0xffffffffffffffffULL);
        r17 = (r2 & r10);
        r17 |= ((r17 << 1) & (r2 ^ r10)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r10 = (((r2 + r10) - r17) - (r17 >> 1)); // 4 ops
        r2 = r16;
        r17 = (r3 & r11);
        r17 |= ((r17 << 1) & (r3 ^ r11)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r3 + r11) - r17) - (r17 >> 1)); // 4 ops
        r11 = (r11 ^ 0xffffffffffffffffULL);
        r17 = (r3 & r11);
        r17 |= ((r17 << 1) & (r3 ^ r11)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r11 = (((r3 + r11) - r17) - (r17 >> 1)); // 4 ops
        r3 = r16;
        r17 = (r4 & r12);
        r17 |= ((r17 << 1) & (r4 ^ r12)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r4 + r12) - r17) - (r17 >> 1)); // 4 ops
        r12 = (r12 ^ 0xffffffffffffffffULL);
        r17 = (r4 & r12);
        r17 |= ((r17 << 1) & (r4 ^ r12)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r12 = (((r4 + r12) - r17) - (r17 >> 1)); // 4 ops
        r4 = r16;
        r17 = (r5 & r13);
        r17 |= ((r17 << 1) & (r5 ^ r13)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r5 + r13) - r17) - (r17 >> 1)); // 4 ops
        r13 = (r13 ^ 0xffffffffffffffffULL);
        r17 = (r5 & r13);
        r17 |= ((r17 << 1) & (r5 ^ r13)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r13 = (((r5 + r13) - r17) - (r17 >> 1)); // 4 ops
        r5 = r16;
        r17 = (r6 & r14);
        r17 |= ((r17 << 1) & (r6 ^ r14)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r6 + r14) - r17) - (r17 >> 1)); // 4 ops
        r14 = (r14 ^ 0xffffffffffffffffULL);
        r17 = (r6 & r14);
        r17 |= ((r17 << 1) & (r6 ^ r14)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r14 = (((r6 + r14) - r17) - (r17 >> 1)); // 4 ops
        r6 = r16;
        r17 = (r7 & r15);
        r17 |= ((r17 << 1) & (r7 ^ r15)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r16 = (((r7 + r15) - r17) - (r17 >> 1)); // 4 ops
        r15 = (r15 ^ 0xffffffffffffffffULL);
        r17 = (r7 & r15);
        r17 |= ((r17 << 1) & (r7 ^ r15)); // 4 ops
        r17 &= 0xaaaaaaaaaaaaaaaaULL;
        r15 = (((r7 + r15) - r17) - (r17 >> 1)); // 4 ops
        r7 = r16;
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        // Multiply vector by scalar 2**-3 mod 3
        r0 = (~r0);
        r1 = (~r1);
        r2 = (~r2);
        r3 = (~r3);
        r4 = (~r4);
        r5 = (~r5);
        r6 = (~r6);
        r7 = (~r7);
        r8 = (~r8);
        r9 = (~r9);
        r10 = (~r10);
        r11 = (~r11);
        r12 = (~r12);
        r13 = (~r13);
        r14 = (~r14);
        r15 = (~r15);
        // 528 lines of code, 1184 operations
        v_out[0] = (r0 ^  p_mask[6]) & 0xffffffffffffULL;
        v_out[1] = (r1 ^  p_mask[6]) & 0xffffffffffffULL;
        v_out[2] = (r2 ^  p_mask[6]) & 0xffffffffffffULL;
        v_out[3] = (r3 ^  p_mask[4]) & 0xffffffffffffULL;
        v_out[4] = (r4 ^  p_mask[6]) & 0xffffffffffffULL;
        v_out[5] = (r5 ^  p_mask[4]) & 0xffffffffffffULL;
        v_out[6] = (r6 ^  p_mask[4]) & 0xffffffffffffULL;
        v_out[7] = (r7 ^  p_mask[4]) & 0xffffffffffffULL;
        v_out[8] = (r8 ^  p_mask[6]) & 0xffffffffffffULL;
        v_out[9] = (r9 ^  p_mask[4]) & 0xffffffffffffULL;
        v_out[10] = (r10 ^  p_mask[4]) & 0xffffffffffffULL;
        v_out[11] = (r11 ^  p_mask[4]) & 0xffffffffffffULL;
        v_out[12] = (r12 ^  p_mask[4]) & 0xffffffffffffULL;
        v_out[13] = (r13 ^  p_mask[4]) & 0xffffffffffffULL;
        v_out[14] = (r14 ^  p_mask[4]) & 0xffffffffffffULL;
        v_out[15] = (r15 ^  p_mask[6]) & 0xffffffffffffULL;
        v_in += 16;
        v_out += 16;
        // 16 lines of code, 32 operations
        }
        // End of automatically generated matrix operation.
 
    }
}  


static void mm_op3_xi_a(uint_mmv_t *v_in,  uint32_t exp1, uint_mmv_t *v_out)
{
    uint_fast32_t i1;
    uint_mmv_t e_mask =  0 - ((uint_mmv_t)exp1 & 0x1ULL);
    for (i1 = 0; i1 < 6; ++i1) {
        // %%MUL_MATRIX_XI16 v_in, e_mask, v_out

        // This is an automatically generated matrix operation, do not change!
        {
        uint_mmv_t r0, r1, r2, r3, r4;
        uint_mmv_t r5;

        // TODO: write comment!!!
        // 
        e_mask = ~(e_mask);
        r0 = v_in[0] ^  (0xfcfcfcfcfcfcULL & e_mask);
        r4 = ((r0 ^ (r0 >> 2)) & 0xc0c0c0c0c0cULL); // 3 ops
        r0 ^= (r4 | (r4 << 2)); // 3 ops
        r1 = v_in[2] ^  (0x30303030303ULL & e_mask);
        r4 = ((r1 ^ (r1 >> 2)) & 0xc0c0c0c0c0cULL); // 3 ops
        r1 ^= (r4 | (r4 << 2)); // 3 ops
        r2 = v_in[1] ^  (0x30303030303ULL & e_mask);
        r4 = ((r2 ^ (r2 >> 2)) & 0xc0c0c0c0c0cULL); // 3 ops
        r2 ^= (r4 | (r4 << 2)); // 3 ops
        r3 = v_in[3] ^  (0x30303030303ULL & e_mask);
        r4 = ((r3 ^ (r3 >> 2)) & 0xc0c0c0c0c0cULL); // 3 ops
        r3 ^= (r4 | (r4 << 2)); // 3 ops
        // Butterfly: v[i], v[i+1] = v[i]+v[i+1], v[i]-v[i+1]
        r4 = (((r0 << 2) & 0xccccccccccccccccULL)
            | ((r0 & 0xccccccccccccccccULL) >> 2)); // 5 ops
        r0 = (r0 ^ 0xccccccccccccccccULL);
        r5 = (r0 & r4);
        r5 |= ((r5 << 1) & (r0 ^ r4)); // 4 ops
        r5 &= 0xaaaaaaaaaaaaaaaaULL;
        r0 = (((r0 + r4) - r5) - (r5 >> 1)); // 4 ops
        r4 = (((r1 << 2) & 0xccccccccccccccccULL)
            | ((r1 & 0xccccccccccccccccULL) >> 2)); // 5 ops
        r1 = (r1 ^ 0xccccccccccccccccULL);
        r5 = (r1 & r4);
        r5 |= ((r5 << 1) & (r1 ^ r4)); // 4 ops
        r5 &= 0xaaaaaaaaaaaaaaaaULL;
        r1 = (((r1 + r4) - r5) - (r5 >> 1)); // 4 ops
        r4 = (((r2 << 2) & 0xccccccccccccccccULL)
            | ((r2 & 0xccccccccccccccccULL) >> 2)); // 5 ops
        r2 = (r2 ^ 0xccccccccccccccccULL);
        r5 = (r2 & r4);
        r5 |= ((r5 << 1) & (r2 ^ r4)); // 4 ops
        r5 &= 0xaaaaaaaaaaaaaaaaULL;
        r2 = (((r2 + r4) - r5) - (r5 >> 1)); // 4 ops
        r4 = (((r3 << 2) & 0xccccccccccccccccULL)
            | ((r3 & 0xccccccccccccccccULL) >> 2)); // 5 ops
        r3 = (r3 ^ 0xccccccccccccccccULL);
        r5 = (r3 & r4);
        r5 |= ((r5 << 1) & (r3 ^ r4)); // 4 ops
        r5 &= 0xaaaaaaaaaaaaaaaaULL;
        r3 = (((r3 + r4) - r5) - (r5 >> 1)); // 4 ops
        // Vector is now  r(i) for i = 0,1,2,3
        // Butterfly: v[i], v[i+2] = v[i]+v[i+2], v[i]-v[i+2]
        r4 = (((r0 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r0 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r0 = (r0 ^ 0xf0f0f0f0f0f0f0f0ULL);
        r5 = (r0 & r4);
        r5 |= ((r5 << 1) & (r0 ^ r4)); // 4 ops
        r5 &= 0xaaaaaaaaaaaaaaaaULL;
        r0 = (((r0 + r4) - r5) - (r5 >> 1)); // 4 ops
        r4 = (((r1 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r1 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r1 = (r1 ^ 0xf0f0f0f0f0f0f0f0ULL);
        r5 = (r1 & r4);
        r5 |= ((r5 << 1) & (r1 ^ r4)); // 4 ops
        r5 &= 0xaaaaaaaaaaaaaaaaULL;
        r1 = (((r1 + r4) - r5) - (r5 >> 1)); // 4 ops
        r4 = (((r2 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r2 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r2 = (r2 ^ 0xf0f0f0f0f0f0f0f0ULL);
        r5 = (r2 & r4);
        r5 |= ((r5 << 1) & (r2 ^ r4)); // 4 ops
        r5 &= 0xaaaaaaaaaaaaaaaaULL;
        r2 = (((r2 + r4) - r5) - (r5 >> 1)); // 4 ops
        r4 = (((r3 << 4) & 0xf0f0f0f0f0f0f0f0ULL)
            | ((r3 & 0xf0f0f0f0f0f0f0f0ULL) >> 4)); // 5 ops
        r3 = (r3 ^ 0xf0f0f0f0f0f0f0f0ULL);
        r5 = (r3 & r4);
        r5 |= ((r5 << 1) & (r3 ^ r4)); // 4 ops
        r5 &= 0xaaaaaaaaaaaaaaaaULL;
        r3 = (((r3 + r4) - r5) - (r5 >> 1)); // 4 ops
        // Vector is now  r(i) for i = 0,1,2,3
        // Butterfly: v[i], v[i+32] = v[i]+v[i+32], v[i]-v[i+32]
        r5 = (r0 & r1);
        r5 |= ((r5 << 1) & (r0 ^ r1)); // 4 ops
        r5 &= 0xaaaaaaaaaaaaaaaaULL;
        r4 = (((r0 + r1) - r5) - (r5 >> 1)); // 4 ops
        r1 = (r1 ^ 0xffffffffffffffffULL);
        r5 = (r0 & r1);
        r5 |= ((r5 << 1) & (r0 ^ r1)); // 4 ops
        r5 &= 0xaaaaaaaaaaaaaaaaULL;
        r1 = (((r0 + r1) - r5) - (r5 >> 1)); // 4 ops
        r0 = r4;
        r5 = (r2 & r3);
        r5 |= ((r5 << 1) & (r2 ^ r3)); // 4 ops
        r5 &= 0xaaaaaaaaaaaaaaaaULL;
        r4 = (((r2 + r3) - r5) - (r5 >> 1)); // 4 ops
        r3 = (r3 ^ 0xffffffffffffffffULL);
        r5 = (r2 & r3);
        r5 |= ((r5 << 1) & (r2 ^ r3)); // 4 ops
        r5 &= 0xaaaaaaaaaaaaaaaaULL;
        r3 = (((r2 + r3) - r5) - (r5 >> 1)); // 4 ops
        r2 = r4;
        // Vector is now  r(i) for i = 0,1,2,3
        // Butterfly: v[i], v[i+64] = v[i]+v[i+64], v[i]-v[i+64]
        r5 = (r0 & r2);
        r5 |= ((r5 << 1) & (r0 ^ r2)); // 4 ops
        r5 &= 0xaaaaaaaaaaaaaaaaULL;
        r4 = (((r0 + r2) - r5) - (r5 >> 1)); // 4 ops
        r2 = (r2 ^ 0xffffffffffffffffULL);
        r5 = (r0 & r2);
        r5 |= ((r5 << 1) & (r0 ^ r2)); // 4 ops
        r5 &= 0xaaaaaaaaaaaaaaaaULL;
        r2 = (((r0 + r2) - r5) - (r5 >> 1)); // 4 ops
        r0 = r4;
        r5 = (r1 & r3);
        r5 |= ((r5 << 1) & (r1 ^ r3)); // 4 ops
        r5 &= 0xaaaaaaaaaaaaaaaaULL;
        r4 = (((r1 + r3) - r5) - (r5 >> 1)); // 4 ops
        r3 = (r3 ^ 0xffffffffffffffffULL);
        r5 = (r1 & r3);
        r5 |= ((r5 << 1) & (r1 ^ r3)); // 4 ops
        r5 &= 0xaaaaaaaaaaaaaaaaULL;
        r3 = (((r1 + r3) - r5) - (r5 >> 1)); // 4 ops
        r1 = r4;
        // Vector is now  r(i) for i = 0,1,2,3
        // Multiplication by 2**0 is trivial mod 3
        e_mask = ~(e_mask);
        v_out[0] = r0 ^ (e_mask & 0xfcfcfcfcfcfcULL);
        v_out[1] = r1 ^ (e_mask & 0x30303030303ULL);
        v_out[2] = r2 ^ (e_mask & 0x30303030303ULL);
        v_out[3] = r3 ^ (e_mask & 0x30303030303ULL);
        // 106 lines of code, 246 operations
        v_in++;
        v_out++;
        v_in += 3;
        v_out += 3;
        }
        // End of automatically generated matrix operation.
 
    }
}  

/// @endcond 


/**
  @brief Compute an operation of the monster group on a vector

  Let ``v_in`` be a vector of the representation \f$\rho_{3}\f$
  of the monster group.

  The function implements the operation of the element \f$\xi^e\f$ 
  of the monster group  on a vector ``v_in`` in the 
  representation \f$\rho_{3}\f$ of the monster.

  Parameter ``exp`` is the exponent \f$e\f$ of the generator 
  \f$\xi^e\f$. The function computes the operation of \f$\xi^e\f$  
  on the input  vector ``v_in`` and  stores the result in the output 
  vector ``v_out.`` 

  Input vector  ``v_in`` is not changed.
*/
// %%EXPORT px
MM_OP3_API
void mm_op3_xi(uint_mmv_t *v_in,  uint32_t exp, uint_mmv_t *v_out)
{
    uint_mmv_t i;
    uint32_t exp1;

    exp %= 3;
    if (exp == 0) {
        for (i = 0; i < 7734; ++i) v_out[i] = v_in[i];
        return;
    }
    exp1 =  exp - 1;

    // Do monomial part, i.e. tags B, C, T, X
    // Caution: this uses v_out[MM_OP3_OFS_Z:] as temporary storage
    mm_op3_xi_mon(v_in, exp1, v_out);

    // Do tag A
    mm_op3_xi_a(v_in, exp1, v_out); 

    // Do tags X, Y
    for (i = 0; i < 4; ++i) {
        uint_mmv_t *p_src = v_in + MM_OP3_OFS_Z + (i << HALF_YZ_SHIFT);
        mm_op3_xi_yz(p_src, exp1, v_out + TAB3_XI64_OFFSET[exp1][i]);
    }
}

/**
  @brief Restriction of function ``mm_op3_xi`` to tag ``A``

  Function ``mm_op3_xi`` computes a certain operation of the
  monster group on a vector ``v_in``. That operation depends
  on a parameter ``exp``.
  
  Function ``mm_op3_xi_tag_A`` computes the same
  operation on the entries of the vector ``v = v_in`` with
  tag ``A`` only, and ignores the other entries of ``v``.
  See section **The representation of the monster group**
  in the **API reference** for tags of entries of a vector in
  the representation of the monster.

  The function overwrites the vector ``v`` with the result.
  Here only entries of ``v`` with tag ``A`` are changed. This 
  function is much faster than function ``mm_op3_xy``.
*/
// %%EXPORT px
MM_OP3_API
void mm_op3_xi_tag_A(uint_mmv_t *v,  uint32_t exp)
{
    uint_mmv_t v_tmp[24 * 1];
    uint_fast32_t i;
    
    exp %= 3;
    if (exp == 0) return;
    mm_op3_xi_a(v, exp - 1, v_tmp);
    for (i = 0; i < 24 * 1; ++i) v[i] = v_tmp[i];
}


//  %%GEN h
//  %%GEN c
