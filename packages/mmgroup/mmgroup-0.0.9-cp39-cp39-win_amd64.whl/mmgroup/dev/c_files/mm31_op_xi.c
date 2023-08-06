/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////

/** @file mm31_op_xi.c

 File ``mm31_op_xi.c`` implements the operation of the element
 \f$\xi^e\f$ of the monster group on a vector in the
 representation \f$\rho_{31}\f$ of the monster.

 Here the generator \f$\xi\f$ of the monster group is defined as 
 in section **The monster group** of the **API reference**.

 The representation \f$\rho_{31}\f$ is equal to the
 196884-dimensional representation  \f$\rho\f$ of the monster,
 with coefficients taken modulo 31, as defined in
 section **The representation of the monster group**
 in the **API reference**.

 An element of \f$\rho_{31}\f$ is implemented as an array of
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
#include "mm_op31.h"   

// %%EXPORT_KWD MM_OP%{P}_API


//  %%GEN h
//  %%GEN c




/// @cond DO_NOT_DOCUMENT 

static void mm_op31_xi_mon(
    uint_mmv_t * v_in,  
    uint32_t exp1, 
    uint_mmv_t * v_out
)
{
    // Caution: this uses v_out[MM_OP31_OFS_Z:] as temporary storage
    uint_mmv_t *p_src, *p_dest;
    uint_fast32_t i, j;
    uint_fast32_t diff = exp1 ? 4096 : 0;
    uint8_t *b =  (uint8_t*)(v_out + MM_OP31_OFS_Z), *p_b;
    mm_sub_table_xi_type *p_tables = mm_sub_table_xi[exp1];
    uint16_t *p_perm;
    uint32_t *p_sign;



    ///////////////////////////////////////////////////////////////
    // Map tag BC to tag BC.
    ///////////////////////////////////////////////////////////////
    p_src = v_in + 96;
    p_dest = v_out + 96;
    p_sign = p_tables[0].p_sign;
    p_perm = p_tables[0].p_perm;

    for (i = 0; i < 1; ++i) {
        p_b = b;
        
        for (j = 0; j < 78; ++j) {
           // %%OP_XI_LOAD p_src, p_b, %{i_src.SHAPE[2]}, uint8_t
           uint_mmv_t r0;
           r0 =  (p_src)[0];
           r0 &= 0x1f1f1f1f1f1f1f1fULL;
           (p_b)[0] = (uint8_t)(r0 >> 0);
           (p_b)[1] = (uint8_t)(r0 >> 8);
           (p_b)[2] = (uint8_t)(r0 >> 16);
           (p_b)[3] = (uint8_t)(r0 >> 24);
           (p_b)[4] = (uint8_t)(r0 >> 32);
           (p_b)[5] = (uint8_t)(r0 >> 40);
           (p_b)[6] = (uint8_t)(r0 >> 48);
           (p_b)[7] = (uint8_t)(r0 >> 56);
           r0 =  (p_src)[1];
           r0 &= 0x1f1f1f1f1f1f1f1fULL;
           (p_b)[8] = (uint8_t)(r0 >> 0);
           (p_b)[9] = (uint8_t)(r0 >> 8);
           (p_b)[10] = (uint8_t)(r0 >> 16);
           (p_b)[11] = (uint8_t)(r0 >> 24);
           (p_b)[12] = (uint8_t)(r0 >> 32);
           (p_b)[13] = (uint8_t)(r0 >> 40);
           (p_b)[14] = (uint8_t)(r0 >> 48);
           (p_b)[15] = (uint8_t)(r0 >> 56);
           r0 =  (p_src)[2];
           r0 &= 0x1f1f1f1f1f1f1f1fULL;
           (p_b)[16] = (uint8_t)(r0 >> 0);
           (p_b)[17] = (uint8_t)(r0 >> 8);
           (p_b)[18] = (uint8_t)(r0 >> 16);
           (p_b)[19] = (uint8_t)(r0 >> 24);
           (p_b)[20] = (uint8_t)(r0 >> 32);
           (p_b)[21] = (uint8_t)(r0 >> 40);
           (p_b)[22] = (uint8_t)(r0 >> 48);
           (p_b)[23] = (uint8_t)(r0 >> 56);
           r0 =  (p_src)[3];
           r0 &= 0x1f1f1f1f1f1f1f1fULL;
           (p_b)[24] = (uint8_t)(r0 >> 0);
           (p_b)[25] = (uint8_t)(r0 >> 8);
           (p_b)[26] = (uint8_t)(r0 >> 16);
           (p_b)[27] = (uint8_t)(r0 >> 24);
           (p_b)[28] = (uint8_t)(r0 >> 32);
           (p_b)[29] = (uint8_t)(r0 >> 40);
           (p_b)[30] = (uint8_t)(r0 >> 48);
           (p_b)[31] = (uint8_t)(r0 >> 56);
           p_src += 4;
           p_b += 32;
        }
        
        for (j = 0; j < 78; ++j) {
           // %%OP_XI_STORE b, p_perm, p_sign, p_dest, %{i_dest.SHAPE[2]}
           uint_mmv_t r0, r1;
           r0 = ((uint_mmv_t)(b[p_perm[0]]) << 0)
             + ((uint_mmv_t)(b[p_perm[1]]) << 8)
             + ((uint_mmv_t)(b[p_perm[2]]) << 16)
             + ((uint_mmv_t)(b[p_perm[3]]) << 24)
             + ((uint_mmv_t)(b[p_perm[4]]) << 32)
             + ((uint_mmv_t)(b[p_perm[5]]) << 40)
             + ((uint_mmv_t)(b[p_perm[6]]) << 48)
             + ((uint_mmv_t)(b[p_perm[7]]) << 56);
           r1 = (p_sign)[0] >> 0;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0x1f if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 31;
           // Bit spreading done.
           (p_dest)[0] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[8]]) << 0)
             + ((uint_mmv_t)(b[p_perm[9]]) << 8)
             + ((uint_mmv_t)(b[p_perm[10]]) << 16)
             + ((uint_mmv_t)(b[p_perm[11]]) << 24)
             + ((uint_mmv_t)(b[p_perm[12]]) << 32)
             + ((uint_mmv_t)(b[p_perm[13]]) << 40)
             + ((uint_mmv_t)(b[p_perm[14]]) << 48)
             + ((uint_mmv_t)(b[p_perm[15]]) << 56);
           r1 = (p_sign)[0] >> 8;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0x1f if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 31;
           // Bit spreading done.
           (p_dest)[1] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[16]]) << 0)
             + ((uint_mmv_t)(b[p_perm[17]]) << 8)
             + ((uint_mmv_t)(b[p_perm[18]]) << 16)
             + ((uint_mmv_t)(b[p_perm[19]]) << 24)
             + ((uint_mmv_t)(b[p_perm[20]]) << 32)
             + ((uint_mmv_t)(b[p_perm[21]]) << 40)
             + ((uint_mmv_t)(b[p_perm[22]]) << 48)
             + ((uint_mmv_t)(b[p_perm[23]]) << 56);
           r1 = (p_sign)[0] >> 16;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0x1f if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 31;
           // Bit spreading done.
           (p_dest)[2] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[24]]) << 0)
             + ((uint_mmv_t)(b[p_perm[25]]) << 8)
             + ((uint_mmv_t)(b[p_perm[26]]) << 16)
             + ((uint_mmv_t)(b[p_perm[27]]) << 24)
             + ((uint_mmv_t)(b[p_perm[28]]) << 32)
             + ((uint_mmv_t)(b[p_perm[29]]) << 40)
             + ((uint_mmv_t)(b[p_perm[30]]) << 48)
             + ((uint_mmv_t)(b[p_perm[31]]) << 56);
           r1 = (p_sign)[0] >> 24;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0x1f if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 31;
           // Bit spreading done.
           (p_dest)[3] = r0 ^ r1;
           p_dest += 4;
           p_perm += 32;
           p_sign += 1;
        }
        
    }

    ///////////////////////////////////////////////////////////////
    // Map tag T0 to tag T0.
    ///////////////////////////////////////////////////////////////
    p_src = v_in + 408;
    p_dest = v_out + 408;
    p_sign = p_tables[1].p_sign;
    p_perm = p_tables[1].p_perm;

    for (i = 0; i < 45; ++i) {
        p_b = b;
        
        for (j = 0; j < 16; ++j) {
           // %%OP_XI_LOAD p_src, p_b, %{i_src.SHAPE[2]}, uint8_t
           uint_mmv_t r0;
           r0 =  (p_src)[0];
           r0 &= 0x1f1f1f1f1f1f1f1fULL;
           (p_b)[0] = (uint8_t)(r0 >> 0);
           (p_b)[1] = (uint8_t)(r0 >> 8);
           (p_b)[2] = (uint8_t)(r0 >> 16);
           (p_b)[3] = (uint8_t)(r0 >> 24);
           (p_b)[4] = (uint8_t)(r0 >> 32);
           (p_b)[5] = (uint8_t)(r0 >> 40);
           (p_b)[6] = (uint8_t)(r0 >> 48);
           (p_b)[7] = (uint8_t)(r0 >> 56);
           r0 =  (p_src)[1];
           r0 &= 0x1f1f1f1f1f1f1f1fULL;
           (p_b)[8] = (uint8_t)(r0 >> 0);
           (p_b)[9] = (uint8_t)(r0 >> 8);
           (p_b)[10] = (uint8_t)(r0 >> 16);
           (p_b)[11] = (uint8_t)(r0 >> 24);
           (p_b)[12] = (uint8_t)(r0 >> 32);
           (p_b)[13] = (uint8_t)(r0 >> 40);
           (p_b)[14] = (uint8_t)(r0 >> 48);
           (p_b)[15] = (uint8_t)(r0 >> 56);
           r0 =  (p_src)[2];
           r0 &= 0x1f1f1f1f1f1f1f1fULL;
           (p_b)[16] = (uint8_t)(r0 >> 0);
           (p_b)[17] = (uint8_t)(r0 >> 8);
           (p_b)[18] = (uint8_t)(r0 >> 16);
           (p_b)[19] = (uint8_t)(r0 >> 24);
           (p_b)[20] = (uint8_t)(r0 >> 32);
           (p_b)[21] = (uint8_t)(r0 >> 40);
           (p_b)[22] = (uint8_t)(r0 >> 48);
           (p_b)[23] = (uint8_t)(r0 >> 56);
           r0 =  (p_src)[3];
           r0 &= 0x1f1f1f1f1f1f1f1fULL;
           (p_b)[24] = (uint8_t)(r0 >> 0);
           (p_b)[25] = (uint8_t)(r0 >> 8);
           (p_b)[26] = (uint8_t)(r0 >> 16);
           (p_b)[27] = (uint8_t)(r0 >> 24);
           (p_b)[28] = (uint8_t)(r0 >> 32);
           (p_b)[29] = (uint8_t)(r0 >> 40);
           (p_b)[30] = (uint8_t)(r0 >> 48);
           (p_b)[31] = (uint8_t)(r0 >> 56);
           p_src += 4;
           p_b += 32;
        }
        
        for (j = 0; j < 16; ++j) {
           // %%OP_XI_STORE b, p_perm, p_sign, p_dest, %{i_dest.SHAPE[2]}
           uint_mmv_t r0, r1;
           r0 = ((uint_mmv_t)(b[p_perm[0]]) << 0)
             + ((uint_mmv_t)(b[p_perm[1]]) << 8)
             + ((uint_mmv_t)(b[p_perm[2]]) << 16)
             + ((uint_mmv_t)(b[p_perm[3]]) << 24)
             + ((uint_mmv_t)(b[p_perm[4]]) << 32)
             + ((uint_mmv_t)(b[p_perm[5]]) << 40)
             + ((uint_mmv_t)(b[p_perm[6]]) << 48)
             + ((uint_mmv_t)(b[p_perm[7]]) << 56);
           r1 = (p_sign)[0] >> 0;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0x1f if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 31;
           // Bit spreading done.
           (p_dest)[0] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[8]]) << 0)
             + ((uint_mmv_t)(b[p_perm[9]]) << 8)
             + ((uint_mmv_t)(b[p_perm[10]]) << 16)
             + ((uint_mmv_t)(b[p_perm[11]]) << 24)
             + ((uint_mmv_t)(b[p_perm[12]]) << 32)
             + ((uint_mmv_t)(b[p_perm[13]]) << 40)
             + ((uint_mmv_t)(b[p_perm[14]]) << 48)
             + ((uint_mmv_t)(b[p_perm[15]]) << 56);
           r1 = (p_sign)[0] >> 8;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0x1f if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 31;
           // Bit spreading done.
           (p_dest)[1] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[16]]) << 0)
             + ((uint_mmv_t)(b[p_perm[17]]) << 8)
             + ((uint_mmv_t)(b[p_perm[18]]) << 16)
             + ((uint_mmv_t)(b[p_perm[19]]) << 24)
             + ((uint_mmv_t)(b[p_perm[20]]) << 32)
             + ((uint_mmv_t)(b[p_perm[21]]) << 40)
             + ((uint_mmv_t)(b[p_perm[22]]) << 48)
             + ((uint_mmv_t)(b[p_perm[23]]) << 56);
           r1 = (p_sign)[0] >> 16;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0x1f if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 31;
           // Bit spreading done.
           (p_dest)[2] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[24]]) << 0)
             + ((uint_mmv_t)(b[p_perm[25]]) << 8)
             + ((uint_mmv_t)(b[p_perm[26]]) << 16)
             + ((uint_mmv_t)(b[p_perm[27]]) << 24)
             + ((uint_mmv_t)(b[p_perm[28]]) << 32)
             + ((uint_mmv_t)(b[p_perm[29]]) << 40)
             + ((uint_mmv_t)(b[p_perm[30]]) << 48)
             + ((uint_mmv_t)(b[p_perm[31]]) << 56);
           r1 = (p_sign)[0] >> 24;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0x1f if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 31;
           // Bit spreading done.
           (p_dest)[3] = r0 ^ r1;
           p_dest += 4;
           p_perm += 32;
           p_sign += 1;
        }
        
    }

    ///////////////////////////////////////////////////////////////
    // Map tag T1 to tag X0 if e = 1
    // Map tag T1 to tag X1 if e = 2
    ///////////////////////////////////////////////////////////////
    p_src = v_in + 3288;
    p_dest = v_out + 6360;
    p_dest += diff;
    p_sign = p_tables[2].p_sign;
    p_perm = p_tables[2].p_perm;

    for (i = 0; i < 64; ++i) {
        p_b = b;
        
        for (j = 0; j < 12; ++j) {
           // %%OP_XI_LOAD p_src, p_b, %{i_src.SHAPE[2]}, uint8_t
           uint_mmv_t r0;
           r0 =  (p_src)[0];
           r0 &= 0x1f1f1f1f1f1f1f1fULL;
           (p_b)[0] = (uint8_t)(r0 >> 0);
           (p_b)[1] = (uint8_t)(r0 >> 8);
           (p_b)[2] = (uint8_t)(r0 >> 16);
           (p_b)[3] = (uint8_t)(r0 >> 24);
           (p_b)[4] = (uint8_t)(r0 >> 32);
           (p_b)[5] = (uint8_t)(r0 >> 40);
           (p_b)[6] = (uint8_t)(r0 >> 48);
           (p_b)[7] = (uint8_t)(r0 >> 56);
           r0 =  (p_src)[1];
           r0 &= 0x1f1f1f1f1f1f1f1fULL;
           (p_b)[8] = (uint8_t)(r0 >> 0);
           (p_b)[9] = (uint8_t)(r0 >> 8);
           (p_b)[10] = (uint8_t)(r0 >> 16);
           (p_b)[11] = (uint8_t)(r0 >> 24);
           (p_b)[12] = (uint8_t)(r0 >> 32);
           (p_b)[13] = (uint8_t)(r0 >> 40);
           (p_b)[14] = (uint8_t)(r0 >> 48);
           (p_b)[15] = (uint8_t)(r0 >> 56);
           r0 =  (p_src)[2];
           r0 &= 0x1f1f1f1f1f1f1f1fULL;
           (p_b)[16] = (uint8_t)(r0 >> 0);
           (p_b)[17] = (uint8_t)(r0 >> 8);
           (p_b)[18] = (uint8_t)(r0 >> 16);
           (p_b)[19] = (uint8_t)(r0 >> 24);
           (p_b)[20] = (uint8_t)(r0 >> 32);
           (p_b)[21] = (uint8_t)(r0 >> 40);
           (p_b)[22] = (uint8_t)(r0 >> 48);
           (p_b)[23] = (uint8_t)(r0 >> 56);
           r0 =  (p_src)[3];
           r0 &= 0x1f1f1f1f1f1f1f1fULL;
           (p_b)[24] = (uint8_t)(r0 >> 0);
           (p_b)[25] = (uint8_t)(r0 >> 8);
           (p_b)[26] = (uint8_t)(r0 >> 16);
           (p_b)[27] = (uint8_t)(r0 >> 24);
           (p_b)[28] = (uint8_t)(r0 >> 32);
           (p_b)[29] = (uint8_t)(r0 >> 40);
           (p_b)[30] = (uint8_t)(r0 >> 48);
           (p_b)[31] = (uint8_t)(r0 >> 56);
           p_src += 4;
           p_b += 32;
        }
        
        for (j = 0; j < 16; ++j) {
           // %%OP_XI_STORE b, p_perm, p_sign, p_dest, %{i_dest.SHAPE[2]}
           uint_mmv_t r0, r1;
           r0 = ((uint_mmv_t)(b[p_perm[0]]) << 0)
             + ((uint_mmv_t)(b[p_perm[1]]) << 8)
             + ((uint_mmv_t)(b[p_perm[2]]) << 16)
             + ((uint_mmv_t)(b[p_perm[3]]) << 24)
             + ((uint_mmv_t)(b[p_perm[4]]) << 32)
             + ((uint_mmv_t)(b[p_perm[5]]) << 40)
             + ((uint_mmv_t)(b[p_perm[6]]) << 48)
             + ((uint_mmv_t)(b[p_perm[7]]) << 56);
           r1 = (p_sign)[0] >> 0;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0x1f if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 31;
           // Bit spreading done.
           (p_dest)[0] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[8]]) << 0)
             + ((uint_mmv_t)(b[p_perm[9]]) << 8)
             + ((uint_mmv_t)(b[p_perm[10]]) << 16)
             + ((uint_mmv_t)(b[p_perm[11]]) << 24)
             + ((uint_mmv_t)(b[p_perm[12]]) << 32)
             + ((uint_mmv_t)(b[p_perm[13]]) << 40)
             + ((uint_mmv_t)(b[p_perm[14]]) << 48)
             + ((uint_mmv_t)(b[p_perm[15]]) << 56);
           r1 = (p_sign)[0] >> 8;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0x1f if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 31;
           // Bit spreading done.
           (p_dest)[1] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[16]]) << 0)
             + ((uint_mmv_t)(b[p_perm[17]]) << 8)
             + ((uint_mmv_t)(b[p_perm[18]]) << 16)
             + ((uint_mmv_t)(b[p_perm[19]]) << 24)
             + ((uint_mmv_t)(b[p_perm[20]]) << 32)
             + ((uint_mmv_t)(b[p_perm[21]]) << 40)
             + ((uint_mmv_t)(b[p_perm[22]]) << 48)
             + ((uint_mmv_t)(b[p_perm[23]]) << 56);
           r1 = (p_sign)[0] >> 16;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0x1f if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 31;
           // Bit spreading done.
           (p_dest)[2] = r0 ^ r1;
           p_dest[3] = 0;
           p_dest += 4;
           p_perm += 24;
           p_sign += 1;
        }
        
    }

    ///////////////////////////////////////////////////////////////
    // Map tag X0 to tag X1 if e = 1
    // Map tag X1 to tag X0 if e = 2
    ///////////////////////////////////////////////////////////////
    p_src = v_in + 6360;
    p_src += diff;
    p_dest = v_out + 10456;
    p_dest -= diff;
    p_sign = p_tables[3].p_sign;
    p_perm = p_tables[3].p_perm;

    for (i = 0; i < 64; ++i) {
        p_b = b;
        
        for (j = 0; j < 16; ++j) {
           // %%OP_XI_LOAD p_src, p_b, %{i_src.SHAPE[2]}, uint8_t
           uint_mmv_t r0;
           r0 =  (p_src)[0];
           r0 &= 0x1f1f1f1f1f1f1f1fULL;
           (p_b)[0] = (uint8_t)(r0 >> 0);
           (p_b)[1] = (uint8_t)(r0 >> 8);
           (p_b)[2] = (uint8_t)(r0 >> 16);
           (p_b)[3] = (uint8_t)(r0 >> 24);
           (p_b)[4] = (uint8_t)(r0 >> 32);
           (p_b)[5] = (uint8_t)(r0 >> 40);
           (p_b)[6] = (uint8_t)(r0 >> 48);
           (p_b)[7] = (uint8_t)(r0 >> 56);
           r0 =  (p_src)[1];
           r0 &= 0x1f1f1f1f1f1f1f1fULL;
           (p_b)[8] = (uint8_t)(r0 >> 0);
           (p_b)[9] = (uint8_t)(r0 >> 8);
           (p_b)[10] = (uint8_t)(r0 >> 16);
           (p_b)[11] = (uint8_t)(r0 >> 24);
           (p_b)[12] = (uint8_t)(r0 >> 32);
           (p_b)[13] = (uint8_t)(r0 >> 40);
           (p_b)[14] = (uint8_t)(r0 >> 48);
           (p_b)[15] = (uint8_t)(r0 >> 56);
           r0 =  (p_src)[2];
           r0 &= 0x1f1f1f1f1f1f1f1fULL;
           (p_b)[16] = (uint8_t)(r0 >> 0);
           (p_b)[17] = (uint8_t)(r0 >> 8);
           (p_b)[18] = (uint8_t)(r0 >> 16);
           (p_b)[19] = (uint8_t)(r0 >> 24);
           (p_b)[20] = (uint8_t)(r0 >> 32);
           (p_b)[21] = (uint8_t)(r0 >> 40);
           (p_b)[22] = (uint8_t)(r0 >> 48);
           (p_b)[23] = (uint8_t)(r0 >> 56);
           p_src += 4;
           p_b += 32;
        }
        
        for (j = 0; j < 16; ++j) {
           // %%OP_XI_STORE b, p_perm, p_sign, p_dest, %{i_dest.SHAPE[2]}
           uint_mmv_t r0, r1;
           r0 = ((uint_mmv_t)(b[p_perm[0]]) << 0)
             + ((uint_mmv_t)(b[p_perm[1]]) << 8)
             + ((uint_mmv_t)(b[p_perm[2]]) << 16)
             + ((uint_mmv_t)(b[p_perm[3]]) << 24)
             + ((uint_mmv_t)(b[p_perm[4]]) << 32)
             + ((uint_mmv_t)(b[p_perm[5]]) << 40)
             + ((uint_mmv_t)(b[p_perm[6]]) << 48)
             + ((uint_mmv_t)(b[p_perm[7]]) << 56);
           r1 = (p_sign)[0] >> 0;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0x1f if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 31;
           // Bit spreading done.
           (p_dest)[0] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[8]]) << 0)
             + ((uint_mmv_t)(b[p_perm[9]]) << 8)
             + ((uint_mmv_t)(b[p_perm[10]]) << 16)
             + ((uint_mmv_t)(b[p_perm[11]]) << 24)
             + ((uint_mmv_t)(b[p_perm[12]]) << 32)
             + ((uint_mmv_t)(b[p_perm[13]]) << 40)
             + ((uint_mmv_t)(b[p_perm[14]]) << 48)
             + ((uint_mmv_t)(b[p_perm[15]]) << 56);
           r1 = (p_sign)[0] >> 8;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0x1f if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 31;
           // Bit spreading done.
           (p_dest)[1] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[16]]) << 0)
             + ((uint_mmv_t)(b[p_perm[17]]) << 8)
             + ((uint_mmv_t)(b[p_perm[18]]) << 16)
             + ((uint_mmv_t)(b[p_perm[19]]) << 24)
             + ((uint_mmv_t)(b[p_perm[20]]) << 32)
             + ((uint_mmv_t)(b[p_perm[21]]) << 40)
             + ((uint_mmv_t)(b[p_perm[22]]) << 48)
             + ((uint_mmv_t)(b[p_perm[23]]) << 56);
           r1 = (p_sign)[0] >> 16;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0x1f if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 31;
           // Bit spreading done.
           (p_dest)[2] = r0 ^ r1;
           p_dest[3] = 0;
           p_dest += 4;
           p_perm += 24;
           p_sign += 1;
        }
        
    }

    ///////////////////////////////////////////////////////////////
    // Map tag X1 to tag T1 if e = 1
    // Map tag X0 to tag T1 if e = 2
    ///////////////////////////////////////////////////////////////
    p_src = v_in + 10456;
    p_src -= diff;
    p_dest = v_out + 3288;
    p_sign = p_tables[4].p_sign;
    p_perm = p_tables[4].p_perm;

    for (i = 0; i < 64; ++i) {
        p_b = b;
        
        for (j = 0; j < 16; ++j) {
           // %%OP_XI_LOAD p_src, p_b, %{i_src.SHAPE[2]}, uint8_t
           uint_mmv_t r0;
           r0 =  (p_src)[0];
           r0 &= 0x1f1f1f1f1f1f1f1fULL;
           (p_b)[0] = (uint8_t)(r0 >> 0);
           (p_b)[1] = (uint8_t)(r0 >> 8);
           (p_b)[2] = (uint8_t)(r0 >> 16);
           (p_b)[3] = (uint8_t)(r0 >> 24);
           (p_b)[4] = (uint8_t)(r0 >> 32);
           (p_b)[5] = (uint8_t)(r0 >> 40);
           (p_b)[6] = (uint8_t)(r0 >> 48);
           (p_b)[7] = (uint8_t)(r0 >> 56);
           r0 =  (p_src)[1];
           r0 &= 0x1f1f1f1f1f1f1f1fULL;
           (p_b)[8] = (uint8_t)(r0 >> 0);
           (p_b)[9] = (uint8_t)(r0 >> 8);
           (p_b)[10] = (uint8_t)(r0 >> 16);
           (p_b)[11] = (uint8_t)(r0 >> 24);
           (p_b)[12] = (uint8_t)(r0 >> 32);
           (p_b)[13] = (uint8_t)(r0 >> 40);
           (p_b)[14] = (uint8_t)(r0 >> 48);
           (p_b)[15] = (uint8_t)(r0 >> 56);
           r0 =  (p_src)[2];
           r0 &= 0x1f1f1f1f1f1f1f1fULL;
           (p_b)[16] = (uint8_t)(r0 >> 0);
           (p_b)[17] = (uint8_t)(r0 >> 8);
           (p_b)[18] = (uint8_t)(r0 >> 16);
           (p_b)[19] = (uint8_t)(r0 >> 24);
           (p_b)[20] = (uint8_t)(r0 >> 32);
           (p_b)[21] = (uint8_t)(r0 >> 40);
           (p_b)[22] = (uint8_t)(r0 >> 48);
           (p_b)[23] = (uint8_t)(r0 >> 56);
           p_src += 4;
           p_b += 32;
        }
        
        for (j = 0; j < 12; ++j) {
           // %%OP_XI_STORE b, p_perm, p_sign, p_dest, %{i_dest.SHAPE[2]}
           uint_mmv_t r0, r1;
           r0 = ((uint_mmv_t)(b[p_perm[0]]) << 0)
             + ((uint_mmv_t)(b[p_perm[1]]) << 8)
             + ((uint_mmv_t)(b[p_perm[2]]) << 16)
             + ((uint_mmv_t)(b[p_perm[3]]) << 24)
             + ((uint_mmv_t)(b[p_perm[4]]) << 32)
             + ((uint_mmv_t)(b[p_perm[5]]) << 40)
             + ((uint_mmv_t)(b[p_perm[6]]) << 48)
             + ((uint_mmv_t)(b[p_perm[7]]) << 56);
           r1 = (p_sign)[0] >> 0;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0x1f if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 31;
           // Bit spreading done.
           (p_dest)[0] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[8]]) << 0)
             + ((uint_mmv_t)(b[p_perm[9]]) << 8)
             + ((uint_mmv_t)(b[p_perm[10]]) << 16)
             + ((uint_mmv_t)(b[p_perm[11]]) << 24)
             + ((uint_mmv_t)(b[p_perm[12]]) << 32)
             + ((uint_mmv_t)(b[p_perm[13]]) << 40)
             + ((uint_mmv_t)(b[p_perm[14]]) << 48)
             + ((uint_mmv_t)(b[p_perm[15]]) << 56);
           r1 = (p_sign)[0] >> 8;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0x1f if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 31;
           // Bit spreading done.
           (p_dest)[1] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[16]]) << 0)
             + ((uint_mmv_t)(b[p_perm[17]]) << 8)
             + ((uint_mmv_t)(b[p_perm[18]]) << 16)
             + ((uint_mmv_t)(b[p_perm[19]]) << 24)
             + ((uint_mmv_t)(b[p_perm[20]]) << 32)
             + ((uint_mmv_t)(b[p_perm[21]]) << 40)
             + ((uint_mmv_t)(b[p_perm[22]]) << 48)
             + ((uint_mmv_t)(b[p_perm[23]]) << 56);
           r1 = (p_sign)[0] >> 16;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0x1f if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 31;
           // Bit spreading done.
           (p_dest)[2] = r0 ^ r1;
           r0 = ((uint_mmv_t)(b[p_perm[24]]) << 0)
             + ((uint_mmv_t)(b[p_perm[25]]) << 8)
             + ((uint_mmv_t)(b[p_perm[26]]) << 16)
             + ((uint_mmv_t)(b[p_perm[27]]) << 24)
             + ((uint_mmv_t)(b[p_perm[28]]) << 32)
             + ((uint_mmv_t)(b[p_perm[29]]) << 40)
             + ((uint_mmv_t)(b[p_perm[30]]) << 48)
             + ((uint_mmv_t)(b[p_perm[31]]) << 56);
           r1 = (p_sign)[0] >> 24;
           // Spread bits 0,...,7 of r1 to the (8-bit long) fields
           // of r1. A field of r1 is set to 0x1f if its 
           // corresponding bit in input r1 is one and to 0 otherwise.
           r1 = (r1 & 0xfULL) + ((r1 & 0xf0ULL) << 28);
           r1 = (r1 & 0x300000003ULL) 
               +  ((r1 & 0xc0000000cULL) << 14);
           r1 = (r1 & 0x1000100010001ULL) 
               +  ((r1 & 0x2000200020002ULL) << 7);
           r1 *= 31;
           // Bit spreading done.
           (p_dest)[3] = r0 ^ r1;
           p_dest += 4;
           p_perm += 32;
           p_sign += 1;
        }
        
    }
}

static uint_mmv_t TAB31_XI64_MASK[] = {
// %%TABLE TABLE_MUL_MATRIX_XI64, uint%{INT_BITS}
0x0000001f0000001fULL,0x0000000000000000ULL,
0x0000001f0000001fULL,0x1f1f1f1f1f1f1f1fULL,
0x0000000000000000ULL,0x0000001f0000001fULL,
0x1f1f1f1f1f1f1f1fULL,0x0000001f0000001fULL
};


#define HALF_YZ_SHIFT 12

static uint32_t TAB31_XI64_OFFSET[2][4] = {
    {
        MM_OP31_OFS_Z + (2 << HALF_YZ_SHIFT),
        MM_OP31_OFS_Z + (0 << HALF_YZ_SHIFT),
        MM_OP31_OFS_Z + (1 << HALF_YZ_SHIFT),
        MM_OP31_OFS_Z + (3 << HALF_YZ_SHIFT)
    },
    {
        MM_OP31_OFS_Z + (1 << HALF_YZ_SHIFT),
        MM_OP31_OFS_Z + (2 << HALF_YZ_SHIFT),
        MM_OP31_OFS_Z + (0 << HALF_YZ_SHIFT),
        MM_OP31_OFS_Z + (3 << HALF_YZ_SHIFT)
    },
};




static void mm_op31_xi_yz(uint_mmv_t *v_in,  uint32_t exp1, uint_mmv_t *v_out)
{
    uint_fast32_t i1;
    uint_mmv_t *p_mask =  TAB31_XI64_MASK + exp1;
    for (i1 = 0; i1 < 64; ++i1) {
        // %%MUL_MATRIX_XI64 v_in, p_mask, v_out

        // This is an automatically generated matrix operation, do not change!
        {
        uint_mmv_t r0, r1, r2, r3, r4;
        uint_mmv_t r5, r6, r7, r8, r9;
        uint_mmv_t r10, r11, r12, r13, r14;
        uint_mmv_t r15, r16;

        uint_fast32_t i;

        // TODO: write comment!!!
        // 
        for (i = 0; i < 3; ++i) {
        r0 = v_in[0] ^  p_mask[2];
        r16 = ((r0 ^ (r0 >> 8)) & 0x1f0000001f00ULL); // 3 ops
        r0 ^= (r16 | (r16 << 8)); // 3 ops
        r1 = v_in[56] ^  p_mask[0];
        r16 = ((r1 ^ (r1 >> 8)) & 0x1f0000001f00ULL); // 3 ops
        r1 ^= (r16 | (r16 << 8)); // 3 ops
        r2 = v_in[52] ^  p_mask[0];
        r16 = ((r2 ^ (r2 >> 8)) & 0x1f0000001f00ULL); // 3 ops
        r2 ^= (r16 | (r16 << 8)); // 3 ops
        r3 = v_in[12] ^  p_mask[0];
        r16 = ((r3 ^ (r3 >> 8)) & 0x1f0000001f00ULL); // 3 ops
        r3 ^= (r16 | (r16 << 8)); // 3 ops
        r4 = v_in[44] ^  p_mask[0];
        r16 = ((r4 ^ (r4 >> 8)) & 0x1f0000001f00ULL); // 3 ops
        r4 ^= (r16 | (r16 << 8)); // 3 ops
        r5 = v_in[20] ^  p_mask[0];
        r16 = ((r5 ^ (r5 >> 8)) & 0x1f0000001f00ULL); // 3 ops
        r5 ^= (r16 | (r16 << 8)); // 3 ops
        r6 = v_in[24] ^  p_mask[0];
        r16 = ((r6 ^ (r6 >> 8)) & 0x1f0000001f00ULL); // 3 ops
        r6 ^= (r16 | (r16 << 8)); // 3 ops
        r7 = v_in[32] ^  p_mask[2];
        r16 = ((r7 ^ (r7 >> 8)) & 0x1f0000001f00ULL); // 3 ops
        r7 ^= (r16 | (r16 << 8)); // 3 ops
        r8 = v_in[28] ^  p_mask[0];
        r16 = ((r8 ^ (r8 >> 8)) & 0x1f0000001f00ULL); // 3 ops
        r8 ^= (r16 | (r16 << 8)); // 3 ops
        r9 = v_in[36] ^  p_mask[0];
        r16 = ((r9 ^ (r9 >> 8)) & 0x1f0000001f00ULL); // 3 ops
        r9 ^= (r16 | (r16 << 8)); // 3 ops
        r10 = v_in[40] ^  p_mask[0];
        r16 = ((r10 ^ (r10 >> 8)) & 0x1f0000001f00ULL); // 3 ops
        r10 ^= (r16 | (r16 << 8)); // 3 ops
        r11 = v_in[16] ^  p_mask[2];
        r16 = ((r11 ^ (r11 >> 8)) & 0x1f0000001f00ULL); // 3 ops
        r11 ^= (r16 | (r16 << 8)); // 3 ops
        r12 = v_in[48] ^  p_mask[0];
        r16 = ((r12 ^ (r12 >> 8)) & 0x1f0000001f00ULL); // 3 ops
        r12 ^= (r16 | (r16 << 8)); // 3 ops
        r13 = v_in[8] ^  p_mask[2];
        r16 = ((r13 ^ (r13 >> 8)) & 0x1f0000001f00ULL); // 3 ops
        r13 ^= (r16 | (r16 << 8)); // 3 ops
        r14 = v_in[4] ^  p_mask[2];
        r16 = ((r14 ^ (r14 >> 8)) & 0x1f0000001f00ULL); // 3 ops
        r14 ^= (r16 | (r16 << 8)); // 3 ops
        r15 = v_in[60] ^  p_mask[2];
        r16 = ((r15 ^ (r15 >> 8)) & 0x1f0000001f00ULL); // 3 ops
        r15 ^= (r16 | (r16 << 8)); // 3 ops
        // Butterfly: v[i], v[i+1] = v[i]+v[i+1], v[i]-v[i+1]
        r16 = (((r0 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r0 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r0 = ((r0 ^ 0x1f001f001f001f00ULL) + r16); // 2 ops
        r16 = (r0 & 0x2020202020202020ULL);
        r0 = ((r0 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r1 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r1 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r1 = ((r1 ^ 0x1f001f001f001f00ULL) + r16); // 2 ops
        r16 = (r1 & 0x2020202020202020ULL);
        r1 = ((r1 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r2 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r2 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r2 = ((r2 ^ 0x1f001f001f001f00ULL) + r16); // 2 ops
        r16 = (r2 & 0x2020202020202020ULL);
        r2 = ((r2 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r3 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r3 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r3 = ((r3 ^ 0x1f001f001f001f00ULL) + r16); // 2 ops
        r16 = (r3 & 0x2020202020202020ULL);
        r3 = ((r3 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r4 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r4 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r4 = ((r4 ^ 0x1f001f001f001f00ULL) + r16); // 2 ops
        r16 = (r4 & 0x2020202020202020ULL);
        r4 = ((r4 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r5 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r5 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r5 = ((r5 ^ 0x1f001f001f001f00ULL) + r16); // 2 ops
        r16 = (r5 & 0x2020202020202020ULL);
        r5 = ((r5 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r6 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r6 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r6 = ((r6 ^ 0x1f001f001f001f00ULL) + r16); // 2 ops
        r16 = (r6 & 0x2020202020202020ULL);
        r6 = ((r6 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r7 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r7 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r7 = ((r7 ^ 0x1f001f001f001f00ULL) + r16); // 2 ops
        r16 = (r7 & 0x2020202020202020ULL);
        r7 = ((r7 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r8 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r8 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r8 = ((r8 ^ 0x1f001f001f001f00ULL) + r16); // 2 ops
        r16 = (r8 & 0x2020202020202020ULL);
        r8 = ((r8 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r9 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r9 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r9 = ((r9 ^ 0x1f001f001f001f00ULL) + r16); // 2 ops
        r16 = (r9 & 0x2020202020202020ULL);
        r9 = ((r9 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r10 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r10 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r10 = ((r10 ^ 0x1f001f001f001f00ULL) + r16); // 2 ops
        r16 = (r10 & 0x2020202020202020ULL);
        r10 = ((r10 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r11 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r11 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r11 = ((r11 ^ 0x1f001f001f001f00ULL) + r16); // 2 ops
        r16 = (r11 & 0x2020202020202020ULL);
        r11 = ((r11 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r12 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r12 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r12 = ((r12 ^ 0x1f001f001f001f00ULL) + r16); // 2 ops
        r16 = (r12 & 0x2020202020202020ULL);
        r12 = ((r12 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r13 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r13 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r13 = ((r13 ^ 0x1f001f001f001f00ULL) + r16); // 2 ops
        r16 = (r13 & 0x2020202020202020ULL);
        r13 = ((r13 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r14 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r14 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r14 = ((r14 ^ 0x1f001f001f001f00ULL) + r16); // 2 ops
        r16 = (r14 & 0x2020202020202020ULL);
        r14 = ((r14 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r15 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r15 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r15 = ((r15 ^ 0x1f001f001f001f00ULL) + r16); // 2 ops
        r16 = (r15 & 0x2020202020202020ULL);
        r15 = ((r15 - r16) + (r16 >> 5)); // 3 ops
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        // Butterfly: v[i], v[i+2] = v[i]+v[i+2], v[i]-v[i+2]
        r16 = (((r0 << 16) & 0xffff0000ffff0000ULL)
            | ((r0 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r0 = ((r0 ^ 0x1f1f00001f1f0000ULL) + r16); // 2 ops
        r16 = (r0 & 0x2020202020202020ULL);
        r0 = ((r0 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r1 << 16) & 0xffff0000ffff0000ULL)
            | ((r1 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r1 = ((r1 ^ 0x1f1f00001f1f0000ULL) + r16); // 2 ops
        r16 = (r1 & 0x2020202020202020ULL);
        r1 = ((r1 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r2 << 16) & 0xffff0000ffff0000ULL)
            | ((r2 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r2 = ((r2 ^ 0x1f1f00001f1f0000ULL) + r16); // 2 ops
        r16 = (r2 & 0x2020202020202020ULL);
        r2 = ((r2 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r3 << 16) & 0xffff0000ffff0000ULL)
            | ((r3 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r3 = ((r3 ^ 0x1f1f00001f1f0000ULL) + r16); // 2 ops
        r16 = (r3 & 0x2020202020202020ULL);
        r3 = ((r3 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r4 << 16) & 0xffff0000ffff0000ULL)
            | ((r4 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r4 = ((r4 ^ 0x1f1f00001f1f0000ULL) + r16); // 2 ops
        r16 = (r4 & 0x2020202020202020ULL);
        r4 = ((r4 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r5 << 16) & 0xffff0000ffff0000ULL)
            | ((r5 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r5 = ((r5 ^ 0x1f1f00001f1f0000ULL) + r16); // 2 ops
        r16 = (r5 & 0x2020202020202020ULL);
        r5 = ((r5 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r6 << 16) & 0xffff0000ffff0000ULL)
            | ((r6 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r6 = ((r6 ^ 0x1f1f00001f1f0000ULL) + r16); // 2 ops
        r16 = (r6 & 0x2020202020202020ULL);
        r6 = ((r6 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r7 << 16) & 0xffff0000ffff0000ULL)
            | ((r7 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r7 = ((r7 ^ 0x1f1f00001f1f0000ULL) + r16); // 2 ops
        r16 = (r7 & 0x2020202020202020ULL);
        r7 = ((r7 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r8 << 16) & 0xffff0000ffff0000ULL)
            | ((r8 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r8 = ((r8 ^ 0x1f1f00001f1f0000ULL) + r16); // 2 ops
        r16 = (r8 & 0x2020202020202020ULL);
        r8 = ((r8 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r9 << 16) & 0xffff0000ffff0000ULL)
            | ((r9 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r9 = ((r9 ^ 0x1f1f00001f1f0000ULL) + r16); // 2 ops
        r16 = (r9 & 0x2020202020202020ULL);
        r9 = ((r9 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r10 << 16) & 0xffff0000ffff0000ULL)
            | ((r10 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r10 = ((r10 ^ 0x1f1f00001f1f0000ULL) + r16); // 2 ops
        r16 = (r10 & 0x2020202020202020ULL);
        r10 = ((r10 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r11 << 16) & 0xffff0000ffff0000ULL)
            | ((r11 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r11 = ((r11 ^ 0x1f1f00001f1f0000ULL) + r16); // 2 ops
        r16 = (r11 & 0x2020202020202020ULL);
        r11 = ((r11 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r12 << 16) & 0xffff0000ffff0000ULL)
            | ((r12 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r12 = ((r12 ^ 0x1f1f00001f1f0000ULL) + r16); // 2 ops
        r16 = (r12 & 0x2020202020202020ULL);
        r12 = ((r12 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r13 << 16) & 0xffff0000ffff0000ULL)
            | ((r13 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r13 = ((r13 ^ 0x1f1f00001f1f0000ULL) + r16); // 2 ops
        r16 = (r13 & 0x2020202020202020ULL);
        r13 = ((r13 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r14 << 16) & 0xffff0000ffff0000ULL)
            | ((r14 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r14 = ((r14 ^ 0x1f1f00001f1f0000ULL) + r16); // 2 ops
        r16 = (r14 & 0x2020202020202020ULL);
        r14 = ((r14 - r16) + (r16 >> 5)); // 3 ops
        r16 = (((r15 << 16) & 0xffff0000ffff0000ULL)
            | ((r15 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r15 = ((r15 ^ 0x1f1f00001f1f0000ULL) + r16); // 2 ops
        r16 = (r15 & 0x2020202020202020ULL);
        r15 = ((r15 - r16) + (r16 >> 5)); // 3 ops
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        // Butterfly: v[i], v[i+8] = v[i]+v[i+8], v[i]-v[i+8]
        r16 = (r0 + (r1 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r0 = (r0 + r1);
        r1 = (r16 & 0x2020202020202020ULL);
        r1 = ((r16 - r1) + (r1 >> 5)); // 3 ops
        r16 = (r0 & 0x2020202020202020ULL);
        r0 = ((r0 - r16) + (r16 >> 5)); // 3 ops
        r16 = (r2 + (r3 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r2 = (r2 + r3);
        r3 = (r16 & 0x2020202020202020ULL);
        r3 = ((r16 - r3) + (r3 >> 5)); // 3 ops
        r16 = (r2 & 0x2020202020202020ULL);
        r2 = ((r2 - r16) + (r16 >> 5)); // 3 ops
        r16 = (r4 + (r5 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r4 = (r4 + r5);
        r5 = (r16 & 0x2020202020202020ULL);
        r5 = ((r16 - r5) + (r5 >> 5)); // 3 ops
        r16 = (r4 & 0x2020202020202020ULL);
        r4 = ((r4 - r16) + (r16 >> 5)); // 3 ops
        r16 = (r6 + (r7 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r6 = (r6 + r7);
        r7 = (r16 & 0x2020202020202020ULL);
        r7 = ((r16 - r7) + (r7 >> 5)); // 3 ops
        r16 = (r6 & 0x2020202020202020ULL);
        r6 = ((r6 - r16) + (r16 >> 5)); // 3 ops
        r16 = (r8 + (r9 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r8 = (r8 + r9);
        r9 = (r16 & 0x2020202020202020ULL);
        r9 = ((r16 - r9) + (r9 >> 5)); // 3 ops
        r16 = (r8 & 0x2020202020202020ULL);
        r8 = ((r8 - r16) + (r16 >> 5)); // 3 ops
        r16 = (r10 + (r11 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r10 = (r10 + r11);
        r11 = (r16 & 0x2020202020202020ULL);
        r11 = ((r16 - r11) + (r11 >> 5)); // 3 ops
        r16 = (r10 & 0x2020202020202020ULL);
        r10 = ((r10 - r16) + (r16 >> 5)); // 3 ops
        r16 = (r12 + (r13 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r12 = (r12 + r13);
        r13 = (r16 & 0x2020202020202020ULL);
        r13 = ((r16 - r13) + (r13 >> 5)); // 3 ops
        r16 = (r12 & 0x2020202020202020ULL);
        r12 = ((r12 - r16) + (r16 >> 5)); // 3 ops
        r16 = (r14 + (r15 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r14 = (r14 + r15);
        r15 = (r16 & 0x2020202020202020ULL);
        r15 = ((r16 - r15) + (r15 >> 5)); // 3 ops
        r16 = (r14 & 0x2020202020202020ULL);
        r14 = ((r14 - r16) + (r16 >> 5)); // 3 ops
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        // Butterfly: v[i], v[i+16] = v[i]+v[i+16], v[i]-v[i+16]
        r16 = (r0 + (r2 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r0 = (r0 + r2);
        r2 = (r16 & 0x2020202020202020ULL);
        r2 = ((r16 - r2) + (r2 >> 5)); // 3 ops
        r16 = (r0 & 0x2020202020202020ULL);
        r0 = ((r0 - r16) + (r16 >> 5)); // 3 ops
        r16 = (r1 + (r3 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r1 = (r1 + r3);
        r3 = (r16 & 0x2020202020202020ULL);
        r3 = ((r16 - r3) + (r3 >> 5)); // 3 ops
        r16 = (r1 & 0x2020202020202020ULL);
        r1 = ((r1 - r16) + (r16 >> 5)); // 3 ops
        r16 = (r4 + (r6 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r4 = (r4 + r6);
        r6 = (r16 & 0x2020202020202020ULL);
        r6 = ((r16 - r6) + (r6 >> 5)); // 3 ops
        r16 = (r4 & 0x2020202020202020ULL);
        r4 = ((r4 - r16) + (r16 >> 5)); // 3 ops
        r16 = (r5 + (r7 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r5 = (r5 + r7);
        r7 = (r16 & 0x2020202020202020ULL);
        r7 = ((r16 - r7) + (r7 >> 5)); // 3 ops
        r16 = (r5 & 0x2020202020202020ULL);
        r5 = ((r5 - r16) + (r16 >> 5)); // 3 ops
        r16 = (r8 + (r10 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r8 = (r8 + r10);
        r10 = (r16 & 0x2020202020202020ULL);
        r10 = ((r16 - r10) + (r10 >> 5)); // 3 ops
        r16 = (r8 & 0x2020202020202020ULL);
        r8 = ((r8 - r16) + (r16 >> 5)); // 3 ops
        r16 = (r9 + (r11 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r9 = (r9 + r11);
        r11 = (r16 & 0x2020202020202020ULL);
        r11 = ((r16 - r11) + (r11 >> 5)); // 3 ops
        r16 = (r9 & 0x2020202020202020ULL);
        r9 = ((r9 - r16) + (r16 >> 5)); // 3 ops
        r16 = (r12 + (r14 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r12 = (r12 + r14);
        r14 = (r16 & 0x2020202020202020ULL);
        r14 = ((r16 - r14) + (r14 >> 5)); // 3 ops
        r16 = (r12 & 0x2020202020202020ULL);
        r12 = ((r12 - r16) + (r16 >> 5)); // 3 ops
        r16 = (r13 + (r15 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r13 = (r13 + r15);
        r15 = (r16 & 0x2020202020202020ULL);
        r15 = ((r16 - r15) + (r15 >> 5)); // 3 ops
        r16 = (r13 & 0x2020202020202020ULL);
        r13 = ((r13 - r16) + (r16 >> 5)); // 3 ops
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        // Butterfly: v[i], v[i+32] = v[i]+v[i+32], v[i]-v[i+32]
        r16 = (r0 + (r4 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r0 = (r0 + r4);
        r4 = (r16 & 0x2020202020202020ULL);
        r4 = ((r16 - r4) + (r4 >> 5)); // 3 ops
        r16 = (r0 & 0x2020202020202020ULL);
        r0 = ((r0 - r16) + (r16 >> 5)); // 3 ops
        r16 = (r1 + (r5 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r1 = (r1 + r5);
        r5 = (r16 & 0x2020202020202020ULL);
        r5 = ((r16 - r5) + (r5 >> 5)); // 3 ops
        r16 = (r1 & 0x2020202020202020ULL);
        r1 = ((r1 - r16) + (r16 >> 5)); // 3 ops
        r16 = (r2 + (r6 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r2 = (r2 + r6);
        r6 = (r16 & 0x2020202020202020ULL);
        r6 = ((r16 - r6) + (r6 >> 5)); // 3 ops
        r16 = (r2 & 0x2020202020202020ULL);
        r2 = ((r2 - r16) + (r16 >> 5)); // 3 ops
        r16 = (r3 + (r7 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r3 = (r3 + r7);
        r7 = (r16 & 0x2020202020202020ULL);
        r7 = ((r16 - r7) + (r7 >> 5)); // 3 ops
        r16 = (r3 & 0x2020202020202020ULL);
        r3 = ((r3 - r16) + (r16 >> 5)); // 3 ops
        r16 = (r8 + (r12 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r8 = (r8 + r12);
        r12 = (r16 & 0x2020202020202020ULL);
        r12 = ((r16 - r12) + (r12 >> 5)); // 3 ops
        r16 = (r8 & 0x2020202020202020ULL);
        r8 = ((r8 - r16) + (r16 >> 5)); // 3 ops
        r16 = (r9 + (r13 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r9 = (r9 + r13);
        r13 = (r16 & 0x2020202020202020ULL);
        r13 = ((r16 - r13) + (r13 >> 5)); // 3 ops
        r16 = (r9 & 0x2020202020202020ULL);
        r9 = ((r9 - r16) + (r16 >> 5)); // 3 ops
        r16 = (r10 + (r14 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r10 = (r10 + r14);
        r14 = (r16 & 0x2020202020202020ULL);
        r14 = ((r16 - r14) + (r14 >> 5)); // 3 ops
        r16 = (r10 & 0x2020202020202020ULL);
        r10 = ((r10 - r16) + (r16 >> 5)); // 3 ops
        r16 = (r11 + (r15 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r11 = (r11 + r15);
        r15 = (r16 & 0x2020202020202020ULL);
        r15 = ((r16 - r15) + (r15 >> 5)); // 3 ops
        r16 = (r11 & 0x2020202020202020ULL);
        r11 = ((r11 - r16) + (r16 >> 5)); // 3 ops
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        // Butterfly: v[i], v[i+64] = v[i]+v[i+64], v[i]-v[i+64]
        r16 = (r0 + (r8 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r0 = (r0 + r8);
        r8 = (r16 & 0x2020202020202020ULL);
        r8 = ((r16 - r8) + (r8 >> 5)); // 3 ops
        r16 = (r0 & 0x2020202020202020ULL);
        r0 = ((r0 - r16) + (r16 >> 5)); // 3 ops
        r16 = (r1 + (r9 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r1 = (r1 + r9);
        r9 = (r16 & 0x2020202020202020ULL);
        r9 = ((r16 - r9) + (r9 >> 5)); // 3 ops
        r16 = (r1 & 0x2020202020202020ULL);
        r1 = ((r1 - r16) + (r16 >> 5)); // 3 ops
        r16 = (r2 + (r10 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r2 = (r2 + r10);
        r10 = (r16 & 0x2020202020202020ULL);
        r10 = ((r16 - r10) + (r10 >> 5)); // 3 ops
        r16 = (r2 & 0x2020202020202020ULL);
        r2 = ((r2 - r16) + (r16 >> 5)); // 3 ops
        r16 = (r3 + (r11 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r3 = (r3 + r11);
        r11 = (r16 & 0x2020202020202020ULL);
        r11 = ((r16 - r11) + (r11 >> 5)); // 3 ops
        r16 = (r3 & 0x2020202020202020ULL);
        r3 = ((r3 - r16) + (r16 >> 5)); // 3 ops
        r16 = (r4 + (r12 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r4 = (r4 + r12);
        r12 = (r16 & 0x2020202020202020ULL);
        r12 = ((r16 - r12) + (r12 >> 5)); // 3 ops
        r16 = (r4 & 0x2020202020202020ULL);
        r4 = ((r4 - r16) + (r16 >> 5)); // 3 ops
        r16 = (r5 + (r13 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r5 = (r5 + r13);
        r13 = (r16 & 0x2020202020202020ULL);
        r13 = ((r16 - r13) + (r13 >> 5)); // 3 ops
        r16 = (r5 & 0x2020202020202020ULL);
        r5 = ((r5 - r16) + (r16 >> 5)); // 3 ops
        r16 = (r6 + (r14 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r6 = (r6 + r14);
        r14 = (r16 & 0x2020202020202020ULL);
        r14 = ((r16 - r14) + (r14 >> 5)); // 3 ops
        r16 = (r6 & 0x2020202020202020ULL);
        r6 = ((r6 - r16) + (r16 >> 5)); // 3 ops
        r16 = (r7 + (r15 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r7 = (r7 + r15);
        r15 = (r16 & 0x2020202020202020ULL);
        r15 = ((r16 - r15) + (r15 >> 5)); // 3 ops
        r16 = (r7 & 0x2020202020202020ULL);
        r7 = ((r7 - r16) + (r16 >> 5)); // 3 ops
        // Vector is now  r(i) for i = 
        //  0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        // Multiply vector by scalar 2**-3 mod 31
        r0 = (((r0 & 0x707070707070707ULL) << 2)
            | ((r0 & 0x1818181818181818ULL) >> 3)); // 5 ops
        r1 = (((r1 & 0x707070707070707ULL) << 2)
            | ((r1 & 0x1818181818181818ULL) >> 3)); // 5 ops
        r2 = (((r2 & 0x707070707070707ULL) << 2)
            | ((r2 & 0x1818181818181818ULL) >> 3)); // 5 ops
        r3 = (((r3 & 0x707070707070707ULL) << 2)
            | ((r3 & 0x1818181818181818ULL) >> 3)); // 5 ops
        r4 = (((r4 & 0x707070707070707ULL) << 2)
            | ((r4 & 0x1818181818181818ULL) >> 3)); // 5 ops
        r5 = (((r5 & 0x707070707070707ULL) << 2)
            | ((r5 & 0x1818181818181818ULL) >> 3)); // 5 ops
        r6 = (((r6 & 0x707070707070707ULL) << 2)
            | ((r6 & 0x1818181818181818ULL) >> 3)); // 5 ops
        r7 = (((r7 & 0x707070707070707ULL) << 2)
            | ((r7 & 0x1818181818181818ULL) >> 3)); // 5 ops
        r8 = (((r8 & 0x707070707070707ULL) << 2)
            | ((r8 & 0x1818181818181818ULL) >> 3)); // 5 ops
        r9 = (((r9 & 0x707070707070707ULL) << 2)
            | ((r9 & 0x1818181818181818ULL) >> 3)); // 5 ops
        r10 = (((r10 & 0x707070707070707ULL) << 2)
            | ((r10 & 0x1818181818181818ULL) >> 3)); // 5 ops
        r11 = (((r11 & 0x707070707070707ULL) << 2)
            | ((r11 & 0x1818181818181818ULL) >> 3)); // 5 ops
        r12 = (((r12 & 0x707070707070707ULL) << 2)
            | ((r12 & 0x1818181818181818ULL) >> 3)); // 5 ops
        r13 = (((r13 & 0x707070707070707ULL) << 2)
            | ((r13 & 0x1818181818181818ULL) >> 3)); // 5 ops
        r14 = (((r14 & 0x707070707070707ULL) << 2)
            | ((r14 & 0x1818181818181818ULL) >> 3)); // 5 ops
        r15 = (((r15 & 0x707070707070707ULL) << 2)
            | ((r15 & 0x1818181818181818ULL) >> 3)); // 5 ops
        v_out[0] = r0 ^  p_mask[6];
        v_out[4] = r1 ^  p_mask[6];
        v_out[8] = r2 ^  p_mask[6];
        v_out[12] = r3 ^  p_mask[4];
        v_out[16] = r4 ^  p_mask[6];
        v_out[20] = r5 ^  p_mask[4];
        v_out[24] = r6 ^  p_mask[4];
        v_out[28] = r7 ^  p_mask[4];
        v_out[32] = r8 ^  p_mask[6];
        v_out[36] = r9 ^  p_mask[4];
        v_out[40] = r10 ^  p_mask[4];
        v_out[44] = r11 ^  p_mask[4];
        v_out[48] = r12 ^  p_mask[4];
        v_out[52] = r13 ^  p_mask[4];
        v_out[56] = r14 ^  p_mask[4];
        v_out[60] = r15 ^  p_mask[6];
        v_in++;
        v_out++;
        }
        v_out[0] = 0;
        v_out[4] = 0;
        v_out[8] = 0;
        v_out[12] = 0;
        v_out[16] = 0;
        v_out[20] = 0;
        v_out[24] = 0;
        v_out[28] = 0;
        v_out[32] = 0;
        v_out[36] = 0;
        v_out[40] = 0;
        v_out[44] = 0;
        v_out[48] = 0;
        v_out[52] = 0;
        v_out[56] = 0;
        v_out[60] = 0;
        v_in += 61;
        v_out += 61;
        }
        // End of automatically generated matrix operation.
 
    }
}  


static void mm_op31_xi_a(uint_mmv_t *v_in,  uint32_t exp1, uint_mmv_t *v_out)
{
    uint_fast32_t i1;
    uint_mmv_t e_mask =  0 - ((uint_mmv_t)exp1 & 0x1ULL);
    for (i1 = 0; i1 < 6; ++i1) {
        // %%MUL_MATRIX_XI16 v_in, e_mask, v_out

        // This is an automatically generated matrix operation, do not change!
        {
        uint_mmv_t r0, r1, r2, r3, r4;

        uint_fast32_t i;
        // TODO: write comment!!!
        // 
        for (i = 0; i < 3; ++i) {
        e_mask = ~(e_mask);
        r0 = v_in[0] ^  (0x1f1f1f001f1f1f00ULL & e_mask);
        r4 = ((r0 ^ (r0 >> 8)) & 0x1f0000001f00ULL); // 3 ops
        r0 ^= (r4 | (r4 << 8)); // 3 ops
        r1 = v_in[8] ^  (0x1f0000001fULL & e_mask);
        r4 = ((r1 ^ (r1 >> 8)) & 0x1f0000001f00ULL); // 3 ops
        r1 ^= (r4 | (r4 << 8)); // 3 ops
        r2 = v_in[4] ^  (0x1f0000001fULL & e_mask);
        r4 = ((r2 ^ (r2 >> 8)) & 0x1f0000001f00ULL); // 3 ops
        r2 ^= (r4 | (r4 << 8)); // 3 ops
        r3 = v_in[12] ^  (0x1f0000001fULL & e_mask);
        r4 = ((r3 ^ (r3 >> 8)) & 0x1f0000001f00ULL); // 3 ops
        r3 ^= (r4 | (r4 << 8)); // 3 ops
        // Butterfly: v[i], v[i+1] = v[i]+v[i+1], v[i]-v[i+1]
        r4 = (((r0 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r0 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r0 = ((r0 ^ 0x1f001f001f001f00ULL) + r4); // 2 ops
        r4 = (r0 & 0x2020202020202020ULL);
        r0 = ((r0 - r4) + (r4 >> 5)); // 3 ops
        r4 = (((r1 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r1 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r1 = ((r1 ^ 0x1f001f001f001f00ULL) + r4); // 2 ops
        r4 = (r1 & 0x2020202020202020ULL);
        r1 = ((r1 - r4) + (r4 >> 5)); // 3 ops
        r4 = (((r2 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r2 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r2 = ((r2 ^ 0x1f001f001f001f00ULL) + r4); // 2 ops
        r4 = (r2 & 0x2020202020202020ULL);
        r2 = ((r2 - r4) + (r4 >> 5)); // 3 ops
        r4 = (((r3 << 8) & 0xff00ff00ff00ff00ULL)
            | ((r3 & 0xff00ff00ff00ff00ULL) >> 8)); // 5 ops
        r3 = ((r3 ^ 0x1f001f001f001f00ULL) + r4); // 2 ops
        r4 = (r3 & 0x2020202020202020ULL);
        r3 = ((r3 - r4) + (r4 >> 5)); // 3 ops
        // Vector is now  r(i) for i = 0,1,2,3
        // Butterfly: v[i], v[i+2] = v[i]+v[i+2], v[i]-v[i+2]
        r4 = (((r0 << 16) & 0xffff0000ffff0000ULL)
            | ((r0 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r0 = ((r0 ^ 0x1f1f00001f1f0000ULL) + r4); // 2 ops
        r4 = (r0 & 0x2020202020202020ULL);
        r0 = ((r0 - r4) + (r4 >> 5)); // 3 ops
        r4 = (((r1 << 16) & 0xffff0000ffff0000ULL)
            | ((r1 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r1 = ((r1 ^ 0x1f1f00001f1f0000ULL) + r4); // 2 ops
        r4 = (r1 & 0x2020202020202020ULL);
        r1 = ((r1 - r4) + (r4 >> 5)); // 3 ops
        r4 = (((r2 << 16) & 0xffff0000ffff0000ULL)
            | ((r2 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r2 = ((r2 ^ 0x1f1f00001f1f0000ULL) + r4); // 2 ops
        r4 = (r2 & 0x2020202020202020ULL);
        r2 = ((r2 - r4) + (r4 >> 5)); // 3 ops
        r4 = (((r3 << 16) & 0xffff0000ffff0000ULL)
            | ((r3 & 0xffff0000ffff0000ULL) >> 16)); // 5 ops
        r3 = ((r3 ^ 0x1f1f00001f1f0000ULL) + r4); // 2 ops
        r4 = (r3 & 0x2020202020202020ULL);
        r3 = ((r3 - r4) + (r4 >> 5)); // 3 ops
        // Vector is now  r(i) for i = 0,1,2,3
        // Butterfly: v[i], v[i+8] = v[i]+v[i+8], v[i]-v[i+8]
        r4 = (r0 + (r1 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r0 = (r0 + r1);
        r1 = (r4 & 0x2020202020202020ULL);
        r1 = ((r4 - r1) + (r1 >> 5)); // 3 ops
        r4 = (r0 & 0x2020202020202020ULL);
        r0 = ((r0 - r4) + (r4 >> 5)); // 3 ops
        r4 = (r2 + (r3 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r2 = (r2 + r3);
        r3 = (r4 & 0x2020202020202020ULL);
        r3 = ((r4 - r3) + (r3 >> 5)); // 3 ops
        r4 = (r2 & 0x2020202020202020ULL);
        r2 = ((r2 - r4) + (r4 >> 5)); // 3 ops
        // Vector is now  r(i) for i = 0,1,2,3
        // Butterfly: v[i], v[i+16] = v[i]+v[i+16], v[i]-v[i+16]
        r4 = (r0 + (r2 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r0 = (r0 + r2);
        r2 = (r4 & 0x2020202020202020ULL);
        r2 = ((r4 - r2) + (r2 >> 5)); // 3 ops
        r4 = (r0 & 0x2020202020202020ULL);
        r0 = ((r0 - r4) + (r4 >> 5)); // 3 ops
        r4 = (r1 + (r3 ^ 0x1f1f1f1f1f1f1f1fULL)); // 2 ops
        r1 = (r1 + r3);
        r3 = (r4 & 0x2020202020202020ULL);
        r3 = ((r4 - r3) + (r3 >> 5)); // 3 ops
        r4 = (r1 & 0x2020202020202020ULL);
        r1 = ((r1 - r4) + (r4 >> 5)); // 3 ops
        // Vector is now  r(i) for i = 0,1,2,3
        // Multiplication by 2**0 is trivial mod 31
        e_mask = ~(e_mask);
        r0 = (((r0 & 0x303030303030303ULL) << 3)
            | ((r0 & 0x1c1c1c1c1c1c1c1cULL) >> 2)); // 5 ops
        v_out[0] = r0 ^ (e_mask & 0x1f1f1f001f1f1f00ULL);
        r1 = (((r1 & 0x303030303030303ULL) << 3)
            | ((r1 & 0x1c1c1c1c1c1c1c1cULL) >> 2)); // 5 ops
        v_out[4] = r1 ^ (e_mask & 0x1f0000001fULL);
        r2 = (((r2 & 0x303030303030303ULL) << 3)
            | ((r2 & 0x1c1c1c1c1c1c1c1cULL) >> 2)); // 5 ops
        v_out[8] = r2 ^ (e_mask & 0x1f0000001fULL);
        r3 = (((r3 & 0x303030303030303ULL) << 3)
            | ((r3 & 0x1c1c1c1c1c1c1c1cULL) >> 2)); // 5 ops
        v_out[12] = r3 ^ (e_mask & 0x1f0000001fULL);
        // 78 lines of code, 186 operations
        v_in++;
        v_out++;
        }
        v_out[0] = 0;
        v_out[4] = 0;
        v_out[8] = 0;
        v_out[12] = 0;
        v_in += 13;
        v_out += 13;
        }
        // End of automatically generated matrix operation.
 
    }
}  

/// @endcond 


/**
  @brief Compute an operation of the monster group on a vector

  Let ``v_in`` be a vector of the representation \f$\rho_{31}\f$
  of the monster group.

  The function implements the operation of the element \f$\xi^e\f$ 
  of the monster group  on a vector ``v_in`` in the 
  representation \f$\rho_{31}\f$ of the monster.

  Parameter ``exp`` is the exponent \f$e\f$ of the generator 
  \f$\xi^e\f$. The function computes the operation of \f$\xi^e\f$  
  on the input  vector ``v_in`` and  stores the result in the output 
  vector ``v_out.`` 

  Input vector  ``v_in`` is not changed.
*/
// %%EXPORT px
MM_OP31_API
void mm_op31_xi(uint_mmv_t *v_in,  uint32_t exp, uint_mmv_t *v_out)
{
    uint_mmv_t i;
    uint32_t exp1;

    exp %= 3;
    if (exp == 0) {
        for (i = 0; i < 30936; ++i) v_out[i] = v_in[i];
        return;
    }
    exp1 =  exp - 1;

    // Do monomial part, i.e. tags B, C, T, X
    // Caution: this uses v_out[MM_OP31_OFS_Z:] as temporary storage
    mm_op31_xi_mon(v_in, exp1, v_out);

    // Do tag A
    mm_op31_xi_a(v_in, exp1, v_out); 

    // Do tags X, Y
    for (i = 0; i < 4; ++i) {
        uint_mmv_t *p_src = v_in + MM_OP31_OFS_Z + (i << HALF_YZ_SHIFT);
        mm_op31_xi_yz(p_src, exp1, v_out + TAB31_XI64_OFFSET[exp1][i]);
    }
}

/**
  @brief Restriction of function ``mm_op31_xi`` to tag ``A``

  Function ``mm_op31_xi`` computes a certain operation of the
  monster group on a vector ``v_in``. That operation depends
  on a parameter ``exp``.
  
  Function ``mm_op31_xi_tag_A`` computes the same
  operation on the entries of the vector ``v = v_in`` with
  tag ``A`` only, and ignores the other entries of ``v``.
  See section **The representation of the monster group**
  in the **API reference** for tags of entries of a vector in
  the representation of the monster.

  The function overwrites the vector ``v`` with the result.
  Here only entries of ``v`` with tag ``A`` are changed. This 
  function is much faster than function ``mm_op31_xy``.
*/
// %%EXPORT px
MM_OP31_API
void mm_op31_xi_tag_A(uint_mmv_t *v,  uint32_t exp)
{
    uint_mmv_t v_tmp[24 * 4];
    uint_fast32_t i;
    
    exp %= 3;
    if (exp == 0) return;
    mm_op31_xi_a(v, exp - 1, v_tmp);
    for (i = 0; i < 24 * 4; ++i) v[i] = v_tmp[i];
}


//  %%GEN h
//  %%GEN c
