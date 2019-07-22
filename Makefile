.PHONY: test
test:
	/usr/bin/env python3 -m unittest discover
	cd write_a_c_compiler ; ./test_compiler.sh ../tcc.sh 1 2
