/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////


#include <stdlib.h>
#include "mat24_functions.h"
#include "mm_basics.h"

// %%EXPORT_KWD MM_BASICS_API

// %%GEN ch
#ifdef __cplusplus
extern "C" {
#endif
// %%GEN c

//  %%GEN h
//  %%GEN c


// Entry 32 * i7 + i31 of the following table is equal to
// (i7 * INV[7] + i31 * INV[31] + NMAX) % N
// Here INV[i] is 1 (mod i) and 0 (mod N/i)
// We have N = 7 * 31 * 127 * 255 and NMAX = N // 2.
static const uint32_t TAB_7_31[256] = { 
// %%TABLE  CRT_TAB_7_31, uint32
0x00359dacUL,0x0027c790UL,0x0019f174UL,0x000c1b58UL,
0x00698095UL,0x005baa79UL,0x004dd45dUL,0x003ffe41UL,
0x00322825UL,0x00245209UL,0x00167bedUL,0x0008a5d1UL,
0x00660b0eUL,0x005834f2UL,0x004a5ed6UL,0x003c88baUL,
0x002eb29eUL,0x0020dc82UL,0x00130666UL,0x0005304aUL,
0x00629587UL,0x0054bf6bUL,0x0046e94fUL,0x00391333UL,
0x002b3d17UL,0x001d66fbUL,0x000f90dfUL,0x0001bac3UL,
0x005f2000UL,0x005149e4UL,0x004373c8UL,0x00359dacUL,
0x0007a8cfUL,0x00650e0cUL,0x005737f0UL,0x004961d4UL,
0x003b8bb8UL,0x002db59cUL,0x001fdf80UL,0x00120964UL,
0x00043348UL,0x00619885UL,0x0053c269UL,0x0045ec4dUL,
0x00381631UL,0x002a4015UL,0x001c69f9UL,0x000e93ddUL,
0x0000bdc1UL,0x005e22feUL,0x00504ce2UL,0x004276c6UL,
0x0034a0aaUL,0x0026ca8eUL,0x0018f472UL,0x000b1e56UL,
0x00688393UL,0x005aad77UL,0x004cd75bUL,0x003f013fUL,
0x00312b23UL,0x00235507UL,0x00157eebUL,0x0007a8cfUL,
0x0044ef4bUL,0x0037192fUL,0x00294313UL,0x001b6cf7UL,
0x000d96dbUL,0x006afc18UL,0x005d25fcUL,0x004f4fe0UL,
0x004179c4UL,0x0033a3a8UL,0x0025cd8cUL,0x0017f770UL,
0x000a2154UL,0x00678691UL,0x0059b075UL,0x004bda59UL,
0x003e043dUL,0x00302e21UL,0x00225805UL,0x001481e9UL,
0x0006abcdUL,0x0064110aUL,0x00563aeeUL,0x004864d2UL,
0x003a8eb6UL,0x002cb89aUL,0x001ee27eUL,0x00110c62UL,
0x00033646UL,0x00609b83UL,0x0052c567UL,0x0044ef4bUL,
0x0016fa6eUL,0x00092452UL,0x0066898fUL,0x0058b373UL,
0x004add57UL,0x003d073bUL,0x002f311fUL,0x00215b03UL,
0x001384e7UL,0x0005aecbUL,0x00631408UL,0x00553decUL,
0x004767d0UL,0x003991b4UL,0x002bbb98UL,0x001de57cUL,
0x00100f60UL,0x00023944UL,0x005f9e81UL,0x0051c865UL,
0x0043f249UL,0x00361c2dUL,0x00284611UL,0x001a6ff5UL,
0x000c99d9UL,0x0069ff16UL,0x005c28faUL,0x004e52deUL,
0x00407cc2UL,0x0032a6a6UL,0x0024d08aUL,0x0016fa6eUL,
0x005440eaUL,0x00466aceUL,0x003894b2UL,0x002abe96UL,
0x001ce87aUL,0x000f125eUL,0x00013c42UL,0x005ea17fUL,
0x0050cb63UL,0x0042f547UL,0x00351f2bUL,0x0027490fUL,
0x001972f3UL,0x000b9cd7UL,0x00690214UL,0x005b2bf8UL,
0x004d55dcUL,0x003f7fc0UL,0x0031a9a4UL,0x0023d388UL,
0x0015fd6cUL,0x00082750UL,0x00658c8dUL,0x0057b671UL,
0x0049e055UL,0x003c0a39UL,0x002e341dUL,0x00205e01UL,
0x001287e5UL,0x0004b1c9UL,0x00621706UL,0x005440eaUL,
0x00264c0dUL,0x001875f1UL,0x000a9fd5UL,0x00680512UL,
0x005a2ef6UL,0x004c58daUL,0x003e82beUL,0x0030aca2UL,
0x0022d686UL,0x0015006aUL,0x00072a4eUL,0x00648f8bUL,
0x0056b96fUL,0x0048e353UL,0x003b0d37UL,0x002d371bUL,
0x001f60ffUL,0x00118ae3UL,0x0003b4c7UL,0x00611a04UL,
0x005343e8UL,0x00456dccUL,0x003797b0UL,0x0029c194UL,
0x001beb78UL,0x000e155cUL,0x00003f40UL,0x005da47dUL,
0x004fce61UL,0x0041f845UL,0x00342229UL,0x00264c0dUL,
0x00639289UL,0x0055bc6dUL,0x0047e651UL,0x003a1035UL,
0x002c3a19UL,0x001e63fdUL,0x00108de1UL,0x0002b7c5UL,
0x00601d02UL,0x005246e6UL,0x004470caUL,0x00369aaeUL,
0x0028c492UL,0x001aee76UL,0x000d185aUL,0x006a7d97UL,
0x005ca77bUL,0x004ed15fUL,0x0040fb43UL,0x00332527UL,
0x00254f0bUL,0x001778efUL,0x0009a2d3UL,0x00670810UL,
0x005931f4UL,0x004b5bd8UL,0x003d85bcUL,0x002fafa0UL,
0x0021d984UL,0x00140368UL,0x00062d4cUL,0x00639289UL,
0x00359dacUL,0x0027c790UL,0x0019f174UL,0x000c1b58UL,
0x00698095UL,0x005baa79UL,0x004dd45dUL,0x003ffe41UL,
0x00322825UL,0x00245209UL,0x00167bedUL,0x0008a5d1UL,
0x00660b0eUL,0x005834f2UL,0x004a5ed6UL,0x003c88baUL,
0x002eb29eUL,0x0020dc82UL,0x00130666UL,0x0005304aUL,
0x00629587UL,0x0054bf6bUL,0x0046e94fUL,0x00391333UL,
0x002b3d17UL,0x001d66fbUL,0x000f90dfUL,0x0001bac3UL,
0x005f2000UL,0x005149e4UL,0x004373c8UL,0x00359dacUL
};

// Entry i of the following table is equal to
// uint32_t(i * INV[127] % N - N) 
// with N, INV[i] as above.
static const uint32_t TAB_127[128] = { 
// %%TABLE  CRT_TAB_127, uint32
0xff94c4a7UL,0xffa9084fUL,0xffbd4bf7UL,0xffd18f9fUL,
0xffe5d347UL,0xfffa16efUL,0xffa31f3eUL,0xffb762e6UL,
0xffcba68eUL,0xffdfea36UL,0xfff42ddeUL,0xff9d362dUL,
0xffb179d5UL,0xffc5bd7dUL,0xffda0125UL,0xffee44cdUL,
0xff974d1cUL,0xffab90c4UL,0xffbfd46cUL,0xffd41814UL,
0xffe85bbcUL,0xfffc9f64UL,0xffa5a7b3UL,0xffb9eb5bUL,
0xffce2f03UL,0xffe272abUL,0xfff6b653UL,0xff9fbea2UL,
0xffb4024aUL,0xffc845f2UL,0xffdc899aUL,0xfff0cd42UL,
0xff99d591UL,0xffae1939UL,0xffc25ce1UL,0xffd6a089UL,
0xffeae431UL,0xffff27d9UL,0xffa83028UL,0xffbc73d0UL,
0xffd0b778UL,0xffe4fb20UL,0xfff93ec8UL,0xffa24717UL,
0xffb68abfUL,0xffcace67UL,0xffdf120fUL,0xfff355b7UL,
0xff9c5e06UL,0xffb0a1aeUL,0xffc4e556UL,0xffd928feUL,
0xffed6ca6UL,0xff9674f5UL,0xffaab89dUL,0xffbefc45UL,
0xffd33fedUL,0xffe78395UL,0xfffbc73dUL,0xffa4cf8cUL,
0xffb91334UL,0xffcd56dcUL,0xffe19a84UL,0xfff5de2cUL,
0xff9ee67bUL,0xffb32a23UL,0xffc76dcbUL,0xffdbb173UL,
0xffeff51bUL,0xff98fd6aUL,0xffad4112UL,0xffc184baUL,
0xffd5c862UL,0xffea0c0aUL,0xfffe4fb2UL,0xffa75801UL,
0xffbb9ba9UL,0xffcfdf51UL,0xffe422f9UL,0xfff866a1UL,
0xffa16ef0UL,0xffb5b298UL,0xffc9f640UL,0xffde39e8UL,
0xfff27d90UL,0xff9b85dfUL,0xffafc987UL,0xffc40d2fUL,
0xffd850d7UL,0xffec947fUL,0xff959cceUL,0xffa9e076UL,
0xffbe241eUL,0xffd267c6UL,0xffe6ab6eUL,0xfffaef16UL,
0xffa3f765UL,0xffb83b0dUL,0xffcc7eb5UL,0xffe0c25dUL,
0xfff50605UL,0xff9e0e54UL,0xffb251fcUL,0xffc695a4UL,
0xffdad94cUL,0xffef1cf4UL,0xff982543UL,0xffac68ebUL,
0xffc0ac93UL,0xffd4f03bUL,0xffe933e3UL,0xfffd778bUL,
0xffa67fdaUL,0xffbac382UL,0xffcf072aUL,0xffe34ad2UL,
0xfff78e7aUL,0xffa096c9UL,0xffb4da71UL,0xffc91e19UL,
0xffdd61c1UL,0xfff1a569UL,0xff9aadb8UL,0xffaef160UL,
0xffc33508UL,0xffd778b0UL,0xffebbc58UL,0xff94c4a7UL
};

// Entry i of the following table is equal to
// uint32_t(i * INV[255] % N - N) 
// with N, INV[i] as above.
static const uint32_t TAB_255[256] = { 
// %%TABLE  CRT_TAB_255, uint32
0xff94c4a7UL,0xffbc4bf9UL,0xffe3d34bUL,0xffa01f44UL,
0xffc7a696UL,0xffef2de8UL,0xffab79e1UL,0xffd30133UL,
0xfffa8885UL,0xffb6d47eUL,0xffde5bd0UL,0xff9aa7c9UL,
0xffc22f1bUL,0xffe9b66dUL,0xffa60266UL,0xffcd89b8UL,
0xfff5110aUL,0xffb15d03UL,0xffd8e455UL,0xff95304eUL,
0xffbcb7a0UL,0xffe43ef2UL,0xffa08aebUL,0xffc8123dUL,
0xffef998fUL,0xffabe588UL,0xffd36cdaUL,0xfffaf42cUL,
0xffb74025UL,0xffdec777UL,0xff9b1370UL,0xffc29ac2UL,
0xffea2214UL,0xffa66e0dUL,0xffcdf55fUL,0xfff57cb1UL,
0xffb1c8aaUL,0xffd94ffcUL,0xff959bf5UL,0xffbd2347UL,
0xffe4aa99UL,0xffa0f692UL,0xffc87de4UL,0xfff00536UL,
0xffac512fUL,0xffd3d881UL,0xfffb5fd3UL,0xffb7abccUL,
0xffdf331eUL,0xff9b7f17UL,0xffc30669UL,0xffea8dbbUL,
0xffa6d9b4UL,0xffce6106UL,0xfff5e858UL,0xffb23451UL,
0xffd9bba3UL,0xff96079cUL,0xffbd8eeeUL,0xffe51640UL,
0xffa16239UL,0xffc8e98bUL,0xfff070ddUL,0xffacbcd6UL,
0xffd44428UL,0xfffbcb7aUL,0xffb81773UL,0xffdf9ec5UL,
0xff9beabeUL,0xffc37210UL,0xffeaf962UL,0xffa7455bUL,
0xffceccadUL,0xfff653ffUL,0xffb29ff8UL,0xffda274aUL,
0xff967343UL,0xffbdfa95UL,0xffe581e7UL,0xffa1cde0UL,
0xffc95532UL,0xfff0dc84UL,0xffad287dUL,0xffd4afcfUL,
0xfffc3721UL,0xffb8831aUL,0xffe00a6cUL,0xff9c5665UL,
0xffc3ddb7UL,0xffeb6509UL,0xffa7b102UL,0xffcf3854UL,
0xfff6bfa6UL,0xffb30b9fUL,0xffda92f1UL,0xff96deeaUL,
0xffbe663cUL,0xffe5ed8eUL,0xffa23987UL,0xffc9c0d9UL,
0xfff1482bUL,0xffad9424UL,0xffd51b76UL,0xfffca2c8UL,
0xffb8eec1UL,0xffe07613UL,0xff9cc20cUL,0xffc4495eUL,
0xffebd0b0UL,0xffa81ca9UL,0xffcfa3fbUL,0xfff72b4dUL,
0xffb37746UL,0xffdafe98UL,0xff974a91UL,0xffbed1e3UL,
0xffe65935UL,0xffa2a52eUL,0xffca2c80UL,0xfff1b3d2UL,
0xffadffcbUL,0xffd5871dUL,0xfffd0e6fUL,0xffb95a68UL,
0xffe0e1baUL,0xff9d2db3UL,0xffc4b505UL,0xffec3c57UL,
0xffa88850UL,0xffd00fa2UL,0xfff796f4UL,0xffb3e2edUL,
0xffdb6a3fUL,0xff97b638UL,0xffbf3d8aUL,0xffe6c4dcUL,
0xffa310d5UL,0xffca9827UL,0xfff21f79UL,0xffae6b72UL,
0xffd5f2c4UL,0xfffd7a16UL,0xffb9c60fUL,0xffe14d61UL,
0xff9d995aUL,0xffc520acUL,0xffeca7feUL,0xffa8f3f7UL,
0xffd07b49UL,0xfff8029bUL,0xffb44e94UL,0xffdbd5e6UL,
0xff9821dfUL,0xffbfa931UL,0xffe73083UL,0xffa37c7cUL,
0xffcb03ceUL,0xfff28b20UL,0xffaed719UL,0xffd65e6bUL,
0xfffde5bdUL,0xffba31b6UL,0xffe1b908UL,0xff9e0501UL,
0xffc58c53UL,0xffed13a5UL,0xffa95f9eUL,0xffd0e6f0UL,
0xfff86e42UL,0xffb4ba3bUL,0xffdc418dUL,0xff988d86UL,
0xffc014d8UL,0xffe79c2aUL,0xffa3e823UL,0xffcb6f75UL,
0xfff2f6c7UL,0xffaf42c0UL,0xffd6ca12UL,0xfffe5164UL,
0xffba9d5dUL,0xffe224afUL,0xff9e70a8UL,0xffc5f7faUL,
0xffed7f4cUL,0xffa9cb45UL,0xffd15297UL,0xfff8d9e9UL,
0xffb525e2UL,0xffdcad34UL,0xff98f92dUL,0xffc0807fUL,
0xffe807d1UL,0xffa453caUL,0xffcbdb1cUL,0xfff3626eUL,
0xffafae67UL,0xffd735b9UL,0xfffebd0bUL,0xffbb0904UL,
0xffe29056UL,0xff9edc4fUL,0xffc663a1UL,0xffedeaf3UL,
0xffaa36ecUL,0xffd1be3eUL,0xfff94590UL,0xffb59189UL,
0xffdd18dbUL,0xff9964d4UL,0xffc0ec26UL,0xffe87378UL,
0xffa4bf71UL,0xffcc46c3UL,0xfff3ce15UL,0xffb01a0eUL,
0xffd7a160UL,0xffff28b2UL,0xffbb74abUL,0xffe2fbfdUL,
0xff9f47f6UL,0xffc6cf48UL,0xffee569aUL,0xffaaa293UL,
0xffd229e5UL,0xfff9b137UL,0xffb5fd30UL,0xffdd8482UL,
0xff99d07bUL,0xffc157cdUL,0xffe8df1fUL,0xffa52b18UL,
0xffccb26aUL,0xfff439bcUL,0xffb085b5UL,0xffd80d07UL,
0xffff9459UL,0xffbbe052UL,0xffe367a4UL,0xff9fb39dUL,
0xffc73aefUL,0xffeec241UL,0xffab0e3aUL,0xffd2958cUL,
0xfffa1cdeUL,0xffb668d7UL,0xffddf029UL,0xff9a3c22UL,
0xffc1c374UL,0xffe94ac6UL,0xffa596bfUL,0xffcd1e11UL,
0xfff4a563UL,0xffb0f15cUL,0xffd878aeUL,0xff94c4a7UL
};



// Function mm_crt_combine_24() combines vectors p7, p31, p127, p255 
// of numbers modulo 7, 31, 127 and 255 (each input vector in 
// internal representation) to a vector p_out of integers via Chinese 
// remaindering. Each entry of the vector p_out is of type int32_t; 
// and it set to the smallest possible absolute value modulo 
// 7*31*127*255. Thus an entry of p_out may be negative.
// Each input vector has nrounds * 32 entries. Entry 32 * i0 + i1
// of the output vector is computed in case 0 <= i1 < 24 only.
// Entries 32 * i0 + i1 with 24 <= i1 < 32 are set to zero.
// The function returns min(24, v2(p_out)). Here v2(p_out) is
// the minmum positions of the least significant bits of all
// entries of the vector p_out. 
//
// Function mm_crt_v2_24() returns the same value as function 
// mm_crt_combine_24(), but does not compute any output vector.

static uint32_t mm_crt_combine_24(
    uint32_t nrounds,
    uint_mmv_t * p7,
    uint_mmv_t * p31,
    uint_mmv_t * p127,
    uint_mmv_t * p255,
    int32_t * pout
)
{
    uint_fast32_t i, res = 0xFF000000;
    for (i = 0; i < nrounds; ++i) {
        uint_mmv_t  a7, a31, a127, a255;
        uint_fast32_t a;
        a7 = *p7++;
        a31 = *p31++;
        a127 = *p127++;
        a255 = *p255++;
        a = TAB_7_31[
             (((a7) << 5) & 0xe0)
           + ((a31 >> 0) & 0x1f)
        ];
        a += TAB_127[(a127 >> 0) & 0x7f];
        a += TAB_255[(a255 >> 0) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;        
        a = TAB_7_31[
             (((a7) << 1) & 0xe0)
           + ((a31 >> 8) & 0x1f)
        ];
        a += TAB_127[(a127 >> 8) & 0x7f];
        a += TAB_255[(a255 >> 8) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;        
        a = TAB_7_31[
             (((a7) >> 3) & 0xe0)
           + ((a31 >> 16) & 0x1f)
        ];
        a += TAB_127[(a127 >> 16) & 0x7f];
        a += TAB_255[(a255 >> 16) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;        
        a = TAB_7_31[
             (((a7) >> 7) & 0xe0)
           + ((a31 >> 24) & 0x1f)
        ];
        a += TAB_127[(a127 >> 24) & 0x7f];
        a += TAB_255[(a255 >> 24) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;        
        a = TAB_7_31[
             (((a7) >> 11) & 0xe0)
           + ((a31 >> 32) & 0x1f)
        ];
        a += TAB_127[(a127 >> 32) & 0x7f];
        a += TAB_255[(a255 >> 32) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;        
        a = TAB_7_31[
             (((a7) >> 15) & 0xe0)
           + ((a31 >> 40) & 0x1f)
        ];
        a += TAB_127[(a127 >> 40) & 0x7f];
        a += TAB_255[(a255 >> 40) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;        
        a = TAB_7_31[
             (((a7) >> 19) & 0xe0)
           + ((a31 >> 48) & 0x1f)
        ];
        a += TAB_127[(a127 >> 48) & 0x7f];
        a += TAB_255[(a255 >> 48) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;        
        a = TAB_7_31[
             (((a7) >> 23) & 0xe0)
           + ((a31 >> 56) & 0x1f)
        ];
        a += TAB_127[(a127 >> 56) & 0x7f];
        a += TAB_255[(a255 >> 56) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;        
        a31 = *p31++;
        a127 = *p127++;
        a255 = *p255++;
        a = TAB_7_31[
             (((a7) >> 27) & 0xe0)
           + ((a31 >> 0) & 0x1f)
        ];
        a += TAB_127[(a127 >> 0) & 0x7f];
        a += TAB_255[(a255 >> 0) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;        
        a = TAB_7_31[
             (((a7) >> 31) & 0xe0)
           + ((a31 >> 8) & 0x1f)
        ];
        a += TAB_127[(a127 >> 8) & 0x7f];
        a += TAB_255[(a255 >> 8) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;        
        a = TAB_7_31[
             (((a7) >> 35) & 0xe0)
           + ((a31 >> 16) & 0x1f)
        ];
        a += TAB_127[(a127 >> 16) & 0x7f];
        a += TAB_255[(a255 >> 16) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;        
        a = TAB_7_31[
             (((a7) >> 39) & 0xe0)
           + ((a31 >> 24) & 0x1f)
        ];
        a += TAB_127[(a127 >> 24) & 0x7f];
        a += TAB_255[(a255 >> 24) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;        
        a = TAB_7_31[
             (((a7) >> 43) & 0xe0)
           + ((a31 >> 32) & 0x1f)
        ];
        a += TAB_127[(a127 >> 32) & 0x7f];
        a += TAB_255[(a255 >> 32) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;        
        a = TAB_7_31[
             (((a7) >> 47) & 0xe0)
           + ((a31 >> 40) & 0x1f)
        ];
        a += TAB_127[(a127 >> 40) & 0x7f];
        a += TAB_255[(a255 >> 40) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;        
        a = TAB_7_31[
             (((a7) >> 51) & 0xe0)
           + ((a31 >> 48) & 0x1f)
        ];
        a += TAB_127[(a127 >> 48) & 0x7f];
        a += TAB_255[(a255 >> 48) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;        
        a = TAB_7_31[
             (((a7) >> 55) & 0xe0)
           + ((a31 >> 56) & 0x1f)
        ];
        a += TAB_127[(a127 >> 56) & 0x7f];
        a += TAB_255[(a255 >> 56) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;        
        a7 = *p7++;
        a31 = *p31++;
        a127 = *p127++;
        a255 = *p255++;
        a = TAB_7_31[
             (((a7) << 5) & 0xe0)
           + ((a31 >> 0) & 0x1f)
        ];
        a += TAB_127[(a127 >> 0) & 0x7f];
        a += TAB_255[(a255 >> 0) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;        
        a = TAB_7_31[
             (((a7) << 1) & 0xe0)
           + ((a31 >> 8) & 0x1f)
        ];
        a += TAB_127[(a127 >> 8) & 0x7f];
        a += TAB_255[(a255 >> 8) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;        
        a = TAB_7_31[
             (((a7) >> 3) & 0xe0)
           + ((a31 >> 16) & 0x1f)
        ];
        a += TAB_127[(a127 >> 16) & 0x7f];
        a += TAB_255[(a255 >> 16) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;        
        a = TAB_7_31[
             (((a7) >> 7) & 0xe0)
           + ((a31 >> 24) & 0x1f)
        ];
        a += TAB_127[(a127 >> 24) & 0x7f];
        a += TAB_255[(a255 >> 24) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;        
        a = TAB_7_31[
             (((a7) >> 11) & 0xe0)
           + ((a31 >> 32) & 0x1f)
        ];
        a += TAB_127[(a127 >> 32) & 0x7f];
        a += TAB_255[(a255 >> 32) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;        
        a = TAB_7_31[
             (((a7) >> 15) & 0xe0)
           + ((a31 >> 40) & 0x1f)
        ];
        a += TAB_127[(a127 >> 40) & 0x7f];
        a += TAB_255[(a255 >> 40) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;        
        a = TAB_7_31[
             (((a7) >> 19) & 0xe0)
           + ((a31 >> 48) & 0x1f)
        ];
        a += TAB_127[(a127 >> 48) & 0x7f];
        a += TAB_255[(a255 >> 48) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;        
        a = TAB_7_31[
             (((a7) >> 23) & 0xe0)
           + ((a31 >> 56) & 0x1f)
        ];
        a += TAB_127[(a127 >> 56) & 0x7f];
        a += TAB_255[(a255 >> 56) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;        
        a31 = *p31++;
        a127 = *p127++;
        a255 = *p255++;
        *pout++ = 0;  
        *pout++ = 0;  
        *pout++ = 0;  
        *pout++ = 0;  
        *pout++ = 0;  
        *pout++ = 0;  
        *pout++ = 0;  
        *pout++ = 0;  
    }
    return res;
}
static uint32_t mm_crt_v2_24(
    uint32_t nrounds,
    uint_mmv_t * p7,
    uint_mmv_t * p31,
    uint_mmv_t * p127,
    uint_mmv_t * p255
)
{
    uint_fast32_t i, res = 0xFF000000;
    for (i = 0; i < nrounds; ++i) {
        uint_mmv_t  a7, a31, a127, a255;
        uint_fast32_t a;
        a7 = *p7++;
        a31 = *p31++;
        a127 = *p127++;
        a255 = *p255++;
        a = TAB_7_31[
             (((a7) << 5) & 0xe0)
           + ((a31 >> 0) & 0x1f)
        ];
        a += TAB_127[(a127 >> 0) & 0x7f];
        a += TAB_255[(a255 >> 0) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) << 1) & 0xe0)
           + ((a31 >> 8) & 0x1f)
        ];
        a += TAB_127[(a127 >> 8) & 0x7f];
        a += TAB_255[(a255 >> 8) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 3) & 0xe0)
           + ((a31 >> 16) & 0x1f)
        ];
        a += TAB_127[(a127 >> 16) & 0x7f];
        a += TAB_255[(a255 >> 16) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 7) & 0xe0)
           + ((a31 >> 24) & 0x1f)
        ];
        a += TAB_127[(a127 >> 24) & 0x7f];
        a += TAB_255[(a255 >> 24) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 11) & 0xe0)
           + ((a31 >> 32) & 0x1f)
        ];
        a += TAB_127[(a127 >> 32) & 0x7f];
        a += TAB_255[(a255 >> 32) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 15) & 0xe0)
           + ((a31 >> 40) & 0x1f)
        ];
        a += TAB_127[(a127 >> 40) & 0x7f];
        a += TAB_255[(a255 >> 40) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 19) & 0xe0)
           + ((a31 >> 48) & 0x1f)
        ];
        a += TAB_127[(a127 >> 48) & 0x7f];
        a += TAB_255[(a255 >> 48) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 23) & 0xe0)
           + ((a31 >> 56) & 0x1f)
        ];
        a += TAB_127[(a127 >> 56) & 0x7f];
        a += TAB_255[(a255 >> 56) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a31 = *p31++;
        a127 = *p127++;
        a255 = *p255++;
        a = TAB_7_31[
             (((a7) >> 27) & 0xe0)
           + ((a31 >> 0) & 0x1f)
        ];
        a += TAB_127[(a127 >> 0) & 0x7f];
        a += TAB_255[(a255 >> 0) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 31) & 0xe0)
           + ((a31 >> 8) & 0x1f)
        ];
        a += TAB_127[(a127 >> 8) & 0x7f];
        a += TAB_255[(a255 >> 8) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 35) & 0xe0)
           + ((a31 >> 16) & 0x1f)
        ];
        a += TAB_127[(a127 >> 16) & 0x7f];
        a += TAB_255[(a255 >> 16) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 39) & 0xe0)
           + ((a31 >> 24) & 0x1f)
        ];
        a += TAB_127[(a127 >> 24) & 0x7f];
        a += TAB_255[(a255 >> 24) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 43) & 0xe0)
           + ((a31 >> 32) & 0x1f)
        ];
        a += TAB_127[(a127 >> 32) & 0x7f];
        a += TAB_255[(a255 >> 32) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 47) & 0xe0)
           + ((a31 >> 40) & 0x1f)
        ];
        a += TAB_127[(a127 >> 40) & 0x7f];
        a += TAB_255[(a255 >> 40) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 51) & 0xe0)
           + ((a31 >> 48) & 0x1f)
        ];
        a += TAB_127[(a127 >> 48) & 0x7f];
        a += TAB_255[(a255 >> 48) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 55) & 0xe0)
           + ((a31 >> 56) & 0x1f)
        ];
        a += TAB_127[(a127 >> 56) & 0x7f];
        a += TAB_255[(a255 >> 56) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a7 = *p7++;
        a31 = *p31++;
        a127 = *p127++;
        a255 = *p255++;
        a = TAB_7_31[
             (((a7) << 5) & 0xe0)
           + ((a31 >> 0) & 0x1f)
        ];
        a += TAB_127[(a127 >> 0) & 0x7f];
        a += TAB_255[(a255 >> 0) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) << 1) & 0xe0)
           + ((a31 >> 8) & 0x1f)
        ];
        a += TAB_127[(a127 >> 8) & 0x7f];
        a += TAB_255[(a255 >> 8) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 3) & 0xe0)
           + ((a31 >> 16) & 0x1f)
        ];
        a += TAB_127[(a127 >> 16) & 0x7f];
        a += TAB_255[(a255 >> 16) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 7) & 0xe0)
           + ((a31 >> 24) & 0x1f)
        ];
        a += TAB_127[(a127 >> 24) & 0x7f];
        a += TAB_255[(a255 >> 24) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 11) & 0xe0)
           + ((a31 >> 32) & 0x1f)
        ];
        a += TAB_127[(a127 >> 32) & 0x7f];
        a += TAB_255[(a255 >> 32) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 15) & 0xe0)
           + ((a31 >> 40) & 0x1f)
        ];
        a += TAB_127[(a127 >> 40) & 0x7f];
        a += TAB_255[(a255 >> 40) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 19) & 0xe0)
           + ((a31 >> 48) & 0x1f)
        ];
        a += TAB_127[(a127 >> 48) & 0x7f];
        a += TAB_255[(a255 >> 48) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 23) & 0xe0)
           + ((a31 >> 56) & 0x1f)
        ];
        a += TAB_127[(a127 >> 56) & 0x7f];
        a += TAB_255[(a255 >> 56) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a31 = *p31++;
        a127 = *p127++;
        a255 = *p255++;
    }
    return res;
}





// Function mm_crt_combine_T() combines vectors p7, p31, p127, p255 
// to a vector p_out in the same way as function mm_crt_combine_24().
// But here all vector have length 759 * 64, and all entries of the
// output vector are computed. The return value is computed from
// all these output vectors in the same way as in function 
// mm_crt_combine_24().
//
// Function mm_crt_v2_T() returns the same value as function 
// mm_crt_combine_T(), but does not compute any output vector.

static uint32_t mm_crt_combine_T(
    uint_mmv_t * p7,
    uint_mmv_t * p31,
    uint_mmv_t * p127,
    uint_mmv_t * p255,
    int32_t * pout
)
{
    uint_fast32_t i, res = 0x1000000;
    for (i = 0; i < 64 * 759 / 16; ++i) {
        uint_mmv_t  a7, a31, a127, a255;
        uint_fast32_t a;
        a7 = *p7++;
        a31 = *p31++;
        a127 = *p127++;
        a255 = *p255++;
        a = TAB_7_31[
             (((a7) << 5) & 0xe0)
           + ((a31 >> 0) & 0x1f)
        ];
        a += TAB_127[(a127 >> 0) & 0x7f];
        a += TAB_255[(a255 >> 0) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;
        a = TAB_7_31[
             (((a7) << 1) & 0xe0)
           + ((a31 >> 8) & 0x1f)
        ];
        a += TAB_127[(a127 >> 8) & 0x7f];
        a += TAB_255[(a255 >> 8) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;
        a = TAB_7_31[
             (((a7) >> 3) & 0xe0)
           + ((a31 >> 16) & 0x1f)
        ];
        a += TAB_127[(a127 >> 16) & 0x7f];
        a += TAB_255[(a255 >> 16) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;
        a = TAB_7_31[
             (((a7) >> 7) & 0xe0)
           + ((a31 >> 24) & 0x1f)
        ];
        a += TAB_127[(a127 >> 24) & 0x7f];
        a += TAB_255[(a255 >> 24) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;
        a = TAB_7_31[
             (((a7) >> 11) & 0xe0)
           + ((a31 >> 32) & 0x1f)
        ];
        a += TAB_127[(a127 >> 32) & 0x7f];
        a += TAB_255[(a255 >> 32) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;
        a = TAB_7_31[
             (((a7) >> 15) & 0xe0)
           + ((a31 >> 40) & 0x1f)
        ];
        a += TAB_127[(a127 >> 40) & 0x7f];
        a += TAB_255[(a255 >> 40) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;
        a = TAB_7_31[
             (((a7) >> 19) & 0xe0)
           + ((a31 >> 48) & 0x1f)
        ];
        a += TAB_127[(a127 >> 48) & 0x7f];
        a += TAB_255[(a255 >> 48) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;
        a = TAB_7_31[
             (((a7) >> 23) & 0xe0)
           + ((a31 >> 56) & 0x1f)
        ];
        a += TAB_127[(a127 >> 56) & 0x7f];
        a += TAB_255[(a255 >> 56) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;
        a31 = *p31++;
        a127 = *p127++;
        a255 = *p255++;
        a = TAB_7_31[
             (((a7) >> 27) & 0xe0)
           + ((a31 >> 0) & 0x1f)
        ];
        a += TAB_127[(a127 >> 0) & 0x7f];
        a += TAB_255[(a255 >> 0) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;
        a = TAB_7_31[
             (((a7) >> 31) & 0xe0)
           + ((a31 >> 8) & 0x1f)
        ];
        a += TAB_127[(a127 >> 8) & 0x7f];
        a += TAB_255[(a255 >> 8) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;
        a = TAB_7_31[
             (((a7) >> 35) & 0xe0)
           + ((a31 >> 16) & 0x1f)
        ];
        a += TAB_127[(a127 >> 16) & 0x7f];
        a += TAB_255[(a255 >> 16) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;
        a = TAB_7_31[
             (((a7) >> 39) & 0xe0)
           + ((a31 >> 24) & 0x1f)
        ];
        a += TAB_127[(a127 >> 24) & 0x7f];
        a += TAB_255[(a255 >> 24) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;
        a = TAB_7_31[
             (((a7) >> 43) & 0xe0)
           + ((a31 >> 32) & 0x1f)
        ];
        a += TAB_127[(a127 >> 32) & 0x7f];
        a += TAB_255[(a255 >> 32) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;
        a = TAB_7_31[
             (((a7) >> 47) & 0xe0)
           + ((a31 >> 40) & 0x1f)
        ];
        a += TAB_127[(a127 >> 40) & 0x7f];
        a += TAB_255[(a255 >> 40) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;
        a = TAB_7_31[
             (((a7) >> 51) & 0xe0)
           + ((a31 >> 48) & 0x1f)
        ];
        a += TAB_127[(a127 >> 48) & 0x7f];
        a += TAB_255[(a255 >> 48) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;
        a = TAB_7_31[
             (((a7) >> 55) & 0xe0)
           + ((a31 >> 56) & 0x1f)
        ];
        a += TAB_127[(a127 >> 56) & 0x7f];
        a += TAB_255[(a255 >> 56) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *pout++ = a - 3513772L;
    }
    return res;
}


static uint32_t mm_crt_v2_T(
    uint_mmv_t * p7,
    uint_mmv_t * p31,
    uint_mmv_t * p127,
    uint_mmv_t * p255
)
{
    uint_fast32_t i, res = 0x1000000;
    for (i = 0; i < 64 * 759 / 16; ++i) {
        uint_mmv_t  a7, a31, a127, a255;
        uint_fast32_t a;
        a7 = *p7++;
        a31 = *p31++;
        a127 = *p127++;
        a255 = *p255++;
        a = TAB_7_31[
             (((a7) << 5) & 0xe0)
           + ((a31 >> 0) & 0x1f)
        ];
        a += TAB_127[(a127 >> 0) & 0x7f];
        a += TAB_255[(a255 >> 0) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) << 1) & 0xe0)
           + ((a31 >> 8) & 0x1f)
        ];
        a += TAB_127[(a127 >> 8) & 0x7f];
        a += TAB_255[(a255 >> 8) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 3) & 0xe0)
           + ((a31 >> 16) & 0x1f)
        ];
        a += TAB_127[(a127 >> 16) & 0x7f];
        a += TAB_255[(a255 >> 16) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 7) & 0xe0)
           + ((a31 >> 24) & 0x1f)
        ];
        a += TAB_127[(a127 >> 24) & 0x7f];
        a += TAB_255[(a255 >> 24) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 11) & 0xe0)
           + ((a31 >> 32) & 0x1f)
        ];
        a += TAB_127[(a127 >> 32) & 0x7f];
        a += TAB_255[(a255 >> 32) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 15) & 0xe0)
           + ((a31 >> 40) & 0x1f)
        ];
        a += TAB_127[(a127 >> 40) & 0x7f];
        a += TAB_255[(a255 >> 40) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 19) & 0xe0)
           + ((a31 >> 48) & 0x1f)
        ];
        a += TAB_127[(a127 >> 48) & 0x7f];
        a += TAB_255[(a255 >> 48) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 23) & 0xe0)
           + ((a31 >> 56) & 0x1f)
        ];
        a += TAB_127[(a127 >> 56) & 0x7f];
        a += TAB_255[(a255 >> 56) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a31 = *p31++;
        a127 = *p127++;
        a255 = *p255++;
        a = TAB_7_31[
             (((a7) >> 27) & 0xe0)
           + ((a31 >> 0) & 0x1f)
        ];
        a += TAB_127[(a127 >> 0) & 0x7f];
        a += TAB_255[(a255 >> 0) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 31) & 0xe0)
           + ((a31 >> 8) & 0x1f)
        ];
        a += TAB_127[(a127 >> 8) & 0x7f];
        a += TAB_255[(a255 >> 8) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 35) & 0xe0)
           + ((a31 >> 16) & 0x1f)
        ];
        a += TAB_127[(a127 >> 16) & 0x7f];
        a += TAB_255[(a255 >> 16) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 39) & 0xe0)
           + ((a31 >> 24) & 0x1f)
        ];
        a += TAB_127[(a127 >> 24) & 0x7f];
        a += TAB_255[(a255 >> 24) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 43) & 0xe0)
           + ((a31 >> 32) & 0x1f)
        ];
        a += TAB_127[(a127 >> 32) & 0x7f];
        a += TAB_255[(a255 >> 32) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 47) & 0xe0)
           + ((a31 >> 40) & 0x1f)
        ];
        a += TAB_127[(a127 >> 40) & 0x7f];
        a += TAB_255[(a255 >> 40) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 51) & 0xe0)
           + ((a31 >> 48) & 0x1f)
        ];
        a += TAB_127[(a127 >> 48) & 0x7f];
        a += TAB_255[(a255 >> 48) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        a = TAB_7_31[
             (((a7) >> 55) & 0xe0)
           + ((a31 >> 56) & 0x1f)
        ];
        a += TAB_127[(a127 >> 56) & 0x7f];
        a += TAB_255[(a255 >> 56) & 0xff];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
    }
    return res;
}




// %%EXPORT px
MM_BASICS_API
uint32_t mm_crt_combine(uint_mmv_t *p7, uint_mmv_t *p31, uint_mmv_t *p127, uint_mmv_t *p255, int32_t *p_out)
// Combine a vector from the vectors  p7, p31, p127, p255  of the
// 198884 dimensional representation modulo 7, 31, 127, and 255
// of the monster via Chinese remaindering. Input vectors  p7, p31,
// p127, p255  must be given in internal representation.
// The function computes the array p_out of type int32_t[247488].
// Entries of the output array are arranged redundantly in the same 
// way as in the internal representation, see file mm_auy.c for
// details.
// Each entry of the vector p_out is of type int32_t; and it set to 
// the smallest possible absolute value modulo 7*31*127*255. Thus 
// an entry of p_out may be negative.
// The function returns min(24, v2(p_out)). Here v2(p_out) is the
// minmum positions of the least significant bits of all entries 
// of the vector p_out.   
{
    uint_fast32_t res = 0;
    res |= mm_crt_combine_24(72, p7, p31, p127, p255, p_out);
    res |= mm_crt_combine_T( 
        p7 + MM_AUX_OFS_T / 16, 
        p31 + MM_AUX_OFS_T / 8, 
        p127 + MM_AUX_OFS_T / 8, 
        p255 + MM_AUX_OFS_T / 8, 
        p_out + MM_AUX_OFS_T 
    );
    res |= mm_crt_combine_24(3*2048, 
        p7 + MM_AUX_OFS_X / 16, 
        p31 + MM_AUX_OFS_X / 8, 
        p127 + MM_AUX_OFS_X / 8, 
        p255 + MM_AUX_OFS_X / 8, 
        p_out + MM_AUX_OFS_X 
    );
    return mat24_lsbit24(res);       
}



// %%EXPORT px
MM_BASICS_API
uint32_t mm_crt_combine_bytes(uint8_t *p7, uint8_t *p31, uint8_t *p127, uint8_t *p255, uint32_t n, int32_t *p_out)
// Combine a vector from the vectors  p7, p31, p127, p255  of the
// 198884 dimensional representation modulo 7, 31, 127, and 255
// of the monster via Chinese remaindering. Input vectors  p7, p31,
// p127, p255  must be given as arrays of ``n`` bytes.
// The function computes the array p_out of type int32_t[n].
// Each entry of the vector p_out is of type int32_t; and it set to 
// the smallest possible absolute value modulo 7*31*127*255. Thus 
// an entry of p_out may be negative.
// The function returns min(24, v2(p_out)). Here v2(p_out) is the
// minmum positions of the least significant bits of all entries 
// of the vector p_out.   
{
    uint_fast32_t i, a, res = 0x1000000;
    for (i = 0; i < n; ++i) {
        a = TAB_127[p127[i] & 0x7f] + TAB_255[p255[i] & 0xff]
           + TAB_7_31[((p7[i] << 5) & 0xe0) + (p31[i] & 0x1f)];
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        a += (0 - ((a & 0x80000000) >> 31)) & 7027545L;
        res |= a + 264921684L;
        *p_out++ = a - 3513772L;
    }
    return mat24_lsbit24(res);       
}



// %%EXPORT px
MM_BASICS_API
uint32_t mm_crt_check_v2(uint_mmv_t *p7, uint_mmv_t *p31, uint_mmv_t *p127, uint_mmv_t *p255)
// For a given tuple of input vectors  p7, p31, p127, p255,  the 
// function mm_crt_check_v2() returns the same value as function
// mm_crt_combine(). But function mm_crt_check_v2() does not 
// compute any output vector p_out.
{
    uint_fast32_t res = 0;
    res |= mm_crt_v2_24(72, p7, p31, p127, p255);
    res |= mm_crt_v2_T( 
        p7 + MM_AUX_OFS_T / 16, 
        p31 + MM_AUX_OFS_T / 8, 
        p127 + MM_AUX_OFS_T / 8, 
        p255 + MM_AUX_OFS_T / 8 
    );
    res |= mm_crt_v2_24(3*2048, 
        p7 + MM_AUX_OFS_X / 16, 
        p31 + MM_AUX_OFS_X / 8, 
        p127 + MM_AUX_OFS_X / 8, 
        p255 + MM_AUX_OFS_X / 8 
    );
    return mat24_lsbit24(res);       
}


static uint32_t crt_check_t(uint_mmv_t *p7, uint_mmv_t *p31, uint_mmv_t *p127, uint_mmv_t *p255)
// Auxiliary function for function mm_crt_check_g()
{
    uint_fast32_t res;
    res = mm_crt_v2_24(72, p7, p31, p127, p255) & 1;
    res |= mm_crt_v2_T(
        p7 + MM_AUX_OFS_T / 16, 
        p31 + MM_AUX_OFS_T / 8, 
        p127 + MM_AUX_OFS_T / 8, 
        p255 + MM_AUX_OFS_T / 8
    ) & 7;
    return res != 0;    
}

static uint32_t crt_check_l(uint_mmv_t *p7, uint_mmv_t *p31, uint_mmv_t *p127, uint_mmv_t *p255)
// Auxiliary function for function mm_crt_check_g()
{
    uint_fast32_t res;
    res = mm_crt_v2_24(24, p7, p31, p127, p255) & 3;
    res |= mm_crt_v2_24(4096, 
        p7 + MM_AUX_OFS_Z / 16, 
        p31 + MM_AUX_OFS_Z / 8, 
        p127 + MM_AUX_OFS_Z / 8, 
        p255 + MM_AUX_OFS_Z / 8
    ) & 7;
    return res != 0;    
}

// %%EXPORT px
MM_BASICS_API
uint32_t mm_crt_check_g(uint32_t g, uint_mmv_t *p7, uint_mmv_t *p31, uint_mmv_t *p127, uint_mmv_t *p255)
{
     switch ((g >> 28) & 7) {
         case 7:
             return 1;
         case 5:
             if ((g & 0x1ffffff) % 3 == 0) return 0;
             return crt_check_t(p7, p31, p127, p255);
         case 6:
             if ((g & 0x1ffffff) % 3 == 0) return 0;
             return crt_check_l(p7, p31, p127, p255);
         default:
             return 0;
     }
}






// %%EXPORT px
MM_BASICS_API
int64_t mm_crt_norm_int32_32(int32_t *pv, uint32_t i0, uint32_t i1)
{
    uint_fast32_t j0, j1, dp;
    int64_t norm = 0;
    i1 >>= 3;
    dp = 32 - (i1 << 3);
    for (j0 = 0; j0 < i0; ++j0) {
        for  (j1 = 0; j1 < i1; ++j1) {
             norm += (int64_t)pv[0] * (int64_t)pv[0]
                  +  (int64_t)pv[1] * (int64_t)pv[1]
                  +  (int64_t)pv[2] * (int64_t)pv[2]
                  +  (int64_t)pv[3] * (int64_t)pv[3]
                  +  (int64_t)pv[4] * (int64_t)pv[4]
                  +  (int64_t)pv[5] * (int64_t)pv[5]
                  +  (int64_t)pv[6] * (int64_t)pv[6]
                  +  (int64_t)pv[7] * (int64_t)pv[7];
             pv += 8;
        }
        pv += dp;
    }
    return norm;
}


// %%EXPORT px
MM_BASICS_API
int64_t mm_crt_norm_int32(int32_t *pv)
{
    return mm_crt_norm_int32_32(pv, 24, 24)
        + (mm_crt_norm_int32_32(pv + MM_AUX_OFS_B, 48, 24) >> 1)
        + mm_crt_norm_int32_32(pv + MM_AUX_OFS_T, 2 * 759, 32)
        + mm_crt_norm_int32_32(pv + MM_AUX_OFS_X, 3 * 2048, 24);
}


// %%EXPORT px
MM_BASICS_API
uint32_t mm_crt_v2_int32_32(int32_t *pv, uint32_t i0, uint32_t i1)
{
    uint_fast32_t j0, j1, dp, res = 0x1000000;
    i1 >>= 3;
    dp = 32 - (i1 << 3);
    for (j0 = 0; j0 < i0; ++j0) {
        for  (j1 = 0; j1 < i1; ++j1) {
             res |=  pv[0] | pv[1] | pv[2] | pv[3] 
                  |  pv[4] | pv[5] | pv[6] | pv[7];
             pv += 8;
        }
        pv += dp;
    }
    return res;
}



// %%EXPORT px
MM_BASICS_API
uint32_t mm_crt_v2_int32(int32_t *pv)
{
    uint_fast32_t  res =  mm_crt_v2_int32_32(pv, 72, 24)
        | mm_crt_v2_int32_32(pv + MM_AUX_OFS_T, 2 * 759, 32)
        | mm_crt_v2_int32_32(pv + MM_AUX_OFS_X, 3 * 2048, 24);
    return mat24_lsbit24(res);  
}


//  %%GEN h
//  %%GEN c


// %%GEN ch
#ifdef __cplusplus
}
#endif
//  %%GEN c
