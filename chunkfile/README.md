# chunkfile
Crytek CRYENGINE python module for loading and reading chunk data from CRYENGINE 3 geometry files. (CGF, CGA, etc)

    import chunkfile



    def main():
	    cgf = chunkfile.load_chunk_file('d:/perforce/gamesdk/objects/test/house.cgf')
	    for chunk in cgf.iter_chunks():
		    print chunk


    if __name__ == '__main__':
	    main()
