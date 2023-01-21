# pds - Persistent data structure framework, Copyright (c) 2022 Ulrik Lindahl
# Licensed under the MIT license https://github.com/Cooolrik/pds/blob/main/LICENSE

import CodeGeneratorHelpers as hlp

def EntityReader_h():
	lines = []
	lines.extend( hlp.generate_header() )
	lines.append('')
	lines.append('#pragma once')
	lines.append('')
	lines.append('#include "ValueTypes.h"')
	lines.append('')
	lines.append('namespace pds')
	lines.append('    {')
	lines.append('    class MemoryReadStream;')
	lines.append('')
	lines.append('    class EntityReader')
	lines.append('        {')
	lines.append('        private:')
	lines.append('            MemoryReadStream &sstream;')
	lines.append('            const u64 end_position;')
	lines.append('')
	lines.append('            std::unique_ptr<EntityReader> active_subsection;')
	lines.append('            size_t active_subsection_array_size = 0;')
	lines.append('            size_t active_subsection_index = size_t(~0);')
	lines.append('            u64 active_subsection_end_pos = 0;')
	lines.append('')
	lines.append('        public:')
	lines.append('            EntityReader( MemoryReadStream &_sstream );')
	lines.append('            EntityReader( MemoryReadStream &_sstream , const u64 _end_position );')
	lines.append('')
	lines.append('            // Read a section. ')
	lines.append('            // If the section is null, the section is directly closed, nullptr+success is returned ')
	lines.append('            // from BeginReadSection, and EndReadSection shall not be called.')
	lines.append('            std::tuple<EntityReader *, bool> BeginReadSection( const char *key, const u8 key_length, const bool null_object_is_allowed );')
	lines.append('            bool EndReadSection( const EntityReader *section_reader );')
	lines.append('')
	lines.append('            // Build a sections array. ')
	lines.append('            // If the section is null, the section array is directly closed, nullptr+0+success is returned ')
	lines.append('            // from BeginReadSectionsArray, and EndReadSectionsArray shall not be called.')
	lines.append('            std::tuple<EntityReader *, size_t, bool> BeginReadSectionsArray( const char *key, const u8 key_length, const bool null_object_is_allowed, std::vector<i32> *dest_index = nullptr );')
	lines.append('            bool BeginReadSectionInArray( const EntityReader *sections_array_reader , const size_t section_index, bool *dest_section_has_data = nullptr /* if nullptr, object is not allowed to be empty*/ );')
	lines.append('            bool EndReadSectionInArray( const EntityReader *sections_array_reader , const size_t section_index );')
	lines.append('            bool EndReadSectionsArray( const EntityReader *sections_array_reader );')
	lines.append('')
	lines.append('            // The Read function template, specifically implemented below for all supported value types.')
	lines.append('            template <class T> bool Read( const char *key, const u8 key_length, T &value );')
	lines.append('')

	# print the base types
	for basetype in hlp.base_types:
		type_name = 'VT_' + basetype.name
		lines.append('            // ' + type_name )
		for type_impl in basetype.variants:
			type_impl_name = type_impl.implementing_type
			lines.append('            template <> bool Read<' + type_impl_name + '>( const char *key, const u8 key_length, ' + type_impl_name + ' &value );')
			lines.append('            template <> bool Read<optional_value<' + type_impl_name + '>>( const char *key, const u8 key_length, optional_value<' + type_impl_name + '> &value );')
		lines.append('')

	# print the array types
	for basetype in hlp.base_types:
		type_name = 'VT_Array_' + basetype.name
		lines.append('            // ' + type_name )
		for type_impl in basetype.variants:
			type_impl_name = type_impl.implementing_type
			lines.append('            template <> bool Read<std::vector<' + type_impl_name + '>>( const char *key, const u8 key_length, std::vector<' + type_impl_name + '> &value );')
			lines.append('            template <> bool Read<optional_vector<' + type_impl_name + '>>( const char *key, const u8 key_length, optional_vector<' + type_impl_name + '> &value );')
			lines.append('            template <> bool Read<idx_vector<' + type_impl_name + '>>( const char *key, const u8 key_length, idx_vector<' + type_impl_name + '> &value );')
			lines.append('            template <> bool Read<optional_idx_vector<' + type_impl_name + '>>( const char *key, const u8 key_length, optional_idx_vector<' + type_impl_name + '> &value );')
		lines.append('')

	lines.append('		};')
	lines.append('')
	#lines.append('	// Read method. Specialized for all supported value types.')
	#lines.append('	template <class T> bool EntityReader::Read( const char *key, const u8 key_length, T &value )')
	#lines.append('		{')
	#lines.append('		static_assert(false, "Error: EntityReader::Read template: The value type T cannot be serialized.");')
	#lines.append('		}')
	lines.append('	};')
	hlp.write_lines_to_file("../Include/pds/EntityReader.h",lines)

def EntityReader_inl():
	lines = []
	lines.extend( hlp.generate_header() )
	lines.append('')
	lines.append('#include "EntityReader.h"')
	lines.append('#include "MemoryReadStream.h"')
	lines.append('')
	lines.append('#include "EntityReaderTemplates.inl"')
	lines.append('')
	lines.append('namespace pds')
	lines.append('	{')
	lines.append('')

	# print the base types
	for basetype in hlp.base_types:
		type_name = 'VT_' + basetype.name
		array_type_name = 'VT_Array_' + basetype.name
		for type_impl in basetype.variants:
			implementing_type = str(type_impl.implementing_type)
			item_type = str(type_impl.item_type)
			num_items_per_object = str(type_impl.num_items_per_object)

			if type_impl.overrides_type:

				lines.append(f'	// {implementing_type}: using {item_type} to read')
				lines.append(f'	template <> inline bool EntityReader::Read<{implementing_type}>( const char *key, const u8 key_length, {implementing_type} &dest_variable )')
				lines.append(f'		{{')
				lines.append(f'		{item_type} tmp_variable;')
				lines.append(f'		if( !this->Read<{item_type}>( key, key_length , tmp_variable ) )')
				lines.append(f'			return false;')
				lines.append(f'')
				lines.append(f'		dest_variable = {implementing_type}( tmp_variable );')
				lines.append(f'')
				lines.append(f'		return true;')
				lines.append(f'		}}')
				lines.append(f'')

				lines.append(f'	// {implementing_type}: using optional_value<{item_type}> to read' )
				lines.append(f'	template <> inline bool EntityReader::Read<optional_value<{implementing_type}>>( const char *key, const u8 key_length, optional_value<{implementing_type}> &dest_variable )')
				lines.append(f'		{{')
				lines.append(f'		optional_value<{item_type}> tmp_variable;')
				lines.append(f'		if( !this->Read<optional_value<{item_type}>>( key, key_length , tmp_variable ) )')
				lines.append(f'			return false;')
				lines.append(f'')
				lines.append(f'		if( tmp_variable.has_value() )')
				lines.append(f'			dest_variable.set( tmp_variable.value() );')
				lines.append(f'		else')
				lines.append(f'			dest_variable.reset();')
				lines.append(f'')
				lines.append(f'		return true;')
				lines.append(f'		}}')
				lines.append(f'')
				
				lines.append(f'	// {implementing_type}: using std::vector<{item_type}> to read' )
				lines.append(f'	template <> inline bool EntityReader::Read<std::vector<{implementing_type}>>( const char *key, const u8 key_length, std::vector<{implementing_type}> &dest_variable )')
				lines.append(f'		{{')
				lines.append(f'		std::vector<{item_type}> tmp_variable;')
				lines.append(f'		if( !this->Read<std::vector<{item_type}>>( key, key_length , tmp_variable ) )')
				lines.append(f'			return false;')
				lines.append(f'')
				lines.append(f'		// copy values. use explicit ctor and emplace, since some objects have private conversion ctors')
				lines.append(f'		dest_variable.reserve( tmp_variable.size() );')
				lines.append(f'		for( size_t i = 0; i < tmp_variable.size(); ++i )')
				lines.append(f'			dest_variable.emplace_back( {implementing_type}(tmp_variable[i]) );')
				lines.append(f'')
				lines.append(f'		return true;')
				lines.append(f'		}}')
				lines.append(f'')
				
				lines.append(f'	//  {implementing_type}: optional_vector<{item_type}> to read' )
				lines.append(f'	template <> inline bool EntityReader::Read<optional_vector<{implementing_type}>>( const char *key, const u8 key_length, optional_vector<{implementing_type}> &dest_variable )')
				lines.append(f'		{{')
				lines.append(f'		optional_vector<{item_type}> tmp_variable;')
				lines.append(f'		if( !this->Read<optional_vector<{item_type}>>( key, key_length , tmp_variable ) )')
				lines.append(f'			return false;')
				lines.append(f'')
				lines.append(f'		if( tmp_variable.has_value() )')
				lines.append(f'			{{')
				lines.append(f'			dest_variable.set();')
				lines.append(f'')
				lines.append(f'			// copy values. use explicit ctor and emplace, since some objects have private conversion ctors')
				lines.append(f'			dest_variable.values().reserve( tmp_variable.values().size() );')
				lines.append(f'			for( size_t i = 0; i < tmp_variable.values().size(); ++i )')
				lines.append(f'				dest_variable.values().emplace_back( {implementing_type}(tmp_variable.values()[i]) );')
				lines.append(f'			}}')
				lines.append(f'		else')
				lines.append(f'			{{')
				lines.append(f'			dest_variable.reset();')
				lines.append(f'			}}')
				lines.append(f'')
				lines.append(f'		return true;')
				lines.append(f'		}}')
				lines.append(f'')
				
				lines.append(f'	// {implementing_type}: using idx_vector<{item_type}> to read' )
				lines.append(f'	template <> inline bool EntityReader::Read<idx_vector<{implementing_type}>>( const char *key, const u8 key_length, idx_vector<{implementing_type}> &dest_variable )')
				lines.append(f'		{{')
				lines.append(f'		idx_vector<{item_type}> tmp_variable;')
				lines.append(f'		if( !this->Read<idx_vector<{item_type}>>( key, key_length , tmp_variable ) )')
				lines.append(f'			return false;')
				lines.append(f'')
				lines.append(f'		// move index, as no conversion is needed')
				lines.append(f'		dest_variable.index() = std::move( tmp_variable.index() );')
				lines.append(f'')
				lines.append(f'		// copy values. use explicit ctor and emplace, since some objects have private conversion ctors')
				lines.append(f'		dest_variable.values().reserve( tmp_variable.values().size() );')
				lines.append(f'		for( size_t i = 0; i < tmp_variable.values().size(); ++i )')
				lines.append(f'			dest_variable.values().emplace_back( {implementing_type}(tmp_variable.values()[i]) );')
				lines.append(f'')
				lines.append(f'		return true;')
				lines.append(f'		}}')
				lines.append(f'')
				
				lines.append(f'	//  {implementing_type}: optional_idx_vector<{item_type}> to read' )
				lines.append(f'	template <> inline bool EntityReader::Read<optional_idx_vector<{implementing_type}>>( const char *key, const u8 key_length, optional_idx_vector<{implementing_type}> &dest_variable )')
				lines.append(f'		{{')
				lines.append(f'		optional_idx_vector<{item_type}> tmp_variable;')
				lines.append(f'		if( !this->Read<optional_idx_vector<{item_type}>>( key, key_length , tmp_variable ) )')
				lines.append(f'			return false;')
				lines.append(f'')
				lines.append(f'		if( tmp_variable.has_value() )')
				lines.append(f'			{{')
				lines.append(f'			dest_variable.set();')
				lines.append(f'')
				lines.append(f'			// move index, as no conversion is needed')
				lines.append(f'			dest_variable.index() = std::move( tmp_variable.index() );')
				lines.append(f'')
				lines.append(f'			// copy values. use explicit ctor and emplace, since some objects have private conversion ctors')
				lines.append(f'			dest_variable.values().reserve( tmp_variable.values().size() );')
				lines.append(f'			for( size_t i = 0; i < tmp_variable.values().size(); ++i )')
				lines.append(f'				dest_variable.values().emplace_back( {implementing_type}(tmp_variable.values()[i]) );')
				lines.append(f'			}}')
				lines.append(f'		else')
				lines.append(f'			{{')
				lines.append(f'			dest_variable.reset();')
				lines.append(f'			}}')
				lines.append(f'')
				lines.append(f'		return true;')
				lines.append(f'		}}')
				lines.append(f'')

			else:
				lines.append(f'	// {type_name}: {implementing_type}')
				lines.append(f'	template <> inline bool EntityReader::Read<{implementing_type}>( const char *key, const u8 key_length, {implementing_type} &dest_variable )')
				lines.append(f'		{{')
				lines.append(f'		reader_status status = read_single_item<ValueType::{type_name},{implementing_type}>(this->sstream, key, key_length, false, &(dest_variable) );')
				lines.append(f'		return status != reader_status::fail;')
				lines.append(f'		}}')
				lines.append(f'')

				lines.append(f'	// {type_name}: optional_value<{implementing_type}>' )
				lines.append(f'	template <> inline bool EntityReader::Read<optional_value<{implementing_type}>>( const char *key, const u8 key_length, optional_value<{implementing_type}> &dest_variable )')
				lines.append(f'		{{')
				lines.append(f'		dest_variable.set();')
				lines.append(f'		reader_status status = read_single_item<ValueType::{type_name},{implementing_type}>(this->sstream, key, key_length, true, &(dest_variable.value()) );')
				lines.append(f'		if( status == reader_status::success_empty )')
				lines.append(f'			dest_variable.reset();')
				lines.append(f'		return status != reader_status::fail;')
				lines.append(f'		}}')
				lines.append(f'')

				lines.append(f'	// {type_name}: std::vector<{implementing_type}>' )
				lines.append(f'	template <> inline bool EntityReader::Read<std::vector<{implementing_type}>>( const char *key, const u8 key_length, std::vector<{implementing_type}> &dest_variable )')
				lines.append(f'		{{')
				lines.append(f'		reader_status status = read_array<ValueType::{array_type_name},{implementing_type}>(this->sstream, key, key_length, false, &(dest_variable), nullptr );')
				lines.append(f'		return status != reader_status::fail;')
				lines.append(f'		}}')
				lines.append(f'')

				lines.append(f'	// {type_name}: optional_vector<{implementing_type}>' )
				lines.append(f'	template <> inline bool EntityReader::Read<optional_vector<{implementing_type}>>( const char *key, const u8 key_length, optional_vector<{implementing_type}> &dest_variable )')
				lines.append(f'		{{')
				lines.append(f'		dest_variable.set();')
				lines.append(f'		reader_status status = read_array<ValueType::{array_type_name},{implementing_type}>(this->sstream, key, key_length, true, &(dest_variable.values()), nullptr );')
				lines.append(f'		if( status == reader_status::success_empty )')
				lines.append(f'			dest_variable.reset();')
				lines.append(f'		return status != reader_status::fail;')
				lines.append(f'		}}')
				lines.append(f'')

				lines.append(f'	// {type_name}: idx_vector<{implementing_type}>' )
				lines.append(f'	template <> inline bool EntityReader::Read<idx_vector<{implementing_type}>>( const char *key, const u8 key_length, idx_vector<{implementing_type}> &dest_variable )')
				lines.append(f'		{{')
				lines.append(f'		reader_status status = read_array<ValueType::{array_type_name},{implementing_type}>(this->sstream, key, key_length, false, &(dest_variable.values()), &(dest_variable.index()) );')
				lines.append(f'		return status != reader_status::fail;')
				lines.append(f'		}}')
				lines.append(f'')

				lines.append(f'	// {type_name}: optional_idx_vector<{implementing_type}>' )
				lines.append(f'	template <> inline bool EntityReader::Read<optional_idx_vector<{implementing_type}>>( const char *key, const u8 key_length, optional_idx_vector<{implementing_type}> &dest_variable )')
				lines.append(f'		{{')
				lines.append(f'		dest_variable.set();')
				lines.append(f'		reader_status status = read_array<ValueType::{array_type_name},{implementing_type}>(this->sstream, key, key_length, true, &(dest_variable.values()), &(dest_variable.index()) );')
				lines.append(f'		if( status == reader_status::success_empty )')
				lines.append(f'			dest_variable.reset();')
				lines.append(f'		return status != reader_status::fail;')
				lines.append(f'		}}')
				lines.append(f'')
				
	lines.append('	};')
	hlp.write_lines_to_file("../Include/pds/EntityReader.inl",lines)

def run():
	EntityReader_h()
	EntityReader_inl()