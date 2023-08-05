from main import PathManager as garam

def bintest():  # Test binary mode
    # Create garam instance at path
    p = garam('path', save=False)

    # Test usings strings as keys
    p['test'] = 'test'
    assert p['test'] == 'test'
    print("bintest 1 passed")

    # Test stacking 
    p['test1']['test2'] = 'test3'
    assert p['test1']['test2'] == 'test3'
    print("bintest 2 passed")

    # Test usings ints as keys
    p[0] = '000'
    assert p[0] == '000'
    print("bintest 3 passed")

    # Test stacking 
    p[1][2] = '111'
    assert p[1][2] == '111'
    print("bintest 4 passed")

    print("all bintests passed")

def texttest():  # Test text mode
    # Create garam instance at path
    p = garam('path', mode='text', save=False)

        # Test usings strings as keys
    p['test'] = 'test'
    assert p['test'] == 'test'
    print("texttest 1 passed")

    # Test stacking 
    p['test1']['test2'] = 'test3'
    assert p['test1']['test2'] == 'test3'
    print("texttest 2 passed")

    # Test usings ints as keys
    p[0] = '000'
    assert p[0] == '000'
    print("texttest 3 passed")

    # Test stacking 
    p[1][2] = '111'
    assert p[1][2] == '111'
    print("texttest 4 passed")

    print("all texttests passed")

if __name__ == "__main__":
    bintest()
    texttest()
    print("all tests passed")