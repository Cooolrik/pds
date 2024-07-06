# pds - Persistent data structure framework, Copyright (c) 2022 Ulrik Lindahl
# Licensed under the MIT license https://github.com/Cooolrik/pds/blob/main/LICENSE

from EntitiesHelpers import *

v1_0 = Version( "v1_0", 
	previousVersion = None, 
	items = [
		NewItem( "TestItemA",
			variables = [ Variable("string", "Name"),
							Variable("string", "OptionalText", optional = True ) ] 
			),
		NewEntity( "TestEntityA", 
			dependencies = [ Dependency( "ItemTable", include_in_header = True),
							 Dependency( "TestItemA", include_in_header = True ) ],
			templates = [ Template("test_table", template = "ItemTable", types = ["item_ref","TestItemA"] , flags=['ZeroKeys'] ) ],
			variables = [ Variable( type="test_table" , name="TestVariableA", optional=True) ,
						  Variable("string", "Name"),
						  Variable("string", "OptionalText", optional = True ) ] 
			)
		]
	) 

v1_1 = Version( "v1_1", 
	previousVersion = v1_0, 
	items = [
		IdenticalItem( "TestItemA" ),
		IdenticalEntity( "TestEntityA" ),
		NewEntity( "TestEntityB", 
			dependencies = [],
			variables = [ Variable("string", "Name") ]
			)
		]
	) 

v1_2 = Version( "v1_2", 
	previousVersion = v1_1, 
	items = [
		IdenticalItem( "TestItemA" ),
		IdenticalEntity( "TestEntityA" ),
		ModifiedEntity( "TestEntityB", 
			dependencies = [],
			variables = [ Variable("string", "Name2") ],
			mappings = [ RenamedVariable("Name2","Name") ]
			)
		]
	) 

TestPackA = Package( "TestPackA", 
	path = "../Tests/TestPackA", 
	versions = [  
		v1_0,
		v1_1,
		v1_2,
		] 
	)

hlp.run_module('PackageGenerator.PackageGenerator', TestPackA, "Latest" )


