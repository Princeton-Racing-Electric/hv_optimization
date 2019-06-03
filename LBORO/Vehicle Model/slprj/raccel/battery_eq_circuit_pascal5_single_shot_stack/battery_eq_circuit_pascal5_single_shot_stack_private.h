#include "__cf_battery_eq_circuit_pascal5_single_shot_stack.h"
#ifndef RTW_HEADER_battery_eq_circuit_pascal5_single_shot_stack_private_h_
#define RTW_HEADER_battery_eq_circuit_pascal5_single_shot_stack_private_h_
#include "rtwtypes.h"
#include "builtin_typeid_types.h"
#include "multiword_types.h"
#include <math.h>
#include <stdlib.h>
#if !defined(rt_VALIDATE_MEMORY)
#define rt_VALIDATE_MEMORY(S, ptr)   if(!(ptr)) {\
  ssSetErrorStatus(rtS, RT_MEMORY_ALLOCATION_ERROR);\
  }
#endif
#if !defined(rt_FREE)
#if !defined(_WIN32)
#define rt_FREE(ptr)   if((ptr) != (NULL)) {\
  free((ptr));\
  (ptr) = (NULL);\
  }
#else
#define rt_FREE(ptr)   if((ptr) != (NULL)) {\
  free((void *)(ptr));\
  (ptr) = (NULL);\
  }
#endif
#endif
#ifndef UCHAR_MAX
#include <limits.h>
#endif
#if ( UCHAR_MAX != (0xFFU) ) || ( SCHAR_MAX != (0x7F) )
#error Code was generated for compiler with different sized uchar/char. \
#endif
#if ( USHRT_MAX != (0xFFFFU) ) || ( SHRT_MAX != (0x7FFF) )
#error Code was generated for compiler with different sized ushort/short. \
#endif
#if ( UINT_MAX != (0xFFFFFFFFU) ) || ( INT_MAX != (0x7FFFFFFF) )
#error Code was generated for compiler with different sized uint/int. \
#endif
#if ( ULONG_MAX != (0xFFFFFFFFU) ) || ( LONG_MAX != (0x7FFFFFFF) )
#error Code was generated for compiler with different sized ulong/long. \
#endif
#ifndef CodeFormat
#define CodeFormat   S-Function
#else
#undef CodeFormat
#define CodeFormat   S-Function
#endif
#ifndef S_FUNCTION_NAME
#define S_FUNCTION_NAME   simulink_only_sfcn
#else
#undef S_FUNCTION_NAME
#define S_FUNCTION_NAME   simulink_only_sfcn
#endif
#ifndef S_FUNCTION_LEVEL
#define S_FUNCTION_LEVEL  2
#else
#undef S_FUNCTION_LEVEL
#define S_FUNCTION_LEVEL  2
#endif
#ifndef RTW_GENERATED_S_FUNCTION
#define RTW_GENERATED_S_FUNCTION
#endif
#ifndef rtmGetDataMapInfo
#define rtmGetDataMapInfo(rtm)        NULL
#endif
#ifndef rtmSetDataMapInfo
#define rtmSetDataMapInfo(rtm, val)
#endif
#if !defined(RTW_SFUNCTION_DEFINES)
#define RTW_SFUNCTION_DEFINES
#ifndef _RTW_COMMON_DEFINES_
#define _RTW_COMMON_DEFINES_
#endif
#endif
#if defined(MULTITASKING)
#error Model (battery_eq_circuit_pascal5_single_shot_stack) was built in \
#endif
#endif