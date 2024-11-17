# pds - Persistent data structure framework, Copyright (c) 2022 Ulrik Lindahl
# Licensed under the MIT license https://github.com/Cooolrik/pds/blob/main/LICENSE

import CodeGeneratorHelpers as hlp
from CodeGeneratorHelpers import int_bit_range, float_type_range, vector_dimension_range, nonconst_const_range

def print_type_information_header( type , value , value_count ):
	lines = []
	lines.append(f'\ttemplate<> struct data_type_information<{type}>')
	lines.append( '\t	{')
	lines.append(f'\t	using value_type = {value}; // the value type of {type} ( {value} )')
	lines.append(f'\t	static constexpr size_t value_count = {value_count}; // the number of values in {type} ( {value_count} )')
	lines.append(f'\t	static constexpr const char * value_name = "{value}"; // name of the value in {type} ( "{value}" ) ')
	lines.append(f'\t	static constexpr const char * type_name = "{type}"; // name of the type ( "{type}" ) ')
	lines.append(f'\t	static constexpr data_type_index type_index = data_type_index::dt_{type}; // the data type index of {type} ( dt_{type} )')
	lines.append(f'\t	static const {type} zero; // zero value of {type}')
	lines.append(f'\t	static const {type} inf; // limit inferior (minimum possible value) of {type}')
	if type != 'string':
		lines.append(f'\t	static const {type} sup; // limit superior (maximum possible value) of {type}')
	lines.append( '\t	};')
	lines.append('')
	return lines

def ElementTypes_h():
	lines = []
	lines.extend( hlp.generate_header() )
	lines.append('')
	lines.append('// ElementTypes.h - All basic types which are used by pds')
	lines.append('')
	lines.append('#pragma once')
	lines.append('')
	#lines.append('// UUID and HASH definitions. Define PDS_SKIP_UUID_AND_HASH if you wish to roll your own UUID and HASH definitions.')
	#lines.append('#ifndef PDS_SKIP_UUID_AND_HASH')
	#lines.append('')
	#lines.extend( hlp.inline_file( 'InlinedCode/uuid_hash_header.inl' ) )
	#lines.append('')
	#lines.append('#endif//PDS_SKIP_UUID_AND_HASH')
	#lines.append('')
	lines.append('#include <limits.h>')
	lines.append('#include <float.h>')
	lines.append('#include <ctle/uuid.h>')
	lines.append('#include <ctle/hash.h>') 
	lines.append('#include <ctle/string_funcs.h>')
	lines.append('#include <ctle/ntup.h>')
	lines.append('')

	lines.append('namespace pds')
	lines.append('{')

	# typedef base integer types
	lines.append(f"\t// scalar types")
	for bit_size in int_bit_range:
		lines.append(f"\ttypedef std::int{bit_size}_t i{bit_size};")
	for bit_size in int_bit_range:
		lines.append(f"\ttypedef std::uint{bit_size}_t u{bit_size};")
	lines.append('')
	lines.append(f"\ttypedef std::string string;")
	lines.append(f"\tusing ctle::uuid;")
	lines.append(f"\tusing hash = ctle::hash<256>;")
	lines.append('')

	# const min/max values of the standard types
	lines.append('\t// scalar types, zero value, minimum possible value ("inf", limit inferior) and maximum possible value ("sup", limit superior)')
	lines.append('\tconstexpr bool bool_zero = false;')
	lines.append('\tconstexpr bool bool_inf = false;')
	lines.append('\tconstexpr bool bool_sup = true;')
	for bit_size in int_bit_range:
		lines.append(f"\tconstexpr i{bit_size} i{bit_size}_zero = 0;")
		lines.append(f"\tconstexpr i{bit_size} i{bit_size}_inf = INT{bit_size}_MIN;")
		lines.append(f"\tconstexpr i{bit_size} i{bit_size}_sup = INT{bit_size}_MAX;")
	for bit_size in int_bit_range:
		lines.append(f"\tconstexpr u{bit_size} u{bit_size}_zero = 0;")
		lines.append(f"\tconstexpr u{bit_size} u{bit_size}_inf = 0;")
		lines.append(f"\tconstexpr u{bit_size} u{bit_size}_sup = UINT{bit_size}_MAX;")
	lines.append('')
	lines.append('\tconstexpr float float_zero = 0.0f;')
	lines.append('\tconstexpr float float_inf = -FLT_MAX;')
	lines.append('\tconstexpr float float_sup = FLT_MAX;')
	lines.append('\tconstexpr float double_zero = 0.0;')
	lines.append('\tconstexpr double double_inf = -DBL_MAX;')
	lines.append('\tconstexpr double double_sup = DBL_MAX;')
	lines.append('')
	lines.append('\tconst string string_zero;')
	lines.append('\tconst string string_inf;')
	lines.append('')
	lines.append('\tconstexpr uuid uuid_zero = {0,0};')
	lines.append('\tconstexpr uuid uuid_inf = {0,0};')
	lines.append('\tconstexpr uuid uuid_sup = {UINT64_MAX,UINT64_MAX};')
	lines.append('')
	lines.append('\tconstexpr hash hash_zero = {0,0,0,0};')
	lines.append('\tconstexpr hash hash_inf = {0,0,0,0};')
	lines.append('\tconstexpr hash hash_sup = {UINT64_MAX,UINT64_MAX,UINT64_MAX,UINT64_MAX};')
	lines.append('')

	# typedef vector types
	lines.append(f"\t// vector types")
	for bit_size in int_bit_range:
		for vec_dim in vector_dimension_range:
			lines.append(f"\tusing i{bit_size}vec{vec_dim} = ctle::i{bit_size}tup{vec_dim};")
	lines.append('')
	for bit_size in int_bit_range:
		for vec_dim in vector_dimension_range:
			lines.append(f"\tusing u{bit_size}vec{vec_dim} = ctle::u{bit_size}tup{vec_dim};")
	lines.append('')
	for vec_dim in vector_dimension_range:
		lines.append(f"\tusing fvec{vec_dim} = ctle::ftup{vec_dim};")
	for vec_dim in vector_dimension_range:
		lines.append(f"\tusing dvec{vec_dim} = ctle::dtup{vec_dim};")
	lines.append('')
	
	# typedef matrix types
	lines.append(f"\t// matrix types")
	for vec_dim in vector_dimension_range:
		lines.append(f"\tusing fmat{vec_dim} = ctle::ftup{vec_dim}x{vec_dim};")
	for vec_dim in vector_dimension_range:
		lines.append(f"\tusing dmat{vec_dim} = ctle::dtup{vec_dim}x{vec_dim};")
	lines.append('')

	# typedef quaternions
	lines.append(f"\t// quaternion types")
	for ty in ['f','d']:
		base_type = 'float' if ty == 'f' else 'double'
		lines.append(f"\tclass {ty}quat : public ctle::{ty}tup4")
		lines.append('\t{')
		lines.append('\tpublic:')
		lines.append(f'\t\t{ty}quat() : ctle::{ty}tup4() {{}}')
		lines.append(f'\t\t{ty}quat( const {ty}quat &other ) : ctle::{ty}tup4( other ) {{}}')
		lines.append(f'\t\t{ty}quat( {base_type} _a, {base_type} _b, {base_type} _c, {base_type} _d ) : ctle::{ty}tup4(_a,_b,_c,_d) {{}}')
		lines.append(f'\t\t{ty}quat &operator=( const {ty}quat &other ) noexcept {{ x = other.x; y = other.y; z = other.z; w = other.w; return *this; }}')
		lines.append('\t};')
		lines.append('')
	lines.append('')

	# typedef standard precision types (32 bit ints and floats)
	for vec_dim in vector_dimension_range:
		lines.append(f"\tusing ivec{vec_dim} = i32vec{vec_dim};")
	for vec_dim in vector_dimension_range:
		lines.append(f"\tusing uvec{vec_dim} = u32vec{vec_dim};")
	for vec_dim in vector_dimension_range:
		lines.append(f"\tusing vec{vec_dim} = fvec{vec_dim};")
	for vec_dim in vector_dimension_range:
		lines.append(f"\tusing mat{vec_dim} = fmat{vec_dim};")
	lines.append('')

	# inline entity_ref and item_ref
	lines.extend( hlp.inline_file( 'InlinedCode/entity_ref.inl' ) )
	lines.extend( hlp.inline_file( 'InlinedCode/item_ref.inl' ) )

	# enum of all data types
	lines.append('\t// all value type indices')
	lines.append('\tenum class data_type_index')
	lines.append('\t\t{')
	for basetype_inx in range(len(hlp.base_types)):
		basetype = hlp.base_types[basetype_inx]
		for variant_inx in range(len(basetype.variants)):
			variant_name = basetype.variants[variant_inx].implementing_type
			variant_id = ( (basetype_inx+1) << 4) + (variant_inx + 1)
			lines.append(f'\t\tdt_{variant_name} = {hex(variant_id)},')
	lines.append('\t\t};')
	lines.append('')

	# type information on all types
	lines.append('\t// type_information stores information on the standard types in PDS')
	lines.append('\ttemplate <class T> struct data_type_information;')
	lines.append('')

	# scalar type info
	lines.extend(print_type_information_header("bool","bool",1))
	for bit_size in int_bit_range:
		lines.extend(print_type_information_header(f"i{bit_size}",f"i{bit_size}",1))
	for bit_size in int_bit_range:
		lines.extend(print_type_information_header(f"u{bit_size}",f"u{bit_size}",1))
	lines.extend(print_type_information_header("float","float",1))
	lines.extend(print_type_information_header("double","double",1))

	# vector type info
	for bit_size in int_bit_range:
		for vec_dim in vector_dimension_range:
			lines.extend(print_type_information_header(f"i{bit_size}vec{vec_dim}",f"i{bit_size}",vec_dim))
	for bit_size in int_bit_range:
		for vec_dim in vector_dimension_range:
			lines.extend(print_type_information_header(f"u{bit_size}vec{vec_dim}",f"u{bit_size}",vec_dim))	
	for vec_dim in vector_dimension_range:
		lines.extend(print_type_information_header(f"fvec{vec_dim}",'float',vec_dim))	
	for vec_dim in vector_dimension_range:
		lines.extend(print_type_information_header(f"dvec{vec_dim}",'double',vec_dim))	

	# matrix type info
	for vec_dim in vector_dimension_range:
		lines.extend(print_type_information_header(f"fmat{vec_dim}",'float',vec_dim*vec_dim))	
	for vec_dim in vector_dimension_range:
		lines.extend(print_type_information_header(f"dmat{vec_dim}",'double',vec_dim*vec_dim))	

	# quaternions info
	lines.extend(print_type_information_header('fquat','float',4))
	lines.extend(print_type_information_header('dquat','double',4))

	# uuid info
	lines.extend(print_type_information_header('uuid','uuid',1))
	lines.extend(print_type_information_header('item_ref','item_ref',1))

	# hash info
	lines.extend(print_type_information_header('hash','hash',1))
	lines.extend(print_type_information_header('entity_ref','entity_ref',1))

	# string info
	lines.extend(print_type_information_header('string','string',1))

	# end of pds namespace
	lines.append('    };')
	
	# define stuff in std namespace
	lines.append('')
	lines.append('// inject hash functions into std')
	lines.append('template<>')
	lines.append('struct std::hash<pds::item_ref>')
	lines.append('    {')
	lines.append('    std::size_t operator()(pds::item_ref const& val) const noexcept')
	lines.append('        {')
	lines.append('        return std::hash<ctle::uuid>{}( val );')
	lines.append('        }')
	lines.append('    };')
	lines.append('')
	lines.append('template<>')
	lines.append('struct std::hash<pds::entity_ref>')
	lines.append('    {')
	lines.append('    std::size_t operator()(pds::entity_ref const& val) const noexcept')
	lines.append('        {')
	lines.append('        return std::hash<pds::hash>{}( pds::hash( val ) );')
	lines.append('        }')
	lines.append('    };')

	# end of file
	hlp.write_lines_to_file("../Include/pds/ElementTypes.h",lines)

def print_type_information_source( type , value , value_count ):
	lines = []
	
	zero = inf = sup = ''
	for i in range(value_count):
		zero += f'{value}_zero'
		inf += f'{value}_inf'
		sup += f'{value}_sup'
		if i < value_count-1:
			zero += ','
			inf += ','
			sup += ','

	lines.append(f'\tconst {type} data_type_information<{type}>::zero = {type}({zero}); // zero value of {type}')
	lines.append(f'\tconst {type} data_type_information<{type}>::inf = {type}({inf}); // limit inferior (minimum bound) of {type}')
	if type != 'string':
		lines.append(f'\tconst {type} data_type_information<{type}>::sup = {type}({sup}); // limit superior (maximum bound) of {type}')
	lines.append('')
	return lines

def print_matrix_type_information_source( type , subtype , value , value_count ):
	lines = []
	
	zero = inf = sup = ''
	for t in range(value_count):
		zero += f'{subtype}('		
		inf += f'{subtype}('		
		sup += f'{subtype}('		
		for i in range(value_count):
			zero += f'{value}_zero'
			inf += f'{value}_inf'
			sup += f'{value}_sup'
			if i < value_count-1:
				zero += ','
				inf += ','
				sup += ','
		zero += ')'
		inf += ')'
		sup += ')'
		if t < value_count-1:
			zero += ','
			inf += ','
			sup += ','

	lines.append(f'\tconst {type} data_type_information<{type}>::zero = {type}({zero}); // zero value of {type}')
	lines.append(f'\tconst {type} data_type_information<{type}>::inf = {type}({inf}); // limit inferior (minimum bound) of {type}')
	lines.append(f'\tconst {type} data_type_information<{type}>::sup = {type}({sup}); // limit superior (maximum bound) of {type}')
	lines.append('')
	return lines

def ElementTypes_inl():
	lines = []
	lines.extend( hlp.generate_header() )
	lines.append('')
	#lines.append('#include <glm/glm.hpp>')
	#lines.append('#include <glm/gtc/type_ptr.hpp>')
	lines.append('')
	lines.append('#include "pds.h"')
	lines.append('')
	#lines.extend( hlp.inline_file( 'InlinedCode/uuid_hash_source.inl' ) )
	lines.append('')
	lines.append('namespace pds')
	lines.append('{')

	# scalar type info
	lines.extend(print_type_information_source("bool","bool",1))
	for bit_size in int_bit_range:
		lines.extend(print_type_information_source(f"i{bit_size}",f"i{bit_size}",1))
	for bit_size in int_bit_range:
		lines.extend(print_type_information_source(f"u{bit_size}",f"u{bit_size}",1))
	lines.extend(print_type_information_source("float","float",1))
	lines.extend(print_type_information_source("double","double",1))

	# vector type info
	for bit_size in int_bit_range:
		for vec_dim in vector_dimension_range:
			lines.extend(print_type_information_source(f"i{bit_size}vec{vec_dim}",f"i{bit_size}",vec_dim))
	for bit_size in int_bit_range:
		for vec_dim in vector_dimension_range:
			lines.extend(print_type_information_source(f"u{bit_size}vec{vec_dim}",f"u{bit_size}",vec_dim))	
	for vec_dim in vector_dimension_range:
		lines.extend(print_type_information_source(f"fvec{vec_dim}",'float',vec_dim))	
	for vec_dim in vector_dimension_range:
		lines.extend(print_type_information_source(f"dvec{vec_dim}",'double',vec_dim))	

	# matrix type info
	for vec_dim in vector_dimension_range:
		lines.extend(print_matrix_type_information_source(f"fmat{vec_dim}",f"fvec{vec_dim}",'float',vec_dim))	
	for vec_dim in vector_dimension_range:
		lines.extend(print_matrix_type_information_source(f"dmat{vec_dim}",f"dvec{vec_dim}",'double',vec_dim))	

	# quaternions info
	lines.extend(print_type_information_source('fquat','float',4))
	lines.extend(print_type_information_source('dquat','double',4))

	# other types that are atomic
	same_type_range = ['uuid','entity_ref','hash','item_ref','string']
	for type in same_type_range:
		lines.extend(print_type_information_source(type,type,1))
	lines.append('};')

	hlp.write_lines_to_file("../Include/pds/ElementTypes.inl",lines)

def ElementValuePointers_h():
	lines = []
	lines.extend( hlp.generate_header() )
	lines.append('')
	lines.append('#pragma once')
	lines.append('')
	lines.append('#include "pds.h"')
	lines.append('')

	#lines.extend( hlp.generate_push_and_disable_warnings( [4201] , [] ) )
	#lines.append('')
	#lines.append('#include <glm/gtc/type_ptr.hpp>')
	lines.append('')
	lines.append('namespace pds')
	lines.append('{')

	# type pointer functions (return pointer to first item in each type)
	lines.append(f"// item pointer functions, returns a pointer to the first item of each type")
	lines.append('')
	for bit_size in int_bit_range:
		for const_type in nonconst_const_range:
			lines.append(f"inline {const_type}i{bit_size} *value_ptr( {const_type}i{bit_size} &value ) {{ return &value; }}")
	lines.append('')
	for bit_size in int_bit_range:
		for const_type in nonconst_const_range:
			lines.append(f"inline {const_type}u{bit_size} *value_ptr( {const_type}u{bit_size} &value ) {{ return &value; }}")
	lines.append('')
	for float_type in float_type_range:
		for const_type in nonconst_const_range:
			lines.append(f"inline {const_type}{float_type} *value_ptr( {const_type}{float_type} &value ) {{ return &value; }}")
	lines.append('')
	for bit_size in int_bit_range:
		for vec_dim in vector_dimension_range:
			for const_type in nonconst_const_range:
				lines.append(f"inline {const_type}i{bit_size} *value_ptr( {const_type}i{bit_size}vec{vec_dim} &value ) {{ return value.data(); }}")
	lines.append('')
	for bit_size in int_bit_range:
		for vec_dim in vector_dimension_range:
			for const_type in nonconst_const_range:
				lines.append(f"inline {const_type}u{bit_size} *value_ptr( {const_type}u{bit_size}vec{vec_dim} &value ) {{ return value.data(); }}")
	lines.append('')

	# vectors
	for vec_dim in vector_dimension_range:
		for const_type in nonconst_const_range:
			lines.append(f"inline {const_type}float *value_ptr( {const_type}fvec{vec_dim} &value ) {{ return value.data(); }}")
	for vec_dim in vector_dimension_range:
		for const_type in nonconst_const_range:
			lines.append(f"inline {const_type}double *value_ptr( {const_type}dvec{vec_dim} &value ) {{ return value.data(); }}")
	lines.append('')

	# matrices
	for vec_dim in vector_dimension_range:
		for const_type in nonconst_const_range:
			lines.append(f"inline {const_type}float *value_ptr( {const_type}fmat{vec_dim} &value ) {{ return value.data()->data(); }}")
	for vec_dim in vector_dimension_range:
		for const_type in nonconst_const_range:
			lines.append(f"inline {const_type}double *value_ptr( {const_type}dmat{vec_dim} &value ) {{ return value.data()->data(); }}")
	lines.append('')

	# quaternions
	for const_type in nonconst_const_range:
		lines.append(f"inline {const_type}float *value_ptr( {const_type}fquat &value ) {{ return value.data(); }}")
	for const_type in nonconst_const_range:
		lines.append(f"inline {const_type}double *value_ptr( {const_type}dquat &value ) {{ return value.data(); }}")
	lines.append('')

	# other types that have no inner item pointer
	same_type_range = ['uuid','hash','string']
	for type in same_type_range:
		for const_type in nonconst_const_range:
			lines.append(f"inline {const_type}{type} *value_ptr( {const_type}{type} &value ) {{ return &value; }}")

	# end of namespace
	lines.append('}')
	lines.append('// namespace pds')
	lines.append('')

	# reenable warning
	#lines.extend( hlp.generate_pop_warnings() )
	
	hlp.write_lines_to_file("../Include/pds/ElementValuePointers.h",lines)

def run():
	ElementTypes_h()
	ElementTypes_inl()
	ElementValuePointers_h()