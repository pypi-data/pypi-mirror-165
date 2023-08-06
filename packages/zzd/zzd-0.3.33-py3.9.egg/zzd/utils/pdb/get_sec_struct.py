import biotite.structure.io.pdb as pdb
import biotite.application.dssp as dssp
import gzip

def get_sec(pdb_file_path):
    """
    pdb_file_path: example  a.pdb or a.pdb.gz
    return: a numpy array of string

    example:
        from tempfile import gettempdir, NamedTemporaryFile
        import biotite.database.rcsb as rcsb
        pdb_file_path = rcsb.fetch("1l2y", "pdb", gettempdir())
        print(get_sec(pdb_file_path))
    """
    if pdb_file_path[-3:] == ".gz":
        with gzip.open(pdb_file_path,'rt') as f:
            model = pdb.PDBFile.read(f).get_structure(model=1)
    else:
        with open(pdb_file_path,'r') as f:
            model = pdb.PDBFile.read(f).get_structure(model=1)
    app = dssp.DsspApp(model)
    try:
        app.start()
    except:
        raise Exception("Error! you many not install dssp!\ntry 'conda install -c salilab dssp'")
    app.join()
    sse = app.get_sse()
    return sse

if __name__ == "__main__":
    from tempfile import gettempdir, NamedTemporaryFile
    import biotite.database.rcsb as rcsb
    pdb_file_path = rcsb.fetch("1l2y", "pdb", gettempdir())
    print(get_sec(pdb_file_path))

